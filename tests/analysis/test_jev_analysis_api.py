import json

from src.analysis.tool_registry import build_analysis_tool_registry
from src.jev.client import ask_jev


def main():
    tool_registry = build_analysis_tool_registry()
    tools = tool_registry.list_tools()

    tool_options = {
        tool.name: {
            "description": tool.description,
            "required_semantics": tool.required_semantics,
            "argument_schema": tool.argument_schema,
            "evidence_type": tool.evidence_type,
        }
        for tool in tools
    }

    state = {
        "query": (
            "Which country has the highest revenue, "
            "what percentage of total revenue does it contribute, "
            "and are there any unusual countries?"
        ),
        "analysis_tools": tool_options,
    }

    questions = {
        "analysis_tools": {
            "type": "choice",
            "multiple": True,
            "instructions": (
                "Select one or more analysis tools required "
                "to answer the user's question. "
                "Do not perform the analysis."
            ),
            "criteria": tool_options,
        }
    }

    result = ask_jev(
        state=state,
        questions=questions,
    )

    print("\n===== RAW JEV RESPONSE =====\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()