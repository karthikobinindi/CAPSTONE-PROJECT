import logging
import random

logger = logging.getLogger(__name__)

def test_give_rating(client):
    rand = random.randint(1000, 9999)

    # Create restaurant
    restaurant = client.post("/api/v1/restaurants", json={
        "name": f"RatingRest_{rand}",
        "category": "Veg",
        "location": "Hyderabad"
    })
    restaurant_id = restaurant.get_json()["id"]

    # Create user
    user = client.post("/api/v1/users/register", json={
        "name": "RatingUser",
        "email": f"user_{rand}@test.com",
        "password": "1234"
    })
    user_id = user.get_json()["user_id"]

    # Place order
    order = client.post("/api/v1/orders", json={
        "user_id": user_id,
        "restaurant_id": restaurant_id
    })
    order_id = order.get_json()["order_id"]

    # Give rating
    rating = client.post("/api/v1/ratings", json={
        "order_id": order_id,
        "rating": 5,
        "comment": "Excellent"
    })

    logger.info(f"Rating Response: {rating.get_json()}")
    assert rating.status_code == 201