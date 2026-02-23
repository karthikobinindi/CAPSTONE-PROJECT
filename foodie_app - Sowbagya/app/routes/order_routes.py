from flask import Blueprint, request, jsonify
from app.services.order_service import (
    place_order, get_orders_by_restaurant, get_orders_by_user
)

order_bp = Blueprint("order", __name__)


@order_bp.route("/api/v1/orders", methods=["POST"])
def place():
    data = request.get_json()
    result, status = place_order(data)
    return jsonify(result), status


@order_bp.route("/api/v1/restaurants/<restaurant_id>/orders", methods=["GET"])
def by_restaurant(restaurant_id):
    result, status = get_orders_by_restaurant(restaurant_id)
    return jsonify(result), status


@order_bp.route("/api/v1/users/<user_id>/orders", methods=["GET"])
def by_user(user_id):
    result, status = get_orders_by_user(user_id)
    return jsonify(result), status
