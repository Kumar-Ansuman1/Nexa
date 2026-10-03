from pathlib import Path
import tempfile

import pandas as pd

from src.data.ingestion.profile_loader import load_and_profile_csv


def test_load_and_profile_csv():
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_path = Path(temp_dir) / "employees.csv"

        dataframe = pd.DataFrame(
    {
        "employee_id": [
            f"EMP{i:03d}"
            for i in range(1, 41)
        ],
        "name": [
            f"Employee {i}"
            for i in range(1, 41)
        ],
        "department": (
            ["Engineering"] * 38
            + ["Sales"] * 2
        ),
        "salary": [
            50000 + (i * 1000)
            for i in range(40)
        ],
    }
    )

        dataframe.to_csv(csv_path, index=False)

        profile = load_and_profile_csv(csv_path)

        assert profile["name"] == "employees"
        assert profile["rows"] == 40
        assert profile["columns"] == 4
        assert "column_profiles" in profile
        assert len(profile["column_profiles"]) == 4

        columns = {
            column["name"]: column
            for column in profile["column_profiles"]
        }

        assert columns["employee_id"]["semantic_type"] == "identifier"
        assert columns["salary"]["semantic_type"] == "numeric"
        assert columns["department"]["semantic_type"] == "categorical"


if __name__ == "__main__":
    test_load_and_profile_csv()
    print("CSV profiling tests passed.")