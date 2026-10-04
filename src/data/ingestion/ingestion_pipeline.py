"""
NEXA Data Ingestion Pipeline

Complete orchestration pipeline for transforming arbitrary CSV
datasets into a semantic registry, semantic catalog, embeddings,
and SQLite database containing the actual datasets.

Flow:

    CSV directory
        ↓
    CSV ingestion
        ↓
    Dataset profiling
        ↓
    Load datasets into SQLite
        ↓
    Semantic interpretation
        ↓
    Semantic registry
        ↓
    HUMAN APPROVAL
        ↓
    Relationship discovery
        ↓
    Relationship interpretation
        ↓
    HUMAN APPROVAL
        ↓
    Normalize + validate registry
        ↓
    Persist semantic registry
        ↓
    Generate semantic embeddings
        ↓
    Semantic catalog
"""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.data.ingestion.csv_loader import load_csv_directory
from src.data.profiling.profiler import profile_dataset

from src.data.database.data_loader import load_dataframe_to_database
from src.data.database.repositories.registry import save_registry
from src.data.database.schema import initialize_database

from src.data.semantic.catalog.catalog import (
    SemanticCatalogEntry,
    build_semantic_catalog,
)

from src.data.semantic.embeddings.generator import (
    generate_registry_embeddings,
)

from src.data.semantic.registry.interpreter import (
    interpret_dataset,
)

from src.data.semantic.registry.registry_builder import (
    build_registry_entry,
)

from src.data.semantic.registry.relationship_discovery import (
    discover_relationships,
)

from src.llm.schemas.registry import SemanticRegistry


# ============================================================
# Pipeline Result
# ============================================================


@dataclass
class IngestionPipelineResult:
    """
    Result produced by the NEXA data ingestion pipeline.

    Attributes
    ----------
    datasets:
        Loaded source datasets.

    profiles:
        Generic profile for every dataset.

    registry:
        Current semantic registry.

    catalog:
        Semantic catalog if all required approval stages
        have completed. Otherwise None.

    pending_approval_stage:
        Name of the approval stage currently blocking
        the pipeline, or None when the pipeline is complete.
    """

    datasets: dict[str, pd.DataFrame]
    profiles: dict[str, dict]
    registry: SemanticRegistry
    catalog: list[SemanticCatalogEntry] | None
    pending_approval_stage: str | None


# ============================================================
# Approval Handler Types
# ============================================================


ColumnApprovalHandler = Callable[
    [SemanticRegistry],
    SemanticRegistry,
]

RelationshipApprovalHandler = Callable[
    [SemanticRegistry],
    SemanticRegistry,
]


# ============================================================
# Stage 1. Load + Profile
# ============================================================


def load_and_profile_datasets(
    directory: str | Path,
) -> tuple[
    dict[str, pd.DataFrame],
    dict[str, dict],
]:
    """
    Load every CSV in a directory and generate a profile
    for every dataset.

    Parameters
    ----------
    directory:
        Directory containing CSV files.

    Returns
    -------
    tuple
        Loaded datasets and their corresponding profiles.
    """

    datasets = load_csv_directory(directory)

    profiles: dict[str, dict] = {}

    for dataset_name, dataframe in datasets.items():
        profiles[dataset_name] = profile_dataset(
            dataframe,
            name=dataset_name,
        )

    return datasets, profiles


# ============================================================
# Stage 2. Load Actual Data into SQLite
# ============================================================


def load_datasets_into_database(
    datasets: dict[str, pd.DataFrame],
) -> None:
    """
    Load every dataset into the NEXA SQLite database.

    Each dataset becomes a SQLite table using the dataset name
    as the table name.
    """

    for dataset_name, dataframe in datasets.items():
        load_dataframe_to_database(
            dataframe=dataframe,
            table_name=dataset_name,
            if_exists="replace",
        )


# ============================================================
# Stage 3. Semantic Interpretation + Registry
# ============================================================


def build_semantic_registry(
    profiles: dict[str, dict],
) -> SemanticRegistry:
    """
    Interpret every dataset semantically and build the
    initial semantic registry.

    All generated dataset and column entries start as
    PENDING and therefore require human approval.
    """

    registry = SemanticRegistry(
        datasets=[],
        relationships=[],
    )

    for dataset_name, profile in profiles.items():
        mapping = interpret_dataset(profile)

        registry_entry = build_registry_entry(
            mapping=mapping,
            dataset_name=dataset_name,
        )

        registry.datasets.append(
            registry_entry
        )

    return registry


# ============================================================
# Stage 4. Relationship Discovery
# ============================================================


def discover_pending_relationships(
    datasets: dict[str, pd.DataFrame],
    registry: SemanticRegistry,
) -> SemanticRegistry:
    """
    Discover and interpret relationships using the current
    semantic registry.

    Only columns already approved in the registry can
    participate in relationship candidate generation.

    Discovered relationships are added as PENDING.
    """

    relationships = discover_relationships(
        datasets=datasets,
        registry=registry,
    )

    registry.relationships.extend(
        relationships
    )

    return registry


