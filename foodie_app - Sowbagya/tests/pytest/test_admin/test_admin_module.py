import sys, os, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))


def uname(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def _register_restaurant(client, prefix="Admin Rest"):
    reg = client.post("/api/v1/restaurants", json={
        "name": uname(prefix), "category": "Indian",
        "location": "Chennai", "contact": "7000000001"
    })
    return reg.get_json()["restaurant_id"]


def test_req9_approve_restaurant(client):
    """REQ-9: PUT /api/v1/admin/restaurants/{restaurant_id}/approve"""
    rid = _register_restaurant(client)
    response = client.put(f"/api/v1/admin/restaurants/{rid}/approve")
    assert response.status_code == 200
    assert "approved" in response.get_json()["message"].lower()
    assert client.get(f"/api/v1/restaurants/{rid}").get_json()["status"] == "approved"


def test_req10_admin_disable_restaurant(client):
    """REQ-10: PUT /api/v1/admin/restaurants/{restaurant_id}/disable"""
    rid = _register_restaurant(client, "Admin Disable")
    response = client.put(f"/api/v1/admin/restaurants/{rid}/disable")
    assert response.status_code == 200
    assert client.get(f"/api/v1/restaurants/{rid}").get_json()["status"] == "disabled"


def test_req11_view_customer_feedback(client):
    """REQ-11: GET /api/v1/admin/feedback"""
    response = client.get("/api/v1/admin/feedback")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_req12_view_order_status(client):
    """REQ-12: GET /api/v1/admin/orders"""
    response = client.get("/api/v1/admin/orders")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)