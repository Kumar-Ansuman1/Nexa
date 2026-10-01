import pandas as pd

from src.data.profiling.profiler import profile_dataset
from src.data.semantic.registry.interpreter import interpret_dataset


df = pd.read_csv("data/raw/customers.csv")

profile = profile_dataset(
    df,
    name="customers",
)

result = interpret_dataset(profile)

print(result.model_dump_json(indent=2))