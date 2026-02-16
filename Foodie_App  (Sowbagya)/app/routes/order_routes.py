from flask import Blueprint, request, jsonify
from app.utils.file_db import read_json, write_json, generate_id

order_bp = Blueprint("order_bp", __name__, url_prefix="/api/v1")


# 15 Place Order
# POST /api/v1/orders
@order_bp.route("/orders", methods=["POST"])
def place_order():
    orders = read_json("orders.json")
    data = request.json

    if not data or not data.get("user_id") or not data.get("restaurant_id") or not data.get("dishes"):
        return jsonify({"error": "user_id, restaurant_id, dishes required"}), 400

    new_order = {
        "id": generate_id(orders),
        "user_id": data["user_id"],
        "restaurant_id": data["restaurant_id"],
        "dishes": data["dishes"],
        "status": "Pending"
    }

    orders.append(new_order)
    write_json("orders.json", orders)

    return jsonify(new_order), 201


# 17 View Orders by Restaurant
# GET /api/v1/restaurants/{restaurant_id}/orders
@order_bp.route("/restaurants/<int:restaurant_id>/orders", methods=["GET"])
def view_orders_by_restaurant(restaurant_id):
    orders = read_json("orders.json")
    result = [o for o in orders if o["restaurant_id"] == restaurant_id]
    return jsonify(result), 200


# 18 View Orders by User
# GET /api/v1/users/{user_id}/orders
@order_bp.route("/users/<int:user_id>/orders", methods=["GET"])
def view_orders_by_user(user_id):
    orders = read_json("orders.json")
    result = [o for o in orders if o["user_id"] == user_id]
    return jsonify(result), 200
