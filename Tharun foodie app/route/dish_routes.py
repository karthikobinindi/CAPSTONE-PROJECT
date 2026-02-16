from flask import Blueprint, request, jsonify
import uuid
from models import dishes, restaurants

dish_bp = Blueprint("dish", __name__)

# 5 Add Dish
@dish_bp.route("/api/v1/restaurants/<rid>/dishes", methods=["POST"])
def add_dish(rid):
    if rid not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404

    data = request.get_json()
    did = str(uuid.uuid4())

    dish = {
        "id": did,
        "restaurant_id": rid,
        "name": data["name"],
        "type": data.get("type", ""),
        "price": data.get("price", 0),
        "enabled": True
    }

    dishes[did] = dish
    return jsonify(dish), 201


# 6 Update Dish
@dish_bp.route("/api/v1/dishes/<did>", methods=["PUT"])
def update_dish(did):
    if did not in dishes:
        return jsonify({"error": "Not found"}), 404

    dishes[did].update(request.get_json())
    return jsonify(dishes[did]), 200


# 7 Enable/Disable Dish
@dish_bp.route("/api/v1/dishes/<did>/status", methods=["PUT"])
def update_dish_status(did):
    if did not in dishes:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    dishes[did]["enabled"] = data.get("enabled", True)
    return jsonify({"message": "Status updated"}), 200


# 8 Delete Dish
@dish_bp.route("/api/v1/dishes/<did>", methods=["DELETE"])
def delete_dish(did):
    if did not in dishes:
        return jsonify({"error": "Not found"}), 404

    del dishes[did]
    return jsonify({"message": "Dish deleted"}), 200