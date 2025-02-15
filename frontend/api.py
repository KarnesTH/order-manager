from typing import Any, Dict, List

import requests

API_URL = 'http://localhost:5000/api'

def get_products() -> List[Dict[str, Any]]:
    """Get all products."""
    try:
        response = requests.get(f'{API_URL}/products')
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        return [{ "message": str(e) }]

def create_product(product: Dict[str, Any]) -> Dict[str, Any]:
    """Create a product."""
    try:
        response = requests.post(f'{API_URL}/products', json=product)
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        return { "message": str(e) }

def update_product(product_id: int, product: Dict[str, Any]) -> Dict[str, Any]:
    """Update a product."""
    try:
        response = requests.put(f'{API_URL}/products/{product_id}', json=product)
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        return { "message": str(e) }

def delete_product(product_id: int) -> Dict[str, Any]:
    """Delete a product."""
    try:
        response = requests.delete(f'{API_URL}/products/{product_id}')
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        return { "message": str(e) }

def get_orders() -> List[Dict[str, Any]]:
    """Get all orders."""
    try:
        response = requests.get(f'{API_URL}/orders')
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        return [{ "message": str(e) }]

def create_order(order: Dict[str, Any]) -> Dict[str, Any]:
    """Create an order."""
    try:
        response = requests.post(f'{API_URL}/orders', json=order)
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        return { "message": str(e) }

def update_order(order_id: int, order: Dict[str, Any]) -> Dict[str, Any]:
    """Update an order."""
    try:
        response = requests.put(f'{API_URL}/orders/{order_id}', json=order)
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        return { "message": str(e) }

def delete_order(order_id: int) -> Dict[str, Any]:
    """Delete an order."""
    try:
        response = requests.delete(f'{API_URL}/orders/{order_id}')
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        return { "message": str(e) }
