from pathlib import Path
import tempfile

import pandas as pd

import src.data.ingestion.ingestion_pipeline as ingestion_pipeline


def test_complete_ingestion_pipeline():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # ---------------------------------------------------------
        # Create arbitrary test datasets
        # ---------------------------------------------------------

        customers = pd.DataFrame(
            {
                "customer_id": ["C001", "C002", "C003"],
                "country": ["India", "India", "USA"],
            }
        )

        transactions = pd.DataFrame(
            {
                "transaction_id": ["T001", "T002", "T003"],
                "customer_id": ["C001", "C002", "C001"],
                "amount": [100, 200, 150],
            }
        )

        customers.to_csv(
            temp_path / "customers.csv",
            index=False,
        )

        transactions.to_csv(
            temp_path / "transactions.csv",
            index=False,
        )

        # ---------------------------------------------------------
        # Mock semantic interpretation
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
        # Run complete pipeline
        # ---------------------------------------------------------

        result = ingestion_pipeline.run_ingestion_pipeline(
            directory=temp_path,
            column_approval_handler=approve_semantics,
            relationship_approval_handler=(
                approve_relationships
            ),
        )

        # ---------------------------------------------------------
        # Assertions
        # ---------------------------------------------------------

        assert result.pending_approval_stage is None

        assert set(result.datasets.keys()) == {
            "customers",
            "transactions",
        }

        assert set(result.profiles.keys()) == {
            "customers",
            "transactions",
        }

        assert len(result.registry.datasets) == 2

        assert relationship_discovery_called
        assert relationship_approval_called
        assert catalog_called

        assert result.catalog == []


if __name__ == "__main__":
    test_complete_ingestion_pipeline()
    print("Complete ingestion pipeline tests passed.")