from __future__ import annotations

"""Dialog displaying active save slots for Continue Game and Save Game flows."""

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

        title_text = "Continue Game - Saved Matches" if mode == self.MODE_CONTINUE else "Save Game - Select Slot"
        self.setWindowTitle(title_text)
        self.resize(520, 560)
        self.setMinimumSize(460, 480)
        self.setStyleSheet("QDialog { background-color: #F8FAFC; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header section
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        dialog_title = QLabel(title_text)
        dialog_title.setStyleSheet(
            "font-size: 20px; font-weight: 800; color: #0F172A; letter-spacing: 0.3px;"
        )
        header_layout.addWidget(dialog_title)

        if mode == self.MODE_CONTINUE:
            sub_text = "Select a saved match to resume playing, or delete old slots."
        else:
            sub_text = "Choose one of the 3 slots below to store your current game state."

        dialog_subtitle = QLabel(sub_text)
        dialog_subtitle.setWordWrap(True)
        dialog_subtitle.setStyleSheet("font-size: 13px; color: #64748B;")
        header_layout.addWidget(dialog_subtitle)

        layout.addLayout(header_layout)

        # Scroll area containing the 3 slot cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        scroll.viewport().setStyleSheet("background: transparent;")

        self.cards_container = QWidget()
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
        self.close_button.setStyleSheet(
            """
            QPushButton {
                background-color: #FFFFFF;
                color: #475569;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #F1F5F9; border-color: #94A3B8; }
            """
        )
        self.close_button.clicked.connect(self.reject)
        footer_layout.addWidget(self.close_button)

        layout.addLayout(footer_layout)

        self.refresh_slots()

    def refresh_slots(self) -> None:
        """Clear and rebuild the 3 slot cards."""
        # Clear previous widgets
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
                    background-color: #FFFFFF;
                    border: 1.5px solid #E2E8F0;
                    border-radius: 12px;
                }
                QFrame:hover {
                    border-color: #93C5FD;
                }
                """
            )
        else:
            card.setStyleSheet(
                """
                QFrame {
                    background-color: #F8FAFC;
                    border: 1.5px dashed #CBD5E1;
                    border-radius: 12px;
                }
                """
            )

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(10)

        # Top row: Slot badge and saved time
        top_row = QHBoxLayout()
        slot_badge = QLabel(f"SLOT {slot.slot_id}")
        slot_badge.setStyleSheet(
            "font-size: 11px; font-weight: 800; color: #2563EB; "
            "background-color: #EFF6FF; border: 1px solid #BFDBFE; "
            "border-radius: 6px; padding: 2px 8px;"
        )
        top_row.addWidget(slot_badge)

        if slot.is_active:
            date_lbl = QLabel(slot.saved_at_formatted)
            date_lbl.setStyleSheet("font-size: 12px; color: #64748B; font-weight: 500;")
            top_row.addWidget(date_lbl, 0, Qt.AlignmentFlag.AlignRight)
        else:
            empty_lbl = QLabel("Empty Slot")
            empty_lbl.setStyleSheet("font-size: 12px; color: #94A3B8; font-style: italic;")
            top_row.addWidget(empty_lbl, 0, Qt.AlignmentFlag.AlignRight)

        card_layout.addLayout(top_row)

        if slot.is_active:
            # Details section
            details_layout = QVBoxLayout()
            details_layout.setSpacing(4)

            # Match mode with difficulty if computer
            if slot.game_mode == "Play vs Computer":
                mode_desc = f"⚔️ Play vs Computer ({slot.difficulty})"
            else:
                mode_desc = "👥 Local 2-Player Match"

            mode_lbl = QLabel(mode_desc)
            mode_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #0F172A;")
            details_layout.addWidget(mode_lbl)

            # Perspective and Move count
            perspective_text = f"Playing as: <b>{slot.player_color}</b>"
            turn_text = f"Turn: <b>{slot.turn}</b>"
            moves_text = f"<b>{slot.move_count}</b> moves played"

            meta_lbl = QLabel(f"{perspective_text}  •  {turn_text}  •  {moves_text}")
            meta_lbl.setStyleSheet("font-size: 12px; color: #475569;")
            details_layout.addWidget(meta_lbl)

            card_layout.addLayout(details_layout)

            # Action buttons row
            btn_row = QHBoxLayout()
            btn_row.setSpacing(8)

            if self.mode == self.MODE_CONTINUE:
                continue_btn = QPushButton("Continue Match →")
                continue_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                continue_btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #2563EB;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 6px;
                        padding: 7px 16px;
                        font-size: 12px;
                        font-weight: 600;
                    }
                    QPushButton:hover { background-color: #1D4ED8; }
                    """
                )
                continue_btn.clicked.connect(lambda _, s=slot.slot_id: self._on_select_slot(s))
                btn_row.addWidget(continue_btn)

                delete_btn = QPushButton("Delete")
                delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                delete_btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: transparent;
                        color: #DC2626;
                        border: 1px solid #FECACA;
                        border-radius: 6px;
                        padding: 7px 12px;
                        font-size: 12px;
                        font-weight: 600;
                    }
                    QPushButton:hover { background-color: #FEE2E2; }
                    """
                )
                delete_btn.clicked.connect(lambda _, s=slot.slot_id: self._on_delete_slot(s))
                btn_row.addWidget(delete_btn)

            else:  # MODE_SAVE
                overwrite_btn = QPushButton(f"Overwrite Slot {slot.slot_id}")
                overwrite_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                overwrite_btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #D97706;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 6px;
                        padding: 7px 16px;
                        font-size: 12px;
                        font-weight: 600;
                    }
                    QPushButton:hover { background-color: #B45309; }
                    """
                )
                overwrite_btn.clicked.connect(lambda _, s=slot.slot_id: self._on_overwrite_slot(s))
                btn_row.addWidget(overwrite_btn)

            btn_row.addStretch(1)
            card_layout.addLayout(btn_row)

        else:  # Slot is empty
            empty_desc = QLabel("No game saved in this slot yet.")
            empty_desc.setStyleSheet("font-size: 12px; color: #94A3B8;")
            card_layout.addWidget(empty_desc)

            if self.mode == self.MODE_SAVE:
                save_btn = QPushButton(f"Save to Slot {slot.slot_id} →")
                save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                save_btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #10B981;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 6px;
                        padding: 7px 16px;
                        font-size: 12px;
                        font-weight: 600;
                    }
                    QPushButton:hover { background-color: #059669; }
                    """
                )
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
        reply = QMessageBox.question(
            self,
            "Confirm Overwrite",
            f"Are you sure you want to overwrite Slot {slot_id} with your current game?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._on_save_slot(slot_id)

    def _on_delete_slot(self, slot_id: int) -> None:
        reply = QMessageBox.question(
            self,
            "Delete Save Slot",
            f"Are you sure you want to delete Slot {slot_id}? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.save_manager.delete_slot(slot_id)
            self.refresh_slots()
