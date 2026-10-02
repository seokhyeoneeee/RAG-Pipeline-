"""7단계: 검색 Context용 Prompt와 LLM을 준비합니다."""

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from python_docs_config import Settings, load_environment


ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 Python 공식 문서를 근거로 답하는 질문-답변 도우미입니다. "
            "반드시 제공된 공식 문서 내용만 사용하세요. 문서에 답의 근거가 "
            "없으면 정확히 '제공된 Python 공식 문서에서 확인할 수 없습니다.'라고 "
            "답하세요. 외부 지식을 사용하거나 추측하지 마세요. 답변은 한국어로 "
            "간결하게 작성하고, 근거 파일을 [pathlib.txt]처럼 표시하세요.",
        ),
        ("human", "[Python 공식 문서]\n{context}\n\n[질문]\n{question}"),
    ]
)


def format_documents(documents: list[Document]) -> str:
    return "\n\n".join(
        f"[출처: {document.metadata['source']}]\n{document.page_content}"
        for document in documents
    )


def build_llm(settings: Settings) -> ChatOpenAI:
    return ChatOpenAI(model=settings.chat_model, temperature=0)


if __name__ == "__main__":
    load_environment()
    config = Settings()
    messages = ANSWER_PROMPT.invoke(
        {
            "context": "[출처: example.txt]\n예시 문서 내용",
            "question": "예시 질문입니다.",
        }
    )
    print("LLM 모델:", config.chat_model)
    print(messages)
