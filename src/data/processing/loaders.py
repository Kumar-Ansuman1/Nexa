from pathlib import Path

import pandas as pd


RAW_DATA_PATH = Path("data/raw")


def load_csv(filename):
    path = RAW_DATA_PATH / filename
    return pd.read_csv(path)