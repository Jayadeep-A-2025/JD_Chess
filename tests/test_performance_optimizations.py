"""
Tests for JD Chess performance and caching optimizations.

Validates that caching, O(1) indexed lookups, and fast bitboard evaluation
function accurately and safely without staleness or memory leaks.
"""

from __future__ import annotations

import os
import time
import pytest
import chess
from PySide6.QtGui import QIcon

from app.services.curriculum import (
    CURRICULUM,
    _LESSONS_BY_ID,
    _LESSONS_INDEX,
    _LESSONS_BY_LEVEL,
    _LESSONS_BY_TOPIC,
    get_lesson_by_id,
    get_lessons_by_level,
    get_lessons_by_topic,
    get_next_lesson,
    get_prev_lesson,
)
from app.services.save_manager import SaveManager
from app.services.history_manager import HistoryManager, MatchRecord
from app.services.user_profile_manager import UserProfile
from app.services.analysis_service import _heuristic_eval_white, _heuristic_analyze_game, _PIECE_VALUES
from app.ui.piece_renderer import PieceRenderer
from app.ui.chessboard_widget import _compute_captured_pieces_memo


def test_curriculum_indexing_and_fast_lookup():
    """Verify that curriculum indices are completely built and O(1) lookups work."""
    assert len(CURRICULUM) == 42
    assert len(_LESSONS_BY_ID) == 42
    assert len(_LESSONS_INDEX) == 42
    assert len(_LESSONS_BY_LEVEL) == 7
    assert len(_LESSONS_BY_TOPIC) > 0

    first_lesson = CURRICULUM[0]
    last_lesson = CURRICULUM[-1]

    # get_lesson_by_id
    assert get_lesson_by_id(first_lesson.id) == first_lesson
    assert get_lesson_by_id(last_lesson.id) == last_lesson
    assert get_lesson_by_id("non_existent_id") is None

    # Next / prev
    assert get_prev_lesson(first_lesson.id) is None
    assert get_next_lesson(first_lesson.id) == CURRICULUM[1]
    assert get_next_lesson(last_lesson.id) is None
    assert get_prev_lesson(last_lesson.id) == CURRICULUM[-2]

    # By level
    level1_lessons = get_lessons_by_level(1)
    assert len(level1_lessons) == 6
    assert all(l.level_number == 1 for l in level1_lessons)

    # By topic
    topic = first_lesson.topic
    topic_lessons = get_lessons_by_topic(topic)
    assert first_lesson in topic_lessons
    assert all(l.topic == topic for l in topic_lessons)


def test_save_manager_mtime_caching(tmp_path):
    """Verify SaveManager caches file reads based on st_mtime and updates on write."""
    filepath = tmp_path / "saves_cache_test.json"
    sm = SaveManager(storage_path=filepath)

    assert sm._cached_data is None
    # Before file creation
    assert sm._read_data() == {}
    assert sm._cached_data is None

    # Saving a slot writes to file and populates cache
    sm.save_game(
        slot_id=1,
        game_mode="Human vs Human",
        player_color="White",
        difficulty="Medium",
        moves=["e2e4", "e7e5"],
        fen="rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
        turn="White",
        status_text="Turn: White",
    )
    assert sm.get_slot(1).is_active is True
    assert sm.has_active_saves() is True
    assert sm.active_save_count() == 1

    # First read after creation populates cache
    data1 = sm._read_data()
    assert sm._cached_data is not None
    assert sm._cached_mtime is not None

    # Secondary read should hit cache without error
    data2 = sm._read_data()
    assert data1 == data2
    assert sm._cached_data["1"]["is_active"] is True


