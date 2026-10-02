"""8단계: Retriever -> Context -> Prompt -> LLM RAG Pipeline을 실행합니다."""

from langchain_core.documents import Document

from python_docs_config import Settings, load_environment
from python_docs_prompt_llm import ANSWER_PROMPT, build_llm, format_documents
from python_docs_retriever import build_retrievers


def answer(
    question: str,
    retriever,
    settings: Settings,
) -> tuple[str, list[Document]]:
    documents = retriever.invoke(question)
    context = format_documents(documents)
    messages = ANSWER_PROMPT.invoke(
        {"context": context, "question": question}
    )
    response = build_llm(settings).invoke(messages)
    return str(response.content), documents


if __name__ == "__main__":
    load_environment()
    config = Settings()
    _, hybrid_retriever, _ = build_retrievers(config)
    question = "변경 가능한 기본 인수가 함수 호출 사이에서 공유되는 이유는 무엇인가요?"
    response, retrieved_documents = answer(question, hybrid_retriever, config)

    print("[질문]")
    print(question)
    print("\n[검색 문서]")
    for rank, document in enumerate(retrieved_documents, start=1):
        print(rank, document.metadata["source"])
    print("\n[답변]")
    print(response)
