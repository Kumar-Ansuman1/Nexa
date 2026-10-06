from src.analysis.tools.correlation_analysis import (
    correlation_analysis,
)


def test_correlation_analysis():
    rows = [
        {
            "marketing_spend": 10.0,
            "revenue": 20.0,
        },
        {
            "marketing_spend": 20.0,
            "revenue": 40.0,
        },
        {
            "marketing_spend": 30.0,
            "revenue": 60.0,
        },
        {
            "marketing_spend": 40.0,
            "revenue": 80.0,
        },
        {
            "marketing_spend": 50.0,
            "revenue": 100.0,
        },
    ]

    result = correlation_analysis(
        rows=rows,
        metric_x="marketing_spend",
        metric_y="revenue",
    )

    print("\n" + "=" * 70)
    print("CORRELATION ANALYSIS RESULT")
    print("=" * 70)

    print("\nSummary:")
    print(result.summary)

    print("\nEvidence:")

    for key, value in result.data.items():
        print(f"{key}: {value}")

    print("=" * 70)

    assert result.tool_name == "correlation_analysis"

    assert result.data["metric_x"] == "marketing_spend"
    assert result.data["metric_y"] == "revenue"

    assert abs(
        result.data["correlation"] - 1.0
    ) < 0.000001

    assert result.data["direction"] == "positive"
    assert result.data["strength"] == "strong"

    assert result.source_columns == [
        "marketing_spend",
        "revenue",
    ]

    assert result.row_count == 5

    print("TEST PASSED")


if __name__ == "__main__":
    test_correlation_analysis()