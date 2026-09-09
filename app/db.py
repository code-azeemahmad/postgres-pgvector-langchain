import asyncio
import os

from dotenv import load_dotenv
from langchain_postgres import PGEngine

# ============================================================
# Windows asyncio compatibility
# ============================================================

if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )


# ============================================================
# Environment
# ============================================================

load_dotenv()


POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "localhost",
)

POSTGRES_PORT = os.getenv(
    "POSTGRES_PORT",
    "5432",
)

POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
    "ai_knowledge",
)

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "postgres",
)

POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD",
    "postgres",
)


# ============================================================
# PostgreSQL connection
# ============================================================

CONNECTION_STRING = (
    f"postgresql+psycopg://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}"
    f"/{POSTGRES_DB}"
)


# ============================================================
# LangChain PostgreSQL engine
# ============================================================

pg_engine = PGEngine.from_connection_string(
    url=CONNECTION_STRING
)