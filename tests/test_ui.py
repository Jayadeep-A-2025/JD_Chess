from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import chess
import pytest
from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow


@pytest.fixture(scope="module")
def qt_app():
    app = QApplication.instance() or QApplication([])
    yield app


def test_board_has_64_squares(qt_app):
    window = MainWindow()
    assert len(window.board_widget.square_buttons) == 64
    for row in range(8):
        for col in range(8):
            assert (row, col) in window.board_widget.square_buttons
    window.close()


def test_coordinate_labels_black_orientation(qt_app):
    window = MainWindow()
    assert window.board_widget.player_color == chess.BLACK
    assert window.board_widget.get_rank_labels() == ["1", "2", "3", "4", "5", "6", "7", "8"]
    assert window.board_widget.get_file_labels() == ["h", "g", "f", "e", "d", "c", "b", "a"]
    # Verify coordinate mapping for Black orientation
    assert chess.square_name(window.board_widget.visual_to_square(0, 0)) == "h1"
    assert chess.square_name(window.board_widget.visual_to_square(0, 7)) == "a1"
    assert chess.square_name(window.board_widget.visual_to_square(7, 0)) == "h8"
    assert chess.square_name(window.board_widget.visual_to_square(7, 7)) == "a8"
    assert chess.square_name(window.board_widget.visual_to_square(1, 3)) == "e2"
    window.close()


def test_coordinate_labels_white_orientation(qt_app):
    window = MainWindow()
    window.board_widget.set_orientation(chess.WHITE)
    assert window.board_widget.player_color == chess.WHITE
    assert window.board_widget.get_rank_labels() == ["8", "7", "6", "5", "4", "3", "2", "1"]
    assert window.board_widget.get_file_labels() == ["a", "b", "c", "d", "e", "f", "g", "h"]
    # Verify coordinate mapping for White orientation
    assert chess.square_name(window.board_widget.visual_to_square(0, 0)) == "a8"
    assert chess.square_name(window.board_widget.visual_to_square(0, 7)) == "h8"
    assert chess.square_name(window.board_widget.visual_to_square(7, 0)) == "a1"
    assert chess.square_name(window.board_widget.visual_to_square(7, 7)) == "h1"
    assert chess.square_name(window.board_widget.visual_to_square(6, 4)) == "e2"
    window.close()


def test_board_squares_remain_square_and_fit_on_resize(qt_app):
    window = MainWindow(start_screen="game")
    window.show()
    qt_app.processEvents()

    # Wide window layout
    window.resize(1200, 600)
    qt_app.processEvents()
    bw = window.board_widget
    btn0 = bw.square_buttons[(0, 0)]
    assert btn0.width() == btn0.height() > 0
    assert bw.board_frame.y() + bw.board_frame.height() <= bw.height()
    assert bw.board_frame.x() + bw.board_frame.width() <= bw.width()

    # Tall window layout
    window.resize(700, 900)
    qt_app.processEvents()
    assert btn0.width() == btn0.height() > 0
    assert bw.board_frame.y() + bw.board_frame.height() <= bw.height()
    assert bw.board_frame.x() + bw.board_frame.width() <= bw.width()

    window.close()


def test_clicking_piece_and_destination_makes_move(qt_app):
    window = MainWindow()

    # With Black at the bottom, e2 is row 1, column 3.
    window.board_widget.square_buttons[(1, 3)].click()

    # e4 is row 3, column 3.
    window.board_widget.square_buttons[(3, 3)].click()

    assert window.game.board.peek().uci() == "e2e4"
    assert window.game.get_status().turn == "Black"

    window.close()



def test_last_move_highlights_both_squares(qt_app):
    window = MainWindow()
    board_widget = window.board_widget

    # Make e2-e4 with Black's orientation.
    board_widget.square_buttons[(1, 3)].click()
    board_widget.square_buttons[(3, 3)].click()

    assert board_widget.last_move_squares == {chess.E2, chess.E4}

    for square in (chess.E2, chess.E4):
        row = chess.square_rank(square)
        col = 7 - chess.square_file(square)
        style = board_widget.square_buttons[(row, col)].styleSheet()
        assert "#E6C657" in style

    window.close()



def test_captured_piece_trays_update_after_capture(qt_app):
    window = MainWindow()

    # Fool's Mate setup, followed by a simple legal capture:
    # 1. e4 d5 2. exd5
    for move in ("e2e4", "d7d5", "e4d5"):
        window.game.make_move(move)

    window.update_game_info()

    white_caps, black_caps = window.get_captured_pieces()

    assert white_caps == ["♟"]
    assert black_caps == []
    assert window.white_captured_tray.text() == "♟"
    assert window.black_captured_tray.text() == ""

    window.close()


