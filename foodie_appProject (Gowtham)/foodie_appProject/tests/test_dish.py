import logging
import random

logger = logging.getLogger(__name__)

def test_add_dish(client):
    rand = random.randint(1000, 9999)

    restaurant = client.post("/api/v1/restaurants", json={
        "name": f"DishRest_{rand}",
        "category": "Veg",
        "location": "Hyderabad"
    })

    assert restaurant.status_code == 201
    restaurant_id = restaurant.get_json()["id"]

    logger.info(f"Restaurant created with ID: {restaurant_id}")

    dish = client.post(f"/api/v1/restaurants/{restaurant_id}/dishes", json={
        "name": "Paneer Biryani",
        "price": 250
    })

    logger.info(f"Dish Response: {dish.get_json()}")
    assert dish.status_code == 201