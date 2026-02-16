import requests

BASE_URL = "http://127.0.0.1:5000/api/v1/restaurants"

def test_register_restaurant():
    payload = {
        "name": "Test Restaurant JSON",
        "category": "Veg",
        "location": "Chennai",

        "contact": "9999999999"
    }

    res = requests.post(BASE_URL, json=payload)
    assert res.status_code in [201, 409]


def test_view_restaurant():
    res = requests.get(f"{BASE_URL}/1")
    assert res.status_code in [200, 404]


def test_search_restaurant():
    res = requests.get(f"{BASE_URL}/search?name=Test&location=Chennai&dish=&rating=")
    assert res.status_code == 200
