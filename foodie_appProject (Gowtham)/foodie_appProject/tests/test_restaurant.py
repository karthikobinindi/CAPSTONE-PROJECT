import random
import logging

logger = logging.getLogger(__name__)

def test_register_restaurant(client):
    rand = random.randint(1000, 9999)

    payload = {
        "name": f"Restaurant_{rand}",
        "category": "Veg",
        "location": "Hyderabad"
    }

    logger.info("Creating restaurant")
    response = client.post("/api/v1/restaurants", json=payload)

    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {response.get_json()}")

    assert response.status_code == 201