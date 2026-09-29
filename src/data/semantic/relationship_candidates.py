import pandas as pd

from src.llm.schemas.relationship import (
    RelationshipCandidate,
    RelationshipSignals,
)
from src.llm.schemas.registry import SemanticRegistry

def are_roles_compatible(role_a: str, role_b: str) -> bool:
    compatible_roles = {
        ("identifier", "identifier"),
        ("identifier", "foreign_key"),
        ("foreign_key", "identifier"),
    }

    return (role_a, role_b) in compatible_roles

def are_datatypes_compatible(dtype_a: str, dtype_b: str) -> bool:
    if dtype_a == dtype_b:
        return True

    numeric_types = {
        "int8",
        "int16",
        "int32",
        "int64",
        "float16",
        "float32",
        "float64",
    }

    if dtype_a in numeric_types and dtype_b in numeric_types:
        return True

    return False

def calculate_name_similarity(name_a: str, name_b: str) -> float:
    name_a = name_a.lower().replace("_", " ").strip()
    name_b = name_b.lower().replace("_", " ").strip()

    if name_a == name_b:
        return 1.0

    words_a = set(name_a.split())
    words_b = set(name_b.split())

    if not words_a or not words_b:
        return 0.0

    intersection = words_a & words_b
    union = words_a | words_b

    return len(intersection) / len(union)

def calculate_value_overlap(
    values_a,
    values_b,
) -> float:
    set_a = set(values_a)
    set_b = set(values_b)

    if not set_a or not set_b:
        return 0.0

    intersection = set_a & set_b

    return len(intersection) / len(set_b)

def calculate_uniqueness_ratio(values) -> float:
    non_null_values = [
        value for value in values
        if value is not None
    ]

    if not non_null_values:
        return 0.0

    unique_values = len(set(non_null_values))

    return unique_values / len(non_null_values)

def calculate_candidate_score(
    role_compatible: bool,
    datatype_compatible: bool,
    name_similarity: float,
    value_overlap: float,
    source_uniqueness: float,
    target_uniqueness: float,
) -> float:
    score = 0.0

    if role_compatible:
        score += 0.25

    if datatype_compatible:
        score += 0.15

    score += name_similarity * 0.15
    score += value_overlap * 0.30

    uniqueness_difference = abs(
        source_uniqueness - target_uniqueness
    )

    score += (1 - uniqueness_difference) * 0.15

    return round(score, 4)

def generate_relationship_candidates(
    datasets: dict[str, pd.DataFrame],
    registry: SemanticRegistry,
) -> list[RelationshipCandidate]:

    candidates = []

    dataset_registry = {
        dataset.dataset_name: dataset
        for dataset in registry.datasets
    }

    dataset_names = list(datasets.keys())

    for i in range(len(dataset_names)):
        for j in range(i + 1, len(dataset_names)):

            source_dataset_name = dataset_names[i]
            target_dataset_name = dataset_names[j]

            source_df = datasets[source_dataset_name]
            target_df = datasets[target_dataset_name]

            source_registry = dataset_registry.get(
                source_dataset_name
            )
            target_registry = dataset_registry.get(
                target_dataset_name
            )

            if not source_registry or not target_registry:
                continue

            for source_column in source_registry.columns:

                if source_column.approval_status.value != "approved":
                    continue

                if source_column.source_column not in source_df.columns:
                    continue

                for target_column in target_registry.columns:

                    if target_column.approval_status.value != "approved":
                        continue

                    if target_column.source_column not in target_df.columns:
                        continue

                    role_compatible = are_roles_compatible(
                        source_column.approved_role,
                        target_column.approved_role,
                    )

                    datatype_compatible = are_datatypes_compatible(
                        str(source_df[source_column.source_column].dtype),
                        str(target_df[target_column.source_column].dtype),
                    )

                    source_values = (
                        source_df[source_column.source_column]
                        .dropna()
                        .tolist()
                    )

                    target_values = (
                        target_df[target_column.source_column]
                        .dropna()
                        .tolist()
                    )

                    name_similarity = calculate_name_similarity(
                        source_column.source_column,
                        target_column.source_column,
                    )

                    value_overlap = calculate_value_overlap(
                        source_values,
                        target_values,
                    )

                    source_uniqueness = calculate_uniqueness_ratio(
                        source_values
                    )

                    target_uniqueness = calculate_uniqueness_ratio(
                        target_values
                    )
                    cardinality = infer_cardinality(
                        source_uniqueness,
                        target_uniqueness,
                    )

                    candidate_score = calculate_candidate_score(
                        role_compatible=role_compatible,
                        datatype_compatible=datatype_compatible,
                        name_similarity=name_similarity,
                        value_overlap=value_overlap,
                        source_uniqueness=source_uniqueness,
                        target_uniqueness=target_uniqueness,
                    )

                    if not role_compatible:
                        continue

                    if value_overlap == 0:
                        continue

                    if candidate_score < 0.50:
                        continue

                    signals = RelationshipSignals(
                        role_compatible=role_compatible,
                        datatype_compatible=datatype_compatible,
                        name_similarity=name_similarity,
                        value_overlap=value_overlap,
                        source_uniqueness=source_uniqueness,
                        target_uniqueness=target_uniqueness,
                        cardinality=cardinality,
                    )

                    candidates.append(
                        RelationshipCandidate(
                            source_dataset=source_dataset_name,
                            source_column=source_column.source_column,
                            target_dataset=target_dataset_name,
                            target_column=target_column.source_column,
                            signals=signals,
                            candidate_score=candidate_score,
                        )
                    )

    return candidates

def infer_cardinality(
    source_uniqueness: float,
    target_uniqueness: float,
) -> str:
    if source_uniqueness >= 0.95 and target_uniqueness >= 0.95:
        return "one_to_one"

    if source_uniqueness >= 0.95 and target_uniqueness < 0.95:
        return "one_to_many"

    if source_uniqueness < 0.95 and target_uniqueness >= 0.95:
        return "many_to_one"

    return "many_to_many"