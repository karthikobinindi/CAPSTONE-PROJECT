import logging
import random

logger = logging.getLogger(__name__)

def test_place_order(client):
    rand = random.randint(1000, 9999)

    # Create restaurant
    restaurant = client.post("/api/v1/restaurants", json={
        "name": f"OrderRest_{rand}",
        "category": "Veg",
        "location": "Hyderabad"
    })
    restaurant_id = restaurant.get_json()["id"]

    # Create user
    user = client.post("/api/v1/users/register", json={
        "name": "OrderUser",
        "email": f"user_{rand}@test.com",
        "password": "1234"
    })
    user_id = user.get_json()["user_id"]

    # Place order
    order = client.post("/api/v1/orders", json={
        "user_id": user_id,
        "restaurant_id": restaurant_id
    })

    logger.info(f"Order Response: {order.get_json()}")
    assert order.status_code == 201