from src.analysis.tools.percentage_change_analysis import (
    percentage_change_analysis,
)


def test_percentage_change_analysis():
    # Deliberately shuffled.
    rows = [
        {
            "month": "March 2026",
            "revenue": 1500.0,
        },
        {
            "month": "January 2026",
            "revenue": 1000.0,
        },
        {
            "month": "February 2026",
            "revenue": 1200.0,
        },
    ]

    result = percentage_change_analysis(
        rows=rows,
        metric="revenue",
        dimension="month",
    )

    print("\n" + "=" * 70)
    print("PERCENTAGE CHANGE ANALYSIS RESULT")
    print("=" * 70)

    print("\nSummary:")
    print(result.summary)

    print("\nOrdered periods:")
    print(result.data["ordered_periods"])

    print("\nChanges:")

    for change in result.data["changes"]:
        print(change)

    print("\nLargest increase:")
    print(result.data["largest_increase"])

    print("\nLargest decrease:")
    print(result.data["largest_decrease"])

    print("=" * 70)

    assert result.tool_name == (
        "percentage_change_analysis"
    )

    assert result.data["ordered_periods"] == [
        "January 2026",
        "February 2026",
        "March 2026",
    ]

    changes = result.data["changes"]

    assert changes[0]["from"] == "January 2026"
    assert changes[0]["to"] == "February 2026"
    assert changes[0]["absolute_change"] == 200.0
    assert changes[0]["percentage_change"] == 20.0
    assert changes[0]["direction"] == "increasing"

    assert changes[1]["from"] == "February 2026"
    assert changes[1]["to"] == "March 2026"
    assert changes[1]["absolute_change"] == 300.0
    assert changes[1]["percentage_change"] == 25.0
    assert changes[1]["direction"] == "increasing"

    assert (
        result.data["largest_increase"]["percentage_change"]
        == 25.0
    )

    assert result.row_count == 3

    print("TEST PASSED")


if __name__ == "__main__":
    test_percentage_change_analysis()