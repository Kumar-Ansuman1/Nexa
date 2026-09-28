from pathlib import Path
import sqlite3


DATABASE_PATH = Path("data/nexa.db")


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection