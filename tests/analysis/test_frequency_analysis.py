from src.analysis.tools.frequency_analysis import (
    frequency_analysis,
)


def test_frequency_analysis():

    rows = [
        {"country": "India"},
        {"country": "India"},
        {"country": "India"},
        {"country": "United States"},
        {"country": "United States"},
        {"country": "Canada"},
        {"country": "Canada"},
        {"country": "Canada"},
        {"country": "Canada"},
        {"country": "Australia"},
    ]

    result = frequency_analysis(
        rows=rows,
        dimension="country",
    )

    assert result.tool_name == "frequency_analysis"

    assert result.data["dimension"] == "country"

    assert result.data["total_count"] == 10

    assert result.data["unique_categories"] == 4

    distribution = result.data["distribution"]

    # Canada = 4
    assert distribution[0]["category"] == "Canada"
    assert distribution[0]["count"] == 4
    assert distribution[0]["percentage"] == 40.0
    assert distribution[0]["cumulative_percentage"] == 40.0

    # India = 3
    assert distribution[1]["category"] == "India"
    assert distribution[1]["count"] == 3
    assert distribution[1]["percentage"] == 30.0
    assert distribution[1]["cumulative_percentage"] == 70.0

    # United States = 2
    assert distribution[2]["category"] == "United States"
    assert distribution[2]["count"] == 2
    assert distribution[2]["percentage"] == 20.0
    assert distribution[2]["cumulative_percentage"] == 90.0

    # Australia = 1
    assert distribution[3]["category"] == "Australia"
    assert distribution[3]["count"] == 1
    assert distribution[3]["percentage"] == 10.0
    assert distribution[3]["cumulative_percentage"] == 100.0

    assert result.source_columns == ["country"]

    assert result.row_count == 10


if __name__ == "__main__":
    test_frequency_analysis()
    print("frequency_analysis test passed.")