from langgraph.graph import END, START, StateGraph

from src.query.nodes.execution_planning import (
    build_execution_plan_node,
)
from src.query.nodes.join_planning import (
    build_join_plan_node,
)
from src.query.nodes.query_planning import (
    build_query_plan_node,
)
from src.query.nodes.resolution import (
    resolve_semantics_node,
)
from src.query.nodes.retrieval import (
    retrieve_semantic_candidates_node,
)
from src.query.nodes.semantic_selection import (
    select_semantics_node,
)
from src.query.nodes.sql_execution import (
    execute_sql_node,
)
from src.query.nodes.sql_generation import (
    generate_sql_node,
)
from src.query.nodes.sql_validation import (
    validate_sql_node,
)
from src.query.nodes.understanding import (
    understand_query_node,
)
from src.query.graph.routes import (
    route_after_sql_validation,
)
from src.query.state import NexaQueryState


def build_query_workflow():
    """
    Build the NEXA query workflow.

    The workflow converts a natural-language question into
    validated SQL and executes it only after successful
    validation.
    """

    graph = StateGraph(NexaQueryState)

    # ---------------------------------------------------------
    # Query understanding
    # ---------------------------------------------------------

    graph.add_node(
        "understand_query",
        understand_query_node,
    )

    graph.add_node(
        "retrieve_semantic_candidates",
        retrieve_semantic_candidates_node,
    )

    graph.add_node(
        "select_semantics",
        select_semantics_node,
    )

    graph.add_node(
        "resolve_semantics",
        resolve_semantics_node,
    )

    # ---------------------------------------------------------
    # Query planning
    # ---------------------------------------------------------

    graph.add_node(
        "build_query_plan",
        build_query_plan_node,
    )

    graph.add_node(
        "build_join_plan",
        build_join_plan_node,
    )

    graph.add_node(
        "build_execution_plan",
        build_execution_plan_node,
    )

    # ---------------------------------------------------------
    # SQL generation and validation
    # ---------------------------------------------------------

    graph.add_node(
        "generate_sql",
        generate_sql_node,
    )

    graph.add_node(
        "validate_sql",
        validate_sql_node,
    )

    graph.add_node(
        "execute_sql",
        execute_sql_node,
    )

    # ---------------------------------------------------------
    # Query flow
    # ---------------------------------------------------------

    graph.add_edge(
        START,
        "understand_query",
    )

    graph.add_edge(
        "understand_query",
        "retrieve_semantic_candidates",
    )

    graph.add_edge(
        "retrieve_semantic_candidates",
        "select_semantics",
    )

    graph.add_edge(
        "select_semantics",
        "resolve_semantics",
    )

    graph.add_edge(
        "resolve_semantics",
        "build_query_plan",
    )

    graph.add_edge(
        "build_query_plan",
        "build_join_plan",
    )

    graph.add_edge(
        "build_join_plan",
        "build_execution_plan",
    )

    graph.add_edge(
        "build_execution_plan",
        "generate_sql",
    )

    graph.add_edge(
        "generate_sql",
        "validate_sql",
    )

    # ---------------------------------------------------------
    # SQL validation routing
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        "validate_sql",
        route_after_sql_validation,
        {
            "execute_sql": "execute_sql",
            "generate_sql": "generate_sql",
            "sql_validation_failed": END,
        },
    )

    # ---------------------------------------------------------
    # Workflow completion
    # ---------------------------------------------------------

    graph.add_edge(
        "execute_sql",
        END,
    )

    return graph.compile()