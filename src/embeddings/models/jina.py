import os

import requests
from dotenv import load_dotenv


load_dotenv()

JINA_API_URL = "https://api.jina.ai/v1/embeddings"
JINA_MODEL = "jina-embeddings-v5-text-nano"


def embed_text(text: str) -> list[float]:
    api_key = os.getenv("JINA_API_KEY")

    if not api_key:
        raise RuntimeError("JINA_API_KEY is not set")

    response = requests.post(
        JINA_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": JINA_MODEL,
            "input": [text],
        },
    )

    response.raise_for_status()

    result = response.json()

    return result["data"][0]["embedding"]