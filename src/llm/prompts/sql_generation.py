def build_sql_generation_prompt(
    execution_plan: dict,
    database_schema: str,
) -> str:

    return f"""
You are the SQL generation component of Nexa.

Your job is to generate a SQL query from the provided execution plan.

Execution plan:
{execution_plan}

Database schema:
{database_schema}

Rules:

- Generate SQL only from the provided execution plan and database schema.
- Do not invent tables.
- Do not invent columns.
- Do not invent relationships.
- Use only the datasets and columns represented in the execution plan.
- Use the joins provided by the execution plan.
- Apply the exact aggregation operation from the execution plan.
- Apply the requested time period when one is provided.
- Include every required dimension from the execution plan.
- Use GROUP BY when dimensions are present.
- Preserve the exact dataset and column mapping from the execution plan.
- Do not substitute a semantically similar column.
- Do not substitute a different dataset containing a similarly named column.

SQL qualification rules:

- Always qualify every metric column with its table alias.
- Always qualify every dimension column with its table alias.
- Always qualify every join column with its table alias.
- Use aliases that clearly map to the corresponding dataset.
- The metric must appear as:
      AGGREGATION(table_alias.metric_column)
  where AGGREGATION is the exact operation from the execution plan.
- Do not generate unqualified metric expressions such as:
      SUM(revenue)
      AVG(amount)
- Do not generate unqualified dimension references when multiple tables are involved.

Example:

Execution plan metric:
    dataset = transactions
    column = revenue
    operation = sum

Correct:
    SUM(t.revenue)

Incorrect:
    SUM(revenue)

Incorrect:
    SUM(c.revenue)

Return only the SQL query.
"""