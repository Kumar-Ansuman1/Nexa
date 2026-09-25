import pandas as pd


def clean_customers(df):
    df = df.copy()

    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["signup_date"] = pd.to_datetime(df["signup_date"])
    df["country"] = df["country"].astype(str).str.strip()
    df["industry"] = df["industry"].astype(str).str.strip()
    df["company_size"] = pd.to_numeric(
        df["company_size"],
        errors="coerce",
    )
    df["plan"] = df["plan"].astype(str).str.strip()
    df["acquisition_channel"] = (
        df["acquisition_channel"]
        .astype(str)
        .str.strip()
    )

    return df


def clean_product_activity(df):
    df = df.copy()

    df["event_id"] = df["event_id"].astype(str).str.strip()
    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["event"] = df["event"].astype(str).str.strip()
    df["feature"] = df["feature"].astype(str).str.strip()

    return df


def clean_transactions(df):
    df = df.copy()

    df["transaction_id"] = (
        df["transaction_id"].astype(str).str.strip()
    )
    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )
    df["type"] = df["type"].astype(str).str.strip()
    df["status"] = df["status"].astype(str).str.strip()

    return df


def clean_sales_leads(df):
    df = df.copy()

    df["lead_id"] = df["lead_id"].astype(str).str.strip()
    df["company_size"] = pd.to_numeric(
        df["company_size"],
        errors="coerce",
    )
    df["industry"] = df["industry"].astype(str).str.strip()
    df["source"] = df["source"].astype(str).str.strip()
    df["plan_interest"] = df["plan_interest"].astype(str).str.strip()
    df["sales_stage"] = df["sales_stage"].astype(str).str.strip()
    df["deal_value"] = pd.to_numeric(
        df["deal_value"],
        errors="coerce",
    )
    df["outcome"] = df["outcome"].astype(str).str.strip()

    return df


def clean_support_tickets(df):
    df = df.copy()

    df["ticket_id"] = df["ticket_id"].astype(str).str.strip()
    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["message"] = df["message"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()
    df["resolution_time"] = pd.to_numeric(
        df["resolution_time"],
        errors="coerce",
    )
    df["resolved"] = df["resolved"].astype(bool)

    return df


def clean_customer_feedback(df):
    df = df.copy()

    df["feedback_id"] = df["feedback_id"].astype(str).str.strip()
    df["customer_id"] = df["customer_id"].astype(str).str.strip()
    df["date"] = pd.to_datetime(df["date"])
    df["feedback_text"] = (
        df["feedback_text"]
        .astype(str)
        .str.strip()
    )
    df["source"] = df["source"].astype(str).str.strip()

    return df