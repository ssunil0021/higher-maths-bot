import os
import requests

BOOKS_SHEET_URL = os.getenv("https://script.google.com/macros/s/AKfycbweKyQJZ8bJ7FGBlshhDFBQmZCcIc8Qmmy9fze51a8N5LLk22FF3YUFJGp6onhbIth8IA/exec")

_CACHE = {
    "data": [],
    "ts": 0
}

CACHE_TTL = 60  # seconds


def load_books():
    if not BOOKS_SHEET_URL:
        return []

    try:
        r = requests.get(BOOKS_SHEET_URL, timeout=5)
        rows = r.json()
    except:
        return []

    books = []

    for row in rows:
        if row.get("status", "").lower() != "approved":
            continue

        books.append({
            "name": row.get("title", "").strip(),
            "author": row.get("author", "").strip(),
            "subject": row.get("subject", "").strip(),
            "keywords": [
                k.strip().lower()
                for k in (
                    row.get("topics", "") + "," +
                    row.get("exam_tags", "")
                ).split(",")
                if k.strip()
            ],
            "link": row.get("pdf_link", "").strip()
        })

    return books


def get_books():
    import time
    now = time.time()

    if now - _CACHE["ts"] < CACHE_TTL:
        return _CACHE["data"]

    data = load_books()
    _CACHE["data"] = data
    _CACHE["ts"] = now
    return data
