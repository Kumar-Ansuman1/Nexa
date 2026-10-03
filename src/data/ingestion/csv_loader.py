"""
Generic CSV ingestion for NEXA.

This module is intentionally domain-agnostic.
It does not know anything about specific datasets.
"""

from pathlib import Path

import pandas as pd


class CSVIngestionError(ValueError):
    """Raised when a CSV cannot be ingested safely."""


def load_csv(path: str | Path) -> tuple[str, pd.DataFrame]:
    """
    Load a single CSV file.

    Parameters
    ----------
    path:
        Path to the CSV file.

    Returns
    -------
    tuple[str, pandas.DataFrame]
        Dataset name and loaded DataFrame.

    The dataset name is derived from the filename.
    """

    file_path = Path(path)

    if not file_path.exists():
        raise CSVIngestionError(
            f"CSV file does not exist: {file_path}"
        )

    if not file_path.is_file():
        raise CSVIngestionError(
            f"CSV path is not a file: {file_path}"
        )

    if file_path.suffix.lower() != ".csv":
        raise CSVIngestionError(
            f"Expected a CSV file, got: {file_path.suffix}"
        )

    dataset_name = file_path.stem.strip()

    if not dataset_name:
        raise CSVIngestionError(
            "CSV filename does not contain a valid dataset name."
        )

    try:
        dataframe = pd.read_csv(file_path)
    except Exception as exc:
        raise CSVIngestionError(
            f"Failed to read CSV '{file_path}': {exc}"
        ) from exc

    if dataframe.empty:
        raise CSVIngestionError(
            f"CSV '{file_path}' contains no rows."
        )

    if len(dataframe.columns) == 0:
        raise CSVIngestionError(
            f"CSV '{file_path}' contains no columns."
        )

    columns = [
        str(column).strip()
        for column in dataframe.columns
    ]

    if any(not column for column in columns):
        raise CSVIngestionError(
            f"CSV '{file_path}' contains an empty column name."
        )

    normalized_columns = [
        column.lower()
        for column in columns
    ]

    if len(normalized_columns) != len(set(normalized_columns)):
        raise CSVIngestionError(
            f"CSV '{file_path}' contains duplicate column names."
        )

    dataframe.columns = columns

    return dataset_name, dataframe


def load_csv_directory(
    directory: str | Path,
) -> dict[str, pd.DataFrame]:
    """
    Load every CSV file from a directory.

    Returns
    -------
    dict[str, pandas.DataFrame]
        Mapping of dataset name to DataFrame.
    """

    directory_path = Path(directory)

    if not directory_path.exists():
        raise CSVIngestionError(
            f"CSV directory does not exist: {directory_path}"
        )

    if not directory_path.is_dir():
        raise CSVIngestionError(
            f"CSV path is not a directory: {directory_path}"
        )

    csv_files = sorted(
        directory_path.glob("*.csv")
    )

    datasets: dict[str, pd.DataFrame] = {}

    for csv_file in csv_files:
        dataset_name, dataframe = load_csv(csv_file)

        if dataset_name in datasets:
            raise CSVIngestionError(
                f"Duplicate dataset name detected: "
                f"'{dataset_name}'"
            )

        datasets[dataset_name] = dataframe

    return datasets