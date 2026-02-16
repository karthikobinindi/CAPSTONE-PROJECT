from flask import Blueprint, request, jsonify
from app.utils.file_db import read_json, write_json, generate_id

rating_bp = Blueprint("rating_bp", __name__, url_prefix="/api/v1/ratings")


# 16 Give Rating
# POST /api/v1/ratings
@rating_bp.route("", methods=["POST"])
def give_rating():
    ratings = read_json("ratings.json")
    orders = read_json("orders.json")

    data = request.json

    if not data or not data.get("order_id") or data.get("rating") is None:
        return jsonify({"error": "order_id and rating required"}), 400

    order_found = False
    for o in orders:
        if o["id"] == data["order_id"]:
            order_found = True
            break

    if not order_found:
        return jsonify({"error": "Order not found"}), 400

    new_rating = {
        "id": generate_id(ratings),
        "order_id": data["order_id"],
        "rating": data["rating"],
        "comment": data.get("comment", "")
    }

    ratings.append(new_rating)
    write_json("ratings.json", ratings)

    return jsonify(new_rating), 201
