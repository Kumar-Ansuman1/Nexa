from src.analysis.tools.calculate_change import calculate_change


def test_calculate_change():
    rows = [
        {
            "month": "January 2026",
            "revenue": 1000.0,
        },
        {
            "month": "February 2026",
            "revenue": 1200.0,
        },
        {
            "month": "March 2026",
            "revenue": 1500.0,
        },
    ]

    result = calculate_change(
        rows=rows,
        metric="revenue",
        dimension="month",
        start="January 2026",
        end="March 2026",
    )

    print("\n" + "=" * 70)
    print("CALCULATE CHANGE RESULT")
    print("=" * 70)

    print("\nSummary:")
    print(result.summary)

    print("\nEvidence:")

    for key, value in result.data.items():
        print(f"{key}: {value}")

    print("=" * 70)

    assert result.tool_name == "calculate_change"

    assert result.data["start"]["period"] == "January 2026"
    assert result.data["start"]["value"] == 1000.0

    assert result.data["end"]["period"] == "March 2026"
    assert result.data["end"]["value"] == 1500.0

    assert result.data["change"] == 500.0
    assert result.data["percentage_change"] == 50.0
    assert result.data["direction"] == "increasing"

    assert result.row_count == 3

    print("TEST PASSED")


if __name__ == "__main__":
    test_calculate_change()