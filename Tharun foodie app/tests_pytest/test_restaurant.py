import requests

BASE_URL = "http://localhost:5001"

def test_register_restaurant():
    response = requests.post(f"{BASE_URL}/api/v1/restaurants",
                             json={"name": "Test Hotel"})
    assert response.status_code == 201