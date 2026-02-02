from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    data_dir: str = os.getenv("DATA_DIR", "data")
    db_dir: str = os.getenv("DB_DIR", "chroma_db")
    embed_model: str = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1")

    chunk_size: int = int(os.getenv("CHUNK_SIZE", "900"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "150"))

    search_type: str = os.getenv("SEARCH_TYPE", "mmr")
    top_k: int = int(os.getenv("TOP_K", "4"))
    fetch_k: int = int(os.getenv("FETCH_K", "20"))