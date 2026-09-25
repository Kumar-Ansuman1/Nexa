import random

import pandas as pd

from src.data import config

random.seed(config.RANDOM_SEED)

def generate_customers():
    customer_ids = [
        f"C{i:04d}"
        for i in range(1, config.NUM_CUSTOMERS + 1)
    ]

    signup_dates = [
        pd.Timestamp(config.START_DATE)
        + pd.Timedelta(days=random.randint(0, 119))
        for _ in range(config.NUM_CUSTOMERS)
    ]

    countries = [
    random.choices(
        population=config.COUNTRIES,
        weights=[
            config.COUNTRY_WEIGHTS[country]
            for country in config.COUNTRIES
        ],
        k=1,
    )[0]
    for _ in range(config.NUM_CUSTOMERS)
    ]

    industries = [
    random.choices(
        population=config.INDUSTRIES,
        weights=[
            config.INDUSTRY_WEIGHTS[industry]
            for industry in config.INDUSTRIES
        ],
        k=1,
    )[0]
    for _ in range(config.NUM_CUSTOMERS)
    ]

    company_sizes = []

    for _ in range(config.NUM_CUSTOMERS):
        size = random.choices(
            population=["Micro", "Small", "Medium", "Large"],
            weights=[40, 35, 20, 5],
            k=1,
        )[0]

        company_sizes.append(size)

        employee_counts = []

    size_ranges = {
        "Micro": (1, 10),
        "Small": (11, 50),
        "Medium": (51, 200),
        "Large": (201, 1000),
    }

    for size in company_sizes:
        minimum, maximum = size_ranges[size]
        employee_counts.append(random.randint(minimum, maximum))


    plans = []

    for size in company_sizes:
        if size == "Micro":
            plan = random.choices(
                population=["Free", "Starter", "Business"],
                weights=[75, 24, 1],
                k=1,
            )[0]

        elif size == "Small":
            plan = random.choices(
                population=["Free", "Starter", "Business"],
                weights=[40, 50, 10],
                k=1,
            )[0]

        elif size == "Medium":
            plan = random.choices(
                population=["Free", "Starter", "Business"],
                weights=[15, 50, 35],
                k=1,
            )[0]

        else:
            plan = random.choices(
                population=["Free", "Starter", "Business"],
                weights=[5, 25, 70],
                k=1,
            )[0]

        plans.append(plan)

    acquisition_channels = [
    random.choices(
        population=config.ACQUISITION_CHANNELS,
        weights=[
            config.ACQUISITION_CHANNEL_WEIGHTS[channel]
            for channel in config.ACQUISITION_CHANNELS
        ],
        k=1,
    )[0]
    for _ in range(config.NUM_CUSTOMERS)
    ]

    customers = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "signup_date": signup_dates,
            "country": countries,
            "industry": industries,
            "company_size": employee_counts,
            "plan": plans,
            "acquisition_channel": acquisition_channels,
        }
    )

    return customers

def generate_product_activity(customers):
    activity_records = []

    for _, customer in customers.iterrows():
        minimum, maximum = config.PLAN_ACTIVITY_RANGES[customer["plan"]]
        base_events = random.randint(minimum, maximum)

        start_date = customer["signup_date"]
        end_date = pd.Timestamp(config.END_DATE)

        # Determine whether this customer is affected by the
        # simulated integration problem.
        affected_probability = config.AFFECTED_BASE_PROBABILITY

        if customer["plan"] == "Business":
            affected_probability += 0.10
        elif customer["plan"] == "Starter":
            affected_probability += 0.03

        is_affected = random.random() < affected_probability

        # Generate activity across the available months.
        current_month = start_date.to_period("M")
        final_month = end_date.to_period("M")

        months = pd.period_range(
            start=current_month,
            end=final_month,
            freq="M",
        )

        for month in months:
            month_number = month.month

            if is_affected:
                multiplier = config.AFFECTED_ACTIVITY_MULTIPLIERS[
                    month_number
                ]
            else:
                multiplier = 1.0

            monthly_count = max(
                1,
                int(base_events * multiplier / len(months)),
            )

            for _ in range(monthly_count):
                month_start = month.start_time
                month_end = min(month.end_time, end_date)

                if month_start < start_date:
                    month_start = start_date

                if month_start > month_end:
                    continue

                timestamp = month_start + pd.Timedelta(
                    seconds=random.randint(
                        0,
                        int((month_end - month_start).total_seconds()),
                    )
                )

                event = random.choices(
                    population=config.EVENT_TYPES,
                    weights=[
                        config.EVENT_WEIGHTS[event_type]
                        for event_type in config.EVENT_TYPES
                    ],
                    k=1,
                )[0]

                feature = random.choice(config.FEATURES)

                activity_records.append(
                    {
                        "event_id": f"E{len(activity_records) + 1:06d}",
                        "customer_id": customer["customer_id"],
                        "timestamp": timestamp,
                        "event": event,
                        "feature": feature,
                    }
                )

    return pd.DataFrame(activity_records)


def generate_transactions(customers):
    transaction_records = []

    transaction_id = 1

    plan_prices = {
        "Free": 0,
        "Starter": 49,
        "Business": 199,
    }

    for _, customer in customers.iterrows():
        signup_date = customer["signup_date"]
        end_date = pd.Timestamp(config.END_DATE)

        current_date = signup_date

        while current_date <= end_date:
            plan = customer["plan"]
            amount = plan_prices[plan]

            if amount > 0:
                transaction_records.append(
                    {
                        "transaction_id": f"T{transaction_id:06d}",
                        "customer_id": customer["customer_id"],
                        "date": current_date,
                        "amount": amount,
                        "type": "subscription",
                        "status": "successful",
                    }
                )

                transaction_id += 1

            current_date += pd.DateOffset(months=1)

    return pd.DataFrame(transaction_records)


def generate_sales_leads(customers):
    lead_records = []

    outcomes = [
        "Converted",
        "Lost",
        "In Progress",
    ]

    sources = [
        "Website",
        "Referral",
        "Paid Ads",
        "Partner",
        "Outbound",
    ]

    stages = [
        "New",
        "Qualified",
        "Demo",
        "Proposal",
        "Negotiation",
    ]

    for i in range(1, config.NUM_LEADS + 1):
        company_size = random.randint(5, 1000)

        if company_size <= 50:
            plan_interest = random.choices(
                ["Free", "Starter", "Business"],
                weights=[50, 45, 5],
                k=1,
            )[0]
        elif company_size <= 200:
            plan_interest = random.choices(
                ["Starter", "Business"],
                weights=[60, 40],
                k=1,
            )[0]
        else:
            plan_interest = random.choices(
                ["Starter", "Business"],
                weights=[25, 75],
                k=1,
            )[0]

        outcome = random.choice(outcomes)

        converted_customer_id = None

        if outcome == "Converted":
            converted_customer_id = random.choice(
                customers["customer_id"].tolist()
            )

        lead_records.append(
            {
                "lead_id": f"L{i:06d}",
                "company_size": company_size,
                "industry": random.choice(config.INDUSTRIES),
                "source": random.choice(sources),
                "plan_interest": plan_interest,
                "sales_stage": random.choice(stages),
                "deal_value": random.randint(500, 20000),
                "outcome": outcome,
                "converted_customer_id": converted_customer_id,
            }
        )

    return pd.DataFrame(lead_records)


def generate_support_tickets(customers):
    ticket_records = []

    messages = {
        "Billing": [
            "I was charged incorrectly this month.",
            "I have a question about my invoice.",
            "Why was my payment charged twice?",
        ],
        "Integration": [
            "The integration is not syncing correctly.",
            "Our integration stopped working.",
            "The integration keeps failing.",
            "We are having problems connecting our tools.",
        ],
        "Bug": [
            "Something is not working correctly.",
            "The application shows an unexpected error.",
            "I found a bug in the dashboard.",
        ],
        "Account": [
            "I cannot access my account.",
            "I need help changing our account settings.",
        ],
        "Performance": [
            "The dashboard is loading slowly.",
            "The application has become slower recently.",
        ],
        "Feature Request": [
            "It would be useful to have this feature.",
            "Can you add more options to the dashboard?",
        ],
        "Other": [
            "I need help with something.",
            "I have a question about the product.",
        ],
    }

    categories = list(messages.keys())

    ticket_id = 1

    for _, customer in customers.iterrows():
        ticket_count = random.randint(1, 8)

        for _ in range(ticket_count):
            category = random.choices(
                categories,
                weights=[10, 20, 15, 10, 10, 10, 25],
                k=1,
            )[0]

            message = random.choice(messages[category])

            timestamp = pd.Timestamp(
                config.START_DATE
                ) + pd.Timedelta(
                    seconds=random.randint(
                        0,
                        int(
                           (
                            pd.Timestamp(config.END_DATE)
                            - pd.Timestamp(config.START_DATE)
                            ).total_seconds()
                        ),
                    )               
                )

            if timestamp < customer["signup_date"]:
                timestamp = customer["signup_date"]

            ticket_records.append(
                {
                    "ticket_id": f"ST{ticket_id:06d}",
                    "customer_id": customer["customer_id"],
                    "timestamp": timestamp,
                    "message": message,
                    "category": category,
                    "resolution_time": round(
                        random.uniform(1, 72), 2
                    ),
                    "resolved": random.choice([True, True, True, False]),
                }
            )

            ticket_id += 1

    return pd.DataFrame(ticket_records)


def generate_customer_feedback(customers):
    feedback_records = []

    positive_feedback = [
        "The product is easy to use.",
        "The dashboard is very useful.",
        "Our team has had a good experience.",
        "The product has improved our workflow.",
    ]

    negative_feedback = [
        "The product has been difficult to use recently.",
        "We are having too many problems.",
        "The experience has become frustrating.",
        "We are considering other options.",
    ]

    integration_feedback = [
        "The integration setup is confusing.",
        "The integration keeps causing problems.",
        "We need a more reliable integration.",
        "Our integration is not working properly.",
    ]

    feedback_id = 1

    for _, customer in customers.iterrows():
        count = random.randint(1, 4)

        for _ in range(count):
            month = random.randint(1, 4)

            if month >= 3 and random.random() < 0.35:
                text = random.choice(integration_feedback)
                source = random.choice(["Survey", "Interview", "Support"])
            elif random.random() < 0.7:
                text = random.choice(positive_feedback)
                source = random.choice(["Survey", "Review", "In-app"])
            else:
                text = random.choice(negative_feedback)
                source = random.choice(["Survey", "Interview", "Support"])

            date = pd.Timestamp(
                f"2026-{month:02d}-01"
            ) + pd.Timedelta(
                days=random.randint(0, 27)
            )

            if date < customer["signup_date"]:
                date = customer["signup_date"]

            feedback_records.append(
                {
                    "feedback_id": f"F{feedback_id:06d}",
                    "customer_id": customer["customer_id"],
                    "date": date,
                    "feedback_text": text,
                    "source": source,
                }
            )

            feedback_id += 1

    return pd.DataFrame(feedback_records)
