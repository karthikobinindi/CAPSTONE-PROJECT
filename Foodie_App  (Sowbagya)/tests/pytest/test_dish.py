import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"


# -------------------------------
# Test 5: Add Dish
# POST /api/v1/restaurants/{restaurant_id}/dishes
# -------------------------------
def test_add_dish():
    payload = {
        "name": "Pizza",
        "type": "Fast Food",
        "price": 120,
        "available_time": "Night"
    }

    res = requests.post(f"{BASE_URL}/restaurants/1/dishes", json=payload)

    assert res.status_code in [201, 400]

    if res.status_code == 201:
        data = res.json()
        assert "id" in data
        assert data["name"] == "Pizza"
        assert data["price"] == 120
        assert data["enabled"] == True
    else:
        assert res.json()["error"] == "name and price are required"


# -------------------------------
# Test 6: Update Dish
# PUT /api/v1/dishes/{dish_id}
# -------------------------------
def test_update_dish():
    dish_id = 1
    payload = {
        "name": "Updated Pizza",
        "type": "Italian",
        "price": 150,
        "available_time": "Evening"
    }

    res = requests.put(f"{BASE_URL}/dishes/{dish_id}", json=payload)

    assert res.status_code in [200, 404]

    if res.status_code == 200:
        data = res.json()
        assert data["name"] == "Updated Pizza"
        assert data["type"] == "Italian"
        assert data["price"] == 150
        assert data["available_time"] == "Evening"
    else:
        assert res.json()["error"] == "Dish not found"


# -------------------------------
# Test 7: Enable / Disable Dish
# PUT /api/v1/dishes/{dish_id}/status
# -------------------------------
def test_disable_dish_status():
    dish_id = 1
    payload = {"enabled": False}

    res = requests.put(f"{BASE_URL}/dishes/{dish_id}/status", json=payload)

    assert res.status_code in [200, 400, 404]

    if res.status_code == 200:
        assert res.json()["message"] == "Dish status updated"
    elif res.status_code == 400:
        assert res.json()["error"] == "enabled field required"
    else:
        assert res.json()["error"] == "Dish not found"


def test_enable_dish_status():
    dish_id = 1
    payload = {"enabled": True}

    res = requests.put(f"{BASE_URL}/dishes/{dish_id}/status", json=payload)

    assert res.status_code in [200, 400, 404]

    if res.status_code == 200:
        assert res.json()["message"] == "Dish status updated"
    elif res.status_code == 400:
        assert res.json()["error"] == "enabled field required"
    else:
        assert res.json()["error"] == "Dish not found"


# -------------------------------
# Test 8: Delete Dish
# DELETE /api/v1/dishes/{dish_id}
# -------------------------------
def test_delete_dish():
    dish_id = 1

    res = requests.delete(f"{BASE_URL}/dishes/{dish_id}")

    assert res.status_code in [200, 404]

    if res.status_code == 200:
        assert res.json()["message"] == "Dish deleted"
    else:
        assert res.json()["error"] == "Dish not found"