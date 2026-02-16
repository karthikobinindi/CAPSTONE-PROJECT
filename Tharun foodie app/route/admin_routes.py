from flask import Blueprint, jsonify
from models import restaurants, orders, ratings

admin_bp = Blueprint("admin", __name__)

# 9 Approve Restaurant
@admin_bp.route("/api/v1/admin/restaurants/<rid>/approve", methods=["PUT"])
def approve_restaurant(rid):
    if rid not in restaurants:
        return jsonify({"error": "Not found"}), 404

    restaurants[rid]["approved"] = True
    return jsonify({"message": "Approved"}), 200


# 10 Disable Restaurant
@admin_bp.route("/api/v1/admin/restaurants/<rid>/disable", methods=["PUT"])
def admin_disable_restaurant(rid):
    if rid not in restaurants:
        return jsonify({"error": "Not found"}), 404

    restaurants[rid]["enabled"] = False
    return jsonify({"message": "Disabled"}), 200


# 11 View Feedback
@admin_bp.route("/api/v1/admin/feedback", methods=["GET"])
def view_feedback():
    return jsonify(ratings), 200


# 12 View Orders
@admin_bp.route("/api/v1/admin/orders", methods=["GET"])
def view_orders():
    return jsonify(list(orders.values())), 200