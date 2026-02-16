import requests

BASE_URL = "http://localhost:5001"

def test_register_user():
    response = requests.post(f"{BASE_URL}/api/v1/users/register",
                             json={"name": "Tharun", "email": "tharun@gmail.com"})
    assert response.status_code == 201