from src.analysis.tools.compare_groups import compare_groups


def test_compare_groups():
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

    result = compare_groups(
        rows=rows,
        metric="total_revenue",
        dimension="country",
        groups=[
            "India",
            "United States",
        ],
    )

    print("\n" + "=" * 70)
    print("COMPARE GROUPS RESULT")
    print("=" * 70)

    print("\nSummary:")
    print(result.summary)

    print("\nGroups:")
    for group in result.data["groups"]:
        print(
            f"{group['group']} → "
            f"{group['value']}"
        )

    print("\nDifference:")
    print(result.data["difference"])

    print("\nPercentage difference:")
    print(result.data["percentage_difference"])

    print("=" * 70)

    assert result.tool_name == "compare_groups"

    assert result.data["highest"]["group"] == "India"
    assert result.data["highest"]["value"] == 50019.0

    assert (
        result.data["lowest"]["group"]
        == "United States"
    )

    assert (
        result.data["lowest"]["value"]
        == 32355.0
    )

    assert result.data["difference"] == 17664.0

    assert len(result.data["groups"]) == 2

    print("TEST PASSED")


if __name__ == "__main__":
    test_compare_groups()