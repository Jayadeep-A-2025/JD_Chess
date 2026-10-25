from __future__ import annotations

"""Move-by-move game analysis service using a chess engine or heuristic fallback."""

import chess
import chess.engine
from dataclasses import dataclass, field
from typing import Any

# Centipawn thresholds
_BLUNDER_THRESHOLD_CP = 200   # ≥ 200 cp loss = blunder
_MISTAKE_THRESHOLD_CP = 80    # ≥  80 cp loss = mistake
_INACCURACY_THRESHOLD_CP = 30 # ≥  30 cp loss = inaccuracy

_PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}


@dataclass
class MoveAnnotation:
    """Analysis result for a single half-move (ply)."""
    ply: int                    # 0-indexed ply number
    move_number: int            # chess move number (1, 2, 3 …)
    color: str                  # "White" | "Black"
    san: str                    # SAN notation played
    uci: str                    # UCI notation played
    score_before_cp: int | None # centipawn evaluation BEFORE move
    score_after_cp: int | None  # centipawn evaluation AFTER move
    best_uci: str               # engine's suggested best move (UCI)
    best_san: str               # engine's suggested best move (SAN)
    cp_loss: int                # centipawn loss (≥ 0)
    classification: str         # "best" | "good" | "inaccuracy" | "mistake" | "blunder"
    comment: str                # human-readable comment


@dataclass
class AnalysisResult:
    """Full post-game analysis output."""
    annotations: list[MoveAnnotation] = field(default_factory=list)
    blunders: int = 0
    mistakes: int = 0
    inaccuracies: int = 0
    accuracy_score: int = 0     # 0-100
    grade: str = "N/A"          # A+ … F

    def player_annotations(self, player_color: str) -> list[MoveAnnotation]:
        return [a for a in self.annotations if a.color == player_color]


def _cp_to_white(score: chess.engine.Score, turn: chess.Color) -> int | None:
    """Return centipawn score from White's perspective, or None if mate."""
    if score.is_mate():
        mate_n = score.mate()
        if mate_n is None:
            return None
        return 30_000 if mate_n > 0 else -30_000
    cp = score.score()
    if cp is None:
        return None
    return cp if turn == chess.WHITE else -cp


def _classify(cp_loss: int) -> str:
    if cp_loss >= _BLUNDER_THRESHOLD_CP:
        return "blunder"
    if cp_loss >= _MISTAKE_THRESHOLD_CP:
        return "mistake"
    if cp_loss >= _INACCURACY_THRESHOLD_CP:
        return "inaccuracy"
    return "best" if cp_loss <= 5 else "good"


def _grade(accuracy: int) -> str:
    if accuracy >= 95:
        return "A+"
    if accuracy >= 85:
        return "A"
    if accuracy >= 75:
        return "B"
    if accuracy >= 65:
        return "C"
    if accuracy >= 50:
        return "D"
    return "F"


def _heuristic_eval_white(board: chess.Board) -> int:
    """Fast material & positional evaluation from White's perspective."""
    if board.is_checkmate():
        return -30000 if board.turn == chess.WHITE else 30000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            val = _PIECE_VALUES.get(piece.piece_type, 0)
            score += val if piece.color == chess.WHITE else -val

    for center_sq in (chess.E4, chess.D4, chess.E5, chess.D5):
        p = board.piece_at(center_sq)
        if p:
            score += 25 if p.color == chess.WHITE else -25

    return score


def _heuristic_analyze_game(
    uci_moves: list[str],
    player_color: str = "White",
) -> AnalysisResult:
    """Offline heuristic analyzer used when computer chess engine binary is not installed."""
    result = AnalysisResult()
    if not uci_moves:
        return result

    board = chess.Board()
    annotations: list[MoveAnnotation] = []

    for ply, uci_str in enumerate(uci_moves):
        move_number = ply // 2 + 1
        color = "White" if board.turn == chess.WHITE else "Black"
        score_before_cp = _heuristic_eval_white(board)

        best_move = None
        best_eval = -999999 if board.turn == chess.WHITE else 999999

        for candidate in board.legal_moves:
            board.push(candidate)
            cand_score = _heuristic_eval_white(board)
            board.pop()
            if board.turn == chess.WHITE:
                if cand_score > best_eval:
                    best_eval = cand_score
                    best_move = candidate
            else:
                if cand_score < best_eval:
                    best_eval = cand_score
                    best_move = candidate

        best_uci = best_move.uci() if best_move else uci_str
        try:
            best_san = board.san(best_move) if best_move else uci_str
        except Exception:
            best_san = best_uci

        try:
            move = chess.Move.from_uci(uci_str)
            san = board.san(move)
            board.push(move)
        except Exception:
            san = uci_str

        score_after_cp = _heuristic_eval_white(board)

        if color == "White":
            cp_loss = max(0, score_before_cp - score_after_cp)
        else:
            cp_loss = max(0, score_after_cp - score_before_cp)

        classification = _classify(cp_loss)

        if classification == "blunder":
            comment = f"Blunder! Material loss or tactical oversight. Better: {best_san}."
        elif classification == "mistake":
            comment = f"Mistake. Weakened position. Consider: {best_san}."
        elif classification == "inaccuracy":
            comment = f"Inaccuracy. {best_san} maintained stronger control."
        elif classification == "best":
            comment = "Best move! Excellent precision. ✓"
        else:
            comment = f"Solid move. {best_san} was also reasonable."

        annotations.append(
            MoveAnnotation(
                ply=ply,
                move_number=move_number,
                color=color,
                san=san,
                uci=uci_str,
                score_before_cp=score_before_cp,
                score_after_cp=score_after_cp,
                best_uci=best_uci,
                best_san=best_san,
                cp_loss=cp_loss,
                classification=classification,
                comment=comment,
            )
        )

    result.annotations = annotations
    _compute_summary(result, player_color)
    return result


