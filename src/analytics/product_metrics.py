import pandas as pd


def total_activity_events(activity):
    return activity["event_id"].nunique()


def monthly_activity(activity):
    return (
        activity.groupby(
            activity["timestamp"].dt.to_period("M")
        )["event_id"]
        .nunique()
    )


def activity_by_event(activity):
    return (
        activity.groupby("event")["event_id"]
        .nunique()
        .sort_values(ascending=False)
    )


def activity_by_plan(activity, customers):
    merged = activity.merge(
        customers[["customer_id", "plan"]],
        on="customer_id",
        how="left",
    )

    return (
        merged.groupby("plan")["event_id"]
        .nunique()
        .sort_values(ascending=False)
    )


def feature_usage(activity):
    return (
        activity.groupby("feature")["event_id"]
        .nunique()
        .sort_values(ascending=False)
    )


def integration_failures(activity):
    return activity[
        activity["event"] == "integration_failed"
    ]["event_id"].nunique()


def active_customers(activity):
    return activity["customer_id"].nunique()