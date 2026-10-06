from src.analysis.tools.share_distribution import (
    share_distribution,
)


def test_share_distribution():
    rows = [
        {
            "country": "India",
            "revenue": 500.0,
        },
        {
            "country": "United States",
            "revenue": 300.0,
        },
        {
            "country": "Canada",
            "revenue": 200.0,
        },
    ]

    result = share_distribution(
        rows=rows,
        metric="revenue",
        dimension="country",
    )

    print("\n" + "=" * 70)
    print("SHARE DISTRIBUTION RESULT")
    print("=" * 70)

    print("\nSummary:")
    print(result.summary)

    print("\nTotal:")
    print(result.data["total_value"])

    print("\nDistribution:")

    for item in result.data["distribution"]:
        print(item)

    print("=" * 70)

    assert result.tool_name == "share_distribution"

    assert result.data["total_value"] == 1000.0

    distribution = result.data["distribution"]

    assert distribution[0]["category"] == "India"
    assert distribution[0]["value"] == 500.0
    assert distribution[0]["percentage"] == 50.0
    assert distribution[0]["cumulative_percentage"] == 50.0

    assert distribution[1]["category"] == "United States"
    assert distribution[1]["percentage"] == 30.0
    assert distribution[1]["cumulative_percentage"] == 80.0

    assert distribution[2]["category"] == "Canada"
    assert distribution[2]["percentage"] == 20.0
    assert distribution[2]["cumulative_percentage"] == 100.0

    assert result.source_columns == [
        "country",
        "revenue",
    ]

    assert result.row_count == 3

    print("TEST PASSED")


if __name__ == "__main__":
    test_share_distribution()