
from PyQt6.QtCore import QEvent, QRect, QSize
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import (
    QStyledItemDelegate,
)


class ActionButtonDelegate(QStyledItemDelegate):
    """Delegate for action buttons in table."""
    edit_clicked = Signal(int)
    delete_clicked = Signal(int)

    def __init__(self, parent=None, type="product"):
        super().__init__(parent)
        self.type = type
        self.edit_btn_rects = {}
        self.delete_btn_rects = {}

    def paint(
        self,
        painter,
        option,
        index
    ):
        """Paint the action buttons."""
        if painter is None:
            return

        super().paint(painter, option, index)

        rect = option.rect
        btn_width = 40
        padding = 4
        icon_size = 16

        edit_rect = QRect(
            rect.x() + padding,
            rect.y() + padding,
            btn_width,
            rect.height() - 2 * padding
        )

        delete_rect = QRect(
            edit_rect.right() + padding,
            rect.y() + padding,
            btn_width,
            rect.height() - 2 * padding
        )

        row = index.row()
        self.edit_btn_rects[row] = edit_rect
        self.delete_btn_rects[row] = delete_rect

        edit_icon_x = edit_rect.x() + (btn_width - icon_size) // 2
        edit_icon_y = edit_rect.y() + (edit_rect.height() - icon_size) // 2
        delete_icon_x = delete_rect.x() + (btn_width - icon_size) // 2
        delete_icon_y = delete_rect.y() + (delete_rect.height() - icon_size) // 2

        painter.drawPixmap(
            edit_icon_x, edit_icon_y, icon_size, icon_size,
            QIcon.fromTheme("document-edit").pixmap(QSize(icon_size, icon_size))
        )
        painter.drawPixmap(
            delete_icon_x, delete_icon_y, icon_size, icon_size,
            QIcon.fromTheme("edit-delete").pixmap(QSize(icon_size, icon_size))
        )

    def editorEvent(self, event, model, option, index):
        """Handle editor events."""
        if event is None:
            return False

        if (isinstance(event, QMouseEvent) and
            event.type() == QEvent.Type.MouseButtonRelease
        ):
            row = index.row()
            pos = event.position().toPoint()

            if (row in self.edit_btn_rects and
                self.edit_btn_rects[row].contains(pos)
            ):
                item_id = self._get_item_id(index)
                self.edit_clicked.emit(item_id)
                return True

            if (row in self.delete_btn_rects and
                self.delete_btn_rects[row].contains(pos)
            ):
                item_id = self._get_item_id(index)
                self.delete_clicked.emit(item_id)
                return True

        return False

    def _get_item_id(self, index):
        """Get the item ID."""
        if self.type == "product":
            return index.model().products[index.row()]["id"]
        elif self.type == "order":
            return index.model().orders[index.row()]["id"]