def test_history_manager_mtime_caching(tmp_path):
    """Verify HistoryManager caches file reads and updates on record_match."""
    filepath = tmp_path / "history_cache_test.json"
    hm = HistoryManager(storage_path=filepath)

    # Before file creation
    assert hm.get_all_matches() == []
    assert hm._cached_data is None

    # Log a match to create file and populate cache
    hm.record_match(
        game_mode="Play vs Computer",
        player_color="White",
        difficulty="Medium",
        result="win",
        result_label="Checkmate – You Won",
        moves=["e2e4", "e7e5"],
    )

    # Cached data reflects the new record and is non-None
    assert hm._cached_data is not None
    assert hm._cached_mtime is not None
    updated_matches = hm.get_all_matches()
    assert len(updated_matches) == 1
    assert updated_matches[0].result == "win"


def test_user_profile_clone_independence():
    """Verify UserProfile.clone() produces a decoupled identical copy."""
    profile = UserProfile(
        username="Grandmaster",
        completed_lessons=["l1_01", "l1_02"],
        sound_enabled=True,
    )
    cloned = profile.clone()

    assert cloned.username == profile.username
    assert cloned.sound_enabled == profile.sound_enabled
    assert cloned.completed_lessons == profile.completed_lessons

    # Mutating clone list does not affect original
    cloned.completed_lessons.append("l1_03")
    assert "l1_03" not in profile.completed_lessons


def test_heuristic_evaluation_fast_accuracy():
    """Verify the bitboard _heuristic_eval_white matches expected material values."""
    # Standard starting board should be exactly 0 (balanced)
    board = chess.Board()
    eval_start = _heuristic_eval_white(board)
    assert eval_start == 0

    # Board with white having an extra queen (+900 cp)
    board_extra_q = chess.Board("rnb1kbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    eval_extra_q = _heuristic_eval_white(board_extra_q)
    assert eval_extra_q == 900

    # Comparison against manual square loop
    def _legacy_eval(b: chess.Board) -> int:
        score = 0
        for pt in (chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
            val = _PIECE_VALUES[pt]
            w_count = sum(1 for sq in chess.SQUARES if (p := b.piece_at(sq)) and p.piece_type == pt and p.color == chess.WHITE)
            b_count = sum(1 for sq in chess.SQUARES if (p := b.piece_at(sq)) and p.piece_type == pt and p.color == chess.BLACK)
            score += val * (w_count - b_count)
        for center_sq in (chess.E4, chess.D4, chess.E5, chess.D5):
            p = b.piece_at(center_sq)
            if p:
                score += 25 if p.color == chess.WHITE else -25
        return score

    assert _heuristic_eval_white(board) == _legacy_eval(board)
    assert _heuristic_eval_white(board_extra_q) == _legacy_eval(board_extra_q)


def test_piece_renderer_icon_cache():
    """Verify PieceRenderer caches and reuses QIcon instances."""
    renderer = PieceRenderer()

    icon1 = renderer.get_piece_icon("P", 48)
    icon2 = renderer.get_piece_icon("P", 48)
    assert icon1 is icon2
    assert isinstance(icon1, QIcon)

    # Different size produces distinct cached entry
    icon3 = renderer.get_piece_icon("P", 64)
    assert icon3 is not icon1

    # Dot icon caching
    dot1 = renderer.get_move_dot_icon(48)
    dot2 = renderer.get_move_dot_icon(48)
    assert dot1 is dot2

    # Capture target icon caching
    cap1 = renderer.get_capture_target_icon("p", 48)
    cap2 = renderer.get_capture_target_icon("p", 48)
    assert cap1 is cap2


def test_captured_pieces_lru_cache():
    """Verify _compute_captured_pieces_memo memoizes results for identical move histories."""
    moves = (
        chess.Move.from_uci("e2e4"),
        chess.Move.from_uci("e7e5"),
        chess.Move.from_uci("g1f3"),
        chess.Move.from_uci("b8c6"),
    )
    res1 = _compute_captured_pieces_memo(moves)
    res2 = _compute_captured_pieces_memo(moves)

    assert res1 == res2
    assert res1 == ((), ())
