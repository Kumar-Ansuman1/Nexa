from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class LLMProvider(ABC):

    @abstractmethod
    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:
        """Generate a structured response from the LLM."""
        raise NotImplementedError