import sqlite3

from src.data.database.connection import DATABASE_PATH
from src.data.database.schema import initialize_database


initialize_database()

connection = sqlite3.connect(DATABASE_PATH)

tables = connection.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
    """
).fetchall()

connection.close()

print("Tables:")
for table in tables:
    print(table[0])