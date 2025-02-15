import sys

from api import get_products
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class ProductsTab(QWidget):
    def __init__(self, products):
        """Products tab."""
        super().__init__()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'ID',
            'Name',
            'Brand',
            'Price',
            'Stock'
        ])

        self.load_products(products)

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_products(self, products):
        """Load products into the table."""
        self.table.setRowCount(len(products))

        for i, product in enumerate(products):
            self.table.setItem(i, 0, QTableWidgetItem(str(product['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(product['name']))
            self.table.setItem(i, 2, QTableWidgetItem(product['brand']))
            self.table.setItem(i, 3, QTableWidgetItem(str(product['price'])))
            self.table.setItem(i, 4, QTableWidgetItem(str(product['stock'])))

class OrdersTab(QWidget):
    def __init__(self):
        """Orders tab."""
        super().__init__()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'ID',
            'Product',
            'Quantity',
            'Customer',
            'Date'
        ])

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        """Main window."""
        super().__init__()

        self.setWindowTitle("Order Manager")
        self.resize(800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.load_products_tab()
        self.load_orders_tab()

    def load_products_tab(self):
        """Load products tab."""
        products = get_products()
        self.products_tab = ProductsTab(products)
        self.tabs.addTab(self.products_tab, "Products")

    def load_orders_tab(self):
        """Load orders tab."""
        self.orders_tab = OrdersTab()
        self.tabs.addTab(self.orders_tab, "Orders")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
