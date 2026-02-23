import logging
import random

logger = logging.getLogger(__name__)

def test_register_user(client):
    rand = random.randint(1000, 9999)

    payload = {
        "name": "TestUser",
        "email": f"user_{rand}@test.com",
        "password": "1234"
    }

    logger.info("Registering user")
    response = client.post("/api/v1/users/register", json=payload)

    logger.info(f"User Response: {response.get_json()}")
    assert response.status_code == 201