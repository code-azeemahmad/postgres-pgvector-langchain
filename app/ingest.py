import os

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import Column, PGVectorStore

from app.db import pg_engine

load_dotenv()


OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

EMBEDDING_MODEL = os.getenv(
    "OLLAMA_EMBEDDING_MODEL",
    "nomic-embed-text",
)

TABLE_NAME = "knowledge_documents"


embeddings = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=OLLAMA_BASE_URL,
)


# Determine embedding dimension dynamically.
VECTOR_SIZE = len(
    embeddings.embed_query("dimension check")
)


def initialize_vector_store():
    """
    Create the PostgreSQL vector table.
    """

    pg_engine.init_vectorstore_table(
        table_name=TABLE_NAME,
        vector_size=VECTOR_SIZE,
        metadata_columns=[
            Column("department", "VARCHAR"),
            Column("tenant_id", "VARCHAR"),
        ],
    )

    print(
        f"Vector store initialized: "
        f"{TABLE_NAME} ({VECTOR_SIZE} dimensions)"
    )


def get_vector_store():
    """
    Create a PGVectorStore instance.
    """

    return PGVectorStore.create_sync(
        engine=pg_engine,
        table_name=TABLE_NAME,
        embedding_service=embeddings,
    )


def add_documents():
    """
    Insert our demo documents.
    """

    documents = [
    Document(
        page_content=(
            "Enterprise refund policy: "
            "All refunds must be processed within "
            "30 days of the invoice date."
        ),
        metadata={
            "department": "finance",
            "tenant_id": "tenant_A",
        },
    ),

    Document(
        page_content=(
            "Vacation policy: "
            "Full-time employees receive "
            "20 days of paid time off per year."
        ),
        metadata={
            "department": "hr",
            "tenant_id": "tenant_A",
        },
    ),

    Document(
        page_content=(
            "Remote work policy: "
            "Employees may work remotely up to "
            "3 days per week with manager approval."
        ),
        metadata={
            "department": "hr",
            "tenant_id": "tenant_A",
        },
    ),

    Document(
        page_content=(
            "Tenant B refund policy: "
            "Refund requests must be submitted "
            "within 14 days of purchase."
        ),
        metadata={
            "department": "finance",
            "tenant_id": "tenant_B",
        },
    ),

    Document(
        page_content=(
            "Tenant B vacation policy: "
            "Employees receive 25 days of PTO."
        ),
        metadata={
            "department": "hr",
            "tenant_id": "tenant_B",
        },
    ),
]

    store = get_vector_store()

    ids = store.add_documents(documents)

    print(f"Inserted {len(ids)} documents.")