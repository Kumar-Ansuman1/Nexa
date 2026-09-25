from pathlib import Path

from src.data.processing.cleaners import (
    clean_customer_feedback,
    clean_customers,
    clean_product_activity,
    clean_sales_leads,
    clean_support_tickets,
    clean_transactions,
)
from src.data.processing.loaders import load_csv


PROCESSED_DATA_PATH = Path("data/processed")


def process_dataset(filename, cleaner):
    df = load_csv(filename)
    return cleaner(df)


def main():
    PROCESSED_DATA_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    datasets = {
        "customers.csv": clean_customers,
        "product_activity.csv": clean_product_activity,
        "transactions.csv": clean_transactions,
        "sales_leads.csv": clean_sales_leads,
        "support_tickets.csv": clean_support_tickets,
        "customer_feedback.csv": clean_customer_feedback,
    }

    for filename, cleaner in datasets.items():
        df = process_dataset(filename, cleaner)

        output_path = PROCESSED_DATA_PATH / filename
        df.to_csv(output_path, index=False)

        print(f"Processed {filename}: {len(df)} rows")


if __name__ == "__main__":
    main()