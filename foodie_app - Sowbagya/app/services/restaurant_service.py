from app.models.data_helper import read_data, write_data, generate_id


def register_restaurant(data):
    """Register a new restaurant. Returns (restaurant, status_code)."""
    required = ["name", "category", "location", "contact"]
    for field in required:
        if not data.get(field):
            return {"error": f"Missing required field: {field}"}, 400

    store = read_data("restaurants.json")
    restaurants = store.get("restaurants", [])

    # Check for duplicate name+location (409 Conflict)
    for r in restaurants:
        if r["name"].lower() == data["name"].lower() and r["location"].lower() == data["location"].lower():
            return {"error": "Restaurant already exists at this location"}, 409

    restaurant = {
        "restaurant_id": generate_id(),
        "name": data["name"],
        "category": data["category"],
        "location": data["location"],
        "images": data.get("images", []),
        "contact": data["contact"],
        "status": "pending",   # pending until admin approves
        "enabled": True
    }
    restaurants.append(restaurant)
    store["restaurants"] = restaurants
    write_data("restaurants.json", store)
    return restaurant, 201


def update_restaurant(restaurant_id, data):
    store = read_data("restaurants.json")
    restaurants = store.get("restaurants", [])
    for i, r in enumerate(restaurants):
        if r["restaurant_id"] == restaurant_id:
            updatable = ["name", "category", "location", "images", "contact"]
            for field in updatable:
                if field in data:
                    restaurants[i][field] = data[field]
            store["restaurants"] = restaurants
            write_data("restaurants.json", store)
            return restaurants[i], 200
    return {"error": "Restaurant not found"}, 404


def disable_restaurant(restaurant_id):
    store = read_data("restaurants.json")
    restaurants = store.get("restaurants", [])
    for i, r in enumerate(restaurants):
        if r["restaurant_id"] == restaurant_id:
            restaurants[i]["enabled"] = False
            store["restaurants"] = restaurants
            write_data("restaurants.json", store)
            return {"message": "Restaurant disabled"}, 200
    return {"error": "Restaurant not found"}, 404


def get_restaurant(restaurant_id):
    store = read_data("restaurants.json")
    for r in store.get("restaurants", []):
        if r["restaurant_id"] == restaurant_id:
            return r, 200
    return {"error": "Restaurant not found"}, 404


def search_restaurants(name=None, location=None, dish=None, rating=None):
    store = read_data("restaurants.json")
    results = store.get("restaurants", [])

    if name:
        results = [r for r in results if name.lower() in r["name"].lower()]
    if location:
        results = [r for r in results if location.lower() in r["location"].lower()]
    if dish:
        dish_store = read_data("dishes.json")
        matching_rest_ids = {
            d["restaurant_id"] for d in dish_store.get("dishes", [])
            if dish.lower() in d["name"].lower()
        }
        results = [r for r in results if r["restaurant_id"] in matching_rest_ids]

    return results, 200
