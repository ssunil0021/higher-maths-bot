import requests, os

def get_books():
    url = os.getenv("BOOKS_SHEET_URL")
    print("URL FROM ENV =", url)

    if not url:
        print("❌ URL is None")
        return []

    try:
        r = requests.get(url, timeout=10)
        print("STATUS =", r.status_code)
        print("TEXT (first 300 chars) =", r.text[:300])

        data = r.json()
        print("TYPE =", type(data))
        print("LEN =", len(data) if isinstance(data, list) else "not list")

        return data if isinstance(data, list) else []

    except Exception as e:
        print("❌ EXCEPTION =", e)
        return []
