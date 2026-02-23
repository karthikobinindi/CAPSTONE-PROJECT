import sys, os, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))


def uname(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def _full_setup(client):
    reg = client.post("/api/v1/restaurants", json={
        "name": uname("User Rest"), "category": "Indian",
        "location": "Chennai", "contact": "6000000001"
    })
    rid = reg.get_json()["restaurant_id"]
    client.put(f"/api/v1/admin/restaurants/{rid}/approve")
    dish = client.post(f"/api/v1/restaurants/{rid}/dishes", json={
        "name": "Test Dish", "type": "Veg", "price": 150.0
    })
    did = dish.get_json()["dish_id"]
    user = client.post("/api/v1/users/register", json={
        "name": "Test User",
        "email": f"{uname('user')}@example.com",
        "password": "Pass@123"
    })
    uid = user.get_json()["user_id"]
    return rid, did, uid


def test_req13_user_registration(client):
    """REQ-13: POST /api/v1/users/register"""
    response = client.post("/api/v1/users/register", json={
        "name": "Arjun Kumar",
        "email": f"{uname('arjun')}@example.com",
        "password": "Arjun@123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "user_id" in data
    assert "password" not in data


def test_req14_search_restaurants(client):
    """REQ-14: GET /api/v1/restaurants/search"""
    name = uname("Search Rest")
    client.post("/api/v1/restaurants", json={
        "name": name, "category": "Chinese",
        "location": "Hyderabad", "contact": "6000000002"
    })
    response = client.get(f"/api/v1/restaurants/search?name={name}")
    assert response.status_code == 200
    assert any(name in r["name"] for r in response.get_json())


def test_req15_place_order(client):
    """REQ-15: POST /api/v1/orders"""
    rid, did, uid = _full_setup(client)
    response = client.post("/api/v1/orders", json={
        "user_id": uid, "restaurant_id": rid, "dishes": [did]
    })
    assert response.status_code == 201
    assert response.get_json()["status"] == "placed"


def test_req16_give_rating(client):
    """REQ-16: POST /api/v1/ratings"""
    rid, did, uid = _full_setup(client)
    oid = client.post("/api/v1/orders", json={
        "user_id": uid, "restaurant_id": rid, "dishes": [did]
    }).get_json()["order_id"]
    response = client.post("/api/v1/ratings", json={
        "order_id": oid, "rating": 5, "comment": "Excellent!"
    })
    assert response.status_code == 201
    assert response.get_json()["rating"] == 5