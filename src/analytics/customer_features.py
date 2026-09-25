import pandas as pd


def build_customer_features(
    customers,
    activity,
    transactions,
    tickets,
    feedback,
):
    features = customers[
        [
            "customer_id",
            "plan",
            "company_size",
            "industry",
            "country",
            "acquisition_channel",
        ]
    ].copy()

    # Product activity
    activity_features = (
        activity.groupby("customer_id")
        .agg(
            activity_count=("event_id", "nunique"),
            active_months=(
                "timestamp",
                lambda x: x.dt.to_period("M").nunique(),
            ),
            integration_failures=(
                "event",
                lambda x: (x == "integration_failed").sum(),
            ),
            feature_usage_count=(
                "event",
                lambda x: (x == "feature_used").sum(),
            ),
        )
        .reset_index()
    )

    # Revenue
    successful_transactions = transactions[
        transactions["status"] == "successful"
    ]

    transaction_features = (
        successful_transactions.groupby("customer_id")
        .agg(
            revenue=("amount", "sum"),
            transaction_count=("transaction_id", "nunique"),
        )
        .reset_index()
    )

    # Support
    ticket_features = (
        tickets.groupby("customer_id")
        .agg(
            ticket_count=("ticket_id", "nunique"),
            integration_ticket_count=(
                "category",
                lambda x: (x == "Integration").sum(),
            ),
            avg_resolution_time=("resolution_time", "mean"),
        )
        .reset_index()
    )

    # Feedback
    feedback_features = (
        feedback.groupby("customer_id")
        .agg(
            feedback_count=("feedback_id", "nunique"),
        )
        .reset_index()
    )

    # Combine all customer-level features
    features = features.merge(
        activity_features,
        on="customer_id",
        how="left",
    )

    features = features.merge(
        transaction_features,
        on="customer_id",
        how="left",
    )

    features = features.merge(
        ticket_features,
        on="customer_id",
        how="left",
    )

    features = features.merge(
        feedback_features,
        on="customer_id",
        how="left",
    )

    # Customers without activity/transactions/tickets/feedback
    # should have zero counts rather than missing values.
    count_columns = [
        "activity_count",
        "active_months",
        "integration_failures",
        "feature_usage_count",
        "revenue",
        "transaction_count",
        "ticket_count",
        "integration_ticket_count",
        "feedback_count",
    ]

    features[count_columns] = features[count_columns].fillna(0)

    return features