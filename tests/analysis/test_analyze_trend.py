from src.analysis.tools.analyze_trend import analyze_trend


def test_analyze_trend_orders_rows_chronologically():
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

    result = analyze_trend(
        rows=rows,
        metric="revenue",
        dimension="month",
    )

    print("\n" + "=" * 70)
    print("TREND ANALYSIS RESULT")
    print("=" * 70)

    print("\nSummary:")
    print(result.summary)

    print("\nOrdered rows:")

    for row in result.data["ordered_rows"]:
        print(row)

    print("\nDirection:")
    print(result.data["direction"])

    print("\nChange:")
    print(result.data["change"])

    print("\nPercentage change:")
    print(
        f"{result.data['percentage_change']:.2f}%"
    )

    print("=" * 70)

    assert result.data["ordered_rows"] == [
        {
            "period": "January 2026",
            "value": 1000.0,
        },
        {
            "period": "February 2026",
            "value": 1200.0,
        },
        {
            "period": "March 2026",
            "value": 1500.0,
        },
    ]

    assert result.data["start"]["period"] == "January 2026"
    assert result.data["end"]["period"] == "March 2026"

    assert result.data["change"] == 500.0
    assert result.data["percentage_change"] == 50.0
    assert result.data["direction"] == "increasing"

    assert result.row_count == 3

    print("TEST PASSED")


if __name__ == "__main__":
    test_analyze_trend_orders_rows_chronologically()