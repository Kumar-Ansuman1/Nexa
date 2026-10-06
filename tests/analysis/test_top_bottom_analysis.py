from src.analysis.tools.top_bottom_analysis import (
    top_bottom_analysis,
)


def test_top_bottom_analysis():
    rows = [
        {"country": "India", "revenue": 50019.0},
        {"country": "United States", "revenue": 32355.0},
        {"country": "Canada", "revenue": 8157.0},
        {"country": "Germany", "revenue": 7722.0},
        {"country": "Australia", "revenue": 6990.0},
        {"country": "Singapore", "revenue": 3800.0},
    ]

    result = top_bottom_analysis(
        rows=rows,
        metric="revenue",
        dimension="country",
        limit=2,
    )

    print("\n" + "=" * 70)
    print("TOP/BOTTOM ANALYSIS RESULT")
    print("=" * 70)

    print("\nSummary:")
    print(result.summary)

    print("\nTop:")
    for item in result.data["top"]:
        print(item)

    print("\nBottom:")
    for item in result.data["bottom"]:
        print(item)

    print("=" * 70)

    assert result.tool_name == "top_bottom_analysis"

    assert result.data["top"] == [
        {
            "rank": 1,
            "category": "India",
            "value": 50019.0,
        },
        {
            "rank": 2,
            "category": "United States",
            "value": 32355.0,
        },
    ]

    assert result.data["bottom"] == [
        {
            "rank": 1,
            "category": "Singapore",
            "value": 3800.0,
        },
        {
            "rank": 2,
            "category": "Australia",
            "value": 6990.0,
        },
    ]

    assert result.data["limit"] == 2

    assert result.source_columns == [
        "country",
        "revenue",
    ]

    assert result.row_count == 6

    print("TEST PASSED")


if __name__ == "__main__":
    test_top_bottom_analysis()