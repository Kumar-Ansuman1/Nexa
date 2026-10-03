import pandas as pd

def detect_semantic_type(series):
    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"

    if pd.api.types.is_string_dtype(series):
        non_null = series.dropna()

        if len(non_null) == 0:
            return "unknown"

        # Check whether the values can be interpreted as dates
        parsed_dates = pd.to_datetime(non_null, errors="coerce",format="mixed",)
        date_ratio = parsed_dates.notna().mean()

        if date_ratio >= 0.95:
            return "date"

        unique_ratio = non_null.nunique() / len(non_null)

        if unique_ratio >= 0.95:
            return "identifier"

        if unique_ratio <= 0.05:
            return "categorical"

        return "text"

    return "unknown"

def profile_dataset(df: pd.DataFrame, name: str = "dataset") -> dict:
    profile = {
        "name": name,
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_profiles": [],
    }

    for column in df.columns:
        series = df[column]

        column_profile = {
            "name": column,
            "dtype": str(series.dtype),
            "semantic_type": detect_semantic_type(series),
            "missing_count": int(series.isna().sum()),
            "missing_percentage": float(series.isna().mean() * 100),
            "unique_count": int(series.nunique(dropna=True)),
            "uniqueness_ratio": float(
                series.nunique(dropna=True) / len(series)
            ) if len(series) > 0 else 0,
            "sample_values": series.dropna().head(5).tolist(),
        }

        profile["column_profiles"].append(column_profile)

    return profile