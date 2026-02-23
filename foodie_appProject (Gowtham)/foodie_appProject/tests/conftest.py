import pytest
import logging
import sys
import os
from app import create_app
from extensions import db

# ===============================
# Reports folder
# ===============================
os.makedirs("reports", exist_ok=True)

# ===============================
# Logging Configuration (UTF-8 Safe)
# ===============================
logger = logging.getLogger()
logger.setLevel(logging.INFO)

if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

file_handler = logging.FileHandler("reports/pytest.log", encoding="utf-8")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ===============================
# Flask App Fixture
# ===============================
@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

# ===============================
# Client Fixture
# ===============================
@pytest.fixture
def client(app):
    return app.test_client()