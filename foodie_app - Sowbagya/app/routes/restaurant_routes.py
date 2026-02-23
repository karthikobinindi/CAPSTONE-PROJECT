from flask import Blueprint, request, jsonify
from app.services.restaurant_service import (
    register_restaurant, update_restaurant, disable_restaurant,
    get_restaurant, search_restaurants
)

restaurant_bp = Blueprint("restaurant", __name__)


@restaurant_bp.route("/api/v1/restaurants", methods=["POST"])
def register():
    data = request.get_json()
    result, status = register_restaurant(data)
    return jsonify(result), status


@restaurant_bp.route("/api/v1/restaurants/<restaurant_id>", methods=["PUT"])
def update(restaurant_id):
    data = request.get_json()
    result, status = update_restaurant(restaurant_id, data)
    return jsonify(result), status


@restaurant_bp.route("/api/v1/restaurants/<restaurant_id>/disable", methods=["PUT"])
def disable(restaurant_id):
    result, status = disable_restaurant(restaurant_id)
    return jsonify(result), status


@restaurant_bp.route("/api/v1/restaurants/<restaurant_id>", methods=["GET"])
def get(restaurant_id):
    result, status = get_restaurant(restaurant_id)
    return jsonify(result), status


@restaurant_bp.route("/api/v1/restaurants/search", methods=["GET"])
def search():
    name = request.args.get("name")
    location = request.args.get("location")
    dish = request.args.get("dish")
    rating = request.args.get("rating")
    result, status = search_restaurants(name, location, dish, rating)
    return jsonify(result), status
