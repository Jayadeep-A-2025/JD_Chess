from __future__ import annotations

"""Automated test suite for the JD Chess Learning Academy Redesign:
- 7 Progressive Curriculum Tiers & 42 Comprehensive Lessons
- 100% Legal Moves, FEN Validity, and Educational Content Integrity
- Smart Progress Tracking (Accuracy %, Topic Weaknesses, Hints, Progressive Unlocking)
- Interactive Learning Screen Modes (Practice, Theory, Demo, Concept Assessment Quiz)
- CM Companion Dynamic Coaching, Threat Detection, and Error Explanations
"""

import tempfile
from pathlib import Path

import chess
import pytest
from PySide6.QtWidgets import QApplication

from app.services.curriculum import (
    CURRICULUM,
    Lesson,
    get_curriculum,
    get_lesson_by_id,
    get_next_lesson,
    get_prev_lesson,
)
from app.services.user_profile_manager import UserProfile, UserProfileManager
from app.ui.learn_screen import LearnScreen


@pytest.fixture(scope="session")
def qt_app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


# =============================================================================
# 1. CURRICULUM ARCHITECTURE & INTEGRITY TESTS
# =============================================================================

def test_academy_curriculum_structure_7_levels_42_lessons():
    """Verify exactly 7 structured levels, each containing 6 lessons (42 total)."""
    lessons = get_curriculum()
    assert len(lessons) == 42, f"Expected 42 lessons in Academy curriculum, got {len(lessons)}"

    level_names = {
        1: "Beginner Foundations",
        2: "Chess Tactics",
        3: "Opening Mastery",
        4: "Middlegame Strategy",
        5: "Advanced Calculation",
        6: "Endgame Mastery",
        7: "Competitive Chess",
    }

    for lvl_num, expected_name in level_names.items():
        lvl_lessons = [l for l in lessons if l.level_number == lvl_num]
        assert len(lvl_lessons) == 6, f"Level {lvl_num} ({expected_name}) must have 6 lessons, found {len(lvl_lessons)}"
        for l in lvl_lessons:
            assert l.level_name == expected_name


def test_academy_all_fens_and_moves_are_100_percent_legal():
    """Verify all 42 lessons have valid FEN positions and 100% legal expected and guided moves."""
    lessons = get_curriculum()
    for l in lessons:
        # Valid FEN
        board = chess.Board(l.fen)
        assert board.is_valid(), f"Lesson {l.id} has invalid FEN: {l.fen}"

        # Turn matches player color
        expected_turn = chess.WHITE if l.player_color == "White" else chess.BLACK
        assert board.turn == expected_turn, (
            f"Lesson {l.id}: player_color is {l.player_color} but FEN turn is {'White' if board.turn else 'Black'}"
        )

        # Expected moves are all legal
        assert len(l.expected_moves) >= 1, f"Lesson {l.id} has no expected moves"
        for uci_move in l.expected_moves:
            m = chess.Move.from_uci(uci_move)
            assert m in board.legal_moves, (
                f"Lesson '{l.id}': move {uci_move} is illegal in position {l.fen}"
            )

        # Guided move is legal
        assert l.guided_move, f"Lesson {l.id} has empty guided_move"
        gm = chess.Move.from_uci(l.guided_move)
        assert gm in board.legal_moves, (
            f"Lesson '{l.id}': guided move {l.guided_move} is illegal in position {l.fen}"
        )


def test_academy_lessons_have_rich_educational_content_and_assessments():
    """Verify every lesson contains progressive hints, threat detection, error explanations, and quizzes."""
    lessons = get_curriculum()
    for l in lessons:
        assert len(l.hints) >= 3, f"Lesson {l.id} must have at least 3 progressive hints"
        assert l.educational_note, f"Lesson {l.id} missing educational note"
        assert l.theory_detail, f"Lesson {l.id} missing theory detail"
        assert l.opponent_threat, f"Lesson {l.id} missing opponent threat"
        assert l.real_application, f"Lesson {l.id} missing real-world master application"
        assert l.why_mistakes_fail, f"Lesson {l.id} missing why_mistakes_fail tactical analysis"

        # Assessment Quiz verification
        assert l.assessment_question, f"Lesson {l.id} missing assessment question"
        assert len(l.assessment_options) == 4, f"Lesson {l.id} must have exactly 4 multiple choice options"
        assert 0 <= l.assessment_answer_index < 4, f"Lesson {l.id} invalid answer index {l.assessment_answer_index}"
        assert l.assessment_explanation, f"Lesson {l.id} missing assessment explanation"


