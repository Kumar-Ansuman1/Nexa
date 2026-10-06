from src.analysis.tool_registry import build_analysis_tool_registry
from src.jev.analysis.selector import select_analysis_tools


def main():
    tool_registry = build_analysis_tool_registry()

    query = (
        "Is revenue increasing or decreasing over time?"
    )

    selection = select_analysis_tools(
        query=query,
        tool_registry=tool_registry,
    )

    print("\n===== SELECTED ANALYSIS TOOLS =====\n")

    for tool_name in selection.tool_names:
        print(f"- {tool_name}")


if __name__ == "__main__":
    main()