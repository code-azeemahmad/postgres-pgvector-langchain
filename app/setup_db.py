from app.db import pg_engine
from app.ingest import (
    TABLE_NAME,
    VECTOR_SIZE,
    add_documents,
)


def setup():
    print("Recreating PostgreSQL vector store...")

    pg_engine.init_vectorstore_table(
        table_name=TABLE_NAME,
        vector_size=VECTOR_SIZE,
        overwrite_existing=True,
    )

    print("Loading demo documents...")

    add_documents()

    print("Database setup complete.")


if __name__ == "__main__":
    setup()