from openai import OpenAI
import json
import os

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

BOOKS = [
    {
        "name": "Principles of Mathematical Analysis",
        "author": "Walter Rudin",
        "keywords": ["real analysis", "rudin", "analysis"],
        "link": "PDF_LINK"
    },
    {
        "name": "Linear Algebra Done Right",
        "author": "Sheldon Axler",
        "keywords": ["linear algebra", "vector", "matrix"],
        "link": "PDF_LINK"
    }
]

def get_embedding(text):
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return res.data[0].embedding

for book in BOOKS:
    text = f"{book['name']} {book['author']} {' '.join(book['keywords'])}"
    book["embedding"] = get_embedding(text)
    print(f"Embedded: {book['name']}")

with open("books_with_embeddings.json", "w") as f:
    json.dump(BOOKS, f)

print("DONE ✅")
