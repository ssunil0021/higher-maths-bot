import requests, os, time

BOOKS_CACHE = []
LAST_FETCH = 0
CACHE_TTL = 300  # 5 minutes

SHEET_URL = os.getenv("https://script.google.com/macros/s/AKfycbyTsGBu0_NRT1xgpKPqIwrTo4HiD6vJCqeQxWKLEU56-tPCngrcM8r8ANS6sATwa2PQIg/exec")

def get_books():
    global BOOKS_CACHE, LAST_FETCH

    if not SHEET_URL:
        return []

    now = time.time()
    if now - LAST_FETCH < CACHE_TTL:
        return BOOKS_CACHE

    try:
        r = requests.get(SHEET_URL, timeout=5)
        data = r.json()

        BOOKS_CACHE = [
            b for b in data
            if str(b.get("status")).lower() == "approved"
        ]
        LAST_FETCH = now
        return BOOKS_CACHE
    except:
        return BOOKS_CACHE
