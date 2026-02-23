import sys, os, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))


def uname(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def _setup_with_order(client):
    reg = client.post("/api/v1/restaurants", json={
        "name": uname("Order Rest"), "category": "Indian",
        "location": "Chennai", "contact": "5000000001"
    })
    rid = reg.get_json()["restaurant_id"]
    client.put(f"/api/v1/admin/restaurants/{rid}/approve")
    dish = client.post(f"/api/v1/restaurants/{rid}/dishes", json={
        "name": "Order Dish", "type": "Veg", "price": 120.0
    })
    did = dish.get_json()["dish_id"]
    user = client.post("/api/v1/users/register", json={
        "name": "Order User",
        "email": f"{uname('order')}@example.com",
        "password": "Pass@123"
    })
    uid = user.get_json()["user_id"]
    oid = client.post("/api/v1/orders", json={
        "user_id": uid, "restaurant_id": rid, "dishes": [did]
    }).get_json()["order_id"]
    return rid, uid, oid


def test_req17_view_orders_by_restaurant(client):
    """REQ-17: GET /api/v1/restaurants/{restaurant_id}/orders"""
    rid, uid, oid = _setup_with_order(client)
    response = client.get(f"/api/v1/restaurants/{rid}/orders")
    assert response.status_code == 200
    assert any(o["order_id"] == oid for o in response.get_json())


def test_req18_view_orders_by_user(client):
    """REQ-18: GET /api/v1/users/{user_id}/orders"""
    rid, uid, oid = _setup_with_order(client)
    response = client.get(f"/api/v1/users/{uid}/orders")
    assert response.status_code == 200
    assert any(o["order_id"] == oid for o in response.get_json())