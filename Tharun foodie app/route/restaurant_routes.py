from flask import Blueprint, request, jsonify
import uuid
from models import restaurants, orders

restaurant_bp = Blueprint("restaurant", __name__, url_prefix="/api/v1/restaurants")

# 1 Register Restaurant
@restaurant_bp.route("", methods=["POST"])
def register_restaurant():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Name required"}), 400

    for r in restaurants.values():
        if r["name"] == data["name"]:
            return jsonify({"error": "Restaurant already exists"}), 409

    rid = str(uuid.uuid4())

    restaurant = {
        "id": rid,
        "name": data["name"],
        "category": data.get("category", ""),
        "location": data.get("location", ""),
        "contact": data.get("contact", ""),
        "approved": False,
        "enabled": True
    }

    restaurants[rid] = restaurant
    return jsonify(restaurant), 201


# 2 Update Restaurant
@restaurant_bp.route("/<rid>", methods=["PUT"])
def update_restaurant(rid):
    if rid not in restaurants:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    restaurants[rid].update(data)
    return jsonify(restaurants[rid]), 200


# 3 Disable Restaurant
@restaurant_bp.route("/<rid>/disable", methods=["PUT"])
def disable_restaurant(rid):
    if rid not in restaurants:
        return jsonify({"error": "Not found"}), 404

    restaurants[rid]["enabled"] = False
    return jsonify({"message": "Restaurant disabled"}), 200


# 4 View Restaurant
@restaurant_bp.route("/<rid>", methods=["GET"])
def view_restaurant(rid):
    if rid not in restaurants:
        return jsonify({"error": "Not found"}), 404

    return jsonify(restaurants[rid]), 200


# 17 View Orders by Restaurant
@restaurant_bp.route("/<rid>/orders", methods=["GET"])
def view_orders_by_restaurant(rid):
    result = [o for o in orders.values() if o["restaurant_id"] == rid]
    return jsonify(result), 200


# 14 Search Restaurants
@restaurant_bp.route("/search", methods=["GET"])
def search_restaurants():
    name = request.args.get("name", "")
    location = request.args.get("location", "")

    result = [
        r for r in restaurants.values()
        if name.lower() in r["name"].lower()
        and location.lower() in r["location"].lower()
    ]
    return jsonify(result), 200