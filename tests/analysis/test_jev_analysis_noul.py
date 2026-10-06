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
            "What are the average, median, minimum, and maximum revenue values?"
        ),
        "analysis_tools": tool_options,
    }

    questions = {
        "rank_categories": {
            "type": "noul",
            "instructions": (
                "Is the rank_categories analysis tool required "
                "to answer the user's question?"
            ),
            "criteria": {
                "true": (
                    "The question requires ranking categories "
                    "by a numeric metric, such as finding the "
                    "highest or lowest category."
                ),
                "false": (
                    "The question does not require ranking "
                    "categories by a numeric metric."
                ),
            },
        },
        "calculate_contribution": {
            "type": "noul",
            "instructions": (
                "Is the calculate_contribution analysis tool "
                "required to answer the user's question?"
            ),
            "criteria": {
                "true": (
                    "The question asks for a category's "
                    "contribution or percentage of the total metric."
                ),
                "false": (
                    "The question does not ask for a category's "
                    "contribution or percentage of the total."
                ),
            },
        },
        "detect_outliers": {
            "type": "noul",
            "instructions": (
                "Is the detect_outliers analysis tool required "
                "to answer the user's question?"
            ),
            "criteria": {
                "true": (
                    "The question asks whether there are unusual, "
                    "abnormal, or statistically outlying values."
                ),
                "false": (
                    "The question does not ask for unusual or "
                    "statistically outlying values."
                ),
            },
        },
        "descriptive_statistics": {
            "type": "noul",
            "instructions": (
                "Is the descriptive_statistics analysis tool "
                "required to answer the user's question?"
            ),
            "criteria": {
                "true": (
                    "The question asks for descriptive statistics "
                    "such as count, sum, average, median, minimum, "
                    "or maximum of a numeric metric."
                ),
                "false": (
                    "The question does not require descriptive "
                    "statistics."
                ),
            },
        },
    }

    result = ask_jev(
        state=state,
        questions=questions,
    )

    print("\n===== RAW JEV NOUL RESPONSE =====\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()