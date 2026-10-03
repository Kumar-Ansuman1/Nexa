from pathlib import Path
import tempfile

import pandas as pd

from src.data.ingestion.csv_loader import (
    CSVIngestionError,
    load_csv,
    load_csv_directory,
)


def main():
    with tempfile.TemporaryDirectory() as temp_dir:

        temp_path = Path(temp_dir)

        # --------------------------------------------
        # Test single CSV
        # --------------------------------------------

        first_csv = temp_path / "employees.csv"

        pd.DataFrame(
            {
                "employee_id": [1, 2, 3],
                "name": ["Alice", "Bob", "Charlie"],
                "salary": [50000, 60000, 70000],
            }
        ).to_csv(
            first_csv,
            index=False,
        )

        dataset_name, dataframe = load_csv(first_csv)

        assert dataset_name == "employees"
        assert list(dataframe.columns) == [
            "employee_id",
            "name",
            "salary",
        ]
        assert len(dataframe) == 3

        # --------------------------------------------
        # Test another completely unrelated dataset
        # --------------------------------------------

        second_csv = temp_path / "products.csv"

        pd.DataFrame(
            {
                "product_code": ["P1", "P2"],
                "price": [100, 250],
            }
        ).to_csv(
            second_csv,
            index=False,
        )

        dataset_name, dataframe = load_csv(second_csv)

        assert dataset_name == "products"
        assert list(dataframe.columns) == [
            "product_code",
            "price",
        ]
        assert len(dataframe) == 2

        # --------------------------------------------
        # Test directory loading
        # --------------------------------------------

        datasets = load_csv_directory(temp_path)

        assert set(datasets.keys()) == {
            "employees",
            "products",
        }

        assert len(datasets["employees"]) == 3
        assert len(datasets["products"]) == 2

        # --------------------------------------------
        # Test invalid extension
        # --------------------------------------------

        invalid_file = temp_path / "test.txt"
        invalid_file.write_text("hello")

        try:
            load_csv(invalid_file)
            raise AssertionError(
                "Expected CSVIngestionError"
            )
        except CSVIngestionError:
            pass

    print("CSV ingestion tests passed.")


if __name__ == "__main__":
    main()