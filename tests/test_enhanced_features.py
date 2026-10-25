from __future__ import annotations

"""Automated test suite verifying the enhanced features:
- UserProfileManager & custom username
- Progressive Curriculum & companion CM (Chess Mate)
- Interactive LearnScreen module
- Match History, rating tracking, and filters
- Game Over feedback dialog & post-game analysis
- Fallback heuristic analysis & performance scorecard
- Renaming Stockfish to Computer across user-facing text
"""

import os
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import chess
import pytest
from PySide6.QtWidgets import QApplication

from app.core.chess_game import ChessGame
from app.services.analysis_service import AnalysisResult, analyze_game
from app.services.curriculum import (
    CURRICULUM,
    get_curriculum,
    get_lesson_by_id,
    get_next_lesson,
    get_prev_lesson,
)
from app.services.history_manager import HistoryManager, compute_rating_change
from app.services.save_manager import SaveManager
from app.services.user_profile_manager import UserProfileManager
from app.ui.analysis_dialog import AnalysisDialog
from app.ui.game_over_dialog import GameOverDialog
from app.ui.history_screen import HistoryScreen
from app.ui.home_screen import HomeScreen
from app.ui.learn_screen import LearnScreen
from app.ui.main_window import MainWindow


@pytest.fixture(scope="module")
def qt_app():
    app = QApplication.instance() or QApplication([])
    yield app


# =====================================================================
# 1. UserProfileManager Tests
# =====================================================================

def test_user_profile_defaults_and_custom_username():
    with tempfile.TemporaryDirectory() as tmpdir:
        profile_path = Path(tmpdir) / "profile.json"
        pm = UserProfileManager(profile_path)

        assert pm.get_username() == "Grandmaster"
        assert pm.get_profile().completed_lessons == []

        # Set custom username
        saved = pm.set_username("Aparna")
        assert saved == "Aparna"
        assert pm.get_username() == "Aparna"

        # Persistence check
        pm2 = UserProfileManager(profile_path)
        assert pm2.get_username() == "Aparna"


def test_user_profile_lesson_progress_saving():
    with tempfile.TemporaryDirectory() as tmpdir:
        profile_path = Path(tmpdir) / "profile.json"
        pm = UserProfileManager(profile_path)

        assert not pm.is_lesson_completed("beginner_pawn")
        pm.mark_lesson_completed("beginner_pawn")
        assert pm.is_lesson_completed("beginner_pawn")

        # Persistence check
        pm2 = UserProfileManager(profile_path)
        assert pm2.is_lesson_completed("beginner_pawn")
        assert "beginner_pawn" in pm2.get_profile().completed_lessons


# =====================================================================
# 2. Progressive Curriculum & CM Companion Tests
# =====================================================================

def test_curriculum_structure_and_categories():
    lessons = get_curriculum()
    assert len(lessons) >= 16

    categories = {l.category for l in lessons}
    assert "Beginner Basics" in categories
    assert "Intermediate Tactics" in categories
    assert "Pro Strategies" in categories

    # Verify lesson progression helpers
    first = lessons[0]
    second = get_next_lesson(first.id)
    assert second is not None
    assert second.id == lessons[1].id
    assert get_prev_lesson(second.id).id == first.id


def test_cm_personalized_dialogue():
    lesson = get_lesson_by_id("beginner_pawn")
    assert lesson is not None
    formatted_intro = lesson.cm_intro.format(username="Alex")
    assert "Alex" in formatted_intro
    assert "CM" in formatted_intro

    formatted_success = lesson.cm_success.format(username="Alex")
    assert "Alex" in formatted_success


# =====================================================================
# 3. Interactive LearnScreen Tests
# =====================================================================

def test_learn_screen_loads_and_displays_cm(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        profile_path = Path(tmpdir) / "profile.json"
        pm = UserProfileManager(profile_path)
        pm.set_username("Kasparov")

        screen = LearnScreen(profile_manager=pm)
        assert "Kasparov" in screen.cm_dialogue_lbl.text()
        assert screen.board_widget is not None
        assert len(screen.lesson_buttons) == len(CURRICULUM)


def test_learn_screen_solve_lesson_with_correct_move(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        profile_path = Path(tmpdir) / "profile.json"
        pm = UserProfileManager(profile_path)
        pm.set_username("Magnus")

        screen = LearnScreen(profile_manager=pm)
        lesson = get_lesson_by_id("beginner_pawn")
        screen.load_lesson(lesson)

        assert not pm.is_lesson_completed(lesson.id)

        # Make the target move e2e4
        screen._on_user_board_move("e2e4")

        assert screen.is_lesson_solved is True
        assert pm.is_lesson_completed(lesson.id)
        assert "Objective Complete" in screen.cm_objective_lbl.text()
        assert "Magnus" in screen.cm_dialogue_lbl.text()


def test_learn_screen_incorrect_move_provides_cm_guidance(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        profile_path = Path(tmpdir) / "profile.json"
        pm = UserProfileManager(profile_path)
        pm.set_username("Hikaru")

        screen = LearnScreen(profile_manager=pm)
        lesson = get_lesson_by_id("beginner_pawn")
        screen.load_lesson(lesson)

        # Make an incorrect move
        screen._on_user_board_move("a2a3")

        assert screen.is_lesson_solved is False
        assert "Not quite, Hikaru" in screen.cm_dialogue_lbl.text()


# =====================================================================
# 4. Match History, Elo Rating & Filters Tests
# =====================================================================

def test_elo_rating_computation():
    # Win against equal opponent -> +16
    assert compute_rating_change(1200, 1200, "win") == 16
    # Loss against equal opponent -> -16
    assert compute_rating_change(1200, 1200, "loss") == -16
    # Draw against equal opponent -> 0
    assert compute_rating_change(1200, 1200, "draw") == 0


def test_history_manager_persistence_and_logging():
    with tempfile.TemporaryDirectory() as tmpdir:
        hist_path = Path(tmpdir) / "history.json"
        hm = HistoryManager(hist_path)

        assert hm.get_rating() == 1200
        assert hm.get_matches_count() == 0

        # Record a win vs Computer
        rec = hm.record_match(
            game_mode="Play vs Computer",
            player_color="White",
            difficulty="Medium",
            result="win",
            result_label="Checkmate – You Won!",
            moves=["e2e4", "e7e5", "g1f3"],
        )
        assert rec.result == "win"
        assert rec.rating_change > 0
        assert hm.get_rating() == 1200 + rec.rating_change
        assert hm.get_matches_count() == 1


def test_history_screen_filtering(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        hist_path = Path(tmpdir) / "history.json"
        hm = HistoryManager(hist_path)

        hm.record_match("Play vs Computer", "White", "Medium", "win", "Won", ["e2e4"])
        hm.record_match("Play vs Computer", "Black", "Hard", "loss", "Lost", ["e2e4"])
        hm.record_match("Local 2-player", "White", "N/A", "draw", "Draw", ["e2e4"])

        screen = HistoryScreen(history_manager=hm)
        all_matches = hm.get_all_matches()
        assert len(all_matches) == 3

        # Test filter by outcome
        screen._selected_outcome = "Wins Only"
        filtered = screen._filter_matches(all_matches)
        assert len(filtered) == 1
        assert filtered[0].result == "win"

        # Test filter by mode
        screen._selected_outcome = "All Outcomes"
        screen._selected_mode = "Local 2-player"
        filtered_mode = screen._filter_matches(all_matches)
        assert len(filtered_mode) == 1
        assert filtered_mode[0].game_mode == "Local 2-player"


# =====================================================================
# 5. Analysis Service & Fallback Tests
# =====================================================================

def test_heuristic_analysis_fallback_produces_scorecard():
    # Run analysis without external engine binary
    moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "g8f6"]
    result = analyze_game(uci_moves=moves, engine_path=None, player_color="White")

    assert isinstance(result, AnalysisResult)
    assert len(result.annotations) == 6
    assert 0 <= result.accuracy_score <= 100
    assert result.grade in ("A+", "A", "B", "C", "D", "F")
    assert all(a.comment for a in result.annotations)


def test_analysis_dialog_renders_without_crashing(qt_app):
    moves = ["e2e4", "e7e5"]
    dialog = AnalysisDialog(
        uci_moves=moves,
        san_moves=["e4", "e5"],
        player_color="White",
        engine_path=None,
    )
    assert dialog.windowTitle() == "Game Analysis"
    dialog.close()


# =====================================================================
# 6. GameOverDialog Tests
# =====================================================================

def test_game_over_dialog_titles_and_actions(qt_app):
    # Win dialog
    win_dlg = GameOverDialog(
        result="win",
        result_label="Checkmate – You Won!",
        move_count=20,
        game_mode="Play vs Computer",
        player_color="White",
        difficulty="Medium",
    )
    assert win_dlg.findChild(object, "gameOverOuter") is not None
    win_dlg.close()

    # Loss dialog
    loss_dlg = GameOverDialog(
        result="loss",
        result_label="Checkmate – Computer Won",
        move_count=25,
        game_mode="Play vs Computer",
        player_color="White",
        difficulty="Hard",
    )
    assert loss_dlg is not None
    loss_dlg.close()


# =====================================================================
# 7. Multi-Window Navigation & No "Stockfish" in UI
# =====================================================================

def test_main_window_multi_screen_navigation(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        sm = SaveManager(Path(tmpdir) / "saves.json")
        pm = UserProfileManager(Path(tmpdir) / "profile.json")
        hm = HistoryManager(Path(tmpdir) / "history.json")

        window = MainWindow(
            start_screen="home",
            save_manager=sm,
            profile_manager=pm,
            history_manager=hm,
        )

        # Starts on Home screen
        assert window.stack.currentWidget() is window.home_screen

        # Navigate to Setup (Window 2)
        window.navigate_to_setup()
        assert window.stack.currentWidget() is window.setup_screen

        # Navigate to Chess Board (Window 3)
        window.navigate_to_game()
        assert window.stack.currentWidget() is window.game_screen

        # Navigate to Learn Screen
        window.navigate_to_learn()
        assert window.stack.currentWidget() is window.learn_screen

        # Navigate to History Screen
        window.navigate_to_history()
        assert window.stack.currentWidget() is window.history_screen

        # Navigate back to Home Screen
        window.navigate_to_home()
        assert window.stack.currentWidget() is window.home_screen

        window.close()


def test_no_stockfish_in_user_facing_ui(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        sm = SaveManager(Path(tmpdir) / "saves.json")
        pm = UserProfileManager(Path(tmpdir) / "profile.json")
        hm = HistoryManager(Path(tmpdir) / "history.json")

        window = MainWindow(
            start_screen="home",
            save_manager=sm,
            profile_manager=pm,
            history_manager=hm,
        )

        # Engine badge on home screen
        assert "Stockfish" not in window.engine_badge.text()
        assert "Computer" in window.engine_badge.text()

        # Status text
        assert "Stockfish" not in window.status_label.text()

        # Setup screen combos
        mode_items = [
            window.setup_screen.mode_combo.itemText(i)
            for i in range(window.setup_screen.mode_combo.count())
        ]
        for item in mode_items:
            assert "Stockfish" not in item

        diff_items = [
            window.setup_screen.difficulty_combo.itemText(i)
            for i in range(window.setup_screen.difficulty_combo.count())
        ]
        for item in diff_items:
            assert "Stockfish" not in item

        window.close()
