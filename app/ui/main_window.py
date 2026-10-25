from __future__ import annotations

"""Main application window managing multi-window navigation and game lifecycle."""

from pathlib import Path

import chess
from PySide6.QtCore import QSize, Qt, QThread, QTimer, Signal
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QWidget,
)

from app.core.chess_game import ChessGame
from app.engine.stockfish_engine import ComputerEngine, StockfishEngine
from app.services.history_manager import HistoryManager, MatchRecord
from app.services.save_manager import SaveManager, SaveSlot
from app.services.user_profile_manager import UserProfileManager
from app.ui.analysis_dialog import AnalysisDialog
from app.ui.chessboard_widget import (
    ChessBoardWidget,
    PIECE_GLYPHS,
    compute_captured_pieces,
)
from app.ui.game_over_dialog import GameOverDialog
from app.ui.game_screen import GameScreen
from app.ui.history_screen import HistoryScreen
from app.ui.home_screen import HomeScreen
from app.ui.learn_screen import LearnScreen
from app.ui.save_slots_dialog import SaveSlotsDialog
from app.ui.setup_screen import SetupScreen
from app.ui.styles import app_global_theme


class ComputerWorker(QThread):
    """Background worker that queries the Computer chess engine without blocking the Qt UI thread."""

    move_ready = Signal(int, object)  # (request_id, uci_move_or_None)
    error_occurred = Signal(int, str)  # (request_id, error_message)

    def __init__(self, engine, board_copy, difficulty, request_id, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.board_copy = board_copy
        self.difficulty = difficulty
        self.request_id = request_id

    def run(self):
        try:
            uci_move = self.engine.get_best_move(
                self.board_copy, self.difficulty
            )
            self.move_ready.emit(self.request_id, uci_move)
        except Exception as exc:
            self.error_occurred.emit(self.request_id, str(exc))


# Backward-compatible alias
StockfishWorker = ComputerWorker


class MainWindow(QMainWindow):
    """Main application window coordinating the multi-screen navigation flow."""

    LOCAL_MODE = "Local 2-player"
    COMPUTER_MODE = "Play vs Computer"
    POST_THINKING_DELAY_MS: int = 1500

    def __init__(
        self,
        start_screen: str = "home",
        save_manager: SaveManager | None = None,
        profile_manager: UserProfileManager | None = None,
        history_manager: HistoryManager | None = None,
    ):
        super().__init__()
        self.setWindowTitle("JD Chess")
        self.resize(1060, 750)
        self.setMinimumSize(320, 480)
        self.setStyleSheet(app_global_theme())

        self.game = ChessGame()
        self.engine = None
        self.engine_error = None
        self.player_color = chess.BLACK
        self.save_manager = save_manager or SaveManager()
        self.profile_manager = profile_manager or UserProfileManager()
        self.history_manager = history_manager or HistoryManager()

        self._game_over_processed = False

        # Engine detection
        detected_engine = ComputerEngine.find_engine()
        self.engine_ready = bool(detected_engine)
        self.engine_path = detected_engine

        # Async Computer worker and post-thinking delay state
        self._computer_request_id = 0
        self._computer_worker = None
        self._pending_computer_move = None
        self._shutting_down = False
        self._computer_delay_timer = QTimer(self)
        self._computer_delay_timer.setSingleShot(True)
        self._computer_delay_timer.timeout.connect(
            self._on_computer_delay_timeout
        )

        # Captured pieces lists
        self.white_captured_pieces = []
        self.black_captured_pieces = []

        # Stacked Widget hosting all application screens
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # 1. Window 1: Main Home Menu
        self.home_screen = HomeScreen(
            save_manager=self.save_manager,
            profile_manager=self.profile_manager,
            history_manager=self.history_manager,
            engine_ready=self.engine_ready,
            engine_path=self.engine_path,
            parent=self,
        )
        self.home_screen.new_game_clicked.connect(self.navigate_to_setup)
        self.home_screen.continue_game_clicked.connect(self.open_continue_dialog)
        self.home_screen.learn_chess_clicked.connect(self.navigate_to_learn)
        self.home_screen.history_clicked.connect(self.navigate_to_history)
        self.home_screen.username_changed.connect(self._on_username_changed)
        self.stack.addWidget(self.home_screen)

        # 2. Window 2: Game Setup & Configuration
        self.setup_screen = SetupScreen(parent=self)
        self.setup_screen.start_game_clicked.connect(self.start_game_from_setup)
        self.setup_screen.back_to_menu_clicked.connect(self.navigate_to_home)
        self.setup_screen.mode_combo.currentTextChanged.connect(self.change_mode)
        self.setup_screen.color_combo.currentTextChanged.connect(self.change_color)
        self.setup_screen.difficulty_combo.currentTextChanged.connect(self.update_game_info)
        self.stack.addWidget(self.setup_screen)

        # 3. Window 3: Chess Board Game Screen
        self.game_screen = GameScreen(game=self.game, parent=self)
        self.game_screen.save_game_clicked.connect(self.open_save_dialog)
        self.game_screen.undo_move_clicked.connect(self.undo_move)
        self.game_screen.restart_game_clicked.connect(self.navigate_to_setup)
        self.game_screen.main_menu_clicked.connect(self.navigate_to_home)
        self.game_screen.analyze_game_clicked.connect(self.open_analysis_dialog)
        self.stack.addWidget(self.game_screen)

        # 4. Interactive Learning Screen (Learn Chess with companion CM)
        self.learn_screen = LearnScreen(
            profile_manager=self.profile_manager, parent=self
        )
        self.learn_screen.main_menu_clicked.connect(self.navigate_to_home)
        self.stack.addWidget(self.learn_screen)

        # 5. History & Rating Dashboard Screen
        self.history_screen = HistoryScreen(
            history_manager=self.history_manager, parent=self
        )
        self.history_screen.back_clicked.connect(self.navigate_to_home)
        self.stack.addWidget(self.history_screen)

        # Backward compatibility aliases for existing attributes and tests
        self.board_widget = self.game_screen.board_widget
        self.mode_combo = self.setup_screen.mode_combo
        self.color_combo = self.setup_screen.color_combo
        self.difficulty_combo = self.setup_screen.difficulty_combo
        self.white_captured_tray = self.game_screen.white_captured_tray
        self.black_captured_tray = self.game_screen.black_captured_tray
        self.status_label = self.game_screen.status_label
        self.turn_label = self.game_screen.turn_label
        self.moves_label = self.game_screen.moves_label
        self.undo_button = self.game_screen.undo_button
        self.new_game_button = self.game_screen.new_game_button
        self.engine_badge = self.home_screen.engine_badge

        self.setStyleSheet("QMainWindow { background-color: #F8FAFC; }")

        # Initial screen navigation
        if start_screen == "game":
            self.navigate_to_game()
        elif start_screen == "setup":
            self.navigate_to_setup()
        elif start_screen == "learn":
            self.navigate_to_learn()
        elif start_screen == "history":
            self.navigate_to_history()
        else:
            self.navigate_to_home()

        self.update_game_info()

    # --- Property delegate for _stockfish_worker to ensure backwards compatibility ---
    @property
    def _stockfish_worker(self):
        return self._computer_worker

    @_stockfish_worker.setter
    def _stockfish_worker(self, worker):
        self._computer_worker = worker

    # --- Multi-Window Navigation Methods ---

    def navigate_to_home(self) -> None:
        """Switch to Window 1: Main Home Menu."""
        self.home_screen.update_save_status()
        self.home_screen.update_profile_ui()
        self.stack.setCurrentWidget(self.home_screen)

    def navigate_to_setup(self) -> None:
        """Switch to Window 2: Game Setup & Configuration."""
        self.stack.setCurrentWidget(self.setup_screen)

    def navigate_to_game(self) -> None:
        """Switch to Window 3: Chess Board Game Screen."""
        self.stack.setCurrentWidget(self.game_screen)
        self.board_widget.update_square_geometry()
        self.board_widget.refresh()

    def navigate_to_learn(self) -> None:
        """Switch to Interactive Learn Screen with companion CM."""
        self.learn_screen.load_lesson(self.learn_screen.current_lesson)
        self.stack.setCurrentWidget(self.learn_screen)
        self.learn_screen.board_widget.update_square_geometry()
        self.learn_screen.board_widget.refresh()

    def navigate_to_history(self) -> None:
        """Switch to History & Player Rating Screen."""
        self.history_screen.refresh()
        self.stack.setCurrentWidget(self.history_screen)

    def _on_username_changed(self, new_name: str) -> None:
        if hasattr(self, "learn_screen"):
            self.learn_screen.load_lesson(self.learn_screen.current_lesson)

    def start_game_from_setup(self) -> None:
        """User clicked 'Start Game' on Window 2."""
        mode = self.setup_screen.mode_combo.currentText()
        color_text = self.setup_screen.color_combo.currentText()
        self.player_color = chess.WHITE if color_text == "White" else chess.BLACK

        if mode == self.COMPUTER_MODE and self.engine is None:
            try:
                self.engine = ComputerEngine()
                self.engine_error = None
            except Exception as exc:
                self.engine_error = str(exc)
                QMessageBox.warning(
                    self,
                    "Computer unavailable",
                    "JD Chess could not start Computer engine.\n\n"
                    f"{exc}\n\n"
                    "Install Computer engine and try again.",
                )
                self.setup_screen.mode_combo.blockSignals(True)
                self.setup_screen.mode_combo.setCurrentText(self.LOCAL_MODE)
                self.setup_screen.mode_combo.blockSignals(False)
                self.update_game_info()
                return

        self.start_new_game()
        self.navigate_to_game()

    # --- Save & Continue Game Flows ---

    def open_continue_dialog(self) -> None:
        """Open Continue Game dialog showing all active slots."""
        dialog = SaveSlotsDialog(self.save_manager, mode=SaveSlotsDialog.MODE_CONTINUE, parent=self)
        dialog.slot_loaded.connect(self.load_saved_game)
        dialog.exec()
        self.home_screen.update_save_status()

    def open_save_dialog(self) -> None:
        """Open Save Game dialog allowing user to choose a slot to save into."""
        dialog = SaveSlotsDialog(self.save_manager, mode=SaveSlotsDialog.MODE_SAVE, parent=self)
        dialog.slot_saved.connect(self.save_current_game)
        dialog.exec()
        self.home_screen.update_save_status()

    def save_current_game(self, slot_id: int, show_confirmation: bool = True) -> None:
        """Save the active match into the selected slot (1-3)."""
        mode = self.setup_screen.mode_combo.currentText()
        diff = self.setup_screen.difficulty_combo.currentText()
        color_str = "White" if self.player_color == chess.WHITE else "Black"
        uci_moves = self.game.get_uci_moves()
        fen = self.game.board.fen()
        turn_str = "White" if self.game.board.turn == chess.WHITE else "Black"
        status_text = self.status_label.text()

        self.save_manager.save_game(
            slot_id=slot_id,
            game_mode=mode,
            player_color=color_str,
            difficulty=diff,
            moves=uci_moves,
            fen=fen,
            turn=turn_str,
            status_text=status_text,
        )

        if show_confirmation and QApplication.platformName() != "offscreen":
            QMessageBox.information(
                self,
                "Game Saved",
                f"Your current game has been successfully saved to Slot {slot_id}!",
            )
        self.home_screen.update_save_status()

    def load_saved_game(self, slot_id: int) -> None:
        """Load and resume a match from the selected slot."""
        slot = self.save_manager.get_slot(slot_id)
        if not slot or not slot.is_active:
            if QApplication.platformName() != "offscreen":
                QMessageBox.warning(self, "Empty Slot", "This slot contains no saved game data.")
            return

        self.cancel_pending_computer_move()
        self._game_over_processed = False

        # Restore match settings
        self.setup_screen.mode_combo.blockSignals(True)
        self.setup_screen.mode_combo.setCurrentText(slot.game_mode)
        self.setup_screen.mode_combo.blockSignals(False)

        self.setup_screen.color_combo.blockSignals(True)
        self.setup_screen.color_combo.setCurrentText(slot.player_color)
        self.setup_screen.color_combo.blockSignals(False)

        self.setup_screen.difficulty_combo.blockSignals(True)
        self.setup_screen.difficulty_combo.setCurrentText(slot.difficulty)
        self.setup_screen.difficulty_combo.blockSignals(False)

        self.player_color = chess.WHITE if slot.player_color == "White" else chess.BLACK

        # Engine initialization if computer mode
        if slot.game_mode == self.COMPUTER_MODE and self.engine is None:
            try:
                self.engine = ComputerEngine()
                self.engine_error = None
            except Exception as exc:
                self.engine_error = str(exc)
                QMessageBox.warning(
                    self,
                    "Computer unavailable",
                    "JD Chess could not start Computer engine.\n\n"
                    f"{exc}\n\n"
                    "Install Computer engine and try again.",
                )
                self.setup_screen.mode_combo.setCurrentText(self.LOCAL_MODE)

        # Restore moves onto board
        self.game.load_uci_moves(slot.moves)
        self.board_widget.clear_selection()
        self.board_widget.set_orientation(self.player_color)
        self.update_game_info()

        # Navigate to Window 3
        self.navigate_to_game()

        # If loaded into computer's turn, trigger computer move
        if (
            self.is_computer_mode()
            and not self.game.board.is_game_over()
            and self.game.board.turn != self.player_color
        ):
            self.make_computer_move()

    # --- Match & Board Methods ---

    def update_tray_layout(self) -> None:
        """Ensure capture trays / banners reflect board perspective."""
        self.board_widget.set_orientation(self.player_color)
        self.update_game_info()

    def get_captured_pieces(self) -> tuple[list[str], list[str]]:
        """Return tuple of (white_captured_glyphs, black_captured_glyphs)."""
        return list(self.white_captured_pieces), list(self.black_captured_pieces)

    def is_computer_mode(self) -> bool:
        return self.setup_screen.mode_combo.currentText() == self.COMPUTER_MODE

    def is_computer_thinking_or_pending(self) -> bool:
        """Return True if Computer is currently calculating or delay timer is active."""
        worker_running = (
            self._computer_worker is not None
            and self._computer_worker.isRunning()
        )
        timer_running = self._computer_delay_timer.isActive()
        return worker_running or timer_running

    def is_human_turn(self) -> bool:
        if not self.is_computer_mode():
            return True
        if self.is_computer_thinking_or_pending():
            return False
        return self.game.board.turn == self.player_color

    def cancel_pending_computer_move(self) -> None:
        """Cancel any in-flight search, delay timer, or queued move."""
        self._computer_request_id += 1
        self._pending_computer_move = None
        if self._computer_delay_timer.isActive():
            self._computer_delay_timer.stop()

    def change_mode(self, mode: str) -> None:
        self.cancel_pending_computer_move()
        if mode == self.COMPUTER_MODE and self.engine is None:
            try:
                self.engine = ComputerEngine()
                self.engine_error = None
            except Exception as exc:
                self.engine_error = str(exc)
                QMessageBox.warning(
                    self,
                    "Computer unavailable",
                    "JD Chess could not start Computer engine.\n\n"
                    f"{exc}\n\n"
                    "Install Computer engine and try again.",
                )
                self.setup_screen.mode_combo.blockSignals(True)
                self.setup_screen.mode_combo.setCurrentText(self.LOCAL_MODE)
                self.setup_screen.mode_combo.blockSignals(False)
                self.update_game_info()
                return

        if mode == self.LOCAL_MODE:
            self.close_engine()

        self.start_new_game()

    def change_color(self, color_name: str) -> None:
        self.cancel_pending_computer_move()
        self.player_color = (
            chess.WHITE if color_name == "White" else chess.BLACK
        )
        self.board_widget.set_orientation(self.player_color)
        self.start_new_game()

    def close_engine(self) -> None:
        self.cancel_pending_computer_move()

        worker = self._computer_worker
        if worker is not None and worker.isRunning():
            worker.wait()

        self._computer_worker = None

        if self.engine is not None:
            try:
                self.engine.close()
            except Exception:
                pass
            self.engine = None

    def start_new_game(self) -> None:
        self.cancel_pending_computer_move()
        self._game_over_processed = False
        self.game.new_game()
        self.board_widget.clear_selection()
        self.board_widget.set_orientation(self.player_color)
        self.board_widget.refresh()
        self.update_game_info()

        if (
            self.is_computer_mode()
            and self.player_color == chess.BLACK
        ):
            self.make_computer_move()

    def on_human_move_made(self) -> None:
        self.update_game_info()

        if self.is_computer_mode() and not self.game.board.is_game_over():
            self.make_computer_move()

    def make_computer_move(self) -> None:
        if self.engine is None or self.game.board.is_game_over():
            self.update_game_info()
            return

        if self.game.board.turn == self.player_color:
            self.update_game_info()
            return

        if self.is_computer_thinking_or_pending():
            return

        self._computer_request_id += 1
        req_id = self._computer_request_id

        board_copy = self.game.board.copy()
        difficulty = self.setup_screen.difficulty_combo.currentText()

        self.status_label.setText("Computer is thinking...")

        self._computer_worker = ComputerWorker(
            self.engine, board_copy, difficulty, req_id, parent=self
        )
        self._computer_worker.move_ready.connect(self._on_computer_move_ready)
        self._computer_worker.error_occurred.connect(self._on_computer_error)
        self._computer_worker.finished.connect(
            self._on_computer_worker_finished
        )
        self._computer_worker.start()

    def _on_computer_worker_finished(self) -> None:
        worker = self.sender()

        if worker is not self._computer_worker:
            return

        worker_req_id = getattr(worker, "request_id", None)
        request_was_stale = (
            worker_req_id != self._computer_request_id
        )
        self._computer_worker = None

        if self._shutting_down or not request_was_stale:
            return

        if (
            self.is_computer_mode()
            and not self.game.board.is_game_over()
            and self.game.board.turn != self.player_color
            and self._pending_computer_move is None
            and not self._computer_delay_timer.isActive()
        ):
            self.make_computer_move()

    _on_stockfish_worker_finished = _on_computer_worker_finished

    def _on_computer_move_ready(self, req_id: int, uci_move: str | None) -> None:
        if req_id != self._computer_request_id:
            return

        if not self.is_computer_mode() or self.game.board.is_game_over():
            return

        if uci_move is None:
            self.update_game_info()
            return

        self._pending_computer_move = uci_move
        delay = getattr(self, "POST_THINKING_DELAY_MS", 1500)
        if delay <= 0:
            self._on_computer_delay_timeout()
        else:
            self.status_label.setText("Computer is thinking...")
            self._computer_delay_timer.start(delay)

    def _on_computer_delay_timeout(self) -> None:
        if self._pending_computer_move is None:
            return

        uci_move = self._pending_computer_move
        self._pending_computer_move = None

        if not self.is_computer_mode() or self.game.board.is_game_over():
            self.update_game_info()
            return

        if self.game.board.turn == self.player_color:
            self.update_game_info()
            return

        try:
            move = chess.Move.from_uci(uci_move)
            if move in self.game.board.legal_moves:
                self.game.make_move(uci_move)
        except Exception as exc:
            QMessageBox.warning(
                self,
                "Computer move failed",
                f"Computer move was invalid:\n{exc}",
            )

        self.board_widget.clear_selection()
        self.update_game_info()

    def _on_computer_error(self, req_id: int, error_msg: str) -> None:
        if req_id != self._computer_request_id:
            return

        self._pending_computer_move = None
        QMessageBox.warning(
            self,
            "Computer move failed",
            f"Computer could not make a move:\n{error_msg}",
        )
        self.board_widget.clear_selection()
        self.update_game_info()

    def update_game_info(self, *_) -> None:
        status = self.game.get_status()

        if status.is_game_over:
            if status.is_checkmate:
                message = f"Checkmate! {status.turn} has no legal move."
            elif status.is_stalemate:
                message = "Draw by stalemate."
            else:
                message = f"Game over: {status.termination}."
        elif status.is_check:
            message = f"⚠ {status.turn} is in check!"
        elif self.is_computer_mode() and not self.is_human_turn():
            message = "Computer is thinking..."
        elif self.is_computer_mode():
            color_text = "White" if self.player_color == chess.WHITE else "Black"
            diff_text = self.setup_screen.difficulty_combo.currentText()
            message = f"Your turn ({color_text}) vs Computer ({diff_text})."
        else:
            message = "Select a piece to see its legal moves."

        turn_symbol = "⚪" if status.turn == "White" else "⚫"
        self.turn_label.setText(f"{turn_symbol} {status.turn} to move")
        self.status_label.setText(message)

        history = self.game.get_move_history()
        if not history:
            self.moves_label.setText("No moves yet")
        else:
            formatted = []
            for index in range(0, len(history), 2):
                white_move = history[index]
                black_move = (
                    history[index + 1] if index + 1 < len(history) else ""
                )
                formatted.append(
                    f"{index // 2 + 1:>2}. {white_move:<8} {black_move}"
                )
            self.moves_label.setText("\n".join(formatted))

        # Reconstruct captured pieces without mutating the live game board
        white_caps, black_caps = compute_captured_pieces(
            self.game.board.move_stack
        )
        self.white_captured_pieces = white_caps
        self.black_captured_pieces = black_caps

        # Update Game Screen match pill and player banners
        mode_text = self.setup_screen.mode_combo.currentText()
        diff_text = self.setup_screen.difficulty_combo.currentText()
        self.game_screen.update_match_pill(mode_text, diff_text, self.player_color)
        self.game_screen.update_banners(status.turn, white_caps, black_caps)

        self.board_widget.refresh()

        # Handle Game Over triggers and recording
        if status.is_game_over and not self._game_over_processed:
            self._game_over_processed = True
            self._process_game_over(status, mode_text, diff_text)

    def _process_game_over(self, status, mode_text: str, diff_text: str) -> None:
        """Record game completion in history and trigger post-game feedback dialog."""
        player_color_str = "White" if self.player_color == chess.WHITE else "Black"

        if status.is_checkmate:
            # The player whose turn it is has no legal move and is checkmated
            if self.game.board.turn != self.player_color:
                result = "win"
                result_label = "Checkmate – You Won!"
            else:
                if self.is_computer_mode():
                    result = "loss"
                    result_label = "Checkmate – Computer Won"
                else:
                    winner = "White" if self.game.board.turn == chess.BLACK else "Black"
                    result = "win"
                    result_label = f"Checkmate – {winner} Won"
        elif status.is_stalemate:
            result = "draw"
            result_label = "Draw – Stalemate"
        else:
            result = "draw"
            result_label = f"Draw – {status.termination}"

        # Record match in player history and update Elo rating
        self.history_manager.record_match(
            game_mode=mode_text,
            player_color=player_color_str,
            difficulty=diff_text,
            result=result,
            result_label=result_label,
            moves=self.game.get_uci_moves(),
        )

        # Show styled GameOverDialog unless running in headless test mode
        if QApplication.platformName() != "offscreen":
            QTimer.singleShot(
                400,
                lambda: self._show_game_over_dialog(
                    result=result,
                    result_label=result_label,
                    game_mode=mode_text,
                    player_color=player_color_str,
                    difficulty=diff_text,
                ),
            )

    def _show_game_over_dialog(
        self,
        result: str,
        result_label: str,
        game_mode: str,
        player_color: str,
        difficulty: str,
    ) -> None:
        moves = self.game.get_uci_moves()
        dialog = GameOverDialog(
            result=result,
            result_label=result_label,
            move_count=len(moves),
            game_mode=game_mode,
            player_color=player_color,
            difficulty=difficulty,
            can_analyze=True,
            parent=self,
        )
        dialog.analyze_clicked.connect(self.open_analysis_dialog)
        dialog.new_game_clicked.connect(self.navigate_to_setup)
        dialog.exec()

    def open_analysis_dialog(self) -> None:
        """Open post-game analysis window with scorecard and move annotations."""
        color_str = "White" if self.player_color == chess.WHITE else "Black"
        dialog = AnalysisDialog(
            uci_moves=self.game.get_uci_moves(),
            san_moves=self.game.get_move_history(),
            player_color=color_str,
            engine_path=self.engine_path,
            parent=self,
        )
        dialog.exec()

    def undo_move(self) -> None:
        computer_mode = self.is_computer_mode()
        human_turn_before_undo = (
            self.game.board.turn == self.player_color
        )
        move_count = len(self.game.board.move_stack)

        self.cancel_pending_computer_move()
        self._game_over_processed = False

        if computer_mode:
            if human_turn_before_undo:
                moves_to_undo = 2 if move_count >= 2 else move_count
            else:
                moves_to_undo = 1 if move_count else 0

            for _ in range(moves_to_undo):
                if self.game.board.move_stack:
                    self.game.undo_move()
        elif self.game.board.move_stack:
            self.game.undo_move()

        self.board_widget.clear_selection()
        self.update_game_info()

        if (
            computer_mode
            and not self.game.board.is_game_over()
            and self.game.board.turn != self.player_color
        ):
            self.make_computer_move()

    def closeEvent(self, event) -> None:
        self._shutting_down = True
        self.close_engine()
        event.accept()