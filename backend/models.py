from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    """Product model."""
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    brand: str = db.Column(db.String(100), nullable=False)
    price: float = db.Column(db.Float, nullable=False)
    stock: int = db.Column(db.Integer, nullable=False)

    def serialize(self):
        """Return object data in serializeable format."""
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'stock': self.stock
        }

    def __repr__(self):
        return f'<Product {self.id}>'

class Order(db.Model):
    """Order model."""
    id: int = db.Column(db.Integer, primary_key=True)
    product_id: int = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity: int = db.Column(db.Integer, nullable=False)
    customer: str = db.Column(db.String(100), nullable=False)
    order_date: str = db.Column(db.String(100), nullable=False)
    status: str = db.Column(db.String(20), default="open")

    product = db.relationship('Product', backref='orders')

    def serialize(self):
        """Return object data in serializeable format."""
        return {
            'id': self.id,
            'product': self.product.serialize(),
            'quantity': self.quantity,
            'customer': self.customer,
            'order_date': self.order_date,
            'status': self.status
        }

    def __repr__(self):
        return f'<Order {self.id}>'
