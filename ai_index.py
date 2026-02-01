import openai, os
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text):
    return openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    ).data[0].embedding
