from __future__ import annotations


def make_retriever(vectordb, search_type: str, k: int, fetch_k: int):
    return vectordb.as_retriever(
        search_type=search_type,
        search_kwargs={"k": k, "fetch_k": fetch_k},
    )
