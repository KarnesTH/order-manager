from typing import Any, Optional

from PyQt6.QtCore import QSize
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtGui import QIcon, QPainter
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QWidget,
)


class ActionButtonDelegate(QStyledItemDelegate):
    """Delegate for action buttons in table."""
    edit_clicked = Signal(int)
    delete_clicked = Signal(int)

    def createEditor(
        self,
        parent: Optional[QWidget],
        option: Any,
        index: Any
    ) -> QWidget:
        editor = QWidget(parent)
        layout = QHBoxLayout(editor)
        layout.setContentsMargins(4, 4, 4, 4)

        edit_btn = QPushButton(editor)
        edit_btn.setIcon(QIcon.fromTheme("document-edit"))
        edit_btn.setToolTip("Edit product")
        edit_btn.setFixedWidth(40)

        delete_btn = QPushButton(editor)
        delete_btn.setIcon(QIcon.fromTheme("edit-delete"))
        delete_btn.setToolTip("Delete product")
        delete_btn.setFixedWidth(40)

        product_id = index.model().products[index.row()]["id"]
        edit_btn.clicked.connect(lambda: self.edit_clicked.emit(product_id))
        delete_btn.clicked.connect(lambda: self.delete_clicked.emit(product_id))

        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)

        editor.setLayout(layout)
        return editor

    def setEditorData(self, editor: Optional[QWidget], index: Any) -> None:
        pass

    def setModelData(
        self,
        editor: Optional[QWidget],
        model: Any,
        index: Any
    ) -> None:
        pass

    def sizeHint(self, option: 'QStyleOptionViewItem', index: Any) -> QSize:
        return QSize(100, 40)

    def paint(
        self,
        painter: Optional[QPainter],
        option: QStyleOptionViewItem,
        index: Any
    ) -> None:
        super().paint(painter, option, index)