def test_capture_trays_update_after_undo_and_restart(qt_app):
    window = MainWindow()

    for move in ("e2e4", "d7d5", "e4d5"):
        window.game.make_move(move)

    window.update_game_info()
    assert window.get_captured_pieces()[0] == ["♟"]

    window.game.undo_move()
    window.update_game_info()
    assert window.get_captured_pieces() == ([], [])

    window.start_new_game()
    assert window.get_captured_pieces() == ([], [])
    assert window.board_widget.last_move_squares == set()

    window.close()


def test_en_passant_capture_appears_in_white_tray(qt_app):
    window = MainWindow()

    for move in ("e2e4", "a7a6", "e4e5", "d7d5", "e5d6"):
        window.game.make_move(move)

    window.update_game_info()

    white_caps, black_caps = window.get_captured_pieces()
    assert white_caps == ["♟"]
    assert black_caps == []

    window.close()


import threading
import time


class SlowFakeEngine:
    """Fake engine that lets a test control when the first search finishes."""

    def __init__(self):
        self.first_search_started = threading.Event()
        self.release_first_search = threading.Event()
        self.lock = threading.Lock()
        self.calls = 0
        self.closed = False

    def get_best_move(self, board, difficulty="Medium"):
        with self.lock:
            self.calls += 1
            call_number = self.calls

        if call_number == 1:
            self.first_search_started.set()
            self.release_first_search.wait(timeout=5)

        legal_moves = list(board.legal_moves)
        return legal_moves[0].uci() if legal_moves else None

    def close(self):
        self.closed = True


def wait_for_condition(qt_app, condition, timeout=3):
    """Process Qt events while waiting for an asynchronous condition."""
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        qt_app.processEvents()
        if condition():
            return True
        time.sleep(0.01)

    qt_app.processEvents()
    return condition()


def test_restart_during_search_starts_fresh_computer_move(qt_app):
    window = MainWindow()
    fake_engine = SlowFakeEngine()
    window.engine = fake_engine  # type: ignore
    window.POST_THINKING_DELAY_MS = 0

    window.mode_combo.blockSignals(True)
    window.mode_combo.setCurrentText(window.COMPUTER_MODE)
    window.mode_combo.blockSignals(False)

    try:
        window.change_mode(window.COMPUTER_MODE)

        assert fake_engine.first_search_started.wait(timeout=2)

        # Restart while the first search is still running.
        window.start_new_game()
        assert len(window.game.board.move_stack) == 0

        # Release the old search. A fresh search should follow.
        fake_engine.release_first_search.set()

        assert wait_for_condition(
            qt_app,
            lambda: fake_engine.calls >= 2
            and len(window.game.board.move_stack) >= 1,
        )
    finally:
        fake_engine.release_first_search.set()
        wait_for_condition(
            qt_app,
            lambda: (
                window._stockfish_worker is None
                or not window._stockfish_worker.isRunning()
            ),
            timeout=6,
        )
        window.close()
        qt_app.processEvents()


def test_undo_after_computer_opening_as_black_restarts_search(qt_app):
    window = MainWindow()
    fake_engine = SlowFakeEngine()
    window.engine = fake_engine  # type: ignore
    window.POST_THINKING_DELAY_MS = 0

    window.mode_combo.blockSignals(True)
    window.mode_combo.setCurrentText(window.COMPUTER_MODE)
    window.mode_combo.blockSignals(False)

    try:
        # Start a new game as Black; the computer plays White.
        window.change_mode(window.COMPUTER_MODE)

        assert fake_engine.first_search_started.wait(timeout=2)

        # Allow the computer's opening move to finish.
        fake_engine.release_first_search.set()
        assert wait_for_condition(
            qt_app,
            lambda: len(window.game.board.move_stack) == 1
            and window.game.board.turn == chess.BLACK,
        )

        # Undo the opening. The computer must play again as White.
        window.undo_move()

        assert wait_for_condition(
            qt_app,
            lambda: fake_engine.calls >= 2
            and len(window.game.board.move_stack) == 1
            and window.game.board.turn == chess.BLACK,
        )

    finally:
        fake_engine.release_first_search.set()
        wait_for_condition(
            qt_app,
            lambda: (
                window._stockfish_worker is None
                or not window._stockfish_worker.isRunning()
            ),
            timeout=6,
        )
        window.close()
        qt_app.processEvents()


import tempfile
from pathlib import Path
from app.services.save_manager import SaveManager


