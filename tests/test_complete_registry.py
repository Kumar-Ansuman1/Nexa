from src.data.database.repositories.datasets import get_dataset


dataset = get_dataset(2)

if dataset is None:
    print("Dataset not found")
else:
    print(dataset.model_dump_json(indent=2))