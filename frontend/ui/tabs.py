from typing import Any, Dict, List

from api import (
    create_order,
    create_product,
    delete_product,
    get_orders,
    get_products,
)
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .dialogs import AddOrderDialog, AddProductDialog
from .messages import show_confirmation, show_error, show_info


class ProductsTab(QWidget):
    """Tab for managing products."""
    def __init__(self, products: List[Dict[str, Any]]):
        super().__init__()
        self.setup_ui()
        self.load_products(products)

    def setup_ui(self):
        """Setup the tab UI."""
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Product")
        refresh_button = QPushButton("Refresh")

        add_button.clicked.connect(self.add_product)
        refresh_button.clicked.connect(self.refresh_products)

        button_layout.addWidget(add_button)
        button_layout.addWidget(refresh_button)
        layout.addLayout(button_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Name', 'Brand', 'Price', 'Stock'
        ])

        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_products(self, products: List[Dict[str, Any]]):
        """Load products into the table."""
        self.table.setRowCount(len(products))

        for i, product in enumerate(products):
            self.table.setItem(i, 0, QTableWidgetItem(str(product.get('id', ''))))
            self.table.setItem(i, 1, QTableWidgetItem(product.get('name', '')))
            self.table.setItem(i, 2, QTableWidgetItem(product.get('brand', '')))
            self.table.setItem(i, 3, QTableWidgetItem(str(product.get('price', ''))))
            self.table.setItem(i, 4, QTableWidgetItem(str(product.get('stock', ''))))

    def add_product(self):
        """Open dialog to add a new product."""
        dialog = AddProductDialog(self)
        if dialog.exec() == AddProductDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                response = create_product(data)
                if 'id' in response:
                    self.refresh_products()
                else:
                    show_error(
                        self,
                        response.get('message', 'Unknown error')
                    )
            except Exception as e:
                show_error(self, str(e))

    def delete_product(self, product_id: int):
        if show_confirmation(
            self,
            "Are you sure you want to delete this product?"
        ):
            try:
                response = delete_product(product_id)
                if 'message' in response:
                    show_info(self, "Product deleted successfully")
                    self.refresh_products()
                else:
                    show_error(self, response.get('message', 'Unknown error'))
            except Exception as e:
                show_error(self, str(e))

    def refresh_products(self):
        """Refresh the products table."""
        products = get_products()
        self.load_products(products)


class OrdersTab(QWidget):
    """Tab for managing orders."""
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_orders()

    def setup_ui(self):
        """Setup the tab UI."""
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Order")
        refresh_button = QPushButton("Refresh")

        add_button.clicked.connect(self.add_order)
        refresh_button.clicked.connect(self.refresh_orders)

        button_layout.addWidget(add_button)
        button_layout.addWidget(refresh_button)
        layout.addLayout(button_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Product', 'Quantity', 'Customer', 'Date', 'Status'
        ])

        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_orders(self):
        """Load orders into the table."""
        orders = get_orders()
        self.table.setRowCount(len(orders))

        for i, order in enumerate(orders):
            self.table.setItem(i, 0, QTableWidgetItem(str(order.get('id', ''))))
            self.table.setItem(
                i,
                1,
                QTableWidgetItem(order.get('product', {}).get('name', ''))
            )
            self.table.setItem(i, 2, QTableWidgetItem(str(order.get('quantity', ''))))
            self.table.setItem(i, 3, QTableWidgetItem(order.get('customer', '')))
            self.table.setItem(i, 4, QTableWidgetItem(order.get('order_date', '')))
            self.table.setItem(i, 5, QTableWidgetItem(order.get('status', '')))

    def add_order(self):
        """Open dialog to add a new order."""
        products = get_products()
        dialog = AddOrderDialog(products, self)
        if dialog.exec() == AddOrderDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                response = create_order(data)
                if 'id' in response:
                    self.refresh_orders()
                else:
                    QMessageBox.warning(
                        self,
                        "Error",
                        response.get('message', 'Unknown error')
                    )
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def refresh_orders(self):
        """Refresh the orders table."""
        self.load_orders()
