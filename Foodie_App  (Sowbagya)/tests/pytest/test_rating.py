import requests

BASE_URL = "http://127.0.0.1:5000/api/v1/ratings"

def test_give_rating():
    payload = {
        "order_id": 1,
        "rating": 5,
        "comment": "Excellent!"
    }

    res = requests.post(BASE_URL, json=payload)
    assert res.status_code in [201, 400]
