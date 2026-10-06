from src.analysis.tool_registry import (
    build_analysis_tool_registry,
)


def test_analysis_tool_registry():

    registry = build_analysis_tool_registry()

    expected_tools = {
        "rank_categories",
        "compare_groups",
        "calculate_contribution",
        "descriptive_statistics",
        "distribution_statistics",
        "analyze_trend",
        "calculate_change",
        "detect_outliers",
        "correlation_analysis",
        "group_statistics",
        "top_bottom_analysis",
        "percentage_change_analysis",
        "share_distribution",
        "frequency_analysis",
    }

    registered_tools = {
        tool.name
        for tool in registry.list_tools()
    }

    assert registered_tools == expected_tools

    assert len(registered_tools) == 14

    for tool_name in expected_tools:
        assert registry.has(tool_name)
        assert registry.get(tool_name).definition.name == tool_name


if __name__ == "__main__":
    test_analysis_tool_registry()
    print("analysis tool registry test passed.")