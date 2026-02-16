import requests

BASE_URL = "http://127.0.0.1:5000/api/v1/orders"

def test_place_order():
    payload = {
        "user_id": 1,
        "restaurant_id": 1,
        "dishes": ["Pizza", "Burger"]
    }

    res = requests.post(BASE_URL, json=payload)
    assert res.status_code in [201, 400]
