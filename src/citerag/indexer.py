from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

from langchain_community.vectorstores import Chroma


MANIFEST_FILE = "index_manifest.json"


def file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_manifest(db_dir: str) -> Dict[str, str]:
    mf = Path(db_dir) / MANIFEST_FILE
    if not mf.exists():
        return {}
    return json.loads(mf.read_text(encoding="utf-8"))


def save_manifest(db_dir: str, manifest: Dict[str, str]) -> None:
    Path(db_dir).mkdir(parents=True, exist_ok=True)
    mf = Path(db_dir) / MANIFEST_FILE
    mf.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def list_pdfs(data_dir: str) -> List[str]:
    paths = []
    for root, _, files in os.walk(data_dir):
        for fn in files:
            if fn.lower().endswith(".pdf"):
                paths.append(os.path.join(root, fn))
    return sorted(paths)


def open_or_create_chroma(db_dir: str, embeddings):
    Path(db_dir).mkdir(parents=True, exist_ok=True)
    return Chroma(persist_directory=db_dir, embedding_function=embeddings)


def compute_changes(data_dir: str, db_dir: str) -> Tuple[List[str], List[str]]:
    """Return (added_or_changed, deleted) pdf paths."""
    current = {p: file_sha256(p) for p in list_pdfs(data_dir)}
    previous = load_manifest(db_dir)

    added_or_changed = [p for p, h in current.items() if previous.get(p) != h]
    deleted = [p for p in previous.keys() if p not in current]
    return added_or_changed, deleted


def update_manifest(data_dir: str, db_dir: str) -> None:
    current = {p: file_sha256(p) for p in list_pdfs(data_dir)}
    save_manifest(db_dir, current)


def delete_docs_for_sources(vectordb: Chroma, sources: List[str]) -> int:
    """
    Delete existing chunks for given sources.
    Chroma supports delete(where=...) when metadata is stored.
    """
    deleted_total = 0
    for src in sources:
        # delete by metadata filter
        try:
            vectordb._collection.delete(where={"source": src})
            deleted_total += 1
        except Exception:
            # Pass if delete not supported in some environments
            pass
    return deleted_total
