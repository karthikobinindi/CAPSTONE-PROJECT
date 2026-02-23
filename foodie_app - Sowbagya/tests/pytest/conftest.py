import pytest
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../"))

from app import create_app

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True

    # Backup original data
    backups = {}
    for fname in ["restaurants.json", "dishes.json", "users.json", "orders.json", "ratings.json"]:
        path = os.path.join(DATA_DIR, fname)
        with open(path) as f:
            backups[fname] = json.load(f)

    with app.test_client() as c:
        yield c

    # Restore original data
    for fname, data in backups.items():
        with open(os.path.join(DATA_DIR, fname), "w") as f:
            json.dump(data, f, indent=2)