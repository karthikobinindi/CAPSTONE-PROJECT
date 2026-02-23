import logging

logger = logging.getLogger(__name__)

def test_admin_feedback(client):
    logger.info("Fetching admin feedback")

    response = client.get("/api/v1/admin/feedback")

    logger.info(f"Admin Feedback Response: {response.get_json()}")
    assert response.status_code == 200