from app.models.data_helper import read_data, write_data, generate_id


def register_user(data):
    required = ["name", "email", "password"]
    for field in required:
        if not data.get(field):
            return {"error": f"Missing required field: {field}"}, 400

    store = read_data("users.json")
    users = store.get("users", [])

    for u in users:
        if u["email"].lower() == data["email"].lower():
            return {"error": "User with this email already exists"}, 409

    user = {
        "user_id": generate_id(),
        "name": data["name"],
        "email": data["email"],
        "password": data["password"]   # NOTE: In production, hash passwords!
    }
    users.append(user)
    store["users"] = users
    write_data("users.json", store)

    # Return without password
    safe_user = {k: v for k, v in user.items() if k != "password"}
    return safe_user, 201


def get_user(user_id):
    store = read_data("users.json")
    for u in store.get("users", []):
        if u["user_id"] == user_id:
            safe_user = {k: v for k, v in u.items() if k != "password"}
            return safe_user, 200
    return {"error": "User not found"}, 404


def get_orders_by_user(user_id):
    store = read_data("orders.json")
    orders = [o for o in store.get("orders", []) if o["user_id"] == user_id]
    return orders, 200
