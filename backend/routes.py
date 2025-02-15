from flask import Blueprint, jsonify, request
from models import Order, Product, db

bp = Blueprint('api', __name__)

@bp.route('/products', methods=['GET'])
def get_products():
    """Get all products."""
    try:
        products = Product.query.all()
        return jsonify([product.serialize() for product in products])
    except Exception as e:
        return jsonify({ "message": str(e) }), 400

@bp.route('/orders', methods=['POST'])
def create_order():
    """Create a new order."""
    try:
        data = request.json

        if data is not None:
            order = Order()
            order.product_id = data.get('product_id')
            order.quantity = data.get('quantity')
            order.customer = data.get('customer')
            order.order_date = data.get('order_date')

            db.session.add(order)
            db.session.commit()
        else:
            raise Exception("Invalid order data.")

        return jsonify({ "message": "Order saved." }), 201
    except Exception as e:
        return jsonify({ "message": str(e) }), 400
