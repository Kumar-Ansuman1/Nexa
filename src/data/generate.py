from src.data.generators import (
    generate_customers,
    generate_product_activity,
    generate_transactions,
    generate_sales_leads,
    generate_support_tickets,
    generate_customer_feedback,
)

def main():
    customers = generate_customers()

    activity = generate_product_activity(customers)
    transactions = generate_transactions(customers)
    leads = generate_sales_leads(customers)
    tickets = generate_support_tickets(customers)
    feedback = generate_customer_feedback(customers)

    customers.to_csv("data/raw/customers.csv", index=False)
    activity.to_csv("data/raw/product_activity.csv", index=False)
    transactions.to_csv("data/raw/transactions.csv", index=False)
    leads.to_csv("data/raw/sales_leads.csv", index=False)
    tickets.to_csv("data/raw/support_tickets.csv", index=False)
    feedback.to_csv("data/raw/customer_feedback.csv", index=False)

    print(f"Customers: {len(customers)}")
    print(f"Activity events: {len(activity)}")
    print(f"Transactions: {len(transactions)}")
    print(f"Sales leads: {len(leads)}")
    print(f"Support tickets: {len(tickets)}")
    print(f"Customer feedback: {len(feedback)}")

if __name__ == "__main__":
    main()