from __future__ import annotations

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

from .prompts import STRICT_SYSTEM, USER_TEMPLATE
from .citations import format_context


def answer_question(llm: Ollama, retriever, question: str):
    source_docs = retriever.get_relevant_documents(question)

    context = format_context(source_docs) if source_docs else "NO_CONTEXT"

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", STRICT_SYSTEM),
            ("human", USER_TEMPLATE),
        ]
    )
    msg = prompt.format_messages(question=question, context=context)
    response = llm.invoke(msg)

    return {
        "answer": response,
        "source_docs": source_docs,
    }
