from flask import Blueprint, request, jsonify
from app.services.order_service import give_rating

rating_bp = Blueprint("rating", __name__)


@rating_bp.route("/api/v1/ratings", methods=["POST"])
def rate():
    data = request.get_json()
    result, status = give_rating(data)
    return jsonify(result), status
