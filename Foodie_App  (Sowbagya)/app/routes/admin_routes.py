from flask import Blueprint, jsonify
from app.utils.file_db import read_json, write_json

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/v1/admin")


# 9 Approve Restaurant
# PUT /api/v1/admin/restaurants/{restaurant_id}/approve
@admin_bp.route("/restaurants/<int:restaurant_id>/approve", methods=["PUT"])
def approve_restaurant(restaurant_id):
    restaurants = read_json("restaurants.json")

    for r in restaurants:
        if r["id"] == restaurant_id:
            r["is_approved"] = True
            write_json("restaurants.json", restaurants)
            return jsonify({"message": "Restaurant approved"}), 200

    return jsonify({"error": "Restaurant not found"}), 404


# 10 Disable Restaurant
# PUT /api/v1/admin/restaurants/{restaurant_id}/disable
@admin_bp.route("/restaurants/<int:restaurant_id>/disable", methods=["PUT"])
def disable_restaurant(restaurant_id):
    restaurants = read_json("restaurants.json")

    for r in restaurants:
        if r["id"] == restaurant_id:
            r["is_active"] = False
            write_json("restaurants.json", restaurants)
            return jsonify({"message": "Restaurant disabled"}), 200

    return jsonify({"error": "Restaurant not found"}), 404


# 11 View Customer Feedback
# GET /api/v1/admin/feedback
@admin_bp.route("/feedback", methods=["GET"])
def view_feedback():
    feedback = read_json("ratings.json")
    return jsonify(feedback), 200


# 12 View Order Status
# GET /api/v1/admin/orders
@admin_bp.route("/orders", methods=["GET"])
def view_orders():
    orders = read_json("orders.json")
    return jsonify(orders), 200
