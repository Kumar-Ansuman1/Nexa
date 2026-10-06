from src.analysis.registry import AnalysisToolRegistry
from src.analysis.schemas.tool import AnalysisTool
from src.jev.client import ask_jev
from src.jev.schemas.analysis_selection import AnalysisToolSelection


ANALYSIS_TOOL_SELECTION_THRESHOLD = 0.50


def _build_tool_options(
    tools: list[AnalysisTool],
) -> dict[str, dict]:
    """
    Convert registered analysis tools into the representation
    exposed to JEV.
    """

    return {
        tool.name: {
            "description": tool.description,
            "required_semantics": tool.required_semantics,
            "argument_schema": tool.argument_schema,
            "evidence_type": tool.evidence_type,
        }
        for tool in tools
    }


def _build_analysis_questions(
    tools: list[AnalysisTool],
) -> dict[str, dict]:
    """
    Build one independent Noul question for every
    registered analysis tool.
    """

    questions = {}

    for tool in tools:
        questions[tool.name] = {
            "type": "noul",
            "instructions": (
                f"Is the {tool.name} analysis tool required "
                "to answer the user's question?"
            ),
            "criteria": {
                "true": (
                    f"The user's question requires the analysis "
                    f"performed by {tool.name}. "
                    f"Tool description: {tool.description}"
                ),
                "false": (
                    f"The user's question does not require the "
                    f"analysis performed by {tool.name}."
                ),
            },
        }

    return questions


def select_analysis_tools(
    query: str,
    tool_registry: AnalysisToolRegistry,
) -> AnalysisToolSelection:
    """
    Ask JEV to independently evaluate every registered
    analysis tool and select all tools whose Noul score
    meets the configured selection threshold.

    JEV only selects the tools.
    It does not execute them.
    """

    if not isinstance(query, str) or not query.strip():
        raise ValueError(
            "query must be a non-empty string."
        )

    available_tools = tool_registry.list_tools()

    if not available_tools:
        raise ValueError(
            "No analysis tools are registered."
        )

    tool_options = _build_tool_options(
        available_tools
    )

    state = {
        "query": query,
        "analysis_tools": tool_options,
    }

    questions = _build_analysis_questions(
        available_tools
    )

    result = ask_jev(
        state=state,
        questions=questions,
    )

    answers = result.get("answers")

    if not isinstance(answers, dict):
        raise ValueError(
            "JEV response does not contain valid analysis answers."
        )

    selected_tools: list[str] = []

    for tool in available_tools:
        answer = answers.get(tool.name)

        if not isinstance(answer, dict):
            continue

        score = answer.get("noul")

        if not isinstance(score, (int, float)):
            continue

        if score >= ANALYSIS_TOOL_SELECTION_THRESHOLD:
            selected_tools.append(tool.name)

    if not selected_tools:
        raise ValueError(
            "JEV did not select any analysis tools above "
            f"the threshold of "
            f"{ANALYSIS_TOOL_SELECTION_THRESHOLD}."
        )

    return AnalysisToolSelection(
        tool_names=selected_tools,
    )