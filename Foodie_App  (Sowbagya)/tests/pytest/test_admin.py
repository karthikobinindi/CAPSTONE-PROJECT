import requests

BASE_URL = "http://127.0.0.1:5000/api/v1/admin"


# Test  Approve Restaurant
# PUT /api/v1/admin/restaurants/{restaurant_id}/approve
def test_approve_restaurant():
    restaurant_id = 1
    res = requests.put(f"{BASE_URL}/restaurants/{restaurant_id}/approve")

    assert res.status_code in [200, 404]

    if res.status_code == 200:
        assert res.json()["message"] == "Restaurant approved"
    else:
        assert res.json()["error"] == "Restaurant not found"


# Test  Disable Restaurant
# PUT /api/v1/admin/restaurants/{restaurant_id}/disable
def test_disable_restaurant():
    restaurant_id = 1
    res = requests.put(f"{BASE_URL}/restaurants/{restaurant_id}/disable")

    assert res.status_code in [200, 404]

    if res.status_code == 200:
        assert res.json()["message"] == "Restaurant disabled"
    else:
        assert res.json()["error"] == "Restaurant not found"


# Test  View Customer Feedback
# GET /api/v1/admin/feedback
def test_view_feedback():
    res = requests.get(f"{BASE_URL}/feedback")

    assert res.status_code == 200
    assert isinstance(res.json(), list) or isinstance(res.json(), dict)


# Test  View Order Status
# GET /api/v1/admin/orders
def test_view_orders():
    res = requests.get(f"{BASE_URL}/orders")

    assert res.status_code == 200
    assert isinstance(res.json(), list) or isinstance(res.json(), dict)