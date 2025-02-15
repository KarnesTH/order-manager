# Order Manager

A demo project showcasing a modern Python application with a REST API backend and PyQt6 desktop frontend.

## Features

- **Backend (Flask)**
  - RESTful API
  - SQLite Database with SQLAlchemy
  - Docker support
  - Unit Tests
  - CI/CD Pipeline

- **Desktop Frontend (PyQt6)**
  - Product Management
  - Order Management
  - Modern UI with Tabs
  - Error Handling

## Project Structure

```
order-manager/
├── backend/
│   ├── tests/
│   ├── models.py
│   ├── routes.py
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── ui/
│   ├── api.py
│   ├── app.py
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

## Setup

### Backend

```bash
# Using Docker
docker-compose up -d --build

# Manual setup
cd backend
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
python server.py
```

### Frontend

```bash
cd frontend
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Testing

```bash
cd backend
python -m unittest discover -s tests
```

## API Endpoints

### Products
- GET /api/products - List all products
- POST /api/products - Create a product
- PUT /api/products/{id} - Update a product
- DELETE /api/products/{id} - Delete a product

### Orders
- GET /api/orders - List all orders
- POST /api/orders - Create an order
- PUT /api/orders/{id} - Update an order
- DELETE /api/orders/{id} - Delete an order

## Technologies Used

- Python 3.9+
- Flask
- SQLAlchemy
- PyQt6
- Docker
- GitHub Actions

## Contributing

This is a demo project, but feel free to use it as a template for your own projects.

## License

MIT License - see LICENSE file
