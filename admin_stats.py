import requests
import os

SHEET_URL = os.getenv("SHEET_URL")

def get_total_users():
    try:
        r = requests.get(SHEET_URL, timeout=5)
        data = r.json()
        return data.get("total", 0)
    except:
        return 0
