from src.query.sql.sql_generator import generate_sql


execution_plan = {
    "query_plan": {
        "metric": {
            "dataset": "transactions",
            "column": "amount",
        },
        "dimensions": [
            {
                "dataset": "customers",
                "column": "plan",
            }
        ],
        "operation": "sum",
        "time_phrase": "March 2026",
        "required_datasets": [
            "transactions",
            "customers",
        ],
    },
    "join_plan": {
        "joins": [
            {
                "left_dataset": "customers",
                "left_column": "customer_id",
                "right_dataset": "transactions",
                "right_column": "customer_id",
            }
        ]
    },
}


database_schema = """
customers:
- customer_id
- plan

transactions:
- transaction_id
- customer_id
- amount
- date
"""


result = generate_sql(
    execution_plan=execution_plan,
    database_schema=database_schema,
)

print("\nGenerated SQL:")
print(result.sql)