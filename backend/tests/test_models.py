import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from models import Order, Product, db
from server import app


class TestModels(unittest.TestCase):
    def setUp(self):
        """Set up test database."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        """Tear down test database."""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_product(self):
        """Test product model."""
        product = Product()
        product.name = 'Test Product'
        product.brand = 'Test Brand'
        product.price = 10.0
        product.stock = 100

        db.session.add(product)
        db.session.commit()

        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.brand, 'Test Brand')
        self.assertEqual(product.price, 10.0)
        self.assertEqual(product.stock, 100)

    def test_order(self):
        """Test order model."""
        product = Product()
        product.name = 'Test Product'
        product.brand = 'Test Brand'
        product.price = 10.0
        product.stock = 100

        db.session.add(product)
        db.session.commit()

        order = Order()
        order.product_id = product.id
        order.quantity = 10
        order.customer = 'Test Customer'
        order.order_date = '2021-01-01'

        db.session.add(order)
        db.session.commit()

        self.assertEqual(order.id, 1)
        self.assertEqual(order.product_id, product.id)
        self.assertEqual(order.quantity, 10)
        self.assertEqual(order.customer, 'Test Customer')
        self.assertEqual(order.order_date, '2021-01-01')
        self.assertEqual(order.status, 'open')

if __name__ == '__main__':
    unittest.main()
