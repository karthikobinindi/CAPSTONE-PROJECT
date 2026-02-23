from flask import Blueprint, request, jsonify
from app.services.dish_service import add_dish, update_dish, set_dish_status, delete_dish

dish_bp = Blueprint("dish", __name__)


@dish_bp.route("/api/v1/restaurants/<restaurant_id>/dishes", methods=["POST"])
def add(restaurant_id):
    data = request.get_json()
    result, status = add_dish(restaurant_id, data)
    return jsonify(result), status


@dish_bp.route("/api/v1/dishes/<dish_id>", methods=["PUT"])
def update(dish_id):
    data = request.get_json()
    result, status = update_dish(dish_id, data)
    return jsonify(result), status


@dish_bp.route("/api/v1/dishes/<dish_id>/status", methods=["PUT"])
def status(dish_id):
    data = request.get_json()
    result, code = set_dish_status(dish_id, data)
    return jsonify(result), code


@dish_bp.route("/api/v1/dishes/<dish_id>", methods=["DELETE"])
def delete(dish_id):
    result, status = delete_dish(dish_id)
    return jsonify(result), status