def _compute_summary(result: AnalysisResult, player_color: str) -> None:
    player_anns = [a for a in result.annotations if a.color == player_color]
    if player_anns:
        result.blunders = sum(1 for a in player_anns if a.classification == "blunder")
        result.mistakes = sum(1 for a in player_anns if a.classification == "mistake")
        result.inaccuracies = sum(1 for a in player_anns if a.classification == "inaccuracy")

        _weights = {"best": 100, "good": 90, "inaccuracy": 60, "mistake": 30, "blunder": 0}
        total = sum(_weights.get(a.classification, 0) for a in player_anns)
        result.accuracy_score = int(total / len(player_anns))
        result.grade = _grade(result.accuracy_score)
    else:
        result.accuracy_score = 0
        result.grade = "N/A"


def analyze_game(
    uci_moves: list[str],
    engine_path: str | None = None,
    player_color: str = "White",
    depth: int = 14,
    time_limit: float = 0.25,
) -> AnalysisResult:
    """Run post-game analysis on a completed game.

    Uses Computer engine if engine_path is valid, otherwise runs heuristic analysis.
    """
    result = AnalysisResult()
    if not uci_moves:
        return result

    if not engine_path:
        return _heuristic_analyze_game(uci_moves, player_color)

    try:
        engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    except Exception:
        return _heuristic_analyze_game(uci_moves, player_color)

    board = chess.Board()
    annotations: list[MoveAnnotation] = []

    try:
        for ply, uci_str in enumerate(uci_moves):
            move_number = ply // 2 + 1
            color = "White" if board.turn == chess.WHITE else "Black"

            info_before = engine.analyse(
                board,
                chess.engine.Limit(depth=depth, time=time_limit),
            )
            score_before_raw = info_before.get("score")
            score_before_cp = (
                _cp_to_white(score_before_raw.white(), board.turn)
                if score_before_raw else None
            )

            best_move = info_before.get("pv", [None])[0]
            if best_move:
                best_uci = best_move.uci()
                try:
                    best_san = board.san(best_move)
                except Exception:
                    best_san = best_uci
            else:
                best_uci = ""
                best_san = ""

            move = chess.Move.from_uci(uci_str)
            try:
                san = board.san(move)
            except Exception:
                san = uci_str
            board.push(move)

            info_after = engine.analyse(
                board,
                chess.engine.Limit(depth=depth, time=time_limit),
            )
            score_after_raw = info_after.get("score")
            score_after_cp = (
                _cp_to_white(score_after_raw.white(), board.turn)
                if score_after_raw else None
            )

            if score_before_cp is not None and score_after_cp is not None:
                if color == "White":
                    cp_loss = max(0, score_before_cp - score_after_cp)
                else:
                    cp_loss = max(0, score_after_cp - score_before_cp)
            else:
                cp_loss = 0

            classification = _classify(cp_loss)

            if classification == "blunder":
                comment = (
                    f"Blunder! Lost ~{cp_loss//100:.1f} pawns. "
                    f"Better: {best_san}."
                )
            elif classification == "mistake":
                comment = (
                    f"Mistake. Lost ~{cp_loss//100:.1f} pawns. "
                    f"Consider: {best_san}."
                )
            elif classification == "inaccuracy":
                comment = f"Inaccuracy. {best_san} was more precise."
            elif classification == "best":
                comment = "Best move! ✓"
            else:
                comment = f"Good move. {best_san} was also fine."

            annotations.append(
                MoveAnnotation(
                    ply=ply,
                    move_number=move_number,
                    color=color,
                    san=san,
                    uci=uci_str,
                    score_before_cp=score_before_cp,
                    score_after_cp=score_after_cp,
                    best_uci=best_uci,
                    best_san=best_san,
                    cp_loss=cp_loss,
                    classification=classification,
                    comment=comment,
                )
            )

    except Exception:
        pass
    finally:
        try:
            engine.quit()
        except Exception:
            pass

    result.annotations = annotations
    _compute_summary(result, player_color)
    return result
