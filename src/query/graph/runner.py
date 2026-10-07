from typing import Any

from src.data.database.introspection import get_database_schema
from src.data.database.repositories.embeddings import (
    get_all_embeddings,
)
from src.data.database.repositories.registry import load_registry
from src.data.semantic.catalog.catalog import (
    SemanticCatalogEntry,
    build_semantic_catalog,
)
from src.llm.schemas.registry import SemanticRegistry
from src.query.graph.workflow import build_query_workflow
from src.query.state import NexaQueryState


def run_query_workflow(
    query: str,
    registry: SemanticRegistry | None = None,
    catalog: list[SemanticCatalogEntry] | None = None,
    database_schema: str | None = None,
) -> NexaQueryState:
    """
    Prepare the initial NEXA workflow state and execute the
    LangGraph query workflow.

    The workflow is responsible for query orchestration.
    This runner is responsible for loading the runtime data
    required by the workflow.
    """

    if not isinstance(query, str):
        raise TypeError("query must be a string.")

    query = query.strip()

    if not query:
        raise ValueError(
            "Natural-language query must not be empty."
        )

    # ---------------------------------------------------------
    # Registry
    # ---------------------------------------------------------

    if registry is None:
        registry = load_registry()

    if not registry.datasets:
        raise ValueError(
            "No datasets are available in the semantic registry."
        )

    # ---------------------------------------------------------
    # Semantic catalog
    # ---------------------------------------------------------

    if catalog is None:
        catalog = build_semantic_catalog(
            registry=registry,
        )

    if not catalog:
        raise ValueError(
            "Semantic catalog is empty. "
            "Ensure approved semantic interpretations "
            "have been persisted."
        )

    # ---------------------------------------------------------
    # Semantic embeddings
    # ---------------------------------------------------------

    embedding_rows = get_all_embeddings()

    stored_embeddings = {
        semantic_id: embedding
        for semantic_id, model_name, embedding
        in embedding_rows
    }

    if not stored_embeddings:
        raise ValueError(
            "No semantic embeddings are available. "
            "Generate embeddings for the approved semantic "
            "registry before running queries."
        )

    missing_embeddings = [
        entry.semantic_id
        for entry in catalog
        if entry.semantic_id not in stored_embeddings
    ]

    if missing_embeddings:
        raise ValueError(
            "Missing embeddings for "
            f"{len(missing_embeddings)} approved semantic columns."
        )

    # ---------------------------------------------------------
    # Database schema
    # ---------------------------------------------------------

    if database_schema is None:
        database_schema = get_database_schema(
            dataset_names=[
                dataset.dataset_name
                for dataset in registry.datasets
            ],
        )

    # ---------------------------------------------------------
    # Initial workflow state
    # ---------------------------------------------------------

    initial_state: NexaQueryState = {
        "user_query": query,
        "registry": registry,
        "catalog": catalog,
        "stored_embeddings": stored_embeddings,
        "database_schema": database_schema,
        "sql_validation_attempts": 0,
        "status": "initialized",
        "error": None,
    }

    # ---------------------------------------------------------
    # Execute workflow
    # ---------------------------------------------------------

    workflow = build_query_workflow()

    final_state = workflow.invoke(initial_state)

    return final_state