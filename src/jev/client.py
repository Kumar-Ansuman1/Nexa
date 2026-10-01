import os

import requests
from dotenv import load_dotenv


load_dotenv()


OPENROUTER_URL = "https://openrouter.ai/api/alpha/decisions"
JEV_MODEL = "typesafe/jev-1.13"


def ask_jev(
    state: dict,
    questions: dict,
) -> dict:

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": JEV_MODEL,
            "state": state,
            "questions": questions,
        },
    )

    response.raise_for_status()

    return response.json()