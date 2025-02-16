import sys

from api import get_products
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from ui.tabs import OrdersTab, ProductsTab


class MainWindow(QMainWindow):
    def __init__(self):
        """Main window."""
        super().__init__()

        self.setWindowTitle("Order Manager")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        """Set up user interface."""
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        products = get_products()

        self.products_tab = ProductsTab(products)
        self.orders_tab = OrdersTab()

        self.tabs.addTab(self.products_tab, "Products")
        self.tabs.addTab(self.orders_tab, "Orders")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