# ============================================================
# Stage 5. Semantic Embeddings
# ============================================================


def generate_semantic_embeddings(
    registry: SemanticRegistry,
) -> int:
    """
    Generate and persist embeddings for approved semantic
    columns.

    Only columns with an approved meaning are embedded.

    Returns
    -------
    int
        Number of embeddings generated.
    """

    return generate_registry_embeddings(
        registry=registry,
    )


# ============================================================
# Stage 6. Semantic Catalog
# ============================================================


def build_catalog(
    registry: SemanticRegistry,
) -> list[SemanticCatalogEntry]:
    """
    Build the semantic catalog from the current registry.

    The catalog builder itself includes only approved
    columns with approved meanings.
    """

    return build_semantic_catalog(
        registry=registry,
    )


# ============================================================
# Stage 7. Persist Registry
# ============================================================


def persist_ingestion_result(
    registry: SemanticRegistry,
) -> None:
    """
    Persist the final approved semantic registry.

    The registry contains:
        - approved datasets
        - approved columns
        - approved relationships
    """

    save_registry(registry)


# ============================================================
# Complete Pipeline
# ============================================================


def run_ingestion_pipeline(
    directory: str | Path,
    column_approval_handler: ColumnApprovalHandler | None = None,
    relationship_approval_handler: (
        RelationshipApprovalHandler | None
    ) = None,
) -> IngestionPipelineResult:
    """
    Run the complete NEXA data ingestion pipeline.

    Parameters
    ----------
    directory:
        Directory containing arbitrary CSV files.

    column_approval_handler:
        Function responsible for handling human approval
        of the generated semantic registry.

        It receives the pending SemanticRegistry and must
        return the registry after human review.

        If omitted, the pipeline stops after semantic
        registry generation.

    relationship_approval_handler:
        Function responsible for handling human approval
        of discovered relationships.

        It receives the registry containing pending
        relationships and must return the registry after
        human review.

        If omitted, the pipeline stops after relationship
        discovery.

    Returns
    -------
    IngestionPipelineResult
        Complete pipeline state.

    Pipeline
    --------
    1. Initialize database.
    2. Load CSV files.
    3. Profile datasets.
    4. Load datasets into SQLite.
    5. Interpret dataset semantics.
    6. Build semantic registry.
    7. Wait for human approval of semantic interpretations.
    8. Discover relationships.
    9. Wait for human approval of relationships.
    10. Normalize and validate registry.
    11. Persist final approved registry.
    12. Generate embeddings for approved columns.
    13. Build semantic catalog.
    """

    # --------------------------------------------------------
    # 1. Initialize database
    # --------------------------------------------------------

    initialize_database()

    # --------------------------------------------------------
    # 2. CSV ingestion
    # --------------------------------------------------------

    datasets, profiles = load_and_profile_datasets(
        directory
    )

    # --------------------------------------------------------
    # 3. Store actual datasets in SQLite
    # --------------------------------------------------------

    load_datasets_into_database(
        datasets=datasets,
    )

    # --------------------------------------------------------
    # 4. Semantic interpretation
    # 5. Registry construction
    # --------------------------------------------------------

    registry = build_semantic_registry(
        profiles
    )

    # --------------------------------------------------------
    # 6. Human approval: semantic registry
    # --------------------------------------------------------

    if column_approval_handler is None:
        return IngestionPipelineResult(
            datasets=datasets,
            profiles=profiles,
            registry=registry,
            catalog=None,
            pending_approval_stage="semantic_registry",
        )

    registry = column_approval_handler(
        registry
    )

    # --------------------------------------------------------
    # 7. Relationship discovery
    # 8. Relationship interpretation
    # --------------------------------------------------------

    registry = discover_pending_relationships(
        datasets=datasets,
        registry=registry,
    )

    # --------------------------------------------------------
    # 9. Human approval: relationships
    # --------------------------------------------------------

    if relationship_approval_handler is None:
        return IngestionPipelineResult(
            datasets=datasets,
            profiles=profiles,
            registry=registry,
            catalog=None,
            pending_approval_stage="relationships",
        )

    registry = relationship_approval_handler(
        registry
    )

    # --------------------------------------------------------
    # 10. Normalize and validate registry
    # --------------------------------------------------------

    registry = SemanticRegistry.model_validate(
        registry.model_dump()
    )

    # --------------------------------------------------------
    # 11. Persist final approved registry
    # --------------------------------------------------------

    persist_ingestion_result(
        registry
    )

    # --------------------------------------------------------
    # 12. Generate embeddings
    # --------------------------------------------------------

    embedding_count = generate_semantic_embeddings(
        registry=registry,
    )

    print(
        f"Generated embeddings for "
        f"{embedding_count} approved columns."
    )

    # --------------------------------------------------------
    # 13. Semantic catalog
    # --------------------------------------------------------

    catalog = build_catalog(
        registry
    )

    return IngestionPipelineResult(
        datasets=datasets,
        profiles=profiles,
        registry=registry,
        catalog=catalog,
        pending_approval_stage=None,
    )