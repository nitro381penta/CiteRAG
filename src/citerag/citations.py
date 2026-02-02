from __future__ import annotations

import os
from typing import List


def format_context(source_docs) -> str:
    # Provide chunk text plus compact source tags for the model
    blocks = []
    for d in source_docs:
        src = os.path.basename(d.metadata.get("source", "unknown"))
        page = d.metadata.get("page", None)
        page_str = str(page + 1) if isinstance(page, int) else "?"
        blocks.append(f"[{src}:{page_str}]\n{d.page_content}")
    return "\n\n".join(blocks)


def unique_sources(source_docs) -> List[str]:
    seen = set()
    out = []
    for d in source_docs:
        src = os.path.basename(d.metadata.get("source", "unknown"))
        page = d.metadata.get("page", None)
        page_str = str(page + 1) if isinstance(page, int) else "?"
        key = (src, page_str)
        if key in seen:
            continue
        seen.add(key)
        out.append(f"{src}:{page_str}")
    return out
