from app.models.data_helper import read_data, write_data, generate_id


def add_dish(restaurant_id, data):
    required = ["name", "type", "price"]
    for field in required:
        if field not in data or data[field] == "" or data[field] is None:
            return {"error": f"Missing required field: {field}"}, 400

    if float(data["price"]) <= 0:
        return {"error": "Price must be greater than 0"}, 400

    # Verify restaurant exists
    rest_store = read_data("restaurants.json")
    rest_ids = [r["restaurant_id"] for r in rest_store.get("restaurants", [])]
    if restaurant_id not in rest_ids:
        return {"error": "Restaurant not found"}, 404

    store = read_data("dishes.json")
    dishes = store.get("dishes", [])

    dish = {
        "dish_id": generate_id(),
        "restaurant_id": restaurant_id,
        "name": data["name"],
        "type": data["type"],
        "price": float(data["price"]),
        "available_time": data.get("available_time", ""),
        "image": data.get("image", ""),
        "enabled": True
    }
    dishes.append(dish)
    store["dishes"] = dishes
    write_data("dishes.json", store)
    return dish, 201


def update_dish(dish_id, data):
    store = read_data("dishes.json")
    dishes = store.get("dishes", [])
    for i, d in enumerate(dishes):
        if d["dish_id"] == dish_id:
            updatable = ["name", "type", "price", "available_time", "image"]
            for field in updatable:
                if field in data:
                    dishes[i][field] = data[field]
            store["dishes"] = dishes
            write_data("dishes.json", store)
            return dishes[i], 200
    return {"error": "Dish not found"}, 404


def set_dish_status(dish_id, data):
    if "enabled" not in data:
        return {"error": "Missing field: enabled"}, 400

    store = read_data("dishes.json")
    dishes = store.get("dishes", [])
    for i, d in enumerate(dishes):
        if d["dish_id"] == dish_id:
            dishes[i]["enabled"] = bool(data["enabled"])
            store["dishes"] = dishes
            write_data("dishes.json", store)
            status_str = "enabled" if dishes[i]["enabled"] else "disabled"
            return {"message": f"Dish {status_str}"}, 200
    return {"error": "Dish not found"}, 404


def delete_dish(dish_id):
    store = read_data("dishes.json")
    dishes = store.get("dishes", [])
    for i, d in enumerate(dishes):
        if d["dish_id"] == dish_id:
            dishes.pop(i)
            store["dishes"] = dishes
            write_data("dishes.json", store)
            return {"message": "Dish deleted"}, 200
    return {"error": "Dish not found"}, 404


def get_dishes_by_restaurant(restaurant_id):
    store = read_data("dishes.json")
    return [d for d in store.get("dishes", []) if d["restaurant_id"] == restaurant_id], 200
