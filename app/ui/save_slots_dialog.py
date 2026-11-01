from __future__ import annotations

"""Dialog displaying active save slots for Continue Game and Save Game flows.
Styled in Royal Gold & Luxury Mahogany Theme.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.services.save_manager import SaveManager, SaveSlot
from app.ui.styles import DANGER_BTN, PRIMARY_BTN, SECONDARY_BTN, SUCCESS_BTN


class SaveSlotsDialog(QDialog):
    """Dialog allowing users to inspect, select, save, and delete game slots."""

    slot_loaded = Signal(int)  # slot_id to load
    slot_saved = Signal(int)   # slot_id to save into

    MODE_CONTINUE = "continue"
    MODE_SAVE = "save"

    def __init__(
        self,
        save_manager: SaveManager,
        mode: str = "continue",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.save_manager = save_manager
        self.mode = mode

        title_text = "Continue Game – Saved Matches" if mode == self.MODE_CONTINUE else "Save Game – Select Slot"
        self.setWindowTitle(title_text)
        self.resize(540, 580)
        self.setMinimumSize(340, 480)
        self.setStyleSheet(
            """
            QDialog {
                background-color: #1E130B;
                color: #FDFBF7;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        # Header section
        header_layout = QVBoxLayout()
        header_layout.setSpacing(6)

        dialog_title = QLabel(title_text)
        dialog_title.setStyleSheet(
            "font-size: 20px; font-weight: 800; color: #FDFBF7; letter-spacing: 0.3px;"
        )
        header_layout.addWidget(dialog_title)

        if mode == self.MODE_CONTINUE:
            sub_text = "Select a saved match to resume playing, or delete old slots."
        else:
            sub_text = "Choose one of the 3 slots below to store your current game state."

        dialog_subtitle = QLabel(sub_text)
        dialog_subtitle.setWordWrap(True)
        dialog_subtitle.setStyleSheet("font-size: 13px; color: #D97706; font-weight: 600;")
        header_layout.addWidget(dialog_subtitle)

        layout.addLayout(header_layout)

        # Scroll area containing the 3 slot cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background-color: #1E130B; border: none; }")
        scroll.viewport().setStyleSheet("background-color: #1E130B;")

        self.cards_container = QWidget()
        self.cards_container.setStyleSheet("background-color: #1E130B;")
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 4, 0, 4)
        self.cards_layout.setSpacing(14)

        scroll.setWidget(self.cards_container)
        layout.addWidget(scroll, 1)

        # Footer button
        footer_layout = QHBoxLayout()
        footer_layout.addStretch(1)

        self.close_button = QPushButton("Cancel" if mode == self.MODE_CONTINUE else "Close")
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.setMinimumHeight(44)
        self.close_button.setStyleSheet(SECONDARY_BTN)
        self.close_button.clicked.connect(self.reject)
        footer_layout.addWidget(self.close_button)

        layout.addLayout(footer_layout)

        self.refresh_slots()

    def refresh_slots(self) -> None:
        """Clear and rebuild the 3 slot cards."""
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        slots = self.save_manager.get_slots()

        for slot in slots:
            card = self._create_slot_card(slot)
            self.cards_layout.addWidget(card)

        self.cards_layout.addStretch(1)

    def _create_slot_card(self, slot: SaveSlot) -> QFrame:
        card = QFrame()
        card.setObjectName(f"slotCard_{slot.slot_id}")

        if slot.is_active:
            card.setStyleSheet(
                """
                QFrame {
                    background-color: #2A1B12;
                    border: 1.5px solid #D97706;
                    border-radius: 14px;
                }
                QFrame:hover {
                    border-color: #FBBF24;
                    background-color: #352317;
                }
                """
            )
        else:
            card.setStyleSheet(
                """
                QFrame {
                    background-color: #2A1B12;
                    border: 1.5px dashed rgba(217, 119, 6, 0.45);
                    border-radius: 14px;
                }
                """
            )

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(12)

        # Header row: Slot Name + Status badge
        header_row = QHBoxLayout()
        slot_title = QLabel(f"Slot {slot.slot_id}")
        slot_title.setStyleSheet("font-size: 16px; font-weight: 800; color: #FDFBF7;")
        header_row.addWidget(slot_title)
        header_row.addStretch(1)

        if slot.is_active:
            status_chip = QLabel("Active Save")
            status_chip.setStyleSheet(
                "font-size: 11px; font-weight: 700; color: #10B981; "
                "background-color: rgba(16, 185, 129, 0.15); border: 1.5px solid #10B981; "
                "border-radius: 6px; padding: 2px 8px;"
            )
        else:
            status_chip = QLabel("Empty Slot")
            status_chip.setStyleSheet(
                "font-size: 11px; font-weight: 600; color: #D97706; "
                "background-color: rgba(217, 119, 6, 0.15); border: 1px solid rgba(217, 119, 6, 0.4); "
                "border-radius: 6px; padding: 2px 8px;"
            )
        header_row.addWidget(status_chip)
        card_layout.addLayout(header_row)

        if slot.is_active:
            details_layout = QVBoxLayout()
            details_layout.setSpacing(4)

            mode_text = slot.game_mode
            if slot.game_mode == "Play vs Computer":
                mode_text = f"Play vs Computer ({slot.difficulty})"

            mode_lbl = QLabel(f"Mode: <b>{mode_text}</b>")
            mode_lbl.setStyleSheet("font-size: 13px; color: #FDFBF7;")
            details_layout.addWidget(mode_lbl)

            date_lbl = QLabel(f"Saved: {slot.saved_at_formatted or 'Unknown date'}")
            date_lbl.setStyleSheet("font-size: 12px; color: #D97706; font-weight: 600;")
            details_layout.addWidget(date_lbl)

            perspective_text = f"Playing as: <b>{slot.player_color}</b>"
            turn_text = f"Turn: <b>{slot.turn}</b>"
            moves_text = f"<b>{slot.move_count}</b> moves played"

            meta_lbl = QLabel(f"{perspective_text}  •  {turn_text}  •  {moves_text}")
            meta_lbl.setStyleSheet("font-size: 12px; color: #E6CCB2;")
            details_layout.addWidget(meta_lbl)

            card_layout.addLayout(details_layout)

            # Action buttons row (Touch-friendly 44px height)
            btn_row = QHBoxLayout()
            btn_row.setSpacing(10)

            if self.mode == self.MODE_CONTINUE:
                continue_btn = QPushButton("Continue Match →")
                continue_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                continue_btn.setMinimumHeight(44)
                continue_btn.setStyleSheet(PRIMARY_BTN)
                continue_btn.clicked.connect(lambda _, s=slot.slot_id: self._on_select_slot(s))
                btn_row.addWidget(continue_btn)

                delete_btn = QPushButton("Delete")
                delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                delete_btn.setMinimumHeight(44)
                delete_btn.setStyleSheet(DANGER_BTN)
                delete_btn.clicked.connect(lambda _, s=slot.slot_id: self._on_delete_slot(s))
                btn_row.addWidget(delete_btn)

            else:  # MODE_SAVE
                overwrite_btn = QPushButton(f"Overwrite Slot {slot.slot_id}")
                overwrite_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                overwrite_btn.setMinimumHeight(44)
                overwrite_btn.setStyleSheet(PRIMARY_BTN)
                overwrite_btn.clicked.connect(lambda _, s=slot.slot_id: self._on_overwrite_slot(s))
                btn_row.addWidget(overwrite_btn)

            btn_row.addStretch(1)
            card_layout.addLayout(btn_row)

        else:  # Slot is empty
            empty_desc = QLabel("No game saved in this slot yet.")
            empty_desc.setStyleSheet("font-size: 13px; color: #D97706; font-weight: 500;")
            card_layout.addWidget(empty_desc)

            if self.mode == self.MODE_SAVE:
                save_btn = QPushButton(f"Save to Slot {slot.slot_id} →")
                save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                save_btn.setMinimumHeight(44)
                save_btn.setStyleSheet(PRIMARY_BTN)
                save_btn.clicked.connect(lambda _, s=slot.slot_id: self._on_save_slot(s))
                card_layout.addWidget(save_btn, 0, Qt.AlignmentFlag.AlignLeft)

        return card

    def _on_select_slot(self, slot_id: int) -> None:
        self.slot_loaded.emit(slot_id)
        self.accept()

    def _on_save_slot(self, slot_id: int) -> None:
        self.slot_saved.emit(slot_id)
        self.accept()

    def _on_overwrite_slot(self, slot_id: int) -> None:
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Overwrite")
        msg_box.setText(f"Are you sure you want to overwrite Slot {slot_id} with your current game?")
        msg_box.setStyleSheet(
            """
            QMessageBox {
                background-color: #1E130B;
                color: #FDFBF7;
                border: 1.5px solid #D97706;
                border-radius: 14px;
            }
            QLabel {
                color: #FDFBF7;
                font-size: 14px;
            }
            """
        )
        yes_btn = msg_box.addButton("Yes, Overwrite", QMessageBox.ButtonRole.YesRole)
        no_btn = msg_box.addButton("Cancel", QMessageBox.ButtonRole.NoRole)
        yes_btn.setStyleSheet(
            "background-color: #D97706; color: #1E130B; font-weight: 800; min-height: 40px; padding: 8px 18px; border-radius: 8px;"
        )
        no_btn.setStyleSheet(
            "background-color: #2A1B12; color: #FDFBF7; border: 1.5px solid #D97706; font-weight: 700; min-height: 40px; padding: 8px 18px; border-radius: 8px;"
        )
        msg_box.exec()
        if msg_box.clickedButton() == yes_btn:
            self._on_save_slot(slot_id)

    def _on_delete_slot(self, slot_id: int) -> None:
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Delete Save Slot")
        msg_box.setText(f"Are you sure you want to delete Slot {slot_id}? This cannot be undone.")
        msg_box.setStyleSheet(
            """
            QMessageBox {
                background-color: #1E130B;
                color: #FDFBF7;
                border: 1.5px solid #D97706;
                border-radius: 14px;
            }
            QLabel {
                color: #FDFBF7;
                font-size: 14px;
            }
            """
        )
        del_btn = msg_box.addButton("Yes, Delete", QMessageBox.ButtonRole.YesRole)
        cancel_btn = msg_box.addButton("Cancel", QMessageBox.ButtonRole.NoRole)
        del_btn.setStyleSheet(
            "background-color: #7F1D1D; color: #FDFBF7; border: 1.5px solid #DC2626; font-weight: 800; min-height: 40px; padding: 8px 18px; border-radius: 8px;"
        )
        cancel_btn.setStyleSheet(
            "background-color: #2A1B12; color: #FDFBF7; border: 1.5px solid #D97706; font-weight: 700; min-height: 40px; padding: 8px 18px; border-radius: 8px;"
        )
        msg_box.exec()
        if msg_box.clickedButton() == del_btn:
            self.save_manager.delete_slot(slot_id)
            self.refresh_slots()
