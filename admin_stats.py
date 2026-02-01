import requests, os

def get_stats():
    try:
        r = requests.get(os.getenv("SHEET_URL"), timeout=5)
        return r.json()
    except:
        return {}
