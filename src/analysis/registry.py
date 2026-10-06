from collections.abc import Callable
from typing import Any

from src.analysis.schemas.tool import AnalysisTool


class RegisteredAnalysisTool:
    """
    Connects an analysis tool definition with its
    deterministic Python implementation.
    """

    def __init__(
        self,
        definition: AnalysisTool,
        execute: Callable[..., Any],
    ) -> None:
        self.definition = definition
        self.execute = execute


class AnalysisToolRegistry:
    """
    Registry of analysis tools available to NEXA.
    """

    def __init__(self) -> None:
        self._tools: dict[str, RegisteredAnalysisTool] = {}

    def register(
        self,
        definition: AnalysisTool,
        execute: Callable[..., Any],
    ) -> None:
        """
        Register a deterministic analysis tool.
        """

        if definition.name in self._tools:
            raise ValueError(
                f"Analysis tool '{definition.name}' "
                "is already registered."
            )

        self._tools[definition.name] = RegisteredAnalysisTool(
            definition=definition,
            execute=execute,
        )

    def get(
        self,
        name: str,
    ) -> RegisteredAnalysisTool:
        """
        Retrieve a registered analysis tool by name.
        """

        try:
            return self._tools[name]
        except KeyError as exc:
            raise ValueError(
                f"Analysis tool '{name}' is not registered."
            ) from exc

    def list_tools(self) -> list[AnalysisTool]:
        """
        Return the definitions of all registered tools.

        These definitions are what we can later expose to JEV.
        """

        return [
            tool.definition
            for tool in self._tools.values()
        ]

    def has(self, name: str) -> bool:
        """
        Check whether a tool is registered.
        """

        return name in self._tools