from app.models.data_helper import read_data, write_data


def approve_restaurant(restaurant_id):
    store = read_data("restaurants.json")
    restaurants = store.get("restaurants", [])
    for i, r in enumerate(restaurants):
        if r["restaurant_id"] == restaurant_id:
            restaurants[i]["status"] = "approved"
            store["restaurants"] = restaurants
            write_data("restaurants.json", store)
            return {"message": "Restaurant approved"}, 200
    return {"error": "Restaurant not found"}, 404


def admin_disable_restaurant(restaurant_id):
    store = read_data("restaurants.json")
    restaurants = store.get("restaurants", [])
    for i, r in enumerate(restaurants):
        if r["restaurant_id"] == restaurant_id:
            restaurants[i]["enabled"] = False
            restaurants[i]["status"] = "disabled"
            store["restaurants"] = restaurants
            write_data("restaurants.json", store)
            return {"message": "Restaurant disabled by admin"}, 200
    return {"error": "Restaurant not found"}, 404


def get_all_feedback():
    store = read_data("ratings.json")
    return store.get("ratings", []), 200


def get_all_orders():
    store = read_data("orders.json")
    return store.get("orders", []), 200
