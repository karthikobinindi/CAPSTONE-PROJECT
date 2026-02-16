from flask import Blueprint, request, jsonify
import uuid
from models import users, orders, ratings

user_bp = Blueprint("user", __name__)

# 13 Register User
@user_bp.route("/api/v1/users/register", methods=["POST"])
def register_user():
    data = request.get_json()

    for u in users.values():
        if u["email"] == data["email"]:
            return jsonify({"error": "User exists"}), 409

    uid = str(uuid.uuid4())
    user = {"id": uid, "name": data["name"], "email": data["email"]}
    users[uid] = user
    return jsonify(user), 201


# 15 Place Order
@user_bp.route("/api/v1/orders", methods=["POST"])
def place_order():
    data = request.get_json()
    oid = str(uuid.uuid4())

    order = {
        "id": oid,
        "user_id": data["user_id"],
        "restaurant_id": data["restaurant_id"],
        "dishes": data["dishes"]
    }

    orders[oid] = order
    return jsonify(order), 201


# 16 Give Rating
@user_bp.route("/api/v1/ratings", methods=["POST"])
def give_rating():
    data = request.get_json()
    ratings.append(data)
    return jsonify(data), 201


# 18 View Orders by User
@user_bp.route("/api/v1/users/<uid>/orders", methods=["GET"])
def view_orders_by_user(uid):
    result = [o for o in orders.values() if o["user_id"] == uid]
    return jsonify(result), 200