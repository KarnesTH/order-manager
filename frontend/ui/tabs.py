from typing import Any, Dict, List

from api import (
    create_order,
    create_product,
    delete_order,
    delete_product,
    get_orders,
    get_products,
    update_order,
    update_product,
)
from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from .delegates import ActionButtonDelegate
from .dialogs import AddOrderDialog, AddProductDialog
from .messages import show_confirmation, show_error, show_info
from .models import OrdersTableModel, ProductsTableModel


class ProductsTab(QWidget):
    """Tab for managing products."""
    def __init__(self, products: List[Dict[str, Any]]):
        """Initialize the products tab."""
        super().__init__()
        self.setup_ui()
        self.load_products(products)

    def setup_ui(self):
        """Setup the tab UI."""
        layout = QVBoxLayout()

        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_lbl = QLabel("Products")
        title_lbl.setFont(QFont("Arial", 20))
        description_lbl = QLabel("Manage your products")
        title_layout.addWidget(title_lbl)
        title_layout.addWidget(description_lbl)

        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Product")
        add_btn.setIcon(QIcon.fromTheme("list-add"))
        add_btn.setToolTip("Add a new product")
        add_btn.setIconSize(QSize(16, 16))
        refresh_btn = QPushButton()
        refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        refresh_btn.setToolTip("Refresh products")

        add_btn.clicked.connect(self.add_product)
        refresh_btn.clicked.connect(self.refresh_products)

        button_layout.addWidget(add_btn)
        button_layout.addWidget(refresh_btn)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addLayout(button_layout)

        layout.addLayout(header_layout)

        self.table = QTableView()
        self.model = ProductsTableModel([])
        self.table.setModel(self.model)

        self.action_delegate = ActionButtonDelegate(self.table, type="product")
        self.action_delegate.edit_clicked.connect(self.edit_product)
        self.action_delegate.delete_clicked.connect(self.delete_product)
        self.table.setItemDelegateForColumn(5, self.action_delegate)

        for row in range(self.model.rowCount()):
            self.table.edit(self.model.index(row, 5))

        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(5, 100)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_products(self, products: List[Dict[str, Any]]):
        """Load products into the table."""
        self.model = ProductsTableModel(products)
        self.table.setModel(self.model)

        self.action_delegate = ActionButtonDelegate(self.table, type="product")
        self.action_delegate.edit_clicked.connect(self.edit_product)
        self.action_delegate.delete_clicked.connect(self.delete_product)
        self.table.setItemDelegateForColumn(5, self.action_delegate)

        def init_editors():
            for row in range(self.model.rowCount()):
                self.table.edit(self.model.index(row, 5))

        QTimer.singleShot(100, init_editors)

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
        """Delete a product."""
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

    def edit_product(self, product_id: int):
        """Open dialog to edit a product."""
        products = get_products()
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            dialog = AddProductDialog(self, product)

            if dialog.exec() == AddProductDialog.DialogCode.Accepted:
                try:
                    data = dialog.get_data()
                    response = update_product(product_id, data)
                    if 'id' in response:
                        self.refresh_products()
                    else:
                        show_error(
                            self,
                            response.get('message', 'Unknown error')
                        )
                except Exception as e:
                    show_error(self, str(e))

    def refresh_products(self):
        """Refresh the products table."""
        products = get_products()
        self.load_products(products)


class OrdersTab(QWidget):
    """Tab for managing orders."""
    def __init__(self, orders: List[Dict[str, Any]]):
        """Initialize the orders tab."""
        super().__init__()
        self.setup_ui()
        self.load_orders(orders)

    def setup_ui(self):
        """Setup the tab UI."""
        layout = QVBoxLayout()

        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_lbl = QLabel("Orders")
        title_lbl.setFont(QFont("Arial", 20))
        description_lbl = QLabel("Manage your orders")
        title_layout.addWidget(title_lbl)
        title_layout.addWidget(description_lbl)

        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Order")
        add_btn.setIcon(QIcon.fromTheme("list-add"))
        add_btn.setToolTip("Add a new Order")
        add_btn.setIconSize(QSize(16, 16))
        refresh_btn = QPushButton()
        refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        refresh_btn.setToolTip("Refresh orders")

        add_btn.clicked.connect(self.add_order)
        refresh_btn.clicked.connect(self.refresh_orders)

        button_layout.addWidget(add_btn)
        button_layout.addWidget(refresh_btn)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addLayout(button_layout)

        layout.addLayout(header_layout)

        self.table = QTableView()
        self.model = OrdersTableModel([])
        self.table.setModel(self.model)

        self.action_delegate = ActionButtonDelegate(self.table, type="order")
        self.action_delegate.edit_clicked.connect(self.edit_order)
        self.action_delegate.delete_clicked.connect(self.delete_order)
        self.table.setItemDelegateForColumn(6, self.action_delegate)

        for row in range(self.model.rowCount()):
            self.table.edit(self.model.index(row, 6))

        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(6, 100)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_orders(self, orders: List[Dict[str, Any]]):
        """Load orders into the table."""
        self.model = OrdersTableModel(orders)
        self.table.setModel(self.model)

        self.action_delegate = ActionButtonDelegate(self.table, type="order")
        self.action_delegate.edit_clicked.connect(self.edit_order)
        self.action_delegate.delete_clicked.connect(self.delete_order)
        self.table.setItemDelegateForColumn(6, self.action_delegate)

        def init_editors():
            for row in range(self.model.rowCount()):
                self.table.edit(self.model.index(row, 6))

        QTimer.singleShot(100, init_editors)

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

    def delete_order(self, order_id: int):
        """Delete an order."""
        if show_confirmation(
            self,
            "Are you sure you want to delete this order?"
        ):
            try:
                response = delete_order(order_id)
                if 'message' in response:
                    show_info(self, "Order deleted successfully")
                    self.refresh_orders()
                else:
                    show_error(self, response.get('message', 'Unknown error'))
            except Exception as e:
                show_error(self, str(e))

    def edit_order(self, order_id: int):
        """Open dialog to edit a product."""
        orders = get_orders()
        order = next((o for o in orders if o['id'] == order_id), None)
        if order:
            dialog = AddProductDialog(self, order)

            if dialog.exec() == AddProductDialog.DialogCode.Accepted:
                try:
                    data = dialog.get_data()
                    response = update_order(order_id, data)
                    if 'id' in response:
                        self.refresh_orders()
                    else:
                        show_error(
                            self,
                            response.get('message', 'Unknown error')
                        )
                except Exception as e:
                    show_error(self, str(e))

    def refresh_orders(self):
        """Refresh the orders table."""
        orders = get_orders()
        self.load_orders(orders)
