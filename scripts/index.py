from __future__ import annotations

from pathlib import Path

from citerag.settings import Settings
from citerag.embeddings import make_embeddings
from citerag.ingest import load_pdfs
from citerag.chunking import split_docs
from citerag.indexer import (
    compute_changes,
    delete_docs_for_sources,
    open_or_create_chroma,
    update_manifest,
)

def main():
    s = Settings()
    Path(s.db_dir).mkdir(parents=True, exist_ok=True)

    embeddings = make_embeddings(s.embed_model)
    vectordb = open_or_create_chroma(s.db_dir, embeddings)

    changed, deleted = compute_changes(s.data_dir, s.db_dir)

    if not changed and not deleted:
        print("No changes detected. Index is up to date.")
        return

    if deleted:
        print(f"Deleting removed PDFs from index: {len(deleted)}")
        delete_docs_for_sources(vectordb, deleted)

    if changed:
        print(f"Re-indexing changed/new PDFs: {len(changed)}")
        # Remove old chunks for these sources (if any)
        delete_docs_for_sources(vectordb, changed)

        # Load all docs, then filter to changed sources only
        docs = load_pdfs(s.data_dir)
        docs = [d for d in docs if d.metadata.get("source") in set(changed)]
        chunks = split_docs(docs, s.chunk_size, s.chunk_overlap)
        print(f"Adding {len(chunks)} chunks...")
        vectordb.add_documents(chunks)

    vectordb.persist()
    update_manifest(s.data_dir, s.db_dir)
    print("Index updated successfully.")

if __name__ == "__main__":
    main()
