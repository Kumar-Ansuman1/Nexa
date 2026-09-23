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