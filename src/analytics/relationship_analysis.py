import pandas as pd


def calculate_numeric_correlations(features):
    numeric_features = features.select_dtypes(
        include="number"
    )

    return numeric_features.corr()


def find_strongest_relationships(
    features,
    minimum_correlation=0.3,
):
    correlation_matrix = calculate_numeric_correlations(features)

    relationships = []

    columns = correlation_matrix.columns

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            feature_a = columns[i]
            feature_b = columns[j]

            correlation = correlation_matrix.loc[
                feature_a,
                feature_b,
            ]

            if abs(correlation) >= minimum_correlation:
                relationships.append(
                    {
                        "feature_a": feature_a,
                        "feature_b": feature_b,
                        "correlation": correlation,
                    }
                )

    relationships = pd.DataFrame(relationships)

    if relationships.empty:
        return relationships

    return relationships.sort_values(
        "correlation",
        key=lambda values: values.abs(),
        ascending=False,
    ).reset_index(drop=True)

def calculate_segment_correlations(
    features,
    segment_column,
    minimum_correlation=0.3,
):
    results = []

    for segment_value, segment_data in features.groupby(
        segment_column
    ):
        relationships = find_strongest_relationships(
            segment_data,
            minimum_correlation=minimum_correlation,
        )

        if relationships.empty:
            continue

        relationships.insert(
            0,
            "segment",
            segment_value,
        )

        results.append(relationships)

    if not results:
        return pd.DataFrame(
            columns=[
                "segment",
                "feature_a",
                "feature_b",
                "correlation",
            ]
        )

    return pd.concat(
        results,
        ignore_index=True,
    )