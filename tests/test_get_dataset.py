from src.data.database.repositories.datasets import get_dataset


dataset = get_dataset(1)

print(dataset.model_dump_json(indent=2) if dataset else "Dataset not found")