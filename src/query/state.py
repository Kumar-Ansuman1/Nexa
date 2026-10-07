from typing import Any, TypedDict
from src.llm.schemas.query_understanding import QueryUnderstanding
from src.data.semantic.catalog.catalog import SemanticCatalogEntry
from src.llm.schemas.execution_plan import ExecutionPlan
from src.llm.schemas.join_plan import JoinPlan
from src.llm.schemas.query_plan import QueryPlan
from src.llm.schemas.semantic_query import SemanticQuery
from src.llm.schemas.registry import SemanticRegistry


class NexaQueryState(TypedDict, total=False):
    """
    Shared state for the NEXA query workflow.

    The state is progressively populated as a natural-language
    question moves through semantic understanding, resolution,
    planning, SQL generation, validation, and execution.
    """

    # ---------------------------------------------------------
    # Input
    # ---------------------------------------------------------

    user_query: str

    # ---------------------------------------------------------
    # Runtime semantic data
    # ---------------------------------------------------------

    catalog: list[SemanticCatalogEntry]
    stored_embeddings: dict[str, list[float]]

    
    # ---------------------------------------------------------
    # Semantic understanding and resolution
    # ---------------------------------------------------------

    semantic_query: SemanticQuery
    resolved_query: dict[str, Any]
    understanding: QueryUnderstanding

    # ---------------------------------------------------------
    # Candidate Columns
    # ---------------------------------------------------------
    candidates: dict[str, Any]


    registry: SemanticRegistry


    # ---------------------------------------------------------
    # Query planning
    # ---------------------------------------------------------

    query_plan: QueryPlan
    join_plan: JoinPlan
    execution_plan: ExecutionPlan

    database_schema: str

    # ---------------------------------------------------------
    # SQL generation and validation
    # ---------------------------------------------------------

    generated_sql: str
    validated_sql: str

    # ---------------------------------------------------------
    # SQL execution
    # ---------------------------------------------------------

    rows: list[dict[str, Any]]
    columns: list[str]

    # ---------------------------------------------------------
    # Workflow control
    # ---------------------------------------------------------

    sql_validation_attempts: int
    status: str
    error: str | None