from __future__ import annotations

from langchain_community.embeddings import HuggingFaceEmbeddings


def make_embeddings(model_name: str):
    return HuggingFaceEmbeddings(model_name=model_name)
