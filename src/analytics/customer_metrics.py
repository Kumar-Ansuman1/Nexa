import pandas as pd


def total_customers(customers):
    return customers["customer_id"].nunique()


def customers_by_plan(customers):
    return (
        customers.groupby("plan")["customer_id"]
        .nunique()
        .sort_values(ascending=False)
    )


def new_customers_by_month(customers):
    return (
        customers.groupby(
            customers["signup_date"].dt.to_period("M")
        )["customer_id"]
        .nunique()
    )


def customers_by_country(customers):
    return (
        customers.groupby("country")["customer_id"]
        .nunique()
        .sort_values(ascending=False)
    )


def customers_by_industry(customers):
    return (
        customers.groupby("industry")["customer_id"]
        .nunique()
        .sort_values(ascending=False)
    )


def customers_by_acquisition_channel(customers):
    return (
        customers.groupby("acquisition_channel")["customer_id"]
        .nunique()
        .sort_values(ascending=False)
    )


def average_company_size(customers):
    return customers["company_size"].mean()