import json
import os


def load_memory(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []


def save_memory(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
