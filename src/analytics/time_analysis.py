import pandas as pd


def monthly_count(df, date_column, value_column):
    return (
        df.groupby(
            df[date_column].dt.to_period("M")
        )[value_column]
        .nunique()
    )

