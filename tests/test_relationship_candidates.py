import pandas as pd

from src.data.profiling.profiler import profile_dataset
from src.data.semantic.relationship_candidates import (
    generate_relationship_candidates,
)
from src.llm.schemas.registry import (
    ApprovalStatus,
    ColumnRegistryEntry,
    DatasetRegistryEntry,
    SemanticRegistry,
)


DATA_PATH = "data/raw"


def build_approved_registry(datasets: dict[str, pd.DataFrame]) -> SemanticRegistry:
    registry_datasets = []

    for dataset_name, df in datasets.items():

        profile = profile_dataset(df, dataset_name)

        columns = []

        for column in profile["column_profiles"]:

            role = column["semantic_type"]

            if column["name"].endswith("_id"):
                series = df[column["name"]].dropna()

                uniqueness_ratio = (
                    series.nunique() / len(series)
                    if len(series) > 0
                    else 0
                )

                if uniqueness_ratio >= 0.95:
                    role = "identifier"
                else:
                    role = "foreign_key"
                    
            columns.append(
                ColumnRegistryEntry(
                    source_column=column["name"],
                    suggested_meaning=column["name"],
                    suggested_description="Test semantic mapping",
                    suggested_role=role,
                    confidence=1.0,
                    evidence=["Test registry"],
                    approved_meaning=column["name"],
                    approved_description="Test semantic mapping",
                    approved_role=role,
                    approval_status=ApprovalStatus.APPROVED,
                )
            )

        registry_datasets.append(
            DatasetRegistryEntry(
                dataset_name=dataset_name,
                suggested_name=dataset_name,
                suggested_description="Test dataset",
                confidence=1.0,
                approved_name=dataset_name,
                approved_description="Test dataset",
                approval_status=ApprovalStatus.APPROVED,
                columns=columns,
            )
        )

    return SemanticRegistry(
        datasets=registry_datasets,
        relationships=[],
    )


def main():

    datasets = {
        "customers": pd.read_csv(
            f"{DATA_PATH}/customers.csv"
        ),
        "transactions": pd.read_csv(
            f"{DATA_PATH}/transactions.csv"
        ),
        "product_activity": pd.read_csv(
            f"{DATA_PATH}/product_activity.csv"
        ),
        "support_tickets": pd.read_csv(
            f"{DATA_PATH}/support_tickets.csv"
        ),
        "customer_feedback": pd.read_csv(
            f"{DATA_PATH}/customer_feedback.csv"
        ),
        "sales_leads": pd.read_csv(
            f"{DATA_PATH}/sales_leads.csv"
        ),
    }

    registry = build_approved_registry(datasets)

    candidates = generate_relationship_candidates(
        datasets=datasets,
        registry=registry,
    )

    print("\nRelationship Candidates")
    print("=" * 60)

    for candidate in candidates:

        print(
            f"\n{candidate.source_dataset}."
            f"{candidate.source_column}"
            f"  →  "
            f"{candidate.target_dataset}."
            f"{candidate.target_column}"
        )

        print(
            f"Score: {candidate.candidate_score}"
        )

        print(
            f"Signals: {candidate.signals.model_dump()}"
        )


if __name__ == "__main__":
    main()