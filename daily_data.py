import requests
import os

def get_daily_questions():
    url = os.getenv("DAILY_SHEET_URL")
    if not url:
        return []

    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        return data if isinstance(data, list) else []
    except:
        return []
