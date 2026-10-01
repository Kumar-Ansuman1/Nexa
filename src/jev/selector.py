from src.llm.schemas.retrieval import SemanticCandidate
from src.jev.client import ask_jev
from src.jev.schemas.selection import JevSelection


def select_semantics(
    query: str,
    metric_candidates: list[SemanticCandidate],
    dimension_candidates: list[SemanticCandidate],
) -> JevSelection:

    metric_options = {
        candidate.semantic_id: candidate.approved_meaning
        for candidate in metric_candidates
    }

    dimension_options = {
        candidate.semantic_id: candidate.approved_meaning
        for candidate in dimension_candidates
    }

    state = {
        "query": query,
        "metric_candidates": metric_options,
        "dimension_candidates": dimension_options,
    }

    questions = {
        "metric": {
            "type": "choice",
            "instructions": (
                "Select the semantic ID that best represents "
                "the metric the user wants to analyze."
            ),
            "criteria": metric_options,
        },
        "dimension": {
            "type": "choice",
            "instructions": (
                "Select the semantic ID that best represents "
                "the dimension the user wants to group by."
            ),
            "criteria": dimension_options,
        },
    }

    result = ask_jev(
        state=state,
        questions=questions,
    )

    answers = result["answers"]

    return JevSelection(
        metric=answers["metric"]["choice"],
        dimensions=[
            answers["dimension"]["choice"]
        ],
    )