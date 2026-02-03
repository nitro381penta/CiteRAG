from __future__ import annotations

from citerag.settings import Settings
from citerag.embeddings import make_embeddings
from citerag.indexer import open_or_create_chroma
from citerag.retrieve import make_retriever
from citerag.rag_chain import answer_question
from langchain_ollama import OllamaLLM
from citerag.citations import unique_sources


def main():
    s = Settings()

    embeddings = make_embeddings(s.embed_model)
    vectordb = open_or_create_chroma(s.db_dir, embeddings)
    retriever = make_retriever(vectordb, s.search_type, s.top_k, s.fetch_k)

    llm = Ollama(model=s.ollama_model, temperature=0)

    print("CiteRAG ready. Type 'quit' to exit.")
    while True:
        q = input("\nQuestion: ").strip()
        if q.lower() == "quit":
            break

        out = answer_question(llm, retriever, q)
        print("\nAnswer:\n")
        print(out["answer"])

        srcs = unique_sources(out["source_docs"])
        if srcs:
            print("\nSources used:")
            for sref in srcs:
                print(f"- {sref}")
        else:
            print("\nSources used: none")


if __name__ == "__main__":
    main()
