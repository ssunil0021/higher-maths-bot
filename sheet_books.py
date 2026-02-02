# sheet_books.py
import os
import requests

BOOKS_SHEET_URL = os.getenv("BOOKS_SHEET_URL")

_CACHE = {
    "data": [],
    "last_fetch": 0
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
        if row.get("status") != "approved":
            continue

        books.append({
            "id": row.get("book_id", ""),
            "title": row.get("title", ""),
            "author": row.get("author", ""),
            "subject": row.get("subject", ""),
            "topics": row.get("topics", ""),
            "level": row.get("level", ""),
            "exam_tags": row.get("exam_tags", ""),
            "link": row.get("pdf_link", "")
        })

    return books


def get_books():
    import time
    now = time.time()

    if now - _CACHE["last_fetch"] < CACHE_TTL:
        return _CACHE["data"]

    data = load_books()
    _CACHE["data"] = data
    _CACHE["last_fetch"] = now
    return data
