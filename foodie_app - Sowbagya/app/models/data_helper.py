import json
import os
import uuid

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")


def _get_path(filename):
    return os.path.join(DATA_DIR, filename)


def read_data(filename):
    path = _get_path(filename)
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def write_data(filename, data):
    path = _get_path(filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def generate_id():
    return str(uuid.uuid4())
