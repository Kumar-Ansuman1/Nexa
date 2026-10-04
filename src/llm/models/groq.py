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

        self.model_name = model_name
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

        print(
            f"\n[LLM] Starting Groq request "
            f"using {self.model_name}...",
            flush=True,
        )

        request_start = time.perf_counter()

        for attempt in range(self.max_retries + 1):

            attempt_start = time.perf_counter()

            print(
                f"[LLM] Attempt {attempt + 1}/"
                f"{self.max_retries + 1}",
                flush=True,
            )

            try:
                response = structured_model.invoke(prompt)

                attempt_end = time.perf_counter()
                request_end = time.perf_counter()

                print(
                    f"[LLM] Attempt {attempt + 1} completed in "
                    f"{attempt_end - attempt_start:.3f} seconds",
                    flush=True,
                )

                print(
                    f"[LLM] Total Groq request time: "
                    f"{request_end - request_start:.3f} seconds",
                    flush=True,
                )

                return response

            except Exception as exc:

                attempt_end = time.perf_counter()

                print(
                    f"[LLM] Attempt {attempt + 1} failed after "
                    f"{attempt_end - attempt_start:.3f} seconds",
                    flush=True,
                )

                if not self._is_rate_limit_error(exc):
                    raise

                if attempt >= self.max_retries:
                    raise

                retry_delay = self._get_retry_delay(
                    exc=exc,
                    attempt=attempt,
                )

                print(
                    f"[LLM] Groq rate limit reached. "
                    f"Retrying in {retry_delay:.1f} seconds "
                    f"(attempt {attempt + 1}/"
                    f"{self.max_retries})...",
                    flush=True,
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

        retry_delay = self.base_retry_delay * (
            2 ** attempt
        )

        return min(
            retry_delay,
            self.max_retry_delay,
        )