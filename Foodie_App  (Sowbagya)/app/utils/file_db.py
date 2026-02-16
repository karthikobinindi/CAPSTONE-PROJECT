import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def read_json(filename):
    filepath = os.path.join(DATA_DIR, filename)

    if not os.path.exists(filepath):
        return []

    with open(filepath, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def write_json(filename, data):
    filepath = os.path.join(DATA_DIR, filename)

    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


def generate_id(data_list):
    if not data_list:
        return 1
    return max(item["id"] for item in data_list) + 1
