from app.models.data_helper import read_data, write_data, generate_id


def place_order(data):
    required = ["user_id", "restaurant_id", "dishes"]
    for field in required:
        if not data.get(field):
            return {"error": f"Missing required field: {field}"}, 400

    if not isinstance(data["dishes"], list) or len(data["dishes"]) == 0:
        return {"error": "dishes must be a non-empty list"}, 400

    store = read_data("orders.json")
    orders = store.get("orders", [])

    order = {
        "order_id": generate_id(),
        "user_id": data["user_id"],
        "restaurant_id": data["restaurant_id"],
        "dishes": data["dishes"],
        "status": "placed"
    }
    orders.append(order)
    store["orders"] = orders
    write_data("orders.json", store)
    return order, 201


def get_orders_by_restaurant(restaurant_id):
    store = read_data("orders.json")
    orders = [o for o in store.get("orders", []) if o["restaurant_id"] == restaurant_id]
    return orders, 200


def get_orders_by_user(user_id):
    store = read_data("orders.json")
    orders = [o for o in store.get("orders", []) if o["user_id"] == user_id]
    return orders, 200


def give_rating(data):
    required = ["order_id", "rating", "comment"]
    for field in required:
        if field not in data or data[field] == "" or data[field] is None:
            return {"error": f"Missing required field: {field}"}, 400

    rating_val = int(data["rating"])
    if rating_val < 1 or rating_val > 5:
        return {"error": "Rating must be between 1 and 5"}, 400

    store = read_data("ratings.json")
    ratings = store.get("ratings", [])

    rating = {
        "rating_id": generate_id(),
        "order_id": data["order_id"],
        "rating": rating_val,
        "comment": data["comment"]
    }
    ratings.append(rating)
    store["ratings"] = ratings
    write_data("ratings.json", store)
    return rating, 201
