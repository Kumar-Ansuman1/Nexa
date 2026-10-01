import os

import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY is not set")


response = requests.post(
    "https://openrouter.ai/api/alpha/decisions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json={
        "model": "typesafe/jev-1.13",
        "state": {
            "query": "Show revenue by subscription plan.",
            "semantic_options": {
                "sem_001": "Transaction amount",
                "sem_002": "Subscription plan",
                "sem_003": "Transaction date",
                "sem_004": "Customer country",
            },
        },
        "questions": {
            "metric": {
                "type": "choice",
                "instructions": (
                    "Which semantic option represents the metric "
                    "the user wants to analyze?"
                ),
                "criteria": {
                    "sem_001": "Transaction amount",
                    "sem_002": "Subscription plan",
                    "sem_003": "Transaction date",
                    "sem_004": "Customer country",
                },
            }
        },
    },
)

response.raise_for_status()

result = response.json()

print(result)