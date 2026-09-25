import pandas as pd


def total_revenue(transactions):
    successful = transactions[
        transactions["status"] == "successful"
    ]

    return successful["amount"].sum()


def monthly_revenue(transactions):
    successful = transactions[
        transactions["status"] == "successful"
    ]

    return (
        successful.groupby(
            successful["date"].dt.to_period("M")
        )["amount"]
        .sum()
    )


def revenue_by_plan(transactions, customers):
    successful = transactions[
        transactions["status"] == "successful"
    ]

    merged = successful.merge(
        customers[["customer_id", "plan"]],
        on="customer_id",
        how="left",
    )

    return (
        merged.groupby("plan")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


def monthly_revenue_by_plan(transactions, customers):
    successful = transactions[
        transactions["status"] == "successful"
    ]

    merged = successful.merge(
        customers[["customer_id", "plan"]],
        on="customer_id",
        how="left",
    )

    return (
        merged.groupby(
            [
                merged["date"].dt.to_period("M"),
                "plan",
            ]
        )["amount"]
        .sum()
    )


def transaction_status_counts(transactions):
    return transactions["status"].value_counts()


def total_refunds(transactions):
    refunded = transactions[
        transactions["status"] == "refunded"
    ]

    return refunded["amount"].sum()