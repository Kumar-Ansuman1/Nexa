from pathlib import Path
import sqlite3

from src.data.database.data_loader import load_csv_directory_to_database


DATA_DIRECTORY = Path(r"C:\Code\Nexa\data\processed")
DATABASE_PATH = Path(r"C:\Code\Nexa\data\nexa.db")


def main() -> None:
    print("Loading CSV datasets into SQLite...")

    loaded_tables = load_csv_directory_to_database(
        directory=DATA_DIRECTORY,
        if_exists="replace",
    )

    print("\nLoaded tables:")
    for table in loaded_tables:
        print(f"  - {table}")

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        print("\nVerifying tables in SQLite...")

        for table_name in loaded_tables:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM sqlite_master
                WHERE type = 'table'
                  AND name = ?
                """,
                (table_name,),
            )

            exists = cursor.fetchone()[0] == 1

            assert exists, (
                f"Table '{table_name}' was not created."
            )

            cursor.execute(
                f'SELECT COUNT(*) FROM "{table_name}"'
            )

            row_count = cursor.fetchone()[0]

            print(
                f"  ✓ {table_name}: "
                f"{row_count} rows"
            )

        print("\nData loader test passed.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()