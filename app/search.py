from app.ingest import get_vector_store


def semantic_search(
    query: str,
    k: int = 3,
    tenant_id: str | None = None,
    department: str | None = None,
):
    store = get_vector_store()

    filter_dict = {}

    if tenant_id is not None:
        filter_dict["tenant_id"] = tenant_id

    if department is not None:
        filter_dict["department"] = department

    return store.similarity_search(
        query,
        k=k,
        filter=filter_dict or None,
    )