from flask import Blueprint, request, jsonify
from app.utils.file_db import read_json, write_json, generate_id

dish_bp = Blueprint("dish_bp", __name__, url_prefix="/api/v1")


# 5 Add Dish
# POST /api/v1/restaurants/{restaurant_id}/dishes
@dish_bp.route("/restaurants/<int:restaurant_id>/dishes", methods=["POST"])
def add_dish(restaurant_id):
    dishes = read_json("dishes.json")
    data = request.json

    if not data or not data.get("name") or data.get("price") is None:
        return jsonify({"error": "name and price are required"}), 400

    new_dish = {
        "id": generate_id(dishes),
        "restaurant_id": restaurant_id,
        "name": data["name"],
        "type": data.get("type", ""),
        "price": data["price"],
        "available_time": data.get("available_time", ""),
        "enabled": True
    }

    dishes.append(new_dish)
    write_json("dishes.json", dishes)

    return jsonify(new_dish), 201


# 6 Update Dish
# PUT /api/v1/dishes/{dish_id}
@dish_bp.route("/dishes/<int:dish_id>", methods=["PUT"])
def update_dish(dish_id):
    dishes = read_json("dishes.json")
    data = request.json

    for d in dishes:
        if d["id"] == dish_id:
            d["name"] = data.get("name", d["name"])
            d["type"] = data.get("type", d["type"])
            d["price"] = data.get("price", d["price"])
            d["available_time"] = data.get("available_time", d["available_time"])


            write_json("dishes.json", dishes)
            return jsonify(d), 200

    return jsonify({"error": "Dish not found"}), 404


# 7 Enable / Disable Dish
# PUT /api/v1/dishes/{dish_id}/status
@dish_bp.route("/dishes/<int:dish_id>/status", methods=["PUT"])
def dish_status(dish_id):
    dishes = read_json("dishes.json")
    data = request.json

    if not data or "enabled" not in data:
        return jsonify({"error": "enabled field required"}), 400

    for d in dishes:
        if d["id"] == dish_id:
            d["enabled"] = data["enabled"]
            write_json("dishes.json", dishes)
            return jsonify({"message": "Dish status updated"}), 200

    return jsonify({"error": "Dish not found"}), 404


# 8 Delete Dish
# DELETE /api/v1/dishes/{dish_id}
@dish_bp.route("/dishes/<int:dish_id>", methods=["DELETE"])
def delete_dish(dish_id):
    dishes = read_json("dishes.json")

    for d in dishes:
        if d["id"] == dish_id:
            dishes.remove(d)
            write_json("dishes.json", dishes)
            return jsonify({"message": "Dish deleted"}), 200

    return jsonify({"error": "Dish not found"}), 404
