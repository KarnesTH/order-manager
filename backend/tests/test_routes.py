import json
import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from models import db
from server import app


class TestRoutes(unittest.TestCase):
    def setUp(self):
        """Set up test database and client."""
        app.config.update({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SERVER_NAME': 'localhost',
        })
        self.app = app
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_get_products_empty(self):
        """Test GET /products with empty database."""
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_create_product(self):
        """Test POST /products."""
        product_data = {
            "name": "Test Product",
            "brand": "Test Brand",
            "price": 99.99,
            "stock": 10
        }
        response = self.client.post(
            '/api/products',
            json=product_data
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], product_data['name'])
        self.assertEqual(data['price'], product_data['price'])

    def test_create_product_invalid(self):
        """Test POST /products with invalid data."""
        product_data = {
            "name": "Test Product"
        }
        response = self.client.post(
            '/api/products',
            json=product_data
        )
        self.assertEqual(response.status_code, 400)

    def test_create_and_get_product(self):
        """Test POST and then GET /products."""
        product_data = {
            "name": "Test Product",
            "brand": "Test Brand",
            "price": 99.99,
            "stock": 10
        }
        self.client.post('/api/products', json=product_data)

        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], product_data['name'])

    def test_update_product(self):
        """Test PUT /products/<id>."""
        product_data = {
            "name": "Test Product",
            "brand": "Test Brand",
            "price": 99.99,
            "stock": 10
        }
        response = self.client.post('/api/products', json=product_data)
        product_id = json.loads(response.data)['id']

        update_data = {
            "name": "Updated Product",
            "brand": "Updated Brand",
            "price": 199.99,
            "stock": 20
        }
        response = self.client.put(
            f'/api/products/{product_id}',
            json=update_data
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], update_data['name'])
        self.assertEqual(data['price'], update_data['price'])

    def test_delete_product(self):
        """Test DELETE /products/<id>."""
        product_data = {
            "name": "Test Product",
            "brand": "Test Brand",
            "price": 99.99,
            "stock": 10
        }
        response = self.client.post('/api/products', json=product_data)
        product_id = json.loads(response.data)['id']

        response = self.client.delete(f'/api/products/{product_id}')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/products')
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

    def test_create_order(self):
        """Test POST /orders."""
        product_data = {
            "name": "Test Product",
            "brand": "Test Brand",
            "price": 99.99,
            "stock": 10
        }
        product_response = self.client.post(
            '/api/products',
            json=product_data
        )
        product_id = json.loads(product_response.data)['id']

        order_data = {
            "product_id": product_id,
            "quantity": 2,
            "customer": "Test Customer",
            "order_date": "2023-09-20"
        }
        response = self.client.post('/api/orders', json=order_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['quantity'], order_data['quantity'])
        self.assertEqual(data['customer'], order_data['customer'])

        product_response = self.client.get('/api/products')
        products = json.loads(product_response.data)
        self.assertEqual(products[0]['stock'], 8)

    def test_update_order(self):
        """Test PUT /orders/<id>."""
        product_data = {
            "name": "Test Product",
            "brand": "Test Brand",
            "price": 99.99,
            "stock": 10
        }
        product_response = self.client.post('/api/products', json=product_data)
        product_id = json.loads(product_response.data)['id']

        order_data = {
            "product_id": product_id,
            "quantity": 2,
            "customer": "Test Customer",
            "order_date": "2023-09-20"
        }
        order_response = self.client.post('/api/orders', json=order_data)
        order_id = json.loads(order_response.data)['id']

        update_data = {
            "product_id": product_id,
            "quantity": 3,
            "customer": "Updated Customer",
            "order_date": "2023-09-21"
        }
        response = self.client.put(
            f'/api/orders/{order_id}',
            json=update_data
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['customer'], update_data['customer'])
        self.assertEqual(data['quantity'], update_data['quantity'])

    def test_delete_order(self):
        """Test DELETE /orders/<id>."""
        product_data = {
            "name": "Test Product",
            "brand": "Test Brand",
            "price": 99.99,
            "stock": 10
        }
        product_response = self.client.post('/api/products', json=product_data)
        product_id = json.loads(product_response.data)['id']

        order_data = {
            "product_id": product_id,
            "quantity": 2,
            "customer": "Test Customer",
            "order_date": "2023-09-20"
        }
        order_response = self.client.post('/api/orders', json=order_data)
        order_id = json.loads(order_response.data)['id']

        response = self.client.delete(f'/api/orders/{order_id}')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/orders')
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

        product_response = self.client.get('/api/products')
        products = json.loads(product_response.data)
        self.assertEqual(products[0]['stock'], 10)

if __name__ == '__main__':
    unittest.main()
