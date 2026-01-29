import requests
import os

def get_total_users():
    url = os.getenv("SHEET_URL")
    if not url:
        return "SHEET_URL missing"

    try:
        r = requests.get(url, timeout=5)
        return r.json().get("total", 0)
    except Exception as e:
        return str(e)
