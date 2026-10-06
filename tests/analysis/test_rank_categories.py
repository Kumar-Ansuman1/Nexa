from src.analysis.tools.rank_categories import rank_categories


def test_rank_categories_descending():
    rows = [
        {
            "country": "Australia",
            "total_revenue": 6990.0,
        },
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

    result = rank_categories(
        rows=rows,
        metric="total_revenue",
        dimension="country",
        order="descending",
        limit=3,
    )

    print("\n" + "=" * 70)
    print("RANK CATEGORIES RESULT")
    print("=" * 70)

    print("Summary:")
    print(result.summary)

    print("\nRanking:")

    for item in result.data["ranking"]:
        print(
            f"{item['rank']}. "
            f"{item['category']} → "
            f"{item['value']}"
        )

    print("\nSource columns:")
    print(result.source_columns)

    print("\nInput row count:")
    print(result.row_count)

    print("=" * 70)

    assert result.tool_name == "rank_categories"

    assert result.data["metric"] == "total_revenue"
    assert result.data["dimension"] == "country"
    assert result.data["order"] == "descending"

    assert result.data["ranking"][0]["category"] == "India"
    assert result.data["ranking"][0]["value"] == 50019.0

    assert result.data["ranking"][1]["category"] == "United States"
    assert result.data["ranking"][1]["value"] == 32355.0

    assert result.data["ranking"][2]["category"] == "Canada"
    assert result.data["ranking"][2]["value"] == 8157.0

    assert len(result.data["ranking"]) == 3
    assert result.row_count == 4

    print("TEST PASSED")


if __name__ == "__main__":
    test_rank_categories_descending()