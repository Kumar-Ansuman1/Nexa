import pandas as pd

from src.analytics.support_metrics import (
    total_tickets,
    monthly_ticket_volume,
    tickets_by_category,
    average_resolution_time,
    unresolved_tickets,
    integration_tickets,
    tickets_by_plan,
)


tickets = pd.read_csv(
    "data/processed/support_tickets.csv",
    parse_dates=["timestamp"],
)

customers = pd.read_csv(
    "data/processed/customers.csv",
    parse_dates=["signup_date"],
)


print("Total tickets:")
print(total_tickets(tickets))

print("\nMonthly ticket volume:")
print(monthly_ticket_volume(tickets))

print("\nTickets by category:")
print(tickets_by_category(tickets))

print("\nAverage resolution time:")
print(average_resolution_time(tickets))

print("\nUnresolved tickets:")
print(unresolved_tickets(tickets))

print("\nIntegration tickets:")
print(integration_tickets(tickets))

print("\nTickets by plan:")
print(tickets_by_plan(tickets, customers))