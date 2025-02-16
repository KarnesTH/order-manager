from typing import Any, Dict, List

from PyQt6.QtCore import QAbstractTableModel, Qt


class ProductsTableModel(QAbstractTableModel):
    """Model for products table."""
    def __init__(self, products: List[Dict[str, Any]]):
        super().__init__()
        self.products = products
        self.headers = ["ID","Name", "Brand", "Price", "Stock", "Actions"]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            product = self.products[index.row()]
            return self._get_display_value(index.column(), product)

        return None

    def _get_display_value(self, column: int, product: Dict[str, Any]) -> str:
        mapping = {
            0: lambda p: str(p.get("id", "")),
            1: lambda p: p.get("name", ""),
            2: lambda p: p.get("brand", ""),
            3: lambda p: f"${p.get('price', 0):,.2f}",
            4: lambda p: str(p.get("stock", "")),
            5: lambda p: ""
        }

        return mapping.get(column, lambda p: "")(product)

    def rowCount(self, parent=None) -> int:
        return len(self.products)

    def columnCount(self, parent=None) -> int:
        return len(self.headers)

    def headerData(
        self,
        section,
        orientation,
        role=Qt.ItemDataRole.DisplayRole
    ):
        check_orientation = orientation == Qt.Orientation.Horizontal
        check_role = role == Qt.ItemDataRole.DisplayRole
        if check_orientation and check_role:
            return self.headers[section]

    def flags(self, index):
        if index.column() == 5:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
        return Qt.ItemFlag.ItemIsEnabled
