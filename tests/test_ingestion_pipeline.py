from pathlib import Path

import src.data.ingestion.ingestion_pipeline as ingestion_pipeline


# ============================================================
# Configuration
# ============================================================

DATA_DIRECTORY = Path("data/processed")
DATABASE_PATH = Path("data/nexa.db")


# ============================================================
# Test
# ============================================================


def test_complete_ingestion_pipeline():
    # ---------------------------------------------------------
    # Validate test data directory
    # ---------------------------------------------------------

    assert DATA_DIRECTORY.exists(), (
        f"Data directory does not exist: {DATA_DIRECTORY}"
    )

    csv_files = list(
        DATA_DIRECTORY.glob("*.csv")
    )

    assert csv_files, (
        f"No CSV files found in {DATA_DIRECTORY}"
    )

    print(
        f"\nFound {len(csv_files)} CSV files:"
    )

    for csv_file in csv_files:
        print(f"  - {csv_file.name}")

    # ---------------------------------------------------------
    # Start with a completely fresh database
    # ---------------------------------------------------------

    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

        print(
            f"\nDeleted existing database: "
            f"{DATABASE_PATH}"
        )

    # ---------------------------------------------------------
    # Mock semantic interpretation
    #
    # We keep this mocked so this test focuses on the complete
    # ingestion pipeline rather than testing the LLM itself.
    # ---------------------------------------------------------

    def fake_interpret_dataset(profile):
        return {
            "dataset_name": profile["name"],
            "columns": [
                {
                    "source_column": column["name"],
                    "suggested_meaning": column["name"],
                    "suggested_description": (
                        f"Description of {column['name']}"
                    ),
                    "suggested_role": "dimension",
                    "confidence": 0.95,
                    "evidence": [
                        "test semantic interpretation"
                    ],
                }
                for column in profile["column_profiles"]
            ],
        }

    ingestion_pipeline.interpret_dataset = (
        fake_interpret_dataset
    )

    # ---------------------------------------------------------
    # Mock registry construction
    # ---------------------------------------------------------

    def fake_build_registry_entry(
        mapping,
        dataset_name,
    ):
        from src.llm.schemas.registry import (
            DatasetRegistryEntry,
            ColumnRegistryEntry,
        )

        return DatasetRegistryEntry(
            dataset_name=dataset_name,
            suggested_name=dataset_name,
            suggested_description=(
                f"Description of {dataset_name}"
            ),
            confidence=0.95,
            columns=[
                ColumnRegistryEntry(
                    source_column=column[
                        "source_column"
                    ],
                    suggested_meaning=column[
                        "suggested_meaning"
                    ],
                    suggested_description=column[
                        "suggested_description"
                    ],
                    suggested_role=column[
                        "suggested_role"
                    ],
                    confidence=column[
                        "confidence"
                    ],
                    evidence=column[
                        "evidence"
                    ],
                )
                for column in mapping["columns"]
            ],
        )

    ingestion_pipeline.build_registry_entry = (
        fake_build_registry_entry
    )

    # ---------------------------------------------------------
    # First approval
    # ---------------------------------------------------------

    approval_called = False

    def approve_semantics(registry):
        nonlocal approval_called

        approval_called = True

        for dataset in registry.datasets:
            dataset.approval_status = "approved"

            for column in dataset.columns:
                column.approval_status = "approved"

                column.approved_meaning = (
                    column.suggested_meaning
                )

                column.approved_description = (
                    column.suggested_description
                )

                column.approved_role = (
                    column.suggested_role
                )

        return registry

    # ---------------------------------------------------------
    # Mock relationship discovery
    # ---------------------------------------------------------

    relationship_discovery_called = False

    def fake_discover_relationships(
        datasets,
        registry,
    ):
        nonlocal relationship_discovery_called

        relationship_discovery_called = True

        assert approval_called

        return []

    ingestion_pipeline.discover_relationships = (
        fake_discover_relationships
    )

    # ---------------------------------------------------------
    # Second approval
    # ---------------------------------------------------------

    relationship_approval_called = False

    def approve_relationships(registry):
        nonlocal relationship_approval_called

        relationship_approval_called = True

        return registry

    # ---------------------------------------------------------
    # Mock catalog construction
    # ---------------------------------------------------------

    catalog_called = False

    def fake_build_semantic_catalog(
        registry,
    ):
        nonlocal catalog_called

        catalog_called = True

        assert relationship_approval_called

        return []

    ingestion_pipeline.build_semantic_catalog = (
        fake_build_semantic_catalog
    )

    # ---------------------------------------------------------
    # Run complete ingestion pipeline
    # ---------------------------------------------------------

    result = ingestion_pipeline.run_ingestion_pipeline(
        directory=DATA_DIRECTORY,
        column_approval_handler=approve_semantics,
        relationship_approval_handler=(
            approve_relationships
        ),
    )

    # ---------------------------------------------------------
    # Assertions
    # ---------------------------------------------------------

    assert result.pending_approval_stage is None

    # The pipeline must load every CSV in data/processed.
    assert set(result.datasets.keys()) == {
        csv_file.stem
        for csv_file in csv_files
    }

    assert set(result.profiles.keys()) == {
        csv_file.stem
        for csv_file in csv_files
    }

    # Registry must contain every dataset.
    assert len(result.registry.datasets) == len(
        csv_files
    )

    assert relationship_discovery_called
    assert relationship_approval_called
    assert catalog_called

    assert result.catalog == []

    # ---------------------------------------------------------
    # Verify database was created
    # ---------------------------------------------------------

    assert DATABASE_PATH.exists()

    print(
        "\nComplete ingestion pipeline test passed."
    )

    print(
        f"Processed {len(csv_files)} datasets."
    )


# ============================================================
# Entry Point
# ============================================================


if __name__ == "__main__":
    test_complete_ingestion_pipeline()

    print(
        "\nComplete ingestion pipeline tests passed."
    )