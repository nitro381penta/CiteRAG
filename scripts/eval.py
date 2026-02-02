from __future__ import annotations

import json

from citerag.settings import Settings
from citerag.embeddings import make_embeddings
from citerag.indexer import open_or_create_chroma
from citerag.retrieve import make_retriever
from citerag.rag_chain import answer_question
from citerag.evals import run_eval, summarize
from langchain_community.llms import Ollama


def main():
    s = Settings()

    embeddings = make_embeddings(s.embed_model)
    vectordb = open_or_create_chroma(s.db_dir, embeddings)
    retriever = make_retriever(vectordb, s.search_type, s.top_k, s.fetch_k)
    llm = Ollama(model=s.ollama_model, temperature=0)

    def qa_fn(q: str):
        return answer_question(llm, retriever, q)

    rows = run_eval(qa_fn, "eval/questions.jsonl")
    print("Summary:")
    print(json.dumps(summarize(rows), indent=2))

    print("\nPer-question:")
    for r in rows:
        print(r)

if __name__ == "__main__":
    main()
