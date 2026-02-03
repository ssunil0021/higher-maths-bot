import requests
import os

def get_books():
    url = os.getenv("BOOKS_SHEET_URL")
    if not url:
        return []

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        # only approved books
        if isinstance(data, list):
            return [b for b in data if b.get("status") == "approved"]

        return []

    except:
        return []
