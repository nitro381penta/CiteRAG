from __future__ import annotations

import json
import re
import time
from typing import Dict, List


CITATION_PATTERN = re.compile(r"\[[^\[\]:]+\.(pdf|PDF):\d+\]")


def has_citation(text: str) -> bool:
    return bool(CITATION_PATTERN.search(text))


def run_eval(qa_fn, questions_path: str) -> List[Dict]:
    rows = []
    with open(questions_path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            q = item["question"]

            t0 = time.time()
            out = qa_fn(q)
            dt = time.time() - t0

            ans = str(out["answer"])
            rows.append(
                {
                    "question": q,
                    "latency_s": round(dt, 3),
                    "has_citation": has_citation(ans),
                }
            )
    return rows


def summarize(rows: List[Dict]) -> Dict:
    if not rows:
        return {"n": 0}

    n = len(rows)
    cite_rate = sum(1 for r in rows if r["has_citation"]) / n
    avg_lat = sum(r["latency_s"] for r in rows) / n
    return {
        "n": n,
        "citation_coverage": round(cite_rate, 3),
        "avg_latency_s": round(avg_lat, 3),
    }
