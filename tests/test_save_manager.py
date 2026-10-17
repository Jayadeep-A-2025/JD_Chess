from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from app.services.save_manager import SaveManager, SaveSlot


@pytest.fixture
def temp_saves_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir) / "test_saves.json"


def test_empty_manager_has_three_empty_slots(temp_saves_file):
    mgr = SaveManager(temp_saves_file)
    slots = mgr.get_slots()

    assert len(slots) == 3
    assert all(not s.is_active for s in slots)
    assert [s.slot_id for s in slots] == [1, 2, 3]
    assert not mgr.has_active_saves()
    assert mgr.active_save_count() == 0


def test_save_and_retrieve_slot(temp_saves_file):
    mgr = SaveManager(temp_saves_file)
    slot = mgr.save_game(
        slot_id=2,
        game_mode="Play vs Computer",
        player_color="White",
        difficulty="Hard",
        moves=["e2e4", "e7e5", "g1f3"],
        fen="rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2",
        turn="Black",
        status_text="Computer is thinking...",
    )

    assert slot.slot_id == 2
    assert slot.is_active is True
    assert slot.move_count == 3
    assert slot.moves == ["e2e4", "e7e5", "g1f3"]
    assert slot.difficulty == "Hard"

    # Reload from disk
    mgr2 = SaveManager(temp_saves_file)
    assert mgr2.has_active_saves()
    assert mgr2.active_save_count() == 1

    slot2 = mgr2.get_slot(2)
    assert slot2 is not None
    assert slot2.is_active is True
    assert slot2.game_mode == "Play vs Computer"
    assert slot2.player_color == "White"
    assert slot2.turn == "Black"
    assert slot2.moves == ["e2e4", "e7e5", "g1f3"]
    assert slot2.saved_at_formatted != ""


def test_delete_slot(temp_saves_file):
    mgr = SaveManager(temp_saves_file)
    mgr.save_game(
        slot_id=1,
        game_mode="Local 2-player",
        player_color="White",
        difficulty="Medium",
        moves=["e2e4"],
        fen="rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
        turn="Black",
    )

    assert mgr.active_save_count() == 1
    assert mgr.delete_slot(1) is True
    assert mgr.active_save_count() == 0
    assert not mgr.get_slot(1).is_active


def test_invalid_slot_id_raises_value_error(temp_saves_file):
    mgr = SaveManager(temp_saves_file)
    with pytest.raises(ValueError):
        mgr.save_game(
            slot_id=4,
            game_mode="Local 2-player",
            player_color="White",
            difficulty="Medium",
            moves=[],
            fen="",
            turn="White",
        )

    assert mgr.get_slot(0) is None
    assert mgr.get_slot(5) is None
