from src.data.database.connection import get_connection


def create_datasets_table() -> None:
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,
            suggested_name TEXT NOT NULL,
            suggested_description TEXT NOT NULL,
            confidence REAL NOT NULL,
            approved_name TEXT,
            approved_description TEXT,
            approval_status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def create_columns_table() -> None:
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS columns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_id INTEGER NOT NULL,

            semantic_id TEXT NOT NULL UNIQUE,
            source_column TEXT NOT NULL,

            suggested_meaning TEXT NOT NULL,
            suggested_description TEXT NOT NULL,
            suggested_role TEXT NOT NULL,
            confidence REAL NOT NULL,
            evidence TEXT NOT NULL,

            approved_meaning TEXT,
            approved_description TEXT,
            approved_role TEXT,

            approval_status TEXT NOT NULL,

            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,

            FOREIGN KEY (dataset_id)
                REFERENCES datasets(id)
                ON DELETE CASCADE
        )
        """
    )

    connection.commit()
    connection.close()


def create_relationships_table() -> None:
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            source_dataset_id INTEGER NOT NULL,
            source_column_id INTEGER NOT NULL,

            target_dataset_id INTEGER NOT NULL,
            target_column_id INTEGER NOT NULL,

            relationship_type TEXT NOT NULL,

            confidence REAL NOT NULL,
            evidence TEXT NOT NULL,

            approval_status TEXT NOT NULL,

            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,

            FOREIGN KEY (source_dataset_id)
                REFERENCES datasets(id)
                ON DELETE CASCADE,

            FOREIGN KEY (source_column_id)
                REFERENCES columns(id)
                ON DELETE CASCADE,

            FOREIGN KEY (target_dataset_id)
                REFERENCES datasets(id)
                ON DELETE CASCADE,

            FOREIGN KEY (target_column_id)
                REFERENCES columns(id)
                ON DELETE CASCADE
        )
        """
    )

    connection.commit()
    connection.close()


def create_semantic_embeddings_table() -> None:
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS semantic_embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            semantic_id TEXT NOT NULL UNIQUE,
            model_name TEXT NOT NULL,
            embedding TEXT NOT NULL,

            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,

            FOREIGN KEY (semantic_id)
                REFERENCES columns(semantic_id)
                ON DELETE CASCADE
        )
        """
    )

    connection.commit()
    connection.close()


def initialize_database() -> None:
    create_datasets_table()
    create_columns_table()
    create_relationships_table()
    create_semantic_embeddings_table()