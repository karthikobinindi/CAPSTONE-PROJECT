from flask import Blueprint, request, jsonify
from app.utils.file_db import read_json, write_json, generate_id

restaurant_bp = Blueprint("restaurant_bp", __name__, url_prefix="/api/v1/restaurants")


# 1 Register Restaurant
# POST /api/v1/restaurants
@restaurant_bp.route("", methods=["POST"])
def register_restaurant():
    restaurants = read_json("restaurants.json")
    data = request.json

    if not data or not data.get("name"):
        return jsonify({"error": "name is required"}), 400

    for r in restaurants:
        if r["name"].lower() == data["name"].lower():
            return jsonify({"error": "Restaurant already exists"}), 409

    new_restaurant = {
        "id": generate_id(restaurants),
        "name": data["name"],
        "category": data.get("category", ""),
        "location": data.get("location", ""),
        "contact": data.get("contact", ""),
        "is_active": True,
        "is_approved": False
    }

    restaurants.append(new_restaurant)
    write_json("restaurants.json", restaurants)

    return jsonify(new_restaurant), 201


# 2 Update Restaurant Details
# PUT /api/v1/restaurants/{restaurant_id}
@restaurant_bp.route("/<int:restaurant_id>", methods=["PUT"])
def update_restaurant_details(restaurant_id):
    restaurants = read_json("restaurants.json")
    data = request.json

    for r in restaurants:
        if r["id"] == restaurant_id:
            r["name"] = data.get("name", r["name"])
            r["category"] = data.get("category", r["category"])
            r["location"] = data.get("location", r["location"])
            r["contact"] = data.get("contact", r["contact"])

            write_json("restaurants.json", restaurants)
            return jsonify(r), 200

    return jsonify({"error": "Restaurant not found"}), 404


# 3 Disable Restaurant
# PUT /api/v1/restaurants/{restaurant_id}/disable
@restaurant_bp.route("/<int:restaurant_id>/disable", methods=["PUT"])
def disable_restaurant(restaurant_id):
    restaurants = read_json("restaurants.json")

    for r in restaurants:
        if r["id"] == restaurant_id:
            r["is_active"] = False
            write_json("restaurants.json", restaurants)
            return jsonify({"message": "Restaurant disabled"}), 200

    return jsonify({"error": "Restaurant not found"}), 404


# 4 View Restaurant Profile
# GET /api/v1/restaurants/{restaurant_id}
@restaurant_bp.route("/<int:restaurant_id>", methods=["GET"])
def view_restaurant_profile(restaurant_id):
    restaurants = read_json("restaurants.json")

    for r in restaurants:
        if r["id"] == restaurant_id:
            return jsonify(r), 200

    return jsonify({"error": "Restaurant not found"}), 404


# 14 Search Restaurants
# GET /api/v1/restaurants/search?name=&location=&dish=&rating=
@restaurant_bp.route("/search", methods=["GET"])
def search_restaurants():
    restaurants = read_json("restaurants.json")
    dishes = read_json("dishes.json")
    orders = read_json("orders.json")
    ratings = read_json("ratings.json")

    name = request.args.get("name")
    location = request.args.get("location")
    dish = request.args.get("dish")
    rating = request.args.get("rating")

    result = []

    for r in restaurants:
        if not r["is_active"] or not r["is_approved"]:
            continue

        if name and name.lower() not in r["name"].lower():
            continue

        if location and location.lower() not in r["location"].lower():
            continue

        # dish filter
        if dish:
            found_dish = False
            for d in dishes:
                if d["restaurant_id"] == r["id"] and dish.lower() in d["name"].lower() and d["enabled"]:
                    found_dish = True
                    break
            if not found_dish:
                continue

        # rating filter
        if rating:
            try:
                rating_val = float(rating)
            except:
                rating_val = None

            if rating_val is not None:
                order_ids = [o["id"] for o in orders if o["restaurant_id"] == r["id"]]
                rest_ratings = [rt["rating"] for rt in ratings if rt["order_id"] in order_ids]

                if not rest_ratings:
                    continue

                avg_rating = sum(rest_ratings) / len(rest_ratings)
                if avg_rating < rating_val:
                    continue

        result.append(r)

    return jsonify(result), 200
