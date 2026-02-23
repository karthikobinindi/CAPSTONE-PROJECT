import sys, os, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))


def uname(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def _setup_restaurant(client):
    reg = client.post("/api/v1/restaurants", json={
        "name": uname("Dish Rest"), "category": "Indian",
        "location": "Chennai", "contact": "8000000001"
    })
    rid = reg.get_json()["restaurant_id"]
    client.put(f"/api/v1/admin/restaurants/{rid}/approve")
    return rid


def test_req5_add_dish(client):
    """REQ-5: POST /api/v1/restaurants/{restaurant_id}/dishes"""
    rid = _setup_restaurant(client)
    response = client.post(f"/api/v1/restaurants/{rid}/dishes", json={
        "name": "Butter Chicken", "type": "Non-Veg",
        "price": 320.0, "available_time": "11:00-23:00"
    })
    assert response.status_code == 201
    assert "dish_id" in response.get_json()


def test_req6_update_dish(client):
    """REQ-6: PUT /api/v1/dishes/{dish_id}"""
    rid = _setup_restaurant(client)
    add = client.post(f"/api/v1/restaurants/{rid}/dishes", json={
        "name": "Old Dish", "type": "Veg", "price": 100.0
    })
    did = add.get_json()["dish_id"]
    response = client.put(f"/api/v1/dishes/{did}", json={"name": "New Dish", "price": 150.0})
    assert response.status_code == 200
    assert response.get_json()["name"] == "New Dish"


def test_req7_enable_disable_dish(client):
    """REQ-7: PUT /api/v1/dishes/{dish_id}/status"""
    rid = _setup_restaurant(client)
    add = client.post(f"/api/v1/restaurants/{rid}/dishes", json={
        "name": "Toggle Dish", "type": "Veg", "price": 80.0
    })
    did = add.get_json()["dish_id"]
    response = client.put(f"/api/v1/dishes/{did}/status", json={"enabled": False})
    assert response.status_code == 200
    assert "disabled" in response.get_json()["message"].lower()


def test_req8_delete_dish(client):
    """REQ-8: DELETE /api/v1/dishes/{dish_id}"""
    rid = _setup_restaurant(client)
    add = client.post(f"/api/v1/restaurants/{rid}/dishes", json={
        "name": "Delete Me", "type": "Veg", "price": 60.0
    })
    did = add.get_json()["dish_id"]
    response = client.delete(f"/api/v1/dishes/{did}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Dish deleted"