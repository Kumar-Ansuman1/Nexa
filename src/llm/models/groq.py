import os
import re
import time
from typing import TypeVar

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from pydantic import BaseModel

from src.llm.base import LLMProvider


load_dotenv()


T = TypeVar("T", bound=BaseModel)


class GroqModel(LLMProvider):

    def __init__(
        self,
        model_name: str = "openai/gpt-oss-120b",
        max_retries: int = 5,
        base_retry_delay: float = 2.0,
        max_retry_delay: float = 30.0,
    ):
        self.model = ChatGroq(
            model=model_name,
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0,
        )

        self.max_retries = max_retries
        self.base_retry_delay = base_retry_delay
        self.max_retry_delay = max_retry_delay

    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:

        structured_model = self.model.with_structured_output(
            response_model,
            method="json_schema",
        )

        for attempt in range(self.max_retries + 1):

            try:
                response = structured_model.invoke(prompt)

                return response

            except Exception as exc:

                if not self._is_rate_limit_error(exc):
                    raise

                if attempt >= self.max_retries:
                    raise

                retry_delay = self._get_retry_delay(
                    exc=exc,
                    attempt=attempt,
                )

                print(
                    f"Groq rate limit reached. "
                    f"Retrying in {retry_delay:.1f} seconds "
                    f"(attempt {attempt + 1}/{self.max_retries})..."
                )

                time.sleep(retry_delay)

        raise RuntimeError(
            "Groq request failed after all retry attempts."
        )

    def _is_rate_limit_error(
        self,
        exc: Exception,
    ) -> bool:

        status_code = getattr(
            exc,
            "status_code",
            None,
        )

        if status_code == 429:
            return True

        response = getattr(
            exc,
            "response",
            None,
        )

        response_status_code = getattr(
            response,
            "status_code",
            None,
        )

        if response_status_code == 429:
            return True

        error_message = str(exc).lower()

        return (
            "rate limit" in error_message
            or "rate_limit_exceeded" in error_message
            or "too many requests" in error_message
        )

    def _get_retry_delay(
        self,
        exc: Exception,
        attempt: int,
    ) -> float:

        error_message = str(exc)

        # ----------------------------------------------------
        # Try to extract Groq's suggested retry time.
        #
        # Example:
        # "Please try again in 5.955s"
        # ----------------------------------------------------

        match = re.search(
            r"try again in\s+([\d.]+)\s*s",
            error_message,
            re.IGNORECASE,
        )

        if match:
            retry_delay = float(match.group(1))

            return min(
                retry_delay + 0.5,
                self.max_retry_delay,
            )

        # ----------------------------------------------------
        # Fallback: exponential backoff
        #
        # Attempt 0 → 2s
        # Attempt 1 → 4s
        # Attempt 2 → 8s
        # Attempt 3 → 16s
        # Attempt 4 → 30s
        # ----------------------------------------------------

        retry_delay = self.base_retry_delay * (
            2 ** attempt
        )

        return min(
            retry_delay,
            self.max_retry_delay,
        )