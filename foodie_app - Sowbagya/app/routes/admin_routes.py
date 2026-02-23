from flask import Blueprint, jsonify
from app.services.admin_service import (
    approve_restaurant, admin_disable_restaurant,
    get_all_feedback, get_all_orders
)

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/api/v1/admin/restaurants/<restaurant_id>/approve", methods=["PUT"])
def approve(restaurant_id):
    result, status = approve_restaurant(restaurant_id)
    return jsonify(result), status


@admin_bp.route("/api/v1/admin/restaurants/<restaurant_id>/disable", methods=["PUT"])
def disable(restaurant_id):
    result, status = admin_disable_restaurant(restaurant_id)
    return jsonify(result), status


@admin_bp.route("/api/v1/admin/feedback", methods=["GET"])
def feedback():
    result, status = get_all_feedback()
    return jsonify(result), status


@admin_bp.route("/api/v1/admin/orders", methods=["GET"])
def orders():
    result, status = get_all_orders()
    return jsonify(result), status
