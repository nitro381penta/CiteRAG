from __future__ import annotations

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

from .prompts import STRICT_SYSTEM, USER_TEMPLATE
from .citations import format_context


def _retrieve(retriever, query: str):
    # Newer LangChain retrievers support .invoke()
    if hasattr(retriever, "invoke"):
        return retriever.invoke(query)

    # Older retrievers used get_relevant_documents()
    if hasattr(retriever, "get_relevant_documents"):
        return retriever.get_relevant_documents(query)

    # Fallback (rare)
    if hasattr(retriever, "_get_relevant_documents"):
        return retriever._get_relevant_documents(query)

    raise AttributeError("Retriever has no supported retrieval method.")


def answer_question(llm: Ollama, retriever, question: str):
    source_docs = _retrieve(retriever, question)

    context = format_context(source_docs) if source_docs else "NO_CONTEXT"

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", STRICT_SYSTEM),
            ("human", USER_TEMPLATE),
        ]
    )

    # Turn the chat prompt into a plain string for a text LLM
    prompt_text = prompt.format(question=question, context=context)

    response = llm.invoke(prompt_text)

    return {
        "answer": response,
        "source_docs": source_docs,
    }
