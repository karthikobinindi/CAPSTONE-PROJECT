from flask import Blueprint, request, jsonify
from app.services.user_service import register_user, get_user, get_orders_by_user

user_bp = Blueprint("user", __name__)


@user_bp.route("/api/v1/users/register", methods=["POST"])
def register():
    data = request.get_json()
    result, status = register_user(data)
    return jsonify(result), status


@user_bp.route("/api/v1/users/<user_id>", methods=["GET"])
def get(user_id):
    result, status = get_user(user_id)
    return jsonify(result), status


@user_bp.route("/api/v1/users/<user_id>/orders", methods=["GET"])
def orders(user_id):
    result, status = get_orders_by_user(user_id)
    return jsonify(result), status
