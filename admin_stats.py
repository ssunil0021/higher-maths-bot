import json
import os

FILE = "users.json"

def _load():
    if not os.path.exists(FILE):
        return set()
    with open(FILE, "r") as f:
        return set(json.load(f))

def _save(users):
    with open(FILE, "w") as f:
        json.dump(list(users), f)

def add_user(user_id):
    users = _load()
    users.add(str(user_id))
    _save(users)

def total_users():
    return len(_load())
