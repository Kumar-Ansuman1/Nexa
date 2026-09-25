import pandas as pd


def total_tickets(tickets):
    return tickets["ticket_id"].nunique()


def monthly_ticket_volume(tickets):
    return (
        tickets.groupby(
            tickets["timestamp"].dt.to_period("M")
        )["ticket_id"]
        .nunique()
    )


def tickets_by_category(tickets):
    return (
        tickets.groupby("category")["ticket_id"]
        .nunique()
        .sort_values(ascending=False)
    )


def average_resolution_time(tickets):
    return tickets["resolution_time"].mean()


def unresolved_tickets(tickets):
    return tickets[
        tickets["resolved"] == False
    ]["ticket_id"].nunique()


def integration_tickets(tickets):
    return tickets[
        tickets["category"] == "Integration"
    ]["ticket_id"].nunique()


def tickets_by_plan(tickets, customers):
    merged = tickets.merge(
        customers[["customer_id", "plan"]],
        on="customer_id",
        how="left",
    )

    return (
        merged.groupby("plan")["ticket_id"]
        .nunique()
        .sort_values(ascending=False)
    )