from pathlib import Path
import sqlite3

from src.data.ingestion.ingestion_pipeline import run_ingestion_pipeline
from src.llm.schemas.registry import ApprovalStatus


DATA_DIRECTORY = Path(r"C:\Code\Nexa\data\processed")
DATABASE_PATH = Path(r"C:\Code\Nexa\data\nexa.db")


def approve_registry(registry):
    """
    Simulate the first human approval stage.

    Approves the dataset and all interpreted columns.
    """

    for dataset in registry.datasets:
        dataset.approval_status = ApprovalStatus.APPROVED
        dataset.approved_name = dataset.suggested_name
        dataset.approved_description = dataset.suggested_description

        for column in dataset.columns:
            column.approval_status = ApprovalStatus.APPROVED
            column.approved_meaning = column.suggested_meaning
            column.approved_description = column.suggested_description
            column.approved_role = column.suggested_role

    return registry


def approve_relationships(registry):
    """
    Simulate the second human approval stage.

    Approves all discovered relationships.
    """

    for relationship in registry.relationships:
        relationship.approval_status = ApprovalStatus.APPROVED

    return registry


def main():
    print("=" * 60)
    print("NEXA REAL INGESTION TEST")
    print("=" * 60)

    print(f"\nData directory:")
    print(f"  {DATA_DIRECTORY}")

    print(f"\nDatabase:")
    print(f"  {DATABASE_PATH}")

    # ---------------------------------------------------------
    # Validate input
    # ---------------------------------------------------------

    if not DATA_DIRECTORY.exists():
        raise FileNotFoundError(
            f"Data directory does not exist: {DATA_DIRECTORY}"
        )

    if not DATA_DIRECTORY.is_dir():
        raise NotADirectoryError(
            f"Expected a directory: {DATA_DIRECTORY}"
        )

    customers_csv = DATA_DIRECTORY / "customers.csv"

    if not customers_csv.exists():
        raise FileNotFoundError(
            f"customers.csv was not found: {customers_csv}"
        )

    # ---------------------------------------------------------
    # Run REAL ingestion pipeline
    # ---------------------------------------------------------

    print("\nRunning real ingestion pipeline...")

    result = run_ingestion_pipeline(
        directory=DATA_DIRECTORY,
        column_approval_handler=approve_registry,
        relationship_approval_handler=approve_relationships,
    )

    # ---------------------------------------------------------
    # Inspect ingestion result
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("INGESTION RESULT")
    print("=" * 60)

    print(f"\nDatasets loaded:    {len(result.datasets)}")
    print(f"Profiles created:   {len(result.profiles)}")
    print(f"Registry datasets:  {len(result.registry.datasets)}")
    print(f"Relationships:      {len(result.registry.relationships)}")
    print(f"Catalog entries:    {len(result.catalog or [])}")
    print(f"Pending approval:   {result.pending_approval_stage}")

    print("\nLoaded datasets:")

    for dataset_name, dataframe in result.datasets.items():
        print(
            f"  - {dataset_name}: "
            f"{len(dataframe)} rows × "
            f"{len(dataframe.columns)} columns"
        )

    # ---------------------------------------------------------
    # Verify customers.csv was actually loaded
    # ---------------------------------------------------------

    assert "customers" in result.datasets, (
        "The customers dataset was not loaded."
    )

    customers = result.datasets["customers"]

    assert len(customers) > 0, (
        "customers.csv was loaded but contains no rows."
    )

    assert len(customers.columns) > 0, (
        "customers.csv was loaded but contains no columns."
    )

    print("\ncustomers.csv:")
    print(f"  Rows:    {len(customers)}")
    print(f"  Columns: {len(customers.columns)}")

    print("\nColumns:")

    for column in customers.columns:
        print(f"  - {column}")

    # ---------------------------------------------------------
    # Verify profiling
    # ---------------------------------------------------------

    assert "customers" in result.profiles, (
        "No profile was generated for customers."
    )

    profile = result.profiles["customers"]

    assert profile["rows"] == len(customers)
    assert profile["columns"] == len(customers.columns)

    print("\nProfiling:")
    print(f"  Rows:             {profile['rows']}")
    print(f"  Columns:          {profile['columns']}")
    print(f"  Duplicate rows:   {profile['duplicate_rows']}")
    print(
        f"  Column profiles:  "
        f"{len(profile['column_profiles'])}"
    )

    # ---------------------------------------------------------
    # Verify semantic registry
    # ---------------------------------------------------------

    assert len(result.registry.datasets) > 0, (
        "Semantic registry contains no datasets."
    )

    customers_registry = next(
        (
            dataset
            for dataset in result.registry.datasets
            if dataset.dataset_name == "customers"
        ),
        None,
    )

    assert customers_registry is not None, (
        "customers dataset was not added to the semantic registry."
    )

    assert len(customers_registry.columns) == len(
        customers.columns
    ), (
        "Registry column count does not match the CSV column count."
    )

    print("\nSemantic registry:")
    print(
        f"  Dataset:  {customers_registry.dataset_name}"
    )
    print(
        f"  Columns:  {len(customers_registry.columns)}"
    )
    print(
        f"  Status:   {customers_registry.approval_status}"
    )

    # ---------------------------------------------------------
    # Verify catalog
    # ---------------------------------------------------------

    assert result.catalog is not None, (
        "Semantic catalog was not created."
    )

    print("\nSemantic catalog:")
    print(f"  Entries: {len(result.catalog)}")

    # ---------------------------------------------------------
    # Verify database persistence
    # ---------------------------------------------------------

    print("\nChecking SQLite persistence...")

    assert DATABASE_PATH.exists(), (
        "nexa.db was not created."
    )

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        dataset_count = connection.execute(
            "SELECT COUNT(*) FROM datasets"
        ).fetchone()[0]

        column_count = connection.execute(
            "SELECT COUNT(*) FROM columns"
        ).fetchone()[0]

        relationship_count = connection.execute(
            "SELECT COUNT(*) FROM relationships"
        ).fetchone()[0]

    finally:
        connection.close()

    print(f"  datasets table:      {dataset_count}")
    print(f"  columns table:       {column_count}")
    print(f"  relationships table: {relationship_count}")

    # ---------------------------------------------------------
    # Verify persisted counts
    # ---------------------------------------------------------

    expected_dataset_count = len(
        result.registry.datasets
    )

    expected_column_count = sum(
        len(dataset.columns)
        for dataset in result.registry.datasets
    )

    expected_relationship_count = len(
        result.registry.relationships
    )

    assert dataset_count == expected_dataset_count, (
        f"Expected {expected_dataset_count} datasets "
        f"in SQLite, found {dataset_count}."
    )

    assert column_count == expected_column_count, (
        f"Expected {expected_column_count} columns "
        f"in SQLite, found {column_count}."
    )

    assert relationship_count == expected_relationship_count, (
        f"Expected {expected_relationship_count} relationships "
        f"in SQLite, found {relationship_count}."
    )

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("REAL INGESTION TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()