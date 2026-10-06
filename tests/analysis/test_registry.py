from src.analysis.tool_registry import (
    build_analysis_tool_registry,
)


def test_analysis_tool_registry():
    registry = build_analysis_tool_registry()

    assert registry.has("rank_categories")

    tool = registry.get("rank_categories")

    print("\n" + "=" * 70)
    print("ANALYSIS TOOL REGISTRY")
    print("=" * 70)

    print("\nTool name:")
    print(tool.definition.name)

    print("\nDescription:")
    print(tool.definition.description)

    print("\nRequired semantics:")
    print(tool.definition.required_semantics)

    print("\nArgument schema:")
    print(tool.definition.argument_schema)

    print("\nEvidence type:")
    print(tool.definition.evidence_type)

    print("=" * 70)

    rows = [
        {
            "country": "Australia",
            "total_revenue": 6990.0,
        },
        {
            "country": "India",
            "total_revenue": 50019.0,
        },
        {
            "country": "United States",
            "total_revenue": 32355.0,
        },
    ]

    result = tool.execute(
        rows=rows,
        metric="total_revenue",
        dimension="country",
        order="descending",
        limit=2,
    )

    assert result.tool_name == "rank_categories"
    assert result.data["ranking"][0]["category"] == "India"
    assert result.data["ranking"][0]["value"] == 50019.0

    assert result.data["ranking"][1]["category"] == "United States"
    assert result.data["ranking"][1]["value"] == 32355.0

    print("\nExecution:")
    print(result.summary)

    print("\nTEST PASSED")


if __name__ == "__main__":
    test_analysis_tool_registry()