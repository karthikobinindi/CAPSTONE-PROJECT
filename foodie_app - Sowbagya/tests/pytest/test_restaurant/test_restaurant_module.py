import sys, os, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))


def uname(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def test_req1_register_restaurant(client):
    """REQ-1: POST /api/v1/restaurants"""
    response = client.post("/api/v1/restaurants", json={
        "name": uname("Spice Garden"),
        "category": "Indian",
        "location": "Chennai",
        "contact": "9876543210"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "restaurant_id" in data
    assert data["status"] == "pending"


def test_req2_update_restaurant(client):
    """REQ-2: PUT /api/v1/restaurants/{restaurant_id}"""
    reg = client.post("/api/v1/restaurants", json={
        "name": uname("Old Name"), "category": "Fast Food",
        "location": "Mumbai", "contact": "9000000001"
    })
    rid = reg.get_json()["restaurant_id"]
    response = client.put(f"/api/v1/restaurants/{rid}", json={
        "name": "New Name", "contact": "9000000099"
    })
    assert response.status_code == 200
    assert response.get_json()["name"] == "New Name"


def test_req3_disable_restaurant(client):
    """REQ-3: PUT /api/v1/restaurants/{restaurant_id}/disable"""
    reg = client.post("/api/v1/restaurants", json={
        "name": uname("To Disable"), "category": "Cafe",
        "location": "Delhi", "contact": "9000000002"
    })
    rid = reg.get_json()["restaurant_id"]
    response = client.put(f"/api/v1/restaurants/{rid}/disable")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Restaurant disabled"


def test_req4_view_restaurant(client):
    """REQ-4: GET /api/v1/restaurants/{restaurant_id}"""
    reg = client.post("/api/v1/restaurants", json={
        "name": uname("View Me"), "category": "Pizza",
        "location": "Bangalore", "contact": "9000000003"
    })
    rid = reg.get_json()["restaurant_id"]
    response = client.get(f"/api/v1/restaurants/{rid}")
    assert response.status_code == 200
    assert response.get_json()["restaurant_id"] == rid