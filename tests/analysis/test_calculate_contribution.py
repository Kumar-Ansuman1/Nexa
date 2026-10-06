from src.analysis.tools.calculate_contribution import (
    calculate_contribution,
)


def test_calculate_contribution():
    rows = [
        {
            "country": "India",
            "total_revenue": 50019.0,
        },
        {
            "country": "United States",
            "total_revenue": 32355.0,
        },
        {
            "country": "Canada",
            "total_revenue": 8157.0,
        },
    ]

    result = calculate_contribution(
        rows=rows,
        metric="total_revenue",
        dimension="country",
        category="India",
    )

    print("\n" + "=" * 70)
    print("CALCULATE CONTRIBUTION RESULT")
    print("=" * 70)

    print("\nSummary:")
    print(result.summary)

    print("\nCategory:")
    print(result.data["category"])

    print("\nCategory value:")
    print(result.data["category_value"])

    print("\nTotal value:")
    print(result.data["total_value"])

    print("\nContribution:")
    print(
        f"{result.data['contribution_percentage']:.2f}%"
    )

    print("=" * 70)

    assert result.tool_name == "calculate_contribution"

    assert result.data["category"] == "India"

    assert result.data["category_value"] == 50019.0

    assert result.data["total_value"] == 90531.0

    expected_percentage = (
        50019.0 / 90531.0
    ) * 100

    assert abs(
        result.data["contribution_percentage"]
        - expected_percentage
    ) < 0.000001

    assert result.row_count == 3

    print("TEST PASSED")


if __name__ == "__main__":
    test_calculate_contribution()