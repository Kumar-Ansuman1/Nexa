from src.data.database.repositories.relationships import get_relationships


relationships = get_relationships()

for relationship in relationships:
    print(relationship.model_dump_json(indent=2))