from flask import Blueprint, request, jsonify
from app.utils.file_db import read_json, write_json, generate_id

user_bp = Blueprint("user_bp", __name__, url_prefix="/api/v1/users")


# 13 User Registration
# POST /api/v1/users/register
@user_bp.route("/register", methods=["POST"])
def user_registration():
    users = read_json("users.json")
    data = request.json

    if not data or not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "name, email, password required"}), 400

    for u in users:
        if u["email"].lower() == data["email"].lower():
            return jsonify({"error": "User already exists"}), 409

    new_user = {
        "id": generate_id(users),
        "name": data["name"],
        "email": data["email"],
        "password": data["password"]
    }

    users.append(new_user)
    write_json("users.json", users)

    return jsonify({
        "id": new_user["id"],
        "name": new_user["name"],
        "email": new_user["email"]
    }), 201
