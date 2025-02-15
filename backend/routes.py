from http import HTTPStatus
from typing import Any, Dict, List

from flask import Blueprint, current_app, jsonify, request
from flask.typing import ResponseReturnValue
from models import Order, Product, db

bp = Blueprint('api', __name__)

# Routes for products
@bp.route('/products', methods=['GET'])
def get_products():
    """
    Get all products.

    Returns:
        ResponseReturnValue:
            JSON response containing list of products and HTTP status code.
            Success: (product_list, 200)
            Error: (error_message, 500)

    Raises:
        Exception: If database query fails
    """
    try:
        products: List[Product] = Product.query.all()
        current_app.logger.info(f"Retrieved {len(products)} products")

        return create_response(
            [product.serialize() for product in products],
            HTTPStatus.OK
        )
    except Exception as e:
        current_app.logger.error(f"Error fetching products: {str(e)}")
        return create_response({
            "message": "Error fetching products",
            "error": str(e)
        }, HTTPStatus.INTERNAL_SERVER_ERROR)

@bp.route('/products', methods=['POST'])
def create_product():
    """
    Create a new product.

    Returns:
        tuple: A tuple containing the response data and status code.

    Raises:
        ValueError: If the JSON is invalid or missing required fields.
        Exception: If an error occurs while creating the product.
    """
    try:
        data: Dict[str, Any] = request.json or {}

        validate_request_data(data, ['name', 'brand', 'price', 'stock'])

        if data.get('price', 0) <= 0:
            raise ValueError("Price must be greater than 0")

        if data.get('stock', 0) < 0:
            raise ValueError("Stock must be greater than or equal to 0")

        product = Product(**data)
        db.session.add(product)
        db.session.commit()

        current_app.logger.info(f"Created product #{product.id} - {product.name}")

        return create_response(product.serialize(), HTTPStatus.CREATED)
    except ValueError as e:
        current_app.logger.error(f"Invalid product data: {str(e)}")
        return create_response({"message": str(e)}, HTTPStatus.BAD_REQUEST)
    except Exception as e:
        current_app.logger.error(f"Error creating product: {str(e)}")
        return create_response({
            "message": "Internal server error"
        }, HTTPStatus.INTERNAL_SERVER_ERROR)

@bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id: int):
    """
    Update a product.

    Args:
        product_id (int): Product ID.

    Returns:
        tuple: A tuple containing the response data and status code.

    Raises:
        ValueError: If the JSON is invalid or missing required fields.
        Exception: If an error occurs while updating the product.
    """
    try:
        data: Dict[str, Any] = request.json or {}

        validate_request_data(data, ['name', 'brand', 'price', 'stock'])

        product = Product.query.get(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")

        for key, value in data.items():
            setattr(product, key, value)

        db.session.commit()

        current_app.logger.info(f"Updated product #{product.id} - {product.name}")

        return create_response(product.serialize(), HTTPStatus.OK)
    except ValueError as e:
        current_app.logger.error(f"Invalid product data: {str(e)}")
        return create_response({"message": str(e)}, HTTPStatus.BAD_REQUEST)
    except Exception as e:
        current_app.logger.error(f"Error updating product: {str(e)}")
        return create_response({
            "message": "Internal server error"
        }, HTTPStatus.INTERNAL_SERVER_ERROR)

@bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int):
    """
    Delete a product.

    Args:
        product_id (int): Product ID.

    Returns:
        tuple: A tuple containing the response data and status code.

    Raises:
        Exception: If an error occurs while deleting the product.
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")

        db.session.delete(product)
        db.session.commit()

        current_app.logger.info(f"Deleted product #{product.id} - {product.name}")

        return create_response(
            {"message": "Product deleted"},
            HTTPStatus.OK
        )
    except Exception as e:
        current_app.logger.error(f"Error deleting product: {str(e)}")
        return create_response({
            "message": "Internal server error"
        }, HTTPStatus.INTERNAL_SERVER_ERROR)

# Routes for orders
@bp.route('/orders', methods=['GET'])
def get_orders():
    """
    Get all orders.

    Returns:
        tuple: JSON response containing list of orders and HTTP status code.
            Success: (order_list, 200)
            Error: (error_message, 500)

    Raises:
        Exception: If database query fails
    """
    try:
        orders: List[Order] = Order.query.all()
        current_app.logger.info(f"Retrieved {len(orders)} orders")
        return create_response(
            [order.serialize() for order in orders],
            HTTPStatus.OK
        )
    except Exception as e:
        current_app.logger.error(f"Error fetching orders: {str(e)}")
        return create_response({
            "message": "Error fetching orders",
            "error": str(e)
        }, HTTPStatus.INTERNAL_SERVER_ERROR)

@bp.route('/orders', methods=['POST'])
def create_order():
    """
    Create a new order.

    Returns:
        tuple: A tuple containing the response data and status code.

    Raises:
        ValueError: If the JSON is invalid or missing required fields.
        Exception: If an error occurs while creating the order.
    """
    try:
        data: Dict[str, Any] = request.json or {}

        validate_request_data(
            data,
            ['product_id', 'quantity', 'customer', 'order_date']
        )

        if data.get('quantity', 0) <= 0:
            raise ValueError("Quantity must be greater than 0")

        product = Product.query.get(data['product_id'])
        if not product:
            raise ValueError(f"Product with ID {data['product_id']} not found")
        if product.stock < data['quantity']:
            raise ValueError(f"Insufficient stock. Available: {product.stock}")

        order = Order(**data)
        db.session.add(order)

        product.stock -= data['quantity']

        db.session.commit()

        current_app.logger.info(
            f"Created order #{order.id} for customer {data['customer']}"
            f" - Product: {product.name}, Quantity: {data['quantity']}"
        )

        return create_response(order.serialize(), HTTPStatus.CREATED)

    except ValueError as e:
        current_app.logger.error(f"Invalid order data: {str(e)}")
        return create_response({"message": str(e)}, HTTPStatus.BAD_REQUEST)
    except Exception as e:
        current_app.logger.error(f"Error creating order: {str(e)}")
        return create_response({
            "message": "Internal server error"
        }, HTTPStatus.INTERNAL_SERVER_ERROR)

@bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id: int):
    """
    Update an order.

    Args:
        order_id (int): Order ID.

    Returns:
        tuple: A tuple containing the response data and status code.

    Raises:
        ValueError: If the JSON is invalid or missing required fields.
        Exception: If an error occurs while updating the order.
    """
    try:
        data: Dict[str, Any] = request.json or {}

        validate_request_data(
            data,
            ['product_id', 'quantity', 'customer', 'order_date']
        )

        order = Order.query.get(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found")

        for key, value in data.items():
            setattr(order, key, value)

        db.session.commit()

        current_app.logger.info(f"Updated order #{order.id} - {order.customer}")

        return create_response(order.serialize(), HTTPStatus.OK)
    except ValueError as e:
        current_app.logger.error(f"Invalid order data: {str(e)}")
        return create_response({"message": str(e)}, HTTPStatus.BAD_REQUEST)
    except Exception as e:
        current_app.logger.error(f"Error updating order: {str(e)}")
        return create_response({
            "message": "Internal server error"
        }, HTTPStatus.INTERNAL_SERVER_ERROR)

@bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id: int):
    """
    Delete an order.

    Args:
        order_id (int): Order ID.

    Returns:
        tuple: A tuple containing the response data and status code.

    Raises:
        Exception: If an error occurs while deleting the order.
    """
    try:
        order = Order.query.get(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found")

        db.session.delete(order)

        product = Product.query.get(order.product_id)

        if product is not None:
            product.stock += order.quantity

        db.session.commit()

        current_app.logger.info(f"Deleted order #{order.id} - {order.customer}")

        return create_response(
            {"message": "Order deleted"},
            HTTPStatus.OK
        )
    except Exception as e:
        current_app.logger.error(f"Error deleting order: {str(e)}")
        return create_response({
            "message": "Internal server error"
        }, HTTPStatus.INTERNAL_SERVER_ERROR)

# Helper functions
def validate_request_data(data: Dict[str, Any], required_fields: List[str]) -> None:
    """
    Validate request data.

    Args:
        data (dict): Request data.
        required_fields (list): List of required fields.

    Raises:
        ValueError: If the JSON is invalid or missing required fields.
    """
    if data is None:
        raise ValueError("Invalid JSON")

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(
            f"Missing required fields: {', '.join(missing_fields)}"
        )

def create_response(
    data: Any,
    status: HTTPStatus = HTTPStatus.OK
) -> ResponseReturnValue:
    """
    Create a JSON response.

    Args:
        data (any): Response data.
        status (HTTPStatus): HTTP status code.

    Returns:
        tuple: A tuple containing the response data and status code.
    """
    return jsonify(data), status
