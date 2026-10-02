# Python Docs Troubleshooting RAG - 설계서

## 설계 요약

| 항목 | 결정 |
|---|---|
| 해결 문제 | Python 공식 문서를 여러 페이지에서 찾아야 하는 학습자의 검색 부담 완화 |
| 사용자 | Python 입문자, 주니어 개발자, 공식 문서 학습자 |
| 질문 범위 | Python 오류, 문법, 내장 기능, `pathlib`·`dataclasses`·`venv` 사용법 |
| 근거 문서 | Python 3.14 공식 한국어 일반 텍스트 문서 |
| Baseline | Dense Similarity Search Top-4 |
| 개선 검색 | Dense + 정규식 BM25 + weighted RRF Top-4 |
| 범위 밖 처리 | 근거가 없으면 지정 문구로 답변을 거절 |
| 평가 | Retrieval 24개 질문 + 문서 밖 Generation 질문 1개 |

## 1. 해결하려는 문제

Python 입문자가 오류와 핵심 문법을 질문할 때 Python 3.14 공식 문서에서 근거를 검색해 답합니다. 정확한 API/예외 이름 질문과 자연어로 바꿔 말한 개념 질문을 모두 다룹니다.

## 2. 대상 사용자

Python 입문자, 주니어 개발자, 공식 문서를 학습하는 사용자입니다.

## 3. 문서와 데이터 범위

Python 3.14 공식 한국어 일반 텍스트 아카이브의 25개 파일 중 라이선스 문서를 제외한 24개를 검색에 사용합니다. 범위는 Tutorial, built-ins, exceptions, `pathlib`, `dataclasses`, `venv`, Programming FAQ이며 외부 패키지와 클라우드 SDK 사용법은 제외합니다.

### 데이터 범위와 사용 내역

`data/` 디렉터리는 제출하지 않아도 재현할 수 있도록 출처와 사용 방식을 아래에 기록합니다.

| 구분 | 파일·범위 | 파일 수 | 사용 방법 |
|---|---|---:|---|
| Tutorial·학습 문서 | `appetite`, `interpreter`, `introduction`, `controlflow`, `datastructures`, `modules`, `inputoutput`, `errors`, `classes`, `stdlib`, `stdlib2`, `whatnow`, `interactive`, `floatingpoint`, `appendix`, `tutorial_venv` | 16 | 문법·개념·오류 질문 검색 |
| 내장 기능·예외 | `functions`, `stdtypes`, `exceptions` | 3 | 내장 함수·자료형·예외 질문 검색 |
| 표준 라이브러리 | `pathlib`, `dataclasses`, `library_venv` | 3 | 정확한 API와 설정 질문 검색 |
| FAQ | `programming` | 1 | 변경 가능한 기본 인수 등 실전 질문 검색 |
| 문서 색인 | `index` | 1 | 문서 범위 보조 검색 |
| 검색 제외 | `copyright` | 1 | 라이선스 보존용이며 인덱싱하지 않음 |

| 처리 항목 | 값 |
|---|---|
| 원본 출처 | `https://docs.python.org/ko/3/download.html`의 Python 3.14 텍스트 아카이브 |
| 인코딩 | UTF-8 |
| 검색 문서 수 | 24개 |
| Chunk | 900자, overlap 150자 |
| 생성 Chunk 수 | 1,009개 |
| Metadata | `source`, `path`, `dataset`, `start_index` |
| 번역 처리 | 별도 기계번역 없이 공식 한국어 배포본 그대로 사용 |

## 4. Baseline RAG 구조

```text
TextLoader -> RecursiveCharacterTextSplitter(900/150)
-> OpenAIEmbeddings -> FAISS -> Similarity Top-4
-> grounded prompt -> ChatOpenAI
```

## 5. 검색 개선 전략과 선택 이유

개선안은 dense similarity와 BM25를 weighted Reciprocal Rank Fusion으로 결합한 Hybrid Search입니다. 자연어 의미 검색은 dense에, `ValueError`, `dict.get`, `Path.read_text` 같은 정확한 토큰 검색은 BM25에 강점이 있어 질문 유형이 섞인 이 프로젝트에 적합합니다. BM25에는 정규식 토큰화와 Kiwi 형태소 토큰화를 적용합니다.

## 6. 평가 질문과 방법

- 고정 질문 25개: exact-token, paraphrase, multi-part, out-of-scope 포함
- Retrieval 점수에는 정답 문서가 있는 24개 질문만 포함
- Retrieval: 정답 source 파일의 Top-4 포함 여부(Hit Rate), 첫 정답 순위(MRR)
- Generation: retrieved context와 답변의 근거 일치, source 인용, 근거 없음 거절을 수동 확인
- Baseline, Hybrid Regex, Hybrid Kiwi는 같은 문서, chunk, embedding, 질문, Top-K를 사용합니다.

평가 결과는 Baseline MRR 0.674, Hybrid Regex 0.781, Hybrid Kiwi 0.747이며 Hit Rate@4는 모두 0.875입니다. 기본 질문 응답에는 형태소 분석 단계가 필요 없고 MRR이 가장 높은 Hybrid Regex를 사용합니다.

## 7. 예상 한계와 보완 방법

파일 단위 relevance label은 평가가 단순하지만 같은 파일의 무관한 chunk도 hit가 될 수 있습니다. 후속 평가에서는 chunk ID 단위 label과 더 많은 질문을 사용합니다. Kiwi의 품사 선택, 사용자 사전, BM25 가중치는 추가로 조정할 수 있습니다.

## 전체 흐름

```text
Documents
  -> Loader -> Splitter -> Embedding -> FAISS
Question
  -> Baseline: Dense Top-4 -----------------------> Context
  -> Improved: Dense Top-10 + Regex/Kiwi BM25 Top-10 -> RRF -> Context
Context -> LLM -> cited or abstained Answer
```
