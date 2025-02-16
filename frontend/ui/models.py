from typing import Any, Dict, List

from PyQt6.QtCore import QAbstractTableModel, Qt


class ProductsTableModel(QAbstractTableModel):
    """Model for products table."""
    def __init__(self, products: List[Dict[str, Any]]):
        """Initialize the products model."""
        super().__init__()
        self.products = products
        self.headers = ["ID","Name", "Brand", "Price", "Stock", "Actions"]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """Get data for table."""
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            product = self.products[index.row()]
            return self._get_display_value(index.column(), product)

        return None

    def _get_display_value(
        self,
        column: int,
        product: Dict[str, Any]
    ) -> str:
        """Get display value for column"""
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
        """Get row count."""
        return len(self.products)

    def columnCount(self, parent=None) -> int:
        """Get column count."""
        return len(self.headers)

    def headerData(
        self,
        section,
        orientation,
        role=Qt.ItemDataRole.DisplayRole
    ):
        """Get header data."""
        check_orientation = orientation == Qt.Orientation.Horizontal
        check_role = role == Qt.ItemDataRole.DisplayRole
        if check_orientation and check_role:
            return self.headers[section]

    def flags(self, index):
        """Get flags for cell."""
        if index.column() == 5:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
        return Qt.ItemFlag.ItemIsEnabled

class OrdersTableModel(QAbstractTableModel):
    """Model for orders table."""
    def __init__(self, orders: List[Dict[str, Any]]):
        """Initialize the orders model."""
        super().__init__()
        self.orders = orders
        self.headers = [
            'ID', 'Product', 'Quantity', 'Customer', 'Date', 'Status', 'Actions'
        ]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """Get data for table."""
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            order = self.orders[index.row()]
            return self._get_display_value(index.column(), order)

        return None

    def _get_display_value(
        self,
        column: int,
        order: Dict[str, Any]
    ) -> str:
        """Get display value for column"""
        mapping = {
            0: lambda o: str(o.get("id", "")),
            1: lambda o: o.get("product", {}).get("name", ""),
            2: lambda o: str(o.get("quantity", "")),
            3: lambda o: o.get("customer", ""),
            4: lambda o: o.get("order_date", ""),
            5: lambda o: o.get("status", ""),
            6: lambda o: ""
        }

        return mapping.get(column, lambda o: "")(order)

    def rowCount(self, parent=None) -> int:
        """Get row count."""
        return len(self.orders)

    def columnCount(self, parent=None) -> int:
        """Get column count."""
        return len(self.headers)

    def headerData(
        self,
        section,
        orientation,
        role=Qt.ItemDataRole.DisplayRole
    ):
        """Get header data."""
        check_orientation = orientation == Qt.Orientation.Horizontal
        check_role = role == Qt.ItemDataRole.DisplayRole
        if check_orientation and check_role:
            return self.headers[section]

    def flags(self, index):
        """Get flags for cell."""
        if index.column() == 6:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
        return Qt.ItemFlag.ItemIsEnabled
