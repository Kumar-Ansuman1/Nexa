from src.analysis.tools.detect_outliers import (
    detect_outliers,
)


def test_detect_outliers():
    rows = [
        {
            "customer": "A",
            "revenue": 100.0,
        },
        {
            "customer": "B",
            "revenue": 110.0,
        },
        {
            "customer": "C",
            "revenue": 105.0,
        },
        {
            "customer": "D",
            "revenue": 115.0,
        },
        {
            "customer": "E",
            "revenue": 500.0,
        },
    ]

    result = detect_outliers(
        rows=rows,
        metric="revenue",
        dimension="customer",
    )

    print("\n" + "=" * 70)
    print("OUTLIER DETECTION RESULT")
    print("=" * 70)

    print("\nSummary:")
    print(result.summary)

    print("\nStatistics:")

    for key, value in result.data.items():
        print(f"{key}: {value}")

    print("=" * 70)

    assert result.tool_name == "detect_outliers"

    assert result.data["method"] == "IQR"

    assert result.data["q1"] == 102.5
    assert result.data["q3"] == 112.5
    assert result.data["iqr"] == 10.0

    assert result.data["lower_bound"] == 87.5
    assert result.data["upper_bound"] == 127.5

    assert result.data["outlier_count"] == 1

    assert result.data["outliers"] == [
        {
            "row_index": 4,
            "value": 500.0,
            "category": "E",
        }
    ]

    assert result.source_columns == [
        "customer",
        "revenue",
    ]

    assert result.row_count == 5

    print("TEST PASSED")


if __name__ == "__main__":
    test_detect_outliers()