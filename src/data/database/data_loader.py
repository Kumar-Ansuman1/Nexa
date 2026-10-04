from pathlib import Path

import pandas as pd

from src.data.database.connection import get_connection


def load_dataframe_to_database(
    dataframe: pd.DataFrame,
    table_name: str,
    if_exists: str = "replace",
) -> None:
    """
    Store a pandas DataFrame as a SQLite table.

    Parameters
    ----------
    dataframe:
        DataFrame containing the dataset.

    table_name:
        SQLite table name.

    if_exists:
        Behavior if the table already exists.
        Supported by pandas.to_sql:
            - "fail"
            - "replace"
            - "append"
    """

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas DataFrame.")

    if dataframe.empty:
        raise ValueError(
            f"Cannot load empty dataframe into table '{table_name}'."
        )

    if not table_name or not table_name.strip():
        raise ValueError("table_name must not be empty.")

    table_name = table_name.strip()

    connection = get_connection()

    try:
        dataframe.to_sql(
            name=table_name,
            con=connection,
            if_exists=if_exists,
            index=False,
        )

        connection.commit()

    finally:
        connection.close()


def load_csv_to_database(
    csv_path: str | Path,
    table_name: str | None = None,
    if_exists: str = "replace",
) -> str:
    """
    Load a CSV file directly into a SQLite table.

    Returns
    -------
    str
        Name of the created SQLite table.
    """

    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV file does not exist: {csv_path}"
        )

    if csv_path.suffix.lower() != ".csv":
        raise ValueError(
            f"Expected a CSV file, got: {csv_path.suffix}"
        )

    dataframe = pd.read_csv(csv_path)

    if table_name is None:
        table_name = csv_path.stem

    load_dataframe_to_database(
        dataframe=dataframe,
        table_name=table_name,
        if_exists=if_exists,
    )

    return table_name


def load_csv_directory_to_database(
    directory: str | Path,
    if_exists: str = "replace",
) -> list[str]:
    """
    Load every CSV file in a directory into SQLite.

    The filename becomes the SQLite table name.

    Example:

        customers.csv
            -> customers

        transactions.csv
            -> transactions
    """

    directory = Path(directory)

    if not directory.exists():
        raise FileNotFoundError(
            f"CSV directory does not exist: {directory}"
        )

    if not directory.is_dir():
        raise NotADirectoryError(
            f"Expected a directory: {directory}"
        )

    csv_files = sorted(directory.glob("*.csv"))

    if not csv_files:
        raise ValueError(
            f"No CSV files found in directory: {directory}"
        )

    loaded_tables: list[str] = []

    for csv_file in csv_files:
        table_name = load_csv_to_database(
            csv_path=csv_file,
            if_exists=if_exists,
        )

        loaded_tables.append(table_name)

    return loaded_tables