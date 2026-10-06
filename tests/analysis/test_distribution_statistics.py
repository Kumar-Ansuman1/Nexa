from src.analysis.tools.distribution_statistics import (
    distribution_statistics,
)


def test_distribution_statistics():
    rows = [
        {"revenue": 100.0},
        {"revenue": 200.0},
        {"revenue": 300.0},
        {"revenue": 400.0},
        {"revenue": 500.0},
    ]

    result = distribution_statistics(
        rows=rows,
        metric="revenue",
    )

    print("\n" + "=" * 70)
    print("DISTRIBUTION STATISTICS RESULT")
    print("=" * 70)

    print("\nSummary:")
    print(result.summary)

    print("\nDistribution:")

    for key, value in result.data.items():
        print(f"{key}: {value}")

    print("=" * 70)

    assert result.tool_name == "distribution_statistics"

    assert result.data["metric"] == "revenue"

    assert result.data["minimum"] == 100.0
    assert result.data["maximum"] == 500.0
    assert result.data["range"] == 400.0

    assert result.data["q1"] == 200.0
    assert result.data["q3"] == 400.0
    assert result.data["iqr"] == 200.0

    assert result.data["percentile_10"] == 140.0
    assert result.data["percentile_90"] == 460.0

    assert result.data["variance"] == 20000.0

    assert result.data["standard_deviation"] == (
        20000.0 ** 0.5
    )

    assert result.source_columns == ["revenue"]
    assert result.row_count == 5

    print("TEST PASSED")


if __name__ == "__main__":
    test_distribution_statistics()