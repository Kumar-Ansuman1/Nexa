import os
from typing import TypeVar

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from pydantic import BaseModel

from src.llm.base import LLMProvider

load_dotenv()

T = TypeVar("T", bound=BaseModel)


class GroqModel(LLMProvider):

    def __init__(self, model_name: str = "openai/gpt-oss-120b"):
        self.model = ChatGroq(
            model=model_name,
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0,
        )

    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:
        structured_model = self.model.with_structured_output(response_model)

        response = structured_model.invoke(prompt)

        return response