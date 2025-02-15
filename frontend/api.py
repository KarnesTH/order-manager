import requests

API_URL = 'http://localhost:5000/api'

def get_products():
    """Get all products."""
    try:
        response = requests.get(f'{API_URL}/products')
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        return [{ "message": str(e) }]
