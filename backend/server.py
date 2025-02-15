import os

from flask import Flask
from models import db
from routes import bp

app = Flask(__name__)
db_path = os.path.join(app.instance_path, 'order_manager.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
