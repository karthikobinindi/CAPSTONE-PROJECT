import requests

BASE_URL = "http://127.0.0.1:5000/api/v1/users/register"

def test_user_registration():
    payload = {
        "name": "UserJSON",
        "email": "userjson@gmail.com",
        "password": "12345"
    }

    res = requests.post(BASE_URL, json=payload)
    assert res.status_code in [201, 409]
