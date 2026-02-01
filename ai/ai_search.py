from difflib import SequenceMatcher
from books.books import BOOKS

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def smart_search(query):
    query = query.lower()
    results = []

    for book in BOOKS:
        text = f"{book['name']} {book['author']} {' '.join(book['keywords'])}".lower()
        score = similarity(query, text)

        if score > 0.45 or query in text:
            results.append((score, book))

    results.sort(reverse=True, key=lambda x: x[0])
    return [b for _, b in results[:5]]
