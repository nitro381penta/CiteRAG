from __future__ import annotations

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader


def load_pdfs(data_dir: str):
    loader = DirectoryLoader(
        data_dir,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
        use_multithreading=True,
    )
    docs = loader.load()

    # Normalize metadata for better citations
    for d in docs:
        # PyPDFLoader sets "source" and "page"
        d.metadata["source"] = d.metadata.get("source", "unknown")
        d.metadata["page"] = d.metadata.get("page", None)
    return docs
