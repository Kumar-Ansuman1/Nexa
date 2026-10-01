from src.llm.schemas.join_plan import JoinPlan, JoinStep
from src.llm.schemas.query_plan import QueryPlan
from src.llm.schemas.registry import SemanticRegistry, ApprovalStatus


def build_join_plan(
    query_plan: QueryPlan,
    registry: SemanticRegistry,
) -> JoinPlan:

    required_datasets = set(query_plan.required_datasets)

    joins = []

    for relationship in registry.relationships:

        if relationship.approval_status != ApprovalStatus.APPROVED:
            continue

        if (
            relationship.source_dataset in required_datasets
            and relationship.target_dataset in required_datasets
        ):
            joins.append(
                JoinStep(
                    left_dataset=relationship.source_dataset,
                    left_column=relationship.source_column,
                    right_dataset=relationship.target_dataset,
                    right_column=relationship.target_column,
                )
            )

    return JoinPlan(joins=joins)