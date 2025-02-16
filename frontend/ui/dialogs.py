from datetime import datetime
from typing import Any, Dict, List, Optional

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)


class AddProductDialog(QDialog):
    """Dialog for adding a new product."""
    def __init__(self, parent=None, product: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        self.setWindowTitle("Edit Product" if product else "Add Product")
        self.setup_ui()

        if product:
            self.name_input.setText(product['name'])
            self.brand_input.setText(product['brand'])
            self.price_input.setText(str(product['price']))
            self.stock_input.setText(str(product['stock']))

    def setup_ui(self):
        """Setup the dialog UI."""
        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.brand_input = QLineEdit()
        self.price_input = QLineEdit()
        self.stock_input = QLineEdit()

        layout.addRow("Name:", self.name_input)
        layout.addRow("Brand:", self.brand_input)
        layout.addRow("Price:", self.price_input)
        layout.addRow("Stock:", self.stock_input)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")

        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addRow(button_layout)

        self.setLayout(layout)

    def get_data(self) -> Dict[str, Any]:
        """Get the dialog data."""
        return {
            "name": self.name_input.text(),
            "brand": self.brand_input.text(),
            "price": float(self.price_input.text()),
            "stock": int(self.stock_input.text())
        }


class AddOrderDialog(QDialog):
    """Dialog for adding a new order."""
    def __init__(self, products: List[Dict[str, Any]], parent=None):
        super().__init__(parent)
        self.products = products
        self.setWindowTitle("Add Order")
        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI."""
        layout = QFormLayout()

        self.product_combo = QComboBox()
        for product in self.products:
            self.product_combo.addItem(
                f"{product['name']} ({product['brand']})",
                product['id']
            )

        self.quantity_input = QLineEdit()
        self.customer_input = QLineEdit()
        self.date_input = QLineEdit()
        self.date_input.setText(datetime.now().strftime("%Y-%m-%d"))

        layout.addRow("Product:", self.product_combo)
        layout.addRow("Quantity:", self.quantity_input)
        layout.addRow("Customer:", self.customer_input)
        layout.addRow("Date:", self.date_input)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")

        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addRow(button_layout)

        self.setLayout(layout)

    def get_data(self) -> Dict[str, Any]:
        """Get the dialog data."""
        return {
            "product_id": self.product_combo.currentData(),
            "quantity": int(self.quantity_input.text()),
            "customer": self.customer_input.text(),
            "order_date": self.date_input.text()
        }