# =============================================================================
# 2. SMART PROGRESS TRACKING & USER PROFILE TESTS
# =============================================================================

def test_user_profile_exercise_attempt_and_accuracy():
    with tempfile.TemporaryDirectory() as tmpdir:
        profile_path = Path(tmpdir) / "profile.json"
        pm = UserProfileManager(profile_path)

        assert pm.get_accuracy_rate() == 100.0

        # Attempt 1: Correct
        pm.record_exercise_attempt("beginner_pawn", "pawn_mechanics", is_correct=True, hints_used=1)
        assert pm.get_accuracy_rate() == 100.0
        assert pm.is_lesson_completed("beginner_pawn")

        # Attempt 2: Incorrect
        pm.record_exercise_attempt("tactics_fork", "forks", is_correct=False, hints_used=0)
        assert pm.get_accuracy_rate() == 50.0
        assert pm.get_accuracy_rate("forks") == 0.0
        assert pm.get_accuracy_rate("pawn_mechanics") == 100.0

        # Attempt 3: Correct on fork
        pm.record_exercise_attempt("tactics_fork", "forks", is_correct=True, hints_used=2)
        assert pm.get_accuracy_rate("forks") == 50.0
        assert pm.get_accuracy_rate() == round(2 / 3 * 100.0, 1)


def test_user_profile_weak_topics_and_recommendations():
    with tempfile.TemporaryDirectory() as tmpdir:
        profile_path = Path(tmpdir) / "profile.json"
        pm = UserProfileManager(profile_path)

        # Make mistakes in pins and forks
        pm.record_exercise_attempt("tactics_pin", "pins", is_correct=False)
        pm.record_exercise_attempt("tactics_pin", "pins", is_correct=False)
        pm.record_exercise_attempt("tactics_fork", "forks", is_correct=False)
        pm.record_exercise_attempt("beginner_pawn", "pawn_mechanics", is_correct=True)

        weak_topics = pm.get_weak_topics()
        assert len(weak_topics) >= 1
        topics = [t for t, _ in weak_topics]
        assert "pins" in topics or "forks" in topics

        # Recommendation points to weakest topic or next uncompleted lesson
        rec_id = pm.get_recommended_lesson_id()
        assert rec_id in ["tactics_pin", "tactics_fork", "curr_coords"]


def test_progressive_level_unlocking():
    with tempfile.TemporaryDirectory() as tmpdir:
        profile_path = Path(tmpdir) / "profile.json"
        pm = UserProfileManager(profile_path)

        # Level 1 is always unlocked
        assert pm.is_level_unlocked(1)
        # Level 2 is initially locked
        assert not pm.is_level_unlocked(2)

        # Complete 4 lessons in Level 1
        lvl1_lessons = [l.id for l in get_curriculum() if l.level_number == 1]
        for lid in lvl1_lessons[:4]:
            pm.record_exercise_attempt(lid, "fundamentals", is_correct=True)

        # Level 2 should now unlock!
        assert pm.is_level_unlocked(2)
        # Level 3 remains locked
        assert not pm.is_level_unlocked(3)


def test_progress_migration_safety():
    """Verify legacy profile data loads cleanly without errors or loss."""
    with tempfile.TemporaryDirectory() as tmpdir:
        profile_path = Path(tmpdir) / "profile.json"
        # Write legacy profile format
        legacy_data = {
            "username": "Magnus",
            "completed_lessons": ["beginner_pawn", "curr_coords", "beginner_pawn"],
            "current_lesson_id": "curr_coords",
            "sound_enabled": False,
        }
        import json
        with open(profile_path, "w", encoding="utf-8") as f:
            json.dump(legacy_data, f)

        pm = UserProfileManager(profile_path)
        pm.migrate_progress()
        prof = pm.get_profile()

        assert prof.username == "Magnus"
        assert not prof.sound_enabled
        # Duplicates removed safely
        assert prof.completed_lessons == ["beginner_pawn", "curr_coords"]
        assert prof.unlocked_level >= 1


