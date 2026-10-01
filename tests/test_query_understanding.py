from src.data.semantic.query_understanding import understand_query


query = "Show me revenue by subscription plan in March 2026."

result = understand_query(query)

print(result.model_dump())