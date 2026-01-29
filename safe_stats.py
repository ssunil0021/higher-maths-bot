import requests
import os

SHEET_URL = os.getenv("SHEET_URL")

def add_user(user):
    if not SHEET_URL:
        return

    payload = {
        "user_id": str(user.id),
        "first_name": user.first_name,
        "username": user.username
    }

    try:
        requests.post(SHEET_URL, json=payload, timeout=2)
    except:
        pass