# =============================================================================
# 3. INTERACTIVE LEARNING SCREEN & CM COACH TESTS
# =============================================================================

def test_learn_screen_loads_academy_layout(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = UserProfileManager(Path(tmpdir) / "profile.json")
        screen = LearnScreen(profile_manager=pm)

        assert "100" in screen.accuracy_pill.text()
        assert screen.level_combo.count() == 8

        screen.close()


def test_learn_screen_four_learning_modes(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = UserProfileManager(Path(tmpdir) / "profile.json")
        screen = LearnScreen(profile_manager=pm)
        lesson = get_lesson_by_id("tactics_fork")
        screen.load_lesson(lesson)

        # 1. Challenge Mode
        screen._set_learning_mode("challenge")
        assert screen._current_mode == "challenge"
        assert not screen.board_container.isHidden()
        assert screen.quiz_card.isHidden()
        assert not screen.cm_threat_lbl.isHidden()

        # 2. Theory Mode
        screen._set_learning_mode("theory")
        assert screen._current_mode == "theory"
        assert not screen.theory_deep_dive_lbl.isHidden()

        # 3. Demo Mode
        screen._set_learning_mode("demo")
        assert screen._current_mode == "demo"
        assert "Demonstration" in screen.cm_dialogue_lbl.text()

        # 4. Assessment Quiz Mode
        screen._set_learning_mode("assessment")
        assert screen._current_mode == "assessment"
        assert screen.board_container.isHidden()
        assert not screen.quiz_card.isHidden()
        assert screen.quiz_question_lbl.text() == lesson.assessment_question

        screen.close()


def test_learn_screen_assessment_quiz_interaction(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = UserProfileManager(Path(tmpdir) / "profile.json")
        screen = LearnScreen(profile_manager=pm)
        lesson = get_lesson_by_id("beginner_pawn")
        screen.load_lesson(lesson)
        screen._set_learning_mode("assessment")

        correct_idx = lesson.assessment_answer_index
        wrong_idx = (correct_idx + 1) % 4

        # Select wrong option first
        screen._on_quiz_option_selected(wrong_idx)
        assert "Review Required" in screen.quiz_status_badge.text()
        assert "Not quite" in screen.quiz_feedback_lbl.text()

        # Select correct option
        screen._on_quiz_option_selected(correct_idx)
        assert "Passed" in screen.quiz_status_badge.text()
        assert "Correct!" in screen.quiz_feedback_lbl.text()

        screen.close()


def test_learn_screen_specific_mistake_tactical_analysis(qt_app):
    """Verify CM provides specific strategic explanations for documented mistake moves."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = UserProfileManager(Path(tmpdir) / "profile.json")
        pm.set_username("Kasparov")
        screen = LearnScreen(profile_manager=pm)

        lesson = get_lesson_by_id("rules_check_checkmate")
        screen.load_lesson(lesson)

        # Make the documented mistake move 'f3e4'
        screen._on_user_board_move("f3e4")

        cm_text = screen.cm_dialogue_lbl.text()
        assert "Tactical Analysis" in cm_text
        assert "Kasparov" in cm_text
        assert "escap" in cm_text or "instant" in cm_text

        screen.close()


def test_learn_screen_sidebar_level_filtering(qt_app):
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = UserProfileManager(Path(tmpdir) / "profile.json")
        screen = LearnScreen(profile_manager=pm)

        # Filter by Level 2 (Chess Tactics)
        screen.level_combo.setCurrentIndex(2)
        assert screen._selected_level_filter == 2

        # Level 2 lesson buttons must be visible
        btn_fork = screen.lesson_buttons.get("tactics_fork")
        assert btn_fork is not None
        assert not btn_fork.isHidden()

        # Level 1 lesson buttons must be hidden
        btn_pawn = screen.lesson_buttons.get("beginner_pawn")
        assert btn_pawn is not None
        assert btn_pawn.isHidden()

        # Switch back to All Levels
        screen.level_combo.setCurrentIndex(0)
        assert not btn_pawn.isHidden()
        assert not btn_fork.isHidden()

        screen.close()