def test_main_window_defaults_to_home_screen(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        sm = SaveManager(Path(tmpdir) / "saves.json")
        window = MainWindow(save_manager=sm)
        assert window.stack.currentWidget() == window.home_screen
        assert window.home_screen.new_game_card is not None
        assert window.home_screen.continue_game_card is not None
        assert "New Game" in window.home_screen.new_game_card.findChild(object, "homeNewGameBtn").text()
        assert "Continue Game" in window.home_screen.continue_btn.text()
        window.close()


def test_navigation_flow_home_setup_game_and_back(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        sm = SaveManager(Path(tmpdir) / "saves.json")
        window = MainWindow(save_manager=sm)

        # 1. Start on Home Screen
        assert window.stack.currentWidget() == window.home_screen

        # 2. Click "New Game" -> navigates to Setup Screen
        window.home_screen.new_game_clicked.emit()
        assert window.stack.currentWidget() == window.setup_screen

        # 3. Click "Back to Menu" -> returns to Home Screen
        window.setup_screen.back_to_menu_clicked.emit()
        assert window.stack.currentWidget() == window.home_screen

        # 4. Navigate back to Setup and click "Start Game" -> navigates to Game Screen
        window.navigate_to_setup()
        assert window.stack.currentWidget() == window.setup_screen
        window.setup_screen.start_game_clicked.emit()
        assert window.stack.currentWidget() == window.game_screen

        # 5. On Game Screen, click "Main Menu" -> returns to Home Screen
        window.game_screen.main_menu_clicked.emit()
        assert window.stack.currentWidget() == window.home_screen

        window.close()


def test_ui_cleanup_chessboard_view_has_no_config_controls(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        sm = SaveManager(Path(tmpdir) / "saves.json")
        window = MainWindow(save_manager=sm)

        # Ensure mode_combo and difficulty_combo are NOT children or descendants of game_screen
        game_screen_combos = window.game_screen.findChildren(object, "modeCombo")
        assert len(game_screen_combos) == 0

        game_screen_diff = window.game_screen.findChildren(object, "difficultyCombo")
        assert len(game_screen_diff) == 0

        # But they ARE present on setup_screen
        setup_screen_combos = window.setup_screen.findChildren(object, "modeCombo")
        assert len(setup_screen_combos) == 1
        assert setup_screen_combos[0] is window.setup_screen.mode_combo

        window.close()


def test_computer_renaming_in_labels_and_badges(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        sm = SaveManager(Path(tmpdir) / "saves.json")
        window = MainWindow(save_manager=sm)

        # Badge says "Computer", never "Stockfish"
        badge_text = window.engine_badge.text()
        assert "Computer" in badge_text
        assert "Stockfish" not in badge_text

        # Worker class alias check
        from app.ui.main_window import ComputerWorker, StockfishWorker
        assert StockfishWorker is ComputerWorker

        # Status text in computer mode when computer is thinking
        window.setup_screen.mode_combo.setCurrentText(window.COMPUTER_MODE)
        window._pending_computer_move = "e2e4"
        window.POST_THINKING_DELAY_MS = 1000
        window.make_computer_move = lambda: None  # mock
        window._on_computer_move_ready(window._computer_request_id, "e2e4")
        assert "Computer is thinking..." in window.status_label.text()
        assert "Stockfish" not in window.status_label.text()

        window.cancel_pending_computer_move()
        window.close()


def test_save_and_continue_game_slots(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        sm = SaveManager(Path(tmpdir) / "saves.json")
        window = MainWindow(save_manager=sm)

        # Navigate to game and make moves: 1. e4 e5
        window.navigate_to_game()
        window.game.make_move("e2e4")
        window.game.make_move("e7e5")
        window.update_game_info()

        assert len(window.game.board.move_stack) == 2
        assert window.game.get_move_history() == ["e4", "e5"]

        # Save into Slot 1
        window.save_current_game(slot_id=1)
        assert sm.active_save_count() == 1
        saved_slot = sm.get_slot(1)
        assert saved_slot.is_active is True
        assert saved_slot.moves == ["e2e4", "e7e5"]
        assert saved_slot.move_count == 2

        # Start a new game, wiping live board
        window.start_new_game()
        assert len(window.game.board.move_stack) == 0
        assert window.game.get_move_history() == []

        # Load from Slot 1
        window.load_saved_game(slot_id=1)
        assert window.stack.currentWidget() == window.game_screen
        assert len(window.game.board.move_stack) == 2
        assert window.game.get_move_history() == ["e4", "e5"]
        assert window.game.board.turn == chess.WHITE

        window.close()


def test_player_banners_and_turn_indicators_update(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        sm = SaveManager(Path(tmpdir) / "saves.json")
        window = MainWindow(start_screen="game", save_manager=sm)

        # Playing as White (player_color = chess.WHITE)
        window.player_color = chess.WHITE
        window.update_tray_layout()

        # Bottom banner is You (White), Top banner is Opponent (Black)
        assert "White" in window.game_screen.bottom_banner["name"].text()
        assert "Black" in window.game_screen.top_banner["name"].text()

        # Turn is White -> bottom banner turn chip shows "● To Move"
        assert window.game_screen.bottom_banner["turn_chip"].text() == "● To Move"
        assert window.game_screen.top_banner["turn_chip"].text() == ""

        # Make move e2e4 -> now Black to move
        window.game.make_move("e2e4")
        window.update_game_info()

        assert window.game_screen.top_banner["turn_chip"].text() == "● To Move"
        assert window.game_screen.bottom_banner["turn_chip"].text() == ""

        window.close()

