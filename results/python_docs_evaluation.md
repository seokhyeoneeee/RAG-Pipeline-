# Python 공식 문서 RAG 평가 결과

## 1. 평가 요약

| 지표 | Baseline | Hybrid Regex | Hybrid Kiwi |
|---|---:|---:|---:|
| Hit Rate@4 | 0.875 | 0.875 | 0.875 |
| MRR@4 | 0.674 | 0.781 | 0.747 |
| 평가 질문 수 | 24 | 24 | 24 |

- Baseline: Dense Similarity Search Top-4
- Hybrid Regex: Dense Search와 정규식 BM25를 weighted RRF로 결합한 Top-4
- Hybrid Kiwi: Dense Search와 Kiwi 형태소 BM25를 weighted RRF로 결합한 Top-4
- 정답 문서가 없는 질문은 Retrieval 점수에서 제외

### 지표 그래프

```text
Hit Rate  Baseline     ██████████████████░░ 0.875
          Hybrid Regex ██████████████████░░ 0.875
          Hybrid Kiwi  ██████████████████░░ 0.875

MRR       Baseline     █████████████░░░░░░░ 0.674
          Hybrid Regex ████████████████░░░░ 0.781
          Hybrid Kiwi  ███████████████░░░░░ 0.747
```

- Hit Rate@4는 세 방식 모두 0.875로 동일합니다.
- Hybrid Regex는 Baseline보다 MRR@4가 +0.107 높아 정답 문서를 더 위에 배치했습니다.
- 기본 질문 응답에는 가장 단순하면서 MRR이 높은 Hybrid Regex를 사용합니다.

## 2. 대표 질문 Generation 비교

근거 여부는 기대 핵심어와 출처 파일 표시를 함께 확인하며, 문서 밖 질문은 지정된 거절 문구를 확인합니다.
전체 Top-4와 실제 답변은 비교표 아래의 질문별 상세 기록에서 확인할 수 있습니다.

| 질문 | Baseline 검색 | 개선 검색 | 답변 변화 | 판단 |
|---|---|---|---|---|
| Q2 | Hit · 정답 1위 | Hit · 정답 1위 | 동일 | 두 답변 모두 기대 내용과 출처를 충족 |
| Q3 | Hit · 정답 2위 | Hit · 정답 1위 | 동일 | 두 답변 모두 기대 내용과 출처를 충족 |
| Q6 | Hit · 정답 1위 | Hit · 정답 1위 | 동일 | 두 답변 모두 기대 내용 또는 출처를 충족하지 못함 |
| Q8 | Hit · 정답 1위 | Hit · 정답 1위 | 동일 | 두 답변 모두 기대 내용과 출처를 충족 |
| Q25 | 평가 제외 | 평가 제외 | 동일 | 두 답변 모두 근거 없이 답하지 않음 |

### Q2. 예외 발생 여부와 관계없이 반드시 실행해야 하는 정리 코드는 어디에 작성해야 하나요?

#### Baseline 답변

- 근거 여부: 충족
- 검색 Top-4: 1. errors.txt@9097, 2. errors.txt@10529, 3. errors.txt@9827, 4. errors.txt@1643

> 예외 발생 여부와 관계없이 반드시 실행해야 하는 정리 코드는 `finally` 절에 작성해야 합니다. `finally` 절은 `try` 문이 완료되기 전에 마지막 작업으로 실행되며, 예외가 발생하더라도 실행됩니다.
>
> [출처: errors.txt]

#### Regex Hybrid 답변

- 근거 여부: 충족
- 검색 Top-4: 1. errors.txt@9097, 2. errors.txt@6274, 3. errors.txt@0, 4. errors.txt@10529

> 예외 발생 여부와 관계없이 반드시 실행해야 하는 정리 코드는 `finally` 절에 작성해야 합니다. `finally` 절은 예외가 발생하든 발생하지 않든 항상 실행됩니다.
>
> [출처: errors.txt]

- 변화: **동일**
- 판단 근거: 두 답변 모두 기대 내용과 출처를 충족

### Q3. 전체 반복문을 작성하지 않고 표현식과 for 절로 리스트를 만드는 방법은 무엇인가요?

#### Baseline 답변

- 근거 여부: 충족
- 검색 Top-4: 1. programming.txt@31848, 2. datastructures.txt@6367, 3. datastructures.txt@1453, 4. controlflow.txt@847

> 리스트를 만드는 방법 중 하나는 리스트 컴프리헨션을 사용하는 것입니다. 리스트 컴프리헨션은 표현식과 for 절을 결합하여 새로운 리스트를 생성하는 간결한 방법입니다. 예를 들어, 다음과 같이 사용할 수 있습니다:
>
> ```python
> [x for x in iterable if condition]
> ```
>
> 이 방식은 전체 반복문을 작성하지 않고도 리스트를 생성할 수 있게 해줍니다.
>
> [출처: datastructures.txt]

#### Regex Hybrid 답변

- 근거 여부: 충족
- 검색 Top-4: 1. datastructures.txt@4363, 2. programming.txt@31848, 3. datastructures.txt@6367, 4. datastructures.txt@1453

> 전체 반복문을 작성하지 않고 표현식과 for 절로 리스트를 만드는 방법은 리스트 컴프리헨션을 사용하는 것입니다. 리스트 컴프리헨션은 표현식과 그 뒤를 따르는 "for" 절로 구성되어 있으며, 간결하고 읽기 쉽습니다. 예를 들어, 다음과 같이 사용할 수 있습니다:
>
> ```python
> squares = [x**2 for x in range(10)]
> ```
>
> 이 코드는 0부터 9까지의 제곱수를 포함하는 리스트를 생성합니다.
>
> [출처: datastructures.txt]

- 변화: **동일**
- 판단 근거: 두 답변 모두 기대 내용과 출처를 충족

### Q6. 데이터클래스에 frozen=True를 지정하면 객체가 완전히 불변이 되나요?

#### Baseline 답변

- 근거 여부: 미충족
- 검색 Top-4: 1. dataclasses.txt@4867, 2. dataclasses.txt@15617, 3. dataclasses.txt@20773, 4. dataclasses.txt@20184

> 제공된 Python 공식 문서에서 확인할 수 없습니다.

#### Regex Hybrid 답변

- 근거 여부: 미충족
- 검색 Top-4: 1. dataclasses.txt@4867, 2. dataclasses.txt@20184, 3. dataclasses.txt@3339, 4. dataclasses.txt@15617

> 제공된 Python 공식 문서에서 확인할 수 없습니다.

- 변화: **동일**
- 판단 근거: 두 답변 모두 기대 내용 또는 출처를 충족하지 못함

### Q8. 변경 가능한 기본 인수가 여러 함수 호출 사이에서 공유되는 이유는 무엇인가요?

#### Baseline 답변

- 근거 여부: 충족
- 검색 Top-4: 1. programming.txt@12074, 2. programming.txt@9057, 3. programming.txt@12795, 4. programming.txt@8338

> 변경 가능한 기본 인수가 여러 함수 호출 사이에서 공유되는 이유는 기본값이 함수가 정의될 때 한 번만 생성되기 때문입니다. 이 객체가 변경되면, 함수에 대한 후속 호출은 이 변경된 객체를 참조하게 됩니다. 따라서 가변 객체를 기본값으로 사용하면 혼란을 초래할 수 있습니다.
>
> 이러한 이유로, 가변 객체를 기본값으로 사용하지 않는 것이 좋으며, 대신 "None"을 기본값으로 사용하고 함수 내부에서 매개변수가 "None"인지 확인한 후 새 객체를 생성하는 것이 권장됩니다.
>
> [출처: programming.txt]

#### Regex Hybrid 답변

- 근거 여부: 충족
- 검색 Top-4: 1. programming.txt@7586, 2. controlflow.txt@29511, 3. programming.txt@12074, 4. programming.txt@9057

> 변경 가능한 기본 인수가 여러 함수 호출 사이에서 공유되는 이유는, 함수가 정의될 때 기본값은 한 번만 생성되기 때문입니다. 예를 들어, 딕셔너리와 같은 가변 객체가 기본값으로 사용되면, 첫 번째 호출에서 해당 객체가 변경되면 이후의 호출에서도 변경된 객체를 참조하게 됩니다. 따라서, 모든 호출이 같은 객체를 공유하게 되어 문제가 발생할 수 있습니다.
>
> [출처: programming.txt]

- 변화: **동일**
- 판단 근거: 두 답변 모두 기대 내용과 출처를 충족

### Q25. pathlib.Path 객체를 Amazon S3 버킷에 직접 업로드하려면 어떻게 하나요?

#### Baseline 답변

- 근거 여부: 충족
- 검색 Top-4: 1. pathlib.txt@0, 2. pathlib.txt@6083, 3. pathlib.txt@56423, 4. pathlib.txt@3871

> 제공된 Python 공식 문서에서 확인할 수 없습니다.

#### Regex Hybrid 답변

- 근거 여부: 충족
- 검색 Top-4: 1. pathlib.txt@0, 2. pathlib.txt@6083, 3. pathlib.txt@56423, 4. pathlib.txt@3871

> 제공된 Python 공식 문서에서 확인할 수 없습니다.

- 변화: **동일**
- 판단 근거: 두 답변 모두 근거 없이 답하지 않음

## 3. 질문별 Retrieval 결과

### 1. 인수의 타입은 올바르지만 값이 부적절할 때는 왜 TypeError가 아니라 ValueError를 발생시켜야 하나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 0 | Top-4 내 없음 | 0.000 |
| Hybrid Regex | 0 | Top-4 내 없음 | 0.000 |
| Hybrid Kiwi | 0 | Top-4 내 없음 | 0.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | dataclasses.txt | 15617 | *changes* 가 "init=False" 를 갖는 것으로 정의된 필드를 포함하는 것 은 에러입니다. 이 경우 "ValueError" 가 발생합니다. "replace()"를 호출하는 동안 "init=False" 필드가 어떻게 작동하는지 미리 경고합니다. 그것들은 소스 객체로부터 복사되는 것이 아니라, (초 기화되기는 한다면) "__post_init__()" 에서 초기화됩니다. "init=False" 필드는 거의 사용되지 않으 |
| 2 | dataclasses.txt | 4867 | *eq* 와 *frozen* 이 모두 참이면, 기본적으로 "@dataclass" 는 "__hash__()" 메서드를 만듭니다. *eq* 가 참이고 *frozen* 이 거짓이 면, "__hash__()" 가 "None" 으로 설정되어 해시 불가능하다고 표시됩 니다(가변이기 때문입니다). 만약 *eq* 가 거짓이면, "__hash__()" 를 건드리지 않는데, 슈퍼 클래스의 "__hash__()" 가 사용된다는 뜻이 됩 니다 (슈 |
| 3 | programming.txt | 9867 | 인자와 매개변수의 차이점은 무엇입니까? -------------------------------------- *Parameters* are defined by the names that appear in a function definition, whereas *arguments* are the values actually passed to a function when calling it. Parameters define wha |
| 4 | introduction.txt | 2126 | 실수를 본격적으로 지원합니다; 서로 다른 형의 피연산자를 갖는 연산자는 정수 피연산자를 실수로 변환합니다: >>> 4 * 3.75 - 1 14.0 대화형 모드에서는, 마지막에 인쇄된 표현식은 변수 "_" 에 대입됩니다. 이 것은 파이썬을 탁상용 계산기로 사용할 때, 계산을 이어 가기가 좀 더 쉬워 짐을 의미합니다. 예를 들어: >>> tax = 12.5 / 100 >>> price = 100.50 >>> price * tax  |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | dataclasses.txt | 15617 | *changes* 가 "init=False" 를 갖는 것으로 정의된 필드를 포함하는 것 은 에러입니다. 이 경우 "ValueError" 가 발생합니다. "replace()"를 호출하는 동안 "init=False" 필드가 어떻게 작동하는지 미리 경고합니다. 그것들은 소스 객체로부터 복사되는 것이 아니라, (초 기화되기는 한다면) "__post_init__()" 에서 초기화됩니다. "init=False" 필드는 거의 사용되지 않으 |
| 2 | dataclasses.txt | 4867 | *eq* 와 *frozen* 이 모두 참이면, 기본적으로 "@dataclass" 는 "__hash__()" 메서드를 만듭니다. *eq* 가 참이고 *frozen* 이 거짓이 면, "__hash__()" 가 "None" 으로 설정되어 해시 불가능하다고 표시됩 니다(가변이기 때문입니다). 만약 *eq* 가 거짓이면, "__hash__()" 를 건드리지 않는데, 슈퍼 클래스의 "__hash__()" 가 사용된다는 뜻이 됩 니다 (슈 |
| 3 | programming.txt | 9867 | 인자와 매개변수의 차이점은 무엇입니까? -------------------------------------- *Parameters* are defined by the names that appear in a function definition, whereas *arguments* are the values actually passed to a function when calling it. Parameters define wha |
| 4 | introduction.txt | 2126 | 실수를 본격적으로 지원합니다; 서로 다른 형의 피연산자를 갖는 연산자는 정수 피연산자를 실수로 변환합니다: >>> 4 * 3.75 - 1 14.0 대화형 모드에서는, 마지막에 인쇄된 표현식은 변수 "_" 에 대입됩니다. 이 것은 파이썬을 탁상용 계산기로 사용할 때, 계산을 이어 가기가 좀 더 쉬워 짐을 의미합니다. 예를 들어: >>> tax = 12.5 / 100 >>> price = 100.50 >>> price * tax  |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | datastructures.txt | 17964 | (1, 2, 3) < (1, 2, 4) [1, 2, 3] < [1, 2, 4] 'ABC' < 'C' < 'Pascal' < 'Python' (1, 2, 3, 4) < (1, 2, 4) (1, 2) < (1, 2, -1) (1, 2, 3) == (1.0, 2.0, 3.0) (1, 2, ('aa', 'ab')) < (1, 2, ('abc', 'a'), 4) 서로 다른 형의 객체들을 "<" 나 ">" 로 비교하는 것은, 그 객체들이 |
| 2 | dataclasses.txt | 15617 | *changes* 가 "init=False" 를 갖는 것으로 정의된 필드를 포함하는 것 은 에러입니다. 이 경우 "ValueError" 가 발생합니다. "replace()"를 호출하는 동안 "init=False" 필드가 어떻게 작동하는지 미리 경고합니다. 그것들은 소스 객체로부터 복사되는 것이 아니라, (초 기화되기는 한다면) "__post_init__()" 에서 초기화됩니다. "init=False" 필드는 거의 사용되지 않으 |
| 3 | dataclasses.txt | 4867 | *eq* 와 *frozen* 이 모두 참이면, 기본적으로 "@dataclass" 는 "__hash__()" 메서드를 만듭니다. *eq* 가 참이고 *frozen* 이 거짓이 면, "__hash__()" 가 "None" 으로 설정되어 해시 불가능하다고 표시됩 니다(가변이기 때문입니다). 만약 *eq* 가 거짓이면, "__hash__()" 를 건드리지 않는데, 슈퍼 클래스의 "__hash__()" 가 사용된다는 뜻이 됩 니다 (슈 |
| 4 | programming.txt | 9867 | 인자와 매개변수의 차이점은 무엇입니까? -------------------------------------- *Parameters* are defined by the names that appear in a function definition, whereas *arguments* are the values actually passed to a function when calling it. Parameters define wha |

### 2. 예외 발생 여부와 관계없이 반드시 실행해야 하는 정리 코드는 어디에 작성해야 하나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 1 | 1.000 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | errors.txt | 9097 | It also allows disabling automatic exception chaining using the "from None" idiom: >>> try: ... open('database.sqlite') ... except OSError: ... raise RuntimeError from None ... Traceback (most recent call last): File "<stdin>", line 4, in < |
| 2 | errors.txt | 10529 | * "except"나 "else" 절 실행 중에 예외가 발생할 수 있습니다. 다시, "finally" 절이 실행된 후 예외가 다시 발생합니다. * If the "finally" clause executes a "break", "continue" or "return" statement, exceptions are not re-raised. This can be confusing and is therefore discouraged |
| 3 | errors.txt | 9827 | 많은 표준 모듈들은 그들이 정의하는 함수들에서 발생할 수 있는 그 자신만 의 예외들을 정의합니다. 8.7. 뒷정리 동작 정의하기 ========================= "try" 문은 또 다른 선택적 절을 가질 수 있는데 모든 상황에 실행되어야만 하는 뒷정리 동작을 정의하는 데 사용됩니다. 예를 들어: >>> try: ... raise KeyboardInterrupt ... finally: ... print('Goodb |
| 4 | errors.txt | 1643 | 줄의 나머지 부분은 예외의 형과 원인에 기반을 둔 상세 명세를 제공합니다 . 에러 메시지의 앞부분은 스택 트레이스의 형태로 예외가 일어난 위치의 문 맥을 보여줍니다. 일반적으로 소스의 줄들을 나열하는 스택 트레이스를 포 함하고 있습니다; 하지만, 표준 입력에서 읽어 들인 줄들은 표시하지 않습 니다. Built-in Exceptions 는 내장 예외들과 그 들의 의미를 나열하고 있습니다. 8.3. 예외 처리하기 ========= |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | errors.txt | 9097 | It also allows disabling automatic exception chaining using the "from None" idiom: >>> try: ... open('database.sqlite') ... except OSError: ... raise RuntimeError from None ... Traceback (most recent call last): File "<stdin>", line 4, in < |
| 2 | errors.txt | 6274 | 예외 처리기는 *try 절*에 직접 등장하는 예외뿐만 아니라, *try 절*에서 ( 간접적으로라도) 호출되는 내부 함수들에서 발생하는 예외들도 처리합니다. 예를 들어: >>> def this_fails(): ... x = 1/0 ... >>> try: ... this_fails() ... except ZeroDivisionError as err: ... print('Handling run-time error:', err) .. |
| 3 | errors.txt | 0 | 8. 에러와 예외 ************** 지금까지 에러 메시지가 언급되지는 않았지만, 예제들을 직접 해보았다면 아마도 몇몇 개를 보았을 것입니다. (적어도) 두 가지 구별되는 에러들이 있습니다; *문법 에러* 와 *예외*. 8.1. 문법 에러 ============== 문법 에러는, 파싱 에러라고도 알려져 있습니다, 아마도 여러분이 파이썬을 배우고 있는 동안에는 가장 자주 만나는 종류의 불평일 것입니다: >>> while  |
| 4 | errors.txt | 10529 | * "except"나 "else" 절 실행 중에 예외가 발생할 수 있습니다. 다시, "finally" 절이 실행된 후 예외가 다시 발생합니다. * If the "finally" clause executes a "break", "continue" or "return" statement, exceptions are not re-raised. This can be confusing and is therefore discouraged |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | errors.txt | 9827 | 많은 표준 모듈들은 그들이 정의하는 함수들에서 발생할 수 있는 그 자신만 의 예외들을 정의합니다. 8.7. 뒷정리 동작 정의하기 ========================= "try" 문은 또 다른 선택적 절을 가질 수 있는데 모든 상황에 실행되어야만 하는 뒷정리 동작을 정의하는 데 사용됩니다. 예를 들어: >>> try: ... raise KeyboardInterrupt ... finally: ... print('Goodb |
| 2 | errors.txt | 10529 | * "except"나 "else" 절 실행 중에 예외가 발생할 수 있습니다. 다시, "finally" 절이 실행된 후 예외가 다시 발생합니다. * If the "finally" clause executes a "break", "continue" or "return" statement, exceptions are not re-raised. This can be confusing and is therefore discouraged |
| 3 | errors.txt | 1643 | 줄의 나머지 부분은 예외의 형과 원인에 기반을 둔 상세 명세를 제공합니다 . 에러 메시지의 앞부분은 스택 트레이스의 형태로 예외가 일어난 위치의 문 맥을 보여줍니다. 일반적으로 소스의 줄들을 나열하는 스택 트레이스를 포 함하고 있습니다; 하지만, 표준 입력에서 읽어 들인 줄들은 표시하지 않습 니다. Built-in Exceptions 는 내장 예외들과 그 들의 의미를 나열하고 있습니다. 8.3. 예외 처리하기 ========= |
| 4 | errors.txt | 6274 | 예외 처리기는 *try 절*에 직접 등장하는 예외뿐만 아니라, *try 절*에서 ( 간접적으로라도) 호출되는 내부 함수들에서 발생하는 예외들도 처리합니다. 예를 들어: >>> def this_fails(): ... x = 1/0 ... >>> try: ... this_fails() ... except ZeroDivisionError as err: ... print('Handling run-time error:', err) .. |

### 3. 전체 반복문을 작성하지 않고 표현식과 for 절로 리스트를 만드는 방법은 무엇인가요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 2 | 0.500 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | programming.txt | 31848 | If all elements of the list may be used as set keys (that is, they are all *hashable*) this is often faster: mylist = list(set(mylist)) 이것은 리스트를 집합으로 변환하여, 중복을 제거한 다음, 리스트로 되돌립 니다. How do you remove multiple items from a list? ------------- |
| 2 | datastructures.txt | 6367 | 리스트 컴프리헨션은 복잡한 표현식과 중첩된 함수들을 포함할 수 있습니다 : >>> from math import pi >>> [str(round(pi, i)) for i in range(1, 6)] ['3.1', '3.14', '3.142', '3.1416', '3.14159'] 5.1.4. 중첩된 리스트 컴프리헨션 ------------------------------- 리스트 컴프리헨션의 첫 표현식으로 임의의 표현식이 올  |
| 3 | datastructures.txt | 1453 | list.reverse() 리스트의 요소들을 제자리에서 뒤집습니다. list.copy() 리스트의 얕은 사본을 돌려줍니다. "a[:]" 와 비슷합니다. 리스트 메서드 대부분을 사용하는 예: >>> fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana'] >>> fruits.count('apple') 2 >>> fruits.count('tangerine' |
| 4 | controlflow.txt | 847 | 4.2. "for" 문 ============= 파이썬에서 "for" 문은 C 나 파스칼에서 사용하던 것과 약간 다릅니다. (파 스칼처럼) 항상 숫자의 산술적인 진행을 통해 이터레이션 하거나, (C처럼) 사용자가 이터레이션 단계와 중지 조건을 정의할 수 있도록 하는 대신, 파 이썬의 "for" 문은 임의의 시퀀스 (리스트나 문자열)의 항목들을 그 시퀀스 에 들어있는 순서대로 이터레이션 합니다. 예를 들어 (말장난이 아니라):  |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | datastructures.txt | 4363 | >>> squares = [] >>> for x in range(10): ... squares.append(x**2) ... >>> squares [0, 1, 4, 9, 16, 25, 36, 49, 64, 81] 이것은 "x" 라는 이름의 변수를 만들고 (또는 덮어쓰고) 루프가 종료된 후 에도 남아있게 만든다는 것에 유의하세요. 어떤 부작용도 없이, 제곱수의 리스트를 이런 식으로 계산할 수 있습니다: squares = list |
| 2 | programming.txt | 31848 | If all elements of the list may be used as set keys (that is, they are all *hashable*) this is often faster: mylist = list(set(mylist)) 이것은 리스트를 집합으로 변환하여, 중복을 제거한 다음, 리스트로 되돌립 니다. How do you remove multiple items from a list? ------------- |
| 3 | datastructures.txt | 6367 | 리스트 컴프리헨션은 복잡한 표현식과 중첩된 함수들을 포함할 수 있습니다 : >>> from math import pi >>> [str(round(pi, i)) for i in range(1, 6)] ['3.1', '3.14', '3.142', '3.1416', '3.14159'] 5.1.4. 중첩된 리스트 컴프리헨션 ------------------------------- 리스트 컴프리헨션의 첫 표현식으로 임의의 표현식이 올  |
| 4 | datastructures.txt | 1453 | list.reverse() 리스트의 요소들을 제자리에서 뒤집습니다. list.copy() 리스트의 얕은 사본을 돌려줍니다. "a[:]" 와 비슷합니다. 리스트 메서드 대부분을 사용하는 예: >>> fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana'] >>> fruits.count('apple') 2 >>> fruits.count('tangerine' |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | datastructures.txt | 6367 | 리스트 컴프리헨션은 복잡한 표현식과 중첩된 함수들을 포함할 수 있습니다 : >>> from math import pi >>> [str(round(pi, i)) for i in range(1, 6)] ['3.1', '3.14', '3.142', '3.1416', '3.14159'] 5.1.4. 중첩된 리스트 컴프리헨션 ------------------------------- 리스트 컴프리헨션의 첫 표현식으로 임의의 표현식이 올  |
| 2 | datastructures.txt | 4363 | >>> squares = [] >>> for x in range(10): ... squares.append(x**2) ... >>> squares [0, 1, 4, 9, 16, 25, 36, 49, 64, 81] 이것은 "x" 라는 이름의 변수를 만들고 (또는 덮어쓰고) 루프가 종료된 후 에도 남아있게 만든다는 것에 유의하세요. 어떤 부작용도 없이, 제곱수의 리스트를 이런 식으로 계산할 수 있습니다: squares = list |
| 3 | programming.txt | 31848 | If all elements of the list may be used as set keys (that is, they are all *hashable*) this is often faster: mylist = list(set(mylist)) 이것은 리스트를 집합으로 변환하여, 중복을 제거한 다음, 리스트로 되돌립 니다. How do you remove multiple items from a list? ------------- |
| 4 | datastructures.txt | 1453 | list.reverse() 리스트의 요소들을 제자리에서 뒤집습니다. list.copy() 리스트의 얕은 사본을 돌려줍니다. "a[:]" 와 비슷합니다. 리스트 메서드 대부분을 사용하는 예: >>> fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana'] >>> fruits.count('apple') 2 >>> fruits.count('tangerine' |

### 4. 키가 없고 기본값도 지정하지 않았을 때 dict.get은 무엇을 반환하나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 3 | 0.333 |
| Hybrid Regex | 1 | 4 | 0.250 |
| Hybrid Kiwi | 1 | 4 | 0.250 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | programming.txt | 8338 | 종종 함수 호출이 기본값으로 새 객체를 만들 것으로 기대합니다. 그렇게 되지 않습니다. 함수가 정의될 때, 기본값은 정확히 한 번 만들어집니다. 이 예제의 딕셔너리와 같이, 해당 객체가 변경되면, 함수에 대한 후속 호출 은 이 변경된 객체를 참조합니다. 정의에 따라, 숫자, 문자열, 튜플 및 "None"과 같은 불변 객체는 변경에 안 전합니다. 딕셔너리, 리스트 및 클래스 인스턴스와 같은 가변 객체를 변경 하면 혼란스러울 수  |
| 2 | datastructures.txt | 12481 | 딕셔너리를 (한 딕셔너리 안에서) 키가 중복되지 않는다는 제약 조건을 가 진 *키: 값* 쌍의 집합으로 생각하는 것이 최선입니다. 중괄호 쌍은 빈 딕 셔너리를 만듭니다: "{}". 중괄호 안에 쉼표로 분리된 키:값 쌍들의 목록을 넣으면, 딕셔너리에 초기 키:값 쌍들을 제공합니다; 이것이 딕셔너리가 출 력되는 방식이기도 합니다. The main operations on a dictionary are storing a value  |
| 3 | stdtypes.txt | 188078 | A dictionary's keys are *almost* arbitrary values. Values that are not *hashable*, that is, values containing lists, dictionaries or other mutable types (that are compared by value rather than by object identity) may not be used as keys. Va |
| 4 | stdtypes.txt | 192531 | >>> class Counter(dict): ... def __missing__(self, key): ... return 0 ... >>> c = Counter() >>> c['red'] 0 >>> c['red'] += 1 >>> c['red'] 1 The example above shows part of the implementation of "collections.Counter". A different "__missing_ |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | datastructures.txt | 13972 | "dict()" 생성자는 키-값 쌍들의 시퀀스로 부터 직접 딕셔너리를 구성합니 다. >>> dict([('sape', 4139), ('guido', 4127), ('jack', 4098)]) {'sape': 4139, 'guido': 4127, 'jack': 4098} 이에 더해, 딕셔너리 컴프리헨션은 임의의 키와 값 표현식들로 부터 딕셔너 리를 만드는데 사용될 수 있습니다: >>> {x: x**2 for x in (2, 4, |
| 2 | programming.txt | 8338 | 종종 함수 호출이 기본값으로 새 객체를 만들 것으로 기대합니다. 그렇게 되지 않습니다. 함수가 정의될 때, 기본값은 정확히 한 번 만들어집니다. 이 예제의 딕셔너리와 같이, 해당 객체가 변경되면, 함수에 대한 후속 호출 은 이 변경된 객체를 참조합니다. 정의에 따라, 숫자, 문자열, 튜플 및 "None"과 같은 불변 객체는 변경에 안 전합니다. 딕셔너리, 리스트 및 클래스 인스턴스와 같은 가변 객체를 변경 하면 혼란스러울 수  |
| 3 | datastructures.txt | 12481 | 딕셔너리를 (한 딕셔너리 안에서) 키가 중복되지 않는다는 제약 조건을 가 진 *키: 값* 쌍의 집합으로 생각하는 것이 최선입니다. 중괄호 쌍은 빈 딕 셔너리를 만듭니다: "{}". 중괄호 안에 쉼표로 분리된 키:값 쌍들의 목록을 넣으면, 딕셔너리에 초기 키:값 쌍들을 제공합니다; 이것이 딕셔너리가 출 력되는 방식이기도 합니다. The main operations on a dictionary are storing a value  |
| 4 | stdtypes.txt | 188078 | A dictionary's keys are *almost* arbitrary values. Values that are not *hashable*, that is, values containing lists, dictionaries or other mutable types (that are compared by value rather than by object identity) may not be used as keys. Va |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | programming.txt | 8338 | 종종 함수 호출이 기본값으로 새 객체를 만들 것으로 기대합니다. 그렇게 되지 않습니다. 함수가 정의될 때, 기본값은 정확히 한 번 만들어집니다. 이 예제의 딕셔너리와 같이, 해당 객체가 변경되면, 함수에 대한 후속 호출 은 이 변경된 객체를 참조합니다. 정의에 따라, 숫자, 문자열, 튜플 및 "None"과 같은 불변 객체는 변경에 안 전합니다. 딕셔너리, 리스트 및 클래스 인스턴스와 같은 가변 객체를 변경 하면 혼란스러울 수  |
| 2 | datastructures.txt | 13972 | "dict()" 생성자는 키-값 쌍들의 시퀀스로 부터 직접 딕셔너리를 구성합니 다. >>> dict([('sape', 4139), ('guido', 4127), ('jack', 4098)]) {'sape': 4139, 'guido': 4127, 'jack': 4098} 이에 더해, 딕셔너리 컴프리헨션은 임의의 키와 값 표현식들로 부터 딕셔너 리를 만드는데 사용될 수 있습니다: >>> {x: x**2 for x in (2, 4, |
| 3 | datastructures.txt | 12481 | 딕셔너리를 (한 딕셔너리 안에서) 키가 중복되지 않는다는 제약 조건을 가 진 *키: 값* 쌍의 집합으로 생각하는 것이 최선입니다. 중괄호 쌍은 빈 딕 셔너리를 만듭니다: "{}". 중괄호 안에 쉼표로 분리된 키:값 쌍들의 목록을 넣으면, 딕셔너리에 초기 키:값 쌍들을 제공합니다; 이것이 딕셔너리가 출 력되는 방식이기도 합니다. The main operations on a dictionary are storing a value  |
| 4 | stdtypes.txt | 188078 | A dictionary's keys are *almost* arbitrary values. Values that are not *hashable*, that is, values containing lists, dictionaries or other mutable types (that are compared by value rather than by object identity) may not be used as keys. Va |

### 5. 인코딩을 지정하여 텍스트 파일을 읽을 수 있는 pathlib 메서드는 무엇인가요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 2 | 0.500 |
| Hybrid Regex | 1 | 2 | 0.500 |
| Hybrid Kiwi | 0 | Top-4 내 없음 | 0.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | interpreter.txt | 3410 | 인코딩을 기본값 외의 것으로 선언하려면, 파일의 첫 줄에 특별한 형태의 주석 문을 추가해야 합니다. 문법은 이렇습니다: # -*- coding: encoding -*- *encoding* 은 파이썬이 지원하는 코덱 ("codecs") 중 하나여야 합니다. 예를 들어, Windows-1252 인코딩을 사용하도록 선언하려면, 소스 코드 파일 의 첫 줄은 이렇게 되어야 합니다: # -*- coding: cp1252 -*- 첫 줄 규 |
| 2 | pathlib.txt | 729 | 이전에 이 모듈을 사용한 적이 없거나 어떤 클래스가 작업에 적합한지 확신 이 없다면, "Path"가 가장 적합할 가능성이 높습니다. 코드가 실행되는 플 랫폼의 구상 경로를 인스턴스화 합니다. 순수한 경로는 특별한 경우에 유용합니다; 예를 들면: 1. 유닉스 기계에서 윈도우 경로를 조작하려고 할 때 (또는 그 반대). 유닉 스에서 실행할 때는 "WindowsPath"를 인스턴스화 할 수 없지만, "PureWindowsPath"는 |
| 3 | pathlib.txt | 56423 | As a consequence of these differences, pathlib is not a drop-in replacement for "os.path". Corresponding tools ------------------- 아래는 다양한 "os" 함수를 해당 "PurePath"/"Path" 대응 물에 매핑하는 표 입니다. |
| 4 | pathlib.txt | 1477 | 이 디렉터리 트리에 있는 파이썬 소스 파일 나열하기: >>> list(p.glob('**/*.py')) [PosixPath('test_pathlib.py'), PosixPath('setup.py'), PosixPath('pathlib.py'), PosixPath('docs/conf.py'), PosixPath('build/lib/pathlib.py')] 디렉터리 트리 내에서 탐색하기: >>> p = Path('/etc') >> |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | inputoutput.txt | 8812 | 텍스트 모드에서, 읽을 때의 기본 동작은 플랫폼 의존적인 줄 종료 (유닉스 에서 "\n", 윈도우에서 "\r\n") 를 단지 "\n" 로 변경하는 것입니다. 텍스 트 모드로 쓸 때, 기본 동작은 "\n" 를 다시 플랫폼 의존적인 줄 종료로 변 환하는 것입니다. 이 파일 데이터에 대한 무대 뒤의 수정은 텍스트 파일의 경우는 문제가 안 되지만, "JPEG" 이나 "EXE" 파일과 같은 바이너리 데이터 를 망치게 됩니다. 그런 파일 |
| 2 | pathlib.txt | 729 | 이전에 이 모듈을 사용한 적이 없거나 어떤 클래스가 작업에 적합한지 확신 이 없다면, "Path"가 가장 적합할 가능성이 높습니다. 코드가 실행되는 플 랫폼의 구상 경로를 인스턴스화 합니다. 순수한 경로는 특별한 경우에 유용합니다; 예를 들면: 1. 유닉스 기계에서 윈도우 경로를 조작하려고 할 때 (또는 그 반대). 유닉 스에서 실행할 때는 "WindowsPath"를 인스턴스화 할 수 없지만, "PureWindowsPath"는 |
| 3 | pathlib.txt | 33409 | 파일이 열린 다음에 닫힙니다. 선택적 매개 변수는 "open()"과 같은 의 미입니다. Added in version 3.5. 버전 3.13에서 변경: The *newline* parameter was added. Path.read_bytes() 가리키는 파일의 바이너리 내용을 바이트열 객체로 반환합니다: >>> p = Path('my_binary_file') >>> p.write_bytes(b'Binary file conte |
| 4 | interpreter.txt | 3410 | 인코딩을 기본값 외의 것으로 선언하려면, 파일의 첫 줄에 특별한 형태의 주석 문을 추가해야 합니다. 문법은 이렇습니다: # -*- coding: encoding -*- *encoding* 은 파이썬이 지원하는 코덱 ("codecs") 중 하나여야 합니다. 예를 들어, Windows-1252 인코딩을 사용하도록 선언하려면, 소스 코드 파일 의 첫 줄은 이렇게 되어야 합니다: # -*- coding: cp1252 -*- 첫 줄 규 |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | inputoutput.txt | 11790 | 텍스트 파일에서는 (모드 문자열에 "b" 가 없이 열린 것들), 파일의 시작에 상대적인 위치 변경만 허락되고 (예외는 "seek(0, 2)" 를 사용해서 파일의 끝으로 위치를 변경하는 경우입니다), 올바른 *offset* 값은 "f.tell()" 이 돌려준 값과 0뿐입니다. 그 밖의 다른 *offset* 값은 정의되지 않은 결과를 낳습니다. 파일 객체는 "isatty()" 나 "truncate()" 같은 몇 가지 메서드를 더  |
| 2 | interpreter.txt | 2632 | $ python3.14 Python 3.14 (default, April 4 2024, 09:25:04) [GCC 10.2.0] on linux Type "help", "copyright", "credits" or "license" for more information. >>> 이어지는 줄은 여러 줄로 구성된 구조물을 입력할 때 필요합니다. 예를 들 자면, 이런 식의 "if" 문이 가능합니다: >>> the_world_is_f |
| 3 | inputoutput.txt | 8812 | 텍스트 모드에서, 읽을 때의 기본 동작은 플랫폼 의존적인 줄 종료 (유닉스 에서 "\n", 윈도우에서 "\r\n") 를 단지 "\n" 로 변경하는 것입니다. 텍스 트 모드로 쓸 때, 기본 동작은 "\n" 를 다시 플랫폼 의존적인 줄 종료로 변 환하는 것입니다. 이 파일 데이터에 대한 무대 뒤의 수정은 텍스트 파일의 경우는 문제가 안 되지만, "JPEG" 이나 "EXE" 파일과 같은 바이너리 데이터 를 망치게 됩니다. 그런 파일 |
| 4 | interpreter.txt | 3410 | 인코딩을 기본값 외의 것으로 선언하려면, 파일의 첫 줄에 특별한 형태의 주석 문을 추가해야 합니다. 문법은 이렇습니다: # -*- coding: encoding -*- *encoding* 은 파이썬이 지원하는 코덱 ("codecs") 중 하나여야 합니다. 예를 들어, Windows-1252 인코딩을 사용하도록 선언하려면, 소스 코드 파일 의 첫 줄은 이렇게 되어야 합니다: # -*- coding: cp1252 -*- 첫 줄 규 |

### 6. 데이터클래스에 frozen=True를 지정하면 객체가 완전히 불변이 되나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 1 | 1.000 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | dataclasses.txt | 4867 | *eq* 와 *frozen* 이 모두 참이면, 기본적으로 "@dataclass" 는 "__hash__()" 메서드를 만듭니다. *eq* 가 참이고 *frozen* 이 거짓이 면, "__hash__()" 가 "None" 으로 설정되어 해시 불가능하다고 표시됩 니다(가변이기 때문입니다). 만약 *eq* 가 거짓이면, "__hash__()" 를 건드리지 않는데, 슈퍼 클래스의 "__hash__()" 가 사용된다는 뜻이 됩 니다 (슈 |
| 2 | dataclasses.txt | 15617 | *changes* 가 "init=False" 를 갖는 것으로 정의된 필드를 포함하는 것 은 에러입니다. 이 경우 "ValueError" 가 발생합니다. "replace()"를 호출하는 동안 "init=False" 필드가 어떻게 작동하는지 미리 경고합니다. 그것들은 소스 객체로부터 복사되는 것이 아니라, (초 기화되기는 한다면) "__post_init__()" 에서 초기화됩니다. "init=False" 필드는 거의 사용되지 않으 |
| 3 | dataclasses.txt | 20773 | "frozen=True" 를 사용할 때 약간의 성능 저하가 있습니다: "__init__()" 는 필드를 초기화하는데 간단한 대입을 사용할 수 없고, "object.__setattr__()" 을 사용해야 합니다. 계승 ==== When the dataclass is being created by the "@dataclass" decorator, it looks through all of the class's base classe |
| 4 | dataclasses.txt | 20184 | def __post_init__(self, database): if self.j is None and database is not None: self.j = database.lookup('j') c = C(10, database=my_database) 이 경우, "fields()" 는 "i" 와 "j" 를 위한 "Field" 객체를 반환하지만, "database" 는 반환하지 않습니다. 고정 인스턴스 =============  |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | dataclasses.txt | 4867 | *eq* 와 *frozen* 이 모두 참이면, 기본적으로 "@dataclass" 는 "__hash__()" 메서드를 만듭니다. *eq* 가 참이고 *frozen* 이 거짓이 면, "__hash__()" 가 "None" 으로 설정되어 해시 불가능하다고 표시됩 니다(가변이기 때문입니다). 만약 *eq* 가 거짓이면, "__hash__()" 를 건드리지 않는데, 슈퍼 클래스의 "__hash__()" 가 사용된다는 뜻이 됩 니다 (슈 |
| 2 | dataclasses.txt | 20184 | def __post_init__(self, database): if self.j is None and database is not None: self.j = database.lookup('j') c = C(10, database=my_database) 이 경우, "fields()" 는 "i" 와 "j" 를 위한 "Field" 객체를 반환하지만, "database" 는 반환하지 않습니다. 고정 인스턴스 =============  |
| 3 | dataclasses.txt | 3339 | * *order*: 참이면 (기본값은 "False"), "__lt__()", "__le__()", "__gt__()", "__ge__()" 메서드가 생성됩니다. 이것들은 클래스를 필 드의 튜플인 것처럼 순서대로 비교합니다. 비교되는 두 인스턴스는 같 은 형이어야 합니다. *order* 가 참이고 *eq* 가 거짓이면 "ValueError" 가 발생합니다. 클래스가 이미 "__lt__()", "__le__()", "__gt__( |
| 4 | dataclasses.txt | 15617 | *changes* 가 "init=False" 를 갖는 것으로 정의된 필드를 포함하는 것 은 에러입니다. 이 경우 "ValueError" 가 발생합니다. "replace()"를 호출하는 동안 "init=False" 필드가 어떻게 작동하는지 미리 경고합니다. 그것들은 소스 객체로부터 복사되는 것이 아니라, (초 기화되기는 한다면) "__post_init__()" 에서 초기화됩니다. "init=False" 필드는 거의 사용되지 않으 |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | dataclasses.txt | 4867 | *eq* 와 *frozen* 이 모두 참이면, 기본적으로 "@dataclass" 는 "__hash__()" 메서드를 만듭니다. *eq* 가 참이고 *frozen* 이 거짓이 면, "__hash__()" 가 "None" 으로 설정되어 해시 불가능하다고 표시됩 니다(가변이기 때문입니다). 만약 *eq* 가 거짓이면, "__hash__()" 를 건드리지 않는데, 슈퍼 클래스의 "__hash__()" 가 사용된다는 뜻이 됩 니다 (슈 |
| 2 | dataclasses.txt | 3339 | * *order*: 참이면 (기본값은 "False"), "__lt__()", "__le__()", "__gt__()", "__ge__()" 메서드가 생성됩니다. 이것들은 클래스를 필 드의 튜플인 것처럼 순서대로 비교합니다. 비교되는 두 인스턴스는 같 은 형이어야 합니다. *order* 가 참이고 *eq* 가 거짓이면 "ValueError" 가 발생합니다. 클래스가 이미 "__lt__()", "__le__()", "__gt__( |
| 3 | dataclasses.txt | 20184 | def __post_init__(self, database): if self.j is None and database is not None: self.j = database.lookup('j') c = C(10, database=my_database) 이 경우, "fields()" 는 "i" 와 "j" 를 위한 "Field" 객체를 반환하지만, "database" 는 반환하지 않습니다. 고정 인스턴스 =============  |
| 4 | dataclasses.txt | 15617 | *changes* 가 "init=False" 를 갖는 것으로 정의된 필드를 포함하는 것 은 에러입니다. 이 경우 "ValueError" 가 발생합니다. "replace()"를 호출하는 동안 "init=False" 필드가 어떻게 작동하는지 미리 경고합니다. 그것들은 소스 객체로부터 복사되는 것이 아니라, (초 기화되기는 한다면) "__post_init__()" 에서 초기화됩니다. "init=False" 필드는 거의 사용되지 않으 |

### 7. 가상환경의 Python 인터프리터를 사용하려면 반드시 가상환경을 활성화해야 하나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 1 | 1.000 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | library_venv.txt | 1841 | 가상 환경 만들기 ================ 가상 환경은 "venv" 모듈을 실행해서 만들어집니다: python -m venv /path/to/new/virtual/environment This creates the target directory (including parent directories as needed) and places a "pyvenv.cfg" file in it with a "home" key poin |
| 2 | tutorial_venv.txt | 737 | 12.2. 가상 환경 만들기 ====================== 가상 환경을 만들고 관리하는 데 사용되는 모듈은 "venv" 라고 합니다. "venv" 는 명령이 실행된 ("--version" 옵션으로 확인할 수 있는) 파이썬 버전을 설치합니다. 예를 들어, "python3.12"로 명령을 실행하면 버전 3.12 가 설치됩니다. 가상 환경을 만들려면, 원하는 디렉터리를 결정하고, "venv" 모듈을 스크립 트로 실행하는데 |
| 3 | library_venv.txt | 8490 | 가상 환경이 활성화되면, "VIRTUAL_ENV" 환경 변수가 환경의 경로로 설정됩 니다. 가상 환경을 사용하기 위해 명시적으로 활성화할 필요가 없기 때문에 , "VIRTUAL_ENV"로 가상 환경이 사용 중인지를 판단할 수 없습니다. 경고: |
| 4 | library_venv.txt | 704 | 가상 환경 내에서 사용될 때, pip와 같은 일반적인 설치 도구는 명시적으로 지정하지 않아도 파이썬 패키지를 가상 환경에 설치합니다. A virtual environment is (amongst other things): * Used to contain a specific Python interpreter and software libraries and binaries which are needed to support a pr |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | library_venv.txt | 1841 | 가상 환경 만들기 ================ 가상 환경은 "venv" 모듈을 실행해서 만들어집니다: python -m venv /path/to/new/virtual/environment This creates the target directory (including parent directories as needed) and places a "pyvenv.cfg" file in it with a "home" key poin |
| 2 | tutorial_venv.txt | 737 | 12.2. 가상 환경 만들기 ====================== 가상 환경을 만들고 관리하는 데 사용되는 모듈은 "venv" 라고 합니다. "venv" 는 명령이 실행된 ("--version" 옵션으로 확인할 수 있는) 파이썬 버전을 설치합니다. 예를 들어, "python3.12"로 명령을 실행하면 버전 3.12 가 설치됩니다. 가상 환경을 만들려면, 원하는 디렉터리를 결정하고, "venv" 모듈을 스크립 트로 실행하는데 |
| 3 | library_venv.txt | 8490 | 가상 환경이 활성화되면, "VIRTUAL_ENV" 환경 변수가 환경의 경로로 설정됩 니다. 가상 환경을 사용하기 위해 명시적으로 활성화할 필요가 없기 때문에 , "VIRTUAL_ENV"로 가상 환경이 사용 중인지를 판단할 수 없습니다. 경고: |
| 4 | library_venv.txt | 704 | 가상 환경 내에서 사용될 때, pip와 같은 일반적인 설치 도구는 명시적으로 지정하지 않아도 파이썬 패키지를 가상 환경에 설치합니다. A virtual environment is (amongst other things): * Used to contain a specific Python interpreter and software libraries and binaries which are needed to support a pr |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | tutorial_venv.txt | 737 | 12.2. 가상 환경 만들기 ====================== 가상 환경을 만들고 관리하는 데 사용되는 모듈은 "venv" 라고 합니다. "venv" 는 명령이 실행된 ("--version" 옵션으로 확인할 수 있는) 파이썬 버전을 설치합니다. 예를 들어, "python3.12"로 명령을 실행하면 버전 3.12 가 설치됩니다. 가상 환경을 만들려면, 원하는 디렉터리를 결정하고, "venv" 모듈을 스크립 트로 실행하는데 |
| 2 | library_venv.txt | 8490 | 가상 환경이 활성화되면, "VIRTUAL_ENV" 환경 변수가 환경의 경로로 설정됩 니다. 가상 환경을 사용하기 위해 명시적으로 활성화할 필요가 없기 때문에 , "VIRTUAL_ENV"로 가상 환경이 사용 중인지를 판단할 수 없습니다. 경고: |
| 3 | tutorial_venv.txt | 1443 | (이 스크립트는 bash 셸을 위해 작성된 것으로, **csh** 또는 **fish** 셸 을 사용하는 경우에는, 대신 "activate.csh" 와 "activate.fish" 스크립트 를 사용해야 합니다.) 가상 환경을 활성화하면, 셸의 프롬프트가 변경되어 사용 중인 가상 환경을 보여주고, 환경을 수정하여 "python" 을 실행하면 특정 버전의 파이썬이 실 행되도록 합니다. 예를 들어: $ source ~/envs/tut |
| 4 | library_venv.txt | 1841 | 가상 환경 만들기 ================ 가상 환경은 "venv" 모듈을 실행해서 만들어집니다: python -m venv /path/to/new/virtual/environment This creates the target directory (including parent directories as needed) and places a "pyvenv.cfg" file in it with a "home" key poin |

### 8. 변경 가능한 기본 인수가 여러 함수 호출 사이에서 공유되는 이유는 무엇인가요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 1 | 1.000 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | programming.txt | 12074 | 그러나, 같은 연산이 때때로 형에 따라 다른 동작을 갖는 한 가지 연산 클 래스가 있습니다: 증분 대입 연산자. 예를 들어, "+="는 리스트를 변경하지 만, 튜플이나 정수는 변경하지 않습니다 ("a_list += [1, 2, 3]"은 "a_list.extend([1, 2, 3])"과 동등하고 "a_list"를 변경하지만, "some_tuple += (1, 2, 3)"과 "some_int += 1"은 새 객체를 만듭니다). 달 |
| 2 | programming.txt | 9057 | # Callers can only provide two parameters and optionally pass _cache by keyword def expensive(arg1, arg2, *, _cache={}): if (arg1, arg2) in _cache: return _cache[(arg1, arg2)] # Calculate the value result = ... expensive computation ... _ca |
| 3 | programming.txt | 12795 | 출력 매개변수가 있는 함수를 작성하려면 어떻게 해야 합니까 (참조에 의한 호출)? ----------------------------------------------------------------------------- Remember that arguments are passed by assignment in Python. Since assignment just creates references to objects, the |
| 4 | programming.txt | 8338 | 종종 함수 호출이 기본값으로 새 객체를 만들 것으로 기대합니다. 그렇게 되지 않습니다. 함수가 정의될 때, 기본값은 정확히 한 번 만들어집니다. 이 예제의 딕셔너리와 같이, 해당 객체가 변경되면, 함수에 대한 후속 호출 은 이 변경된 객체를 참조합니다. 정의에 따라, 숫자, 문자열, 튜플 및 "None"과 같은 불변 객체는 변경에 안 전합니다. 딕셔너리, 리스트 및 클래스 인스턴스와 같은 가변 객체를 변경 하면 혼란스러울 수  |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | programming.txt | 7586 | 순환 임포트를 피하거나 모듈의 초기화 시간을 줄이려는 등의 문제를 해결 하는 데 필요할 때만, 함수 정의 내부와 같은 지역 스코프로 임포트를 옮기 십시오. 이 기법은 프로그램 실행 방법에 따라 많은 임포트가 필요하지 않 을 때 특히 유용합니다. 모듈이 해당 함수에서만 사용될 때 임포트를 함수 로 옮기고 싶을 수도 있습니다. 모듈의 일회성 초기화 때문에 모듈을 처음 로드하는 데 비용이 많이들 수 있지만, 모듈을 여러 번 로드하는 |
| 2 | controlflow.txt | 29511 | * 여러분의 코드를 국제적인 환경에서 사용하려고 한다면 특별한 인코딩을 사용하지 마세요. 어떤 경우에도 파이썬의 기본, UTF-8, 또는 단순 ASCII 조차, 이 최선입니다. * 마찬가지로, 다른 언어를 사용하는 사람이 코드를 읽거나 유지할 약간의 가능성만 있더라도, 식별자에 ASCII 이외의 문자를 사용하지 마세요. -[ 각주 ]- [1] 실제로, *객체 참조에 의한 호출 (call by object reference)*  |
| 3 | programming.txt | 12074 | 그러나, 같은 연산이 때때로 형에 따라 다른 동작을 갖는 한 가지 연산 클 래스가 있습니다: 증분 대입 연산자. 예를 들어, "+="는 리스트를 변경하지 만, 튜플이나 정수는 변경하지 않습니다 ("a_list += [1, 2, 3]"은 "a_list.extend([1, 2, 3])"과 동등하고 "a_list"를 변경하지만, "some_tuple += (1, 2, 3)"과 "some_int += 1"은 새 객체를 만듭니다). 달 |
| 4 | programming.txt | 9057 | # Callers can only provide two parameters and optionally pass _cache by keyword def expensive(arg1, arg2, *, _cache={}): if (arg1, arg2) in _cache: return _cache[(arg1, arg2)] # Calculate the value result = ... expensive computation ... _ca |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | programming.txt | 8338 | 종종 함수 호출이 기본값으로 새 객체를 만들 것으로 기대합니다. 그렇게 되지 않습니다. 함수가 정의될 때, 기본값은 정확히 한 번 만들어집니다. 이 예제의 딕셔너리와 같이, 해당 객체가 변경되면, 함수에 대한 후속 호출 은 이 변경된 객체를 참조합니다. 정의에 따라, 숫자, 문자열, 튜플 및 "None"과 같은 불변 객체는 변경에 안 전합니다. 딕셔너리, 리스트 및 클래스 인스턴스와 같은 가변 객체를 변경 하면 혼란스러울 수  |
| 2 | programming.txt | 7586 | 순환 임포트를 피하거나 모듈의 초기화 시간을 줄이려는 등의 문제를 해결 하는 데 필요할 때만, 함수 정의 내부와 같은 지역 스코프로 임포트를 옮기 십시오. 이 기법은 프로그램 실행 방법에 따라 많은 임포트가 필요하지 않 을 때 특히 유용합니다. 모듈이 해당 함수에서만 사용될 때 임포트를 함수 로 옮기고 싶을 수도 있습니다. 모듈의 일회성 초기화 때문에 모듈을 처음 로드하는 데 비용이 많이들 수 있지만, 모듈을 여러 번 로드하는 |
| 3 | controlflow.txt | 29511 | * 여러분의 코드를 국제적인 환경에서 사용하려고 한다면 특별한 인코딩을 사용하지 마세요. 어떤 경우에도 파이썬의 기본, UTF-8, 또는 단순 ASCII 조차, 이 최선입니다. * 마찬가지로, 다른 언어를 사용하는 사람이 코드를 읽거나 유지할 약간의 가능성만 있더라도, 식별자에 ASCII 이외의 문자를 사용하지 마세요. -[ 각주 ]- [1] 실제로, *객체 참조에 의한 호출 (call by object reference)*  |
| 4 | controlflow.txt | 15887 | 4.9. 함수 정의 더 보기 ====================== 정해지지 않은 개수의 인자들로 함수를 정의하는 것도 가능합니다. 세 가지 형식이 있는데, 조합할 수 있습니다. 4.9.1. 기본 인자 값 ------------------- 가장 쓸모 있는 형식은 하나나 그 이상 인자들의 기본값을 지정하는 것입니 다. 정의된 것보다 더 적은 개수의 인자들로 호출될 수 있는 함수를 만듭니 다. 예를 들어: def ask_ok( |

### 9. 스크립트를 직접 실행할 때 __name__의 값은 무엇이며, 이를 이용해 직접 실행할 때만 코드를 실행하려면 어떻게 하나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 0 | Top-4 내 없음 | 0.000 |
| Hybrid Regex | 0 | Top-4 내 없음 | 0.000 |
| Hybrid Kiwi | 0 | Top-4 내 없음 | 0.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | library_venv.txt | 25693 | if __name__ == '__main__': rc = 1 try: main() rc = 0 except Exception as e: print('Error: %s' % e, file=sys.stderr) sys.exit(rc) 이 스크립트는 온라인에서 내려받을 수도 있습니다. |
| 2 | programming.txt | 56699 | "foo"에 대한 ".pyc" 파일을 만들 필요가 있으면 -- 즉, 임포트 되지 않는 모듈에 대한 ".pyc" 파일을 만들려면 -- "py_compile"과 "compileall" 모듈 을 사용할 수 있습니다. "py_compile" 모듈은 임의의 모듈을 수동으로 컴파일할 수 있습니다. 한 가 지 방법은 해당 모듈에서 "compile()" 함수를 대화식으로 사용하는 것입니 다: >>> import py_compile >>> p |
| 3 | programming.txt | 16530 | 코드에서 객체 이름을 어떻게 찾을 수 있습니까? --------------------------------------------- 일반적으로 말하자면, 객체에는 실제로 이름이 없기 때문에 그럴 수 없습니 다. 기본적으로, 대입은 항상 이름을 값에 연결합니다; "def"와 "class" 문 의 경우도 마찬가지이지만, 이 경우 값은 콜러블입니다. 다음 코드를 고려 하십시오: >>> class A: ... pass ... >>> B |
| 4 | appendix.txt | 1493 | 16.1.2. 실행 가능한 파이썬 스크립트 ----------------------------------- BSD 스타일의 유닉스 시스템에서 파이썬 스크립트는 셸 스크립트처럼 직접 실행할 수 있게 만들 수 있습니다. 다음과 같은 줄 #!/usr/bin/env python3 (인터프리터가 사용자의 "PATH" 에 있다고 가정할 때)을 스크립트의 시작 부분에 넣고 파일에 실행 가능 모드를 줍니다. "#!" 는 반드시 파일의 처음  |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | appendix.txt | 1493 | 16.1.2. 실행 가능한 파이썬 스크립트 ----------------------------------- BSD 스타일의 유닉스 시스템에서 파이썬 스크립트는 셸 스크립트처럼 직접 실행할 수 있게 만들 수 있습니다. 다음과 같은 줄 #!/usr/bin/env python3 (인터프리터가 사용자의 "PATH" 에 있다고 가정할 때)을 스크립트의 시작 부분에 넣고 파일에 실행 가능 모드를 줍니다. "#!" 는 반드시 파일의 처음  |
| 2 | programming.txt | 56699 | "foo"에 대한 ".pyc" 파일을 만들 필요가 있으면 -- 즉, 임포트 되지 않는 모듈에 대한 ".pyc" 파일을 만들려면 -- "py_compile"과 "compileall" 모듈 을 사용할 수 있습니다. "py_compile" 모듈은 임의의 모듈을 수동으로 컴파일할 수 있습니다. 한 가 지 방법은 해당 모듈에서 "compile()" 함수를 대화식으로 사용하는 것입니 다: >>> import py_compile >>> p |
| 3 | library_venv.txt | 25693 | if __name__ == '__main__': rc = 1 try: main() rc = 0 except Exception as e: print('Error: %s' % e, file=sys.stderr) sys.exit(rc) 이 스크립트는 온라인에서 내려받을 수도 있습니다. |
| 4 | programming.txt | 16530 | 코드에서 객체 이름을 어떻게 찾을 수 있습니까? --------------------------------------------- 일반적으로 말하자면, 객체에는 실제로 이름이 없기 때문에 그럴 수 없습니 다. 기본적으로, 대입은 항상 이름을 값에 연결합니다; "def"와 "class" 문 의 경우도 마찬가지이지만, 이 경우 값은 콜러블입니다. 다음 코드를 고려 하십시오: >>> class A: ... pass ... >>> B |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | appendix.txt | 1493 | 16.1.2. 실행 가능한 파이썬 스크립트 ----------------------------------- BSD 스타일의 유닉스 시스템에서 파이썬 스크립트는 셸 스크립트처럼 직접 실행할 수 있게 만들 수 있습니다. 다음과 같은 줄 #!/usr/bin/env python3 (인터프리터가 사용자의 "PATH" 에 있다고 가정할 때)을 스크립트의 시작 부분에 넣고 파일에 실행 가능 모드를 줍니다. "#!" 는 반드시 파일의 처음  |
| 2 | programming.txt | 56699 | "foo"에 대한 ".pyc" 파일을 만들 필요가 있으면 -- 즉, 임포트 되지 않는 모듈에 대한 ".pyc" 파일을 만들려면 -- "py_compile"과 "compileall" 모듈 을 사용할 수 있습니다. "py_compile" 모듈은 임의의 모듈을 수동으로 컴파일할 수 있습니다. 한 가 지 방법은 해당 모듈에서 "compile()" 함수를 대화식으로 사용하는 것입니 다: >>> import py_compile >>> p |
| 3 | library_venv.txt | 25693 | if __name__ == '__main__': rc = 1 try: main() rc = 0 except Exception as e: print('Error: %s' % e, file=sys.stderr) sys.exit(rc) 이 스크립트는 온라인에서 내려받을 수도 있습니다. |
| 4 | programming.txt | 16530 | 코드에서 객체 이름을 어떻게 찾을 수 있습니까? --------------------------------------------- 일반적으로 말하자면, 객체에는 실제로 이름이 없기 때문에 그럴 수 없습니 다. 기본적으로, 대입은 항상 이름을 값에 연결합니다; "def"와 "class" 문 의 경우도 마찬가지이지만, 이 경우 값은 콜러블입니다. 다음 코드를 고려 하십시오: >>> class A: ... pass ... >>> B |

### 10. range 함수가 만드는 수열에 stop 값 자체도 포함되나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 2 | 0.500 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | controlflow.txt | 2457 | 하지만, 그럴 때 대부분은, "enumerate()" 함수를 쓰는 것이 편리합니다, 루프 테크닉 를 보세요. 범위를 그냥 인쇄하면 이상한 일이 일어납니다: >>> range(10) range(0, 10) 많은 경우에 "range()"가 돌려준 객체는 리스트인 것처럼 동작하지만, 사실 리스트가 아닙니다. 이터레이트할 때 원하는 시퀀스 항목들을 순서대로 돌 려주는 객체이지만, 실제로 리스트를 만들지 않아서 공간을 절약합니다. We |
| 2 | stdtypes.txt | 53043 | Ranges implement all of the common sequence operations except concatenation and repetition (due to the fact that range objects can only represent sequences that follow a strict pattern and repetition and concatenation will usually violate t |
| 3 | stdtypes.txt | 51420 | The "range" type represents an immutable sequence of numbers and is commonly used for looping a specific number of times in "for" loops. class range(stop, /) class range(start, stop, step=1, /) The arguments to the range constructor must be |
| 4 | datastructures.txt | 5387 | >>> vec = [-4, -2, 0, 2, 4] >>> # 값을 두배로 하여 새 리스트를 만듭니다 >>> [x*2 for x in vec] [-8, -4, 0, 4, 8] >>> # 음수를 제외하도록 리스트를 필터링합니다 >>> [x for x in vec if x >= 0] [0, 2, 4] >>> # 모든 요소에 함수를 적용합니다 >>> [abs(x) for x in vec] [4, 2, 0, 2, 4] >>> # 각 요 |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | stdtypes.txt | 51420 | The "range" type represents an immutable sequence of numbers and is commonly used for looping a specific number of times in "for" loops. class range(stop, /) class range(start, stop, step=1, /) The arguments to the range constructor must be |
| 2 | stdtypes.txt | 53043 | Ranges implement all of the common sequence operations except concatenation and repetition (due to the fact that range objects can only represent sequences that follow a strict pattern and repetition and concatenation will usually violate t |
| 3 | functions.txt | 65451 | Added in version 3.13. class range(stop, /) class range(start, stop, step=1, /) Rather than being a function, "range" is actually an immutable sequence type, as documented in Ranges and Sequence Types --- list, tuple, range. repr(object, /) |
| 4 | controlflow.txt | 2457 | 하지만, 그럴 때 대부분은, "enumerate()" 함수를 쓰는 것이 편리합니다, 루프 테크닉 를 보세요. 범위를 그냥 인쇄하면 이상한 일이 일어납니다: >>> range(10) range(0, 10) 많은 경우에 "range()"가 돌려준 객체는 리스트인 것처럼 동작하지만, 사실 리스트가 아닙니다. 이터레이트할 때 원하는 시퀀스 항목들을 순서대로 돌 려주는 객체이지만, 실제로 리스트를 만들지 않아서 공간을 절약합니다. We |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | stdtypes.txt | 53043 | Ranges implement all of the common sequence operations except concatenation and repetition (due to the fact that range objects can only represent sequences that follow a strict pattern and repetition and concatenation will usually violate t |
| 2 | stdtypes.txt | 51420 | The "range" type represents an immutable sequence of numbers and is commonly used for looping a specific number of times in "for" loops. class range(stop, /) class range(start, stop, step=1, /) The arguments to the range constructor must be |
| 3 | controlflow.txt | 2457 | 하지만, 그럴 때 대부분은, "enumerate()" 함수를 쓰는 것이 편리합니다, 루프 테크닉 를 보세요. 범위를 그냥 인쇄하면 이상한 일이 일어납니다: >>> range(10) range(0, 10) 많은 경우에 "range()"가 돌려준 객체는 리스트인 것처럼 동작하지만, 사실 리스트가 아닙니다. 이터레이트할 때 원하는 시퀀스 항목들을 순서대로 돌 려주는 객체이지만, 실제로 리스트를 만들지 않아서 공간을 절약합니다. We |
| 4 | datastructures.txt | 5387 | >>> vec = [-4, -2, 0, 2, 4] >>> # 값을 두배로 하여 새 리스트를 만듭니다 >>> [x*2 for x in vec] [-8, -4, 0, 4, 8] >>> # 음수를 제외하도록 리스트를 필터링합니다 >>> [x for x in vec if x >= 0] [0, 2, 4] >>> # 모든 요소에 함수를 적용합니다 >>> [abs(x) for x in vec] [4, 2, 0, 2, 4] >>> # 각 요 |

### 11. 리스트의 append와 extend는 어떤 차이가 있나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 0 | Top-4 내 없음 | 0.000 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 3 | 0.333 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | programming.txt | 32602 | 리스트를 사용하십시오: ["this", 1, "is", "an", "array"] 리스트는 시간 복잡성 면에서 C나 파스칼(Pascal) 배열과 동등합니다; 가장 큰 차이점은 파이썬 리스트에 다양한 형의 객체가 포함될 수 있다는 것입니 다. The "array" module also provides methods for creating arrays of fixed types with compact representations, |
| 2 | introduction.txt | 9213 | 리스트는 이어붙이기 같은 연산도 지원합니다: >>> squares + [36, 49, 64, 81, 100] [1, 4, 9, 16, 25, 36, 49, 64, 81, 100] *불변* 인 문자열과는 달리, 리스트는 *가변* 입니다. 즉 내용을 변경할 수 있습니다: >>> cubes = [1, 8, 27, 65, 125] # 여기 뭔가 잘못 됐습니다 >>> 4 ** 3 # 4의 세제곱은 65가 아니라 64입니다! 64 >>> |
| 3 | programming.txt | 10520 | >>> x = [] >>> y = x >>> y.append(10) >>> y [10] >>> x [10] "y"에 요소를 추가하면 "x"도 변경되는 이유가 궁금할 것입니다. 이 결과를 만드는 두 가지 요소가 있습니다: 1. 변수는 단순히 객체를 가리키는 이름입니다. "y = x"를 수행하면 리스트 의 사본을 만들지 않습니다 -- "x"가 참조하는 것과 같은 객체를 참조하 는 새 변수 "y"를 만듭니다. 이는 하나의 객체(리스 |
| 4 | programming.txt | 35739 | 예외는 조금 더 놀랍습니다, 더 놀라운 것은 에러가 있었지만 더하기가 동 작했다는 사실입니다: >>> a_tuple[0] ['foo', 'item'] To see why this happens, you need to know that (a) if an object implements an "__iadd__()" magic method, it gets called when the "+=" augmented assignment i |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | datastructures.txt | 1453 | list.reverse() 리스트의 요소들을 제자리에서 뒤집습니다. list.copy() 리스트의 얕은 사본을 돌려줍니다. "a[:]" 와 비슷합니다. 리스트 메서드 대부분을 사용하는 예: >>> fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana'] >>> fruits.count('apple') 2 >>> fruits.count('tangerine' |
| 2 | programming.txt | 10520 | >>> x = [] >>> y = x >>> y.append(10) >>> y [10] >>> x [10] "y"에 요소를 추가하면 "x"도 변경되는 이유가 궁금할 것입니다. 이 결과를 만드는 두 가지 요소가 있습니다: 1. 변수는 단순히 객체를 가리키는 이름입니다. "y = x"를 수행하면 리스트 의 사본을 만들지 않습니다 -- "x"가 참조하는 것과 같은 객체를 참조하 는 새 변수 "y"를 만듭니다. 이는 하나의 객체(리스 |
| 3 | datastructures.txt | 0 | 5. 자료 구조 ************ 이 장에서는 여러분이 이미 배운 것들을 좀 더 자세히 설명하고, 몇 가지 새로운 것들을 덧붙입니다. 5.1. 리스트 더 보기 =================== The list data type has some more methods. Here are all of the methods of list objects: list.append(value, /) 리스트의 끝에 항목을 더합니다. " |
| 4 | programming.txt | 32602 | 리스트를 사용하십시오: ["this", 1, "is", "an", "array"] 리스트는 시간 복잡성 면에서 C나 파스칼(Pascal) 배열과 동등합니다; 가장 큰 차이점은 파이썬 리스트에 다양한 형의 객체가 포함될 수 있다는 것입니 다. The "array" module also provides methods for creating arrays of fixed types with compact representations, |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | programming.txt | 10520 | >>> x = [] >>> y = x >>> y.append(10) >>> y [10] >>> x [10] "y"에 요소를 추가하면 "x"도 변경되는 이유가 궁금할 것입니다. 이 결과를 만드는 두 가지 요소가 있습니다: 1. 변수는 단순히 객체를 가리키는 이름입니다. "y = x"를 수행하면 리스트 의 사본을 만들지 않습니다 -- "x"가 참조하는 것과 같은 객체를 참조하 는 새 변수 "y"를 만듭니다. 이는 하나의 객체(리스 |
| 2 | introduction.txt | 8468 | String Methods 문자열은 기본적인 변환과 검색을 위한 여러 가지 메서드들을 지원합 니다. 포맷 문자열 리터럴 내장된 표현식을 갖는 문자열 리터럴 Format string syntax "str.format()" 으로 문자열을 포맷하는 방법에 대한 정보. printf-style String Formatting 이곳에서 문자열을 "%" 연산자 왼쪽에 사용하는 예전 방식의 포매팅에 관해 좀 더 상세하게 설명하고 있습니다.  |
| 3 | datastructures.txt | 0 | 5. 자료 구조 ************ 이 장에서는 여러분이 이미 배운 것들을 좀 더 자세히 설명하고, 몇 가지 새로운 것들을 덧붙입니다. 5.1. 리스트 더 보기 =================== The list data type has some more methods. Here are all of the methods of list objects: list.append(value, /) 리스트의 끝에 항목을 더합니다. " |
| 4 | programming.txt | 32602 | 리스트를 사용하십시오: ["this", 1, "is", "an", "array"] 리스트는 시간 복잡성 면에서 C나 파스칼(Pascal) 배열과 동등합니다; 가장 큰 차이점은 파이썬 리스트에 다양한 형의 객체가 포함될 수 있다는 것입니 다. The "array" module also provides methods for creating arrays of fixed types with compact representations, |

### 12. 요소가 하나뿐인 튜플을 만들 때 끝에 쉼표가 필요한 이유는 무엇인가요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 1 | 1.000 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | datastructures.txt | 9167 | 여러분이 보듯이, 출력되는 튜플은 항상 괄호로 둘러싸입니다, 그래서 중첩 된 튜플이 올바르게 해석됩니다; 종종 괄호가 필요하기는 하지만 (튜플이 더 큰 표현식의 일부일 때), 둘러싼 괄호와 함께 또는 없이 입력될 수 있습 니다. 튜플의 개별 항목에 대입하는 것은 가능하지 않지만, 리스트 같은 가 변 객체를 포함하는 튜플을 만들 수는 있습니다. 튜플이 리스트처럼 보인다 하더라도, 이것들은 다른 상황에서 다른 목적으 로 사용됩니다 |
| 2 | programming.txt | 17343 | comp.lang.python에서, Fredrik Lundh는 언젠가 이 질문에 대해 훌륭한 비 유를 했습니다: 여러분이 현관에서 발견한 고양이의 이름을 얻는 것과 같은 방법: 고양 이(객체) 자체는 여러분에게 자신의 이름을 말할 수 없고, 전혀 신경 쓰 지도 않습니다 -- 따라서 그것이 어떻게 불리는지 알아내는 유일한 방법 은 여러분 이웃 모두(이름 공간)에게 자신의 고양이(객체)인지 묻는 것 입니다... .... 여러 이름 |
| 3 | controlflow.txt | 5209 | (이것은 올바른 코드입니다. 자세히 들여다보면: "else" 절은 "if" 문이 ** 아니라** "for" 루프에 속합니다.) One way to think of the else clause is to imagine it paired with the "if" inside the loop. As the loop executes, it will run a sequence like if/if/if/else. The "if" is i |
| 4 | stdlib2.txt | 3554 | img_1074.jpg --> Ashley_0.jpg img_1076.jpg --> Ashley_1.jpg img_1077.jpg --> Ashley_2.jpg 템플릿의 또 다른 응용은 다중 출력 형식의 세부 사항에서 프로그램 논리를 분리하는 것입니다. 이렇게 하면 XML 파일, 일반 텍스트 보고서 및 HTML 웹 보고서에 대한 커스텀 템플릿을 치환할 수 있습니다. 11.3. Working with binary data rec |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | datastructures.txt | 9167 | 여러분이 보듯이, 출력되는 튜플은 항상 괄호로 둘러싸입니다, 그래서 중첩 된 튜플이 올바르게 해석됩니다; 종종 괄호가 필요하기는 하지만 (튜플이 더 큰 표현식의 일부일 때), 둘러싼 괄호와 함께 또는 없이 입력될 수 있습 니다. 튜플의 개별 항목에 대입하는 것은 가능하지 않지만, 리스트 같은 가 변 객체를 포함하는 튜플을 만들 수는 있습니다. 튜플이 리스트처럼 보인다 하더라도, 이것들은 다른 상황에서 다른 목적으 로 사용됩니다 |
| 2 | programming.txt | 17343 | comp.lang.python에서, Fredrik Lundh는 언젠가 이 질문에 대해 훌륭한 비 유를 했습니다: 여러분이 현관에서 발견한 고양이의 이름을 얻는 것과 같은 방법: 고양 이(객체) 자체는 여러분에게 자신의 이름을 말할 수 없고, 전혀 신경 쓰 지도 않습니다 -- 따라서 그것이 어떻게 불리는지 알아내는 유일한 방법 은 여러분 이웃 모두(이름 공간)에게 자신의 고양이(객체)인지 묻는 것 입니다... .... 여러 이름 |
| 3 | controlflow.txt | 5209 | (이것은 올바른 코드입니다. 자세히 들여다보면: "else" 절은 "if" 문이 ** 아니라** "for" 루프에 속합니다.) One way to think of the else clause is to imagine it paired with the "if" inside the loop. As the loop executes, it will run a sequence like if/if/if/else. The "if" is i |
| 4 | stdlib2.txt | 3554 | img_1074.jpg --> Ashley_0.jpg img_1076.jpg --> Ashley_1.jpg img_1077.jpg --> Ashley_2.jpg 템플릿의 또 다른 응용은 다중 출력 형식의 세부 사항에서 프로그램 논리를 분리하는 것입니다. 이렇게 하면 XML 파일, 일반 텍스트 보고서 및 HTML 웹 보고서에 대한 커스텀 템플릿을 치환할 수 있습니다. 11.3. Working with binary data rec |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | datastructures.txt | 9167 | 여러분이 보듯이, 출력되는 튜플은 항상 괄호로 둘러싸입니다, 그래서 중첩 된 튜플이 올바르게 해석됩니다; 종종 괄호가 필요하기는 하지만 (튜플이 더 큰 표현식의 일부일 때), 둘러싼 괄호와 함께 또는 없이 입력될 수 있습 니다. 튜플의 개별 항목에 대입하는 것은 가능하지 않지만, 리스트 같은 가 변 객체를 포함하는 튜플을 만들 수는 있습니다. 튜플이 리스트처럼 보인다 하더라도, 이것들은 다른 상황에서 다른 목적으 로 사용됩니다 |
| 2 | programming.txt | 17343 | comp.lang.python에서, Fredrik Lundh는 언젠가 이 질문에 대해 훌륭한 비 유를 했습니다: 여러분이 현관에서 발견한 고양이의 이름을 얻는 것과 같은 방법: 고양 이(객체) 자체는 여러분에게 자신의 이름을 말할 수 없고, 전혀 신경 쓰 지도 않습니다 -- 따라서 그것이 어떻게 불리는지 알아내는 유일한 방법 은 여러분 이웃 모두(이름 공간)에게 자신의 고양이(객체)인지 묻는 것 입니다... .... 여러 이름 |
| 3 | controlflow.txt | 5209 | (이것은 올바른 코드입니다. 자세히 들여다보면: "else" 절은 "if" 문이 ** 아니라** "for" 루프에 속합니다.) One way to think of the else clause is to imagine it paired with the "if" inside the loop. As the loop executes, it will run a sequence like if/if/if/else. The "if" is i |
| 4 | stdlib2.txt | 3554 | img_1074.jpg --> Ashley_0.jpg img_1076.jpg --> Ashley_1.jpg img_1077.jpg --> Ashley_2.jpg 템플릿의 또 다른 응용은 다중 출력 형식의 세부 사항에서 프로그램 논리를 분리하는 것입니다. 이렇게 하면 XML 파일, 일반 텍스트 보고서 및 HTML 웹 보고서에 대한 커스텀 템플릿을 치환할 수 있습니다. 11.3. Working with binary data rec |

### 13. 빈 집합을 만들 때 중괄호 대신 set 함수를 사용해야 하는 이유는 무엇인가요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 4 | 0.250 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | controlflow.txt | 13534 | 함수의 *실행*은 함수의 지역 변수들을 위한 새 심볼 테이블을 만듭니다. 좀 더 구체적으로, 함수에서의 모든 변수 대입들은 값을 지역 심볼 테이블 에 저장합니다; 반면에 변수 참조는 먼저 지역 심볼 테이블을 본 다음, 전 역 심볼 테이블을 본 후, 마지막으로 내장 이름들의 테이블을 살핍니다. 그 래서, 참조될 수는 있다 하더라도, 전역 변수들과 둘러싸는 함수의 변수들 은 함수 내에서 직접 값이 대입될 수 없습니다 (전역 변수를 |
| 2 | programming.txt | 12074 | 그러나, 같은 연산이 때때로 형에 따라 다른 동작을 갖는 한 가지 연산 클 래스가 있습니다: 증분 대입 연산자. 예를 들어, "+="는 리스트를 변경하지 만, 튜플이나 정수는 변경하지 않습니다 ("a_list += [1, 2, 3]"은 "a_list.extend([1, 2, 3])"과 동등하고 "a_list"를 변경하지만, "some_tuple += (1, 2, 3)"과 "some_int += 1"은 새 객체를 만듭니다). 달 |
| 3 | controlflow.txt | 29511 | * 여러분의 코드를 국제적인 환경에서 사용하려고 한다면 특별한 인코딩을 사용하지 마세요. 어떤 경우에도 파이썬의 기본, UTF-8, 또는 단순 ASCII 조차, 이 최선입니다. * 마찬가지로, 다른 언어를 사용하는 사람이 코드를 읽거나 유지할 약간의 가능성만 있더라도, 식별자에 ASCII 이외의 문자를 사용하지 마세요. -[ 각주 ]- [1] 실제로, *객체 참조에 의한 호출 (call by object reference)*  |
| 4 | datastructures.txt | 11087 | >>> # 두 단어의 고유한 글자들로 집합 연산 시연 >>> >>> a = set('abracadabra') >>> b = set('alacazam') >>> a # a 의 고유한 글자들 {'a', 'r', 'b', 'c', 'd'} >>> a - b # a 에 있으나 b 에 없는 글자들 {'r', 'd', 'b'} >>> a \| b # a 나 b, 혹은 양쪽 모두에 있는 글자들 {'a', 'c', 'r', 'd', 'b',  |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | datastructures.txt | 9929 | 문장 "t = 12345, 54321, 'hello!'" 는 *튜플 패킹* 의 예입니다: 값 "12345", "54321", "'hello!'" 는 함께 튜플로 패킹 됩니다. 반대 연산 또 한 가능합니다: >>> x, y, z = t 이것은, 충분히 적절하게도, *시퀀스 언 패킹* 이라고 불리고 오른쪽에 어 떤 시퀀스가 와도 됩니다. 시퀀스 언 패킹은 등호의 좌변에 시퀀스에 있는 요소들과 같은 개수의 변수들이 올 것을 요구합니 |
| 2 | controlflow.txt | 13534 | 함수의 *실행*은 함수의 지역 변수들을 위한 새 심볼 테이블을 만듭니다. 좀 더 구체적으로, 함수에서의 모든 변수 대입들은 값을 지역 심볼 테이블 에 저장합니다; 반면에 변수 참조는 먼저 지역 심볼 테이블을 본 다음, 전 역 심볼 테이블을 본 후, 마지막으로 내장 이름들의 테이블을 살핍니다. 그 래서, 참조될 수는 있다 하더라도, 전역 변수들과 둘러싸는 함수의 변수들 은 함수 내에서 직접 값이 대입될 수 없습니다 (전역 변수를 |
| 3 | programming.txt | 12074 | 그러나, 같은 연산이 때때로 형에 따라 다른 동작을 갖는 한 가지 연산 클 래스가 있습니다: 증분 대입 연산자. 예를 들어, "+="는 리스트를 변경하지 만, 튜플이나 정수는 변경하지 않습니다 ("a_list += [1, 2, 3]"은 "a_list.extend([1, 2, 3])"과 동등하고 "a_list"를 변경하지만, "some_tuple += (1, 2, 3)"과 "some_int += 1"은 새 객체를 만듭니다). 달 |
| 4 | controlflow.txt | 29511 | * 여러분의 코드를 국제적인 환경에서 사용하려고 한다면 특별한 인코딩을 사용하지 마세요. 어떤 경우에도 파이썬의 기본, UTF-8, 또는 단순 ASCII 조차, 이 최선입니다. * 마찬가지로, 다른 언어를 사용하는 사람이 코드를 읽거나 유지할 약간의 가능성만 있더라도, 식별자에 ASCII 이외의 문자를 사용하지 마세요. -[ 각주 ]- [1] 실제로, *객체 참조에 의한 호출 (call by object reference)*  |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | datastructures.txt | 9929 | 문장 "t = 12345, 54321, 'hello!'" 는 *튜플 패킹* 의 예입니다: 값 "12345", "54321", "'hello!'" 는 함께 튜플로 패킹 됩니다. 반대 연산 또 한 가능합니다: >>> x, y, z = t 이것은, 충분히 적절하게도, *시퀀스 언 패킹* 이라고 불리고 오른쪽에 어 떤 시퀀스가 와도 됩니다. 시퀀스 언 패킹은 등호의 좌변에 시퀀스에 있는 요소들과 같은 개수의 변수들이 올 것을 요구합니 |
| 2 | controlflow.txt | 13534 | 함수의 *실행*은 함수의 지역 변수들을 위한 새 심볼 테이블을 만듭니다. 좀 더 구체적으로, 함수에서의 모든 변수 대입들은 값을 지역 심볼 테이블 에 저장합니다; 반면에 변수 참조는 먼저 지역 심볼 테이블을 본 다음, 전 역 심볼 테이블을 본 후, 마지막으로 내장 이름들의 테이블을 살핍니다. 그 래서, 참조될 수는 있다 하더라도, 전역 변수들과 둘러싸는 함수의 변수들 은 함수 내에서 직접 값이 대입될 수 없습니다 (전역 변수를 |
| 3 | programming.txt | 12074 | 그러나, 같은 연산이 때때로 형에 따라 다른 동작을 갖는 한 가지 연산 클 래스가 있습니다: 증분 대입 연산자. 예를 들어, "+="는 리스트를 변경하지 만, 튜플이나 정수는 변경하지 않습니다 ("a_list += [1, 2, 3]"은 "a_list.extend([1, 2, 3])"과 동등하고 "a_list"를 변경하지만, "some_tuple += (1, 2, 3)"과 "some_int += 1"은 새 객체를 만듭니다). 달 |
| 4 | controlflow.txt | 29511 | * 여러분의 코드를 국제적인 환경에서 사용하려고 한다면 특별한 인코딩을 사용하지 마세요. 어떤 경우에도 파이썬의 기본, UTF-8, 또는 단순 ASCII 조차, 이 최선입니다. * 마찬가지로, 다른 언어를 사용하는 사람이 코드를 읽거나 유지할 약간의 가능성만 있더라도, 식별자에 ASCII 이외의 문자를 사용하지 마세요. -[ 각주 ]- [1] 실제로, *객체 참조에 의한 호출 (call by object reference)*  |

### 14. open 함수에서 encoding을 생략하면 어떤 인코딩이 사용되나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 4 | 0.250 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 2 | 0.500 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | interpreter.txt | 3410 | 인코딩을 기본값 외의 것으로 선언하려면, 파일의 첫 줄에 특별한 형태의 주석 문을 추가해야 합니다. 문법은 이렇습니다: # -*- coding: encoding -*- *encoding* 은 파이썬이 지원하는 코덱 ("codecs") 중 하나여야 합니다. 예를 들어, Windows-1252 인코딩을 사용하도록 선언하려면, 소스 코드 파일 의 첫 줄은 이렇게 되어야 합니다: # -*- coding: cp1252 -*- 첫 줄 규 |
| 2 | controlflow.txt | 29511 | * 여러분의 코드를 국제적인 환경에서 사용하려고 한다면 특별한 인코딩을 사용하지 마세요. 어떤 경우에도 파이썬의 기본, UTF-8, 또는 단순 ASCII 조차, 이 최선입니다. * 마찬가지로, 다른 언어를 사용하는 사람이 코드를 읽거나 유지할 약간의 가능성만 있더라도, 식별자에 ASCII 이외의 문자를 사용하지 마세요. -[ 각주 ]- [1] 실제로, *객체 참조에 의한 호출 (call by object reference)*  |
| 3 | interpreter.txt | 2632 | $ python3.14 Python 3.14 (default, April 4 2024, 09:25:04) [GCC 10.2.0] on linux Type "help", "copyright", "credits" or "license" for more information. >>> 이어지는 줄은 여러 줄로 구성된 구조물을 입력할 때 필요합니다. 예를 들 자면, 이런 식의 "if" 문이 가능합니다: >>> the_world_is_f |
| 4 | inputoutput.txt | 8061 | >>> f = open('workfile', 'w', encoding="utf-8") 첫 번째 인자는 파일 이름을 담은 문자열입니다. 두 번째 인자는 파일이 사 용될 방식을 설명하는 몇 개의 문자들을 담은 또 하나의 문자열입니다. *mode* 는 파일을 읽기만 하면 "'r'", 쓰기만 하면 "'w'" (같은 이름의 이 미 존재하는 파일은 삭제됩니다) 가 되고, "'a'" 는 파일을 덧붙이기 위해 엽니다; 파일에 기록되는 모든  |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | inputoutput.txt | 8061 | >>> f = open('workfile', 'w', encoding="utf-8") 첫 번째 인자는 파일 이름을 담은 문자열입니다. 두 번째 인자는 파일이 사 용될 방식을 설명하는 몇 개의 문자들을 담은 또 하나의 문자열입니다. *mode* 는 파일을 읽기만 하면 "'r'", 쓰기만 하면 "'w'" (같은 이름의 이 미 존재하는 파일은 삭제됩니다) 가 되고, "'a'" 는 파일을 덧붙이기 위해 엽니다; 파일에 기록되는 모든  |
| 2 | inputoutput.txt | 7308 | 다른 메서드도 있습니다, "str.zfill()". 숫자 문자열의 왼쪽에 0을 채웁니 다. 플러스와 마이너스 부호도 이해합니다: >>> '12'.zfill(5) '00012' >>> '-3.14'.zfill(7) '-003.14' >>> '3.14159265359'.zfill(5) '3.14159265359' 7.1.4. 예전의 문자열 포매팅 --------------------------- % 연산자(모듈로)는 문자열 포매팅 |
| 3 | interpreter.txt | 3410 | 인코딩을 기본값 외의 것으로 선언하려면, 파일의 첫 줄에 특별한 형태의 주석 문을 추가해야 합니다. 문법은 이렇습니다: # -*- coding: encoding -*- *encoding* 은 파이썬이 지원하는 코덱 ("codecs") 중 하나여야 합니다. 예를 들어, Windows-1252 인코딩을 사용하도록 선언하려면, 소스 코드 파일 의 첫 줄은 이렇게 되어야 합니다: # -*- coding: cp1252 -*- 첫 줄 규 |
| 4 | controlflow.txt | 29511 | * 여러분의 코드를 국제적인 환경에서 사용하려고 한다면 특별한 인코딩을 사용하지 마세요. 어떤 경우에도 파이썬의 기본, UTF-8, 또는 단순 ASCII 조차, 이 최선입니다. * 마찬가지로, 다른 언어를 사용하는 사람이 코드를 읽거나 유지할 약간의 가능성만 있더라도, 식별자에 ASCII 이외의 문자를 사용하지 마세요. -[ 각주 ]- [1] 실제로, *객체 참조에 의한 호출 (call by object reference)*  |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | interpreter.txt | 3410 | 인코딩을 기본값 외의 것으로 선언하려면, 파일의 첫 줄에 특별한 형태의 주석 문을 추가해야 합니다. 문법은 이렇습니다: # -*- coding: encoding -*- *encoding* 은 파이썬이 지원하는 코덱 ("codecs") 중 하나여야 합니다. 예를 들어, Windows-1252 인코딩을 사용하도록 선언하려면, 소스 코드 파일 의 첫 줄은 이렇게 되어야 합니다: # -*- coding: cp1252 -*- 첫 줄 규 |
| 2 | inputoutput.txt | 8061 | >>> f = open('workfile', 'w', encoding="utf-8") 첫 번째 인자는 파일 이름을 담은 문자열입니다. 두 번째 인자는 파일이 사 용될 방식을 설명하는 몇 개의 문자들을 담은 또 하나의 문자열입니다. *mode* 는 파일을 읽기만 하면 "'r'", 쓰기만 하면 "'w'" (같은 이름의 이 미 존재하는 파일은 삭제됩니다) 가 되고, "'a'" 는 파일을 덧붙이기 위해 엽니다; 파일에 기록되는 모든  |
| 3 | interpreter.txt | 2632 | $ python3.14 Python 3.14 (default, April 4 2024, 09:25:04) [GCC 10.2.0] on linux Type "help", "copyright", "credits" or "license" for more information. >>> 이어지는 줄은 여러 줄로 구성된 구조물을 입력할 때 필요합니다. 예를 들 자면, 이런 식의 "if" 문이 가능합니다: >>> the_world_is_f |
| 4 | inputoutput.txt | 7308 | 다른 메서드도 있습니다, "str.zfill()". 숫자 문자열의 왼쪽에 0을 채웁니 다. 플러스와 마이너스 부호도 이해합니다: >>> '12'.zfill(5) '00012' >>> '-3.14'.zfill(7) '-003.14' >>> '3.14159265359'.zfill(5) '3.14159265359' 7.1.4. 예전의 문자열 포매팅 --------------------------- % 연산자(모듈로)는 문자열 포매팅 |

### 15. 파일을 with 문으로 열면 작업이 끝난 뒤 자동으로 닫히나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 1 | 1.000 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | inputoutput.txt | 8812 | 텍스트 모드에서, 읽을 때의 기본 동작은 플랫폼 의존적인 줄 종료 (유닉스 에서 "\n", 윈도우에서 "\r\n") 를 단지 "\n" 로 변경하는 것입니다. 텍스 트 모드로 쓸 때, 기본 동작은 "\n" 를 다시 플랫폼 의존적인 줄 종료로 변 환하는 것입니다. 이 파일 데이터에 대한 무대 뒤의 수정은 텍스트 파일의 경우는 문제가 안 되지만, "JPEG" 이나 "EXE" 파일과 같은 바이너리 데이터 를 망치게 됩니다. 그런 파일 |
| 2 | inputoutput.txt | 9597 | 파일 객체가 닫힌 후에는, "with" 문이나 "f.close()" 를 호출하는 경우 모 두, 파일 객체를 사용하려는 시도는 자동으로 실패합니다. >>> f.close() >>> f.read() Traceback (most recent call last): File "<stdin>", line 1, in <module> ValueError: I/O operation on closed file. 7.2.1. 파일 객체의 매소드  |
| 3 | errors.txt | 12239 | 보인 바와 같이, "finally" 절은 모든 경우에 실행됩니다. 두 문자열을 나 눠서 발생한 "TypeError" 는 "except" 절에 의해 처리되지 않고 "finally" 절이 실행된 후에 다시 일어납니다. 실제 세상의 응용 프로그램에서, "finally" 절은 외부 자원을 사용할 때, 성공적인지 아닌지와 관계없이, 그 자원을 반납하는 데 유용합니다 (파일이 나 네트워크 연결 같은 것들). 8.8. 미리 정의된 뒷정리  |
| 4 | inputoutput.txt | 8061 | >>> f = open('workfile', 'w', encoding="utf-8") 첫 번째 인자는 파일 이름을 담은 문자열입니다. 두 번째 인자는 파일이 사 용될 방식을 설명하는 몇 개의 문자들을 담은 또 하나의 문자열입니다. *mode* 는 파일을 읽기만 하면 "'r'", 쓰기만 하면 "'w'" (같은 이름의 이 미 존재하는 파일은 삭제됩니다) 가 되고, "'a'" 는 파일을 덧붙이기 위해 엽니다; 파일에 기록되는 모든  |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | inputoutput.txt | 8812 | 텍스트 모드에서, 읽을 때의 기본 동작은 플랫폼 의존적인 줄 종료 (유닉스 에서 "\n", 윈도우에서 "\r\n") 를 단지 "\n" 로 변경하는 것입니다. 텍스 트 모드로 쓸 때, 기본 동작은 "\n" 를 다시 플랫폼 의존적인 줄 종료로 변 환하는 것입니다. 이 파일 데이터에 대한 무대 뒤의 수정은 텍스트 파일의 경우는 문제가 안 되지만, "JPEG" 이나 "EXE" 파일과 같은 바이너리 데이터 를 망치게 됩니다. 그런 파일 |
| 2 | inputoutput.txt | 8061 | >>> f = open('workfile', 'w', encoding="utf-8") 첫 번째 인자는 파일 이름을 담은 문자열입니다. 두 번째 인자는 파일이 사 용될 방식을 설명하는 몇 개의 문자들을 담은 또 하나의 문자열입니다. *mode* 는 파일을 읽기만 하면 "'r'", 쓰기만 하면 "'w'" (같은 이름의 이 미 존재하는 파일은 삭제됩니다) 가 되고, "'a'" 는 파일을 덧붙이기 위해 엽니다; 파일에 기록되는 모든  |
| 3 | errors.txt | 12239 | 보인 바와 같이, "finally" 절은 모든 경우에 실행됩니다. 두 문자열을 나 눠서 발생한 "TypeError" 는 "except" 절에 의해 처리되지 않고 "finally" 절이 실행된 후에 다시 일어납니다. 실제 세상의 응용 프로그램에서, "finally" 절은 외부 자원을 사용할 때, 성공적인지 아닌지와 관계없이, 그 자원을 반납하는 데 유용합니다 (파일이 나 네트워크 연결 같은 것들). 8.8. 미리 정의된 뒷정리  |
| 4 | inputoutput.txt | 9597 | 파일 객체가 닫힌 후에는, "with" 문이나 "f.close()" 를 호출하는 경우 모 두, 파일 객체를 사용하려는 시도는 자동으로 실패합니다. >>> f.close() >>> f.read() Traceback (most recent call last): File "<stdin>", line 1, in <module> ValueError: I/O operation on closed file. 7.2.1. 파일 객체의 매소드  |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | inputoutput.txt | 8812 | 텍스트 모드에서, 읽을 때의 기본 동작은 플랫폼 의존적인 줄 종료 (유닉스 에서 "\n", 윈도우에서 "\r\n") 를 단지 "\n" 로 변경하는 것입니다. 텍스 트 모드로 쓸 때, 기본 동작은 "\n" 를 다시 플랫폼 의존적인 줄 종료로 변 환하는 것입니다. 이 파일 데이터에 대한 무대 뒤의 수정은 텍스트 파일의 경우는 문제가 안 되지만, "JPEG" 이나 "EXE" 파일과 같은 바이너리 데이터 를 망치게 됩니다. 그런 파일 |
| 2 | errors.txt | 12239 | 보인 바와 같이, "finally" 절은 모든 경우에 실행됩니다. 두 문자열을 나 눠서 발생한 "TypeError" 는 "except" 절에 의해 처리되지 않고 "finally" 절이 실행된 후에 다시 일어납니다. 실제 세상의 응용 프로그램에서, "finally" 절은 외부 자원을 사용할 때, 성공적인지 아닌지와 관계없이, 그 자원을 반납하는 데 유용합니다 (파일이 나 네트워크 연결 같은 것들). 8.8. 미리 정의된 뒷정리  |
| 3 | inputoutput.txt | 9597 | 파일 객체가 닫힌 후에는, "with" 문이나 "f.close()" 를 호출하는 경우 모 두, 파일 객체를 사용하려는 시도는 자동으로 실패합니다. >>> f.close() >>> f.read() Traceback (most recent call last): File "<stdin>", line 1, in <module> ValueError: I/O operation on closed file. 7.2.1. 파일 객체의 매소드  |
| 4 | inputoutput.txt | 8061 | >>> f = open('workfile', 'w', encoding="utf-8") 첫 번째 인자는 파일 이름을 담은 문자열입니다. 두 번째 인자는 파일이 사 용될 방식을 설명하는 몇 개의 문자들을 담은 또 하나의 문자열입니다. *mode* 는 파일을 읽기만 하면 "'r'", 쓰기만 하면 "'w'" (같은 이름의 이 미 존재하는 파일은 삭제됩니다) 가 되고, "'a'" 는 파일을 덧붙이기 위해 엽니다; 파일에 기록되는 모든  |

### 16. import할 모듈을 찾을 때 Python은 어떤 경로들을 검색하나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 1 | 1.000 |
| Hybrid Regex | 0 | Top-4 내 없음 | 0.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | modules.txt | 3797 | $ python fibo.py 50 0 1 1 2 3 5 8 13 21 34 모듈이 임포트될 때, 코드는 실행되지 않습니다: >>> import fibo >>> 이것은 종종 모듈에 대한 편리한 사용자 인터페이스를 제공하거나 테스트 목적으로 사용됩니다 (모듈을 스크립트로 실행하면 테스트 스위트를 실행하 기). 6.1.2. 모듈 검색 경로 --------------------- "spam" 이라는 이름의 모듈이 임포트될 때, 인터 |
| 2 | modules.txt | 6767 | >>> import sys >>> sys.path.append('/ufs/guido/lib/python') 6.3. "dir()" 함수 ================= 내장 함수 "dir()" 은 모듈이 정의하는 이름들을 찾는 데 사용됩니다. 문자 열들의 정렬된 리스트를 돌려줍니다: |
| 3 | programming.txt | 59120 | "importlib"의 편의 함수 "import_module()"을 대신 사용하는 곳을 고려하 십시오: z = importlib.import_module('x.y.z') 임포트 된 모듈을 편집하고 다시 임포트 할 때, 변경 사항이 표시되지 않습니다. 왜 이런 일이 발생합니까? ------------------------------------------------------------------------------------- |
| 4 | pathlib.txt | 729 | 이전에 이 모듈을 사용한 적이 없거나 어떤 클래스가 작업에 적합한지 확신 이 없다면, "Path"가 가장 적합할 가능성이 높습니다. 코드가 실행되는 플 랫폼의 구상 경로를 인스턴스화 합니다. 순수한 경로는 특별한 경우에 유용합니다; 예를 들면: 1. 유닉스 기계에서 윈도우 경로를 조작하려고 할 때 (또는 그 반대). 유닉 스에서 실행할 때는 "WindowsPath"를 인스턴스화 할 수 없지만, "PureWindowsPath"는 |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | programming.txt | 59120 | "importlib"의 편의 함수 "import_module()"을 대신 사용하는 곳을 고려하 십시오: z = importlib.import_module('x.y.z') 임포트 된 모듈을 편집하고 다시 임포트 할 때, 변경 사항이 표시되지 않습니다. 왜 이런 일이 발생합니까? ------------------------------------------------------------------------------------- |
| 2 | pathlib.txt | 729 | 이전에 이 모듈을 사용한 적이 없거나 어떤 클래스가 작업에 적합한지 확신 이 없다면, "Path"가 가장 적합할 가능성이 높습니다. 코드가 실행되는 플 랫폼의 구상 경로를 인스턴스화 합니다. 순수한 경로는 특별한 경우에 유용합니다; 예를 들면: 1. 유닉스 기계에서 윈도우 경로를 조작하려고 할 때 (또는 그 반대). 유닉 스에서 실행할 때는 "WindowsPath"를 인스턴스화 할 수 없지만, "PureWindowsPath"는 |
| 3 | programming.txt | 6834 | 2. third-party library modules (anything installed in Python's site- packages directory) -- such as dateutil, requests, tzdata 3. locally developed modules 순환 임포트 관련 문제를 피하고자 임포트를 함수나 클래스로 이동해야 하 는 경우가 있습니다. Gordon McMillan은 다음과 같이 말했습니다: 두 |
| 4 | programming.txt | 56699 | "foo"에 대한 ".pyc" 파일을 만들 필요가 있으면 -- 즉, 임포트 되지 않는 모듈에 대한 ".pyc" 파일을 만들려면 -- "py_compile"과 "compileall" 모듈 을 사용할 수 있습니다. "py_compile" 모듈은 임의의 모듈을 수동으로 컴파일할 수 있습니다. 한 가 지 방법은 해당 모듈에서 "compile()" 함수를 대화식으로 사용하는 것입니 다: >>> import py_compile >>> p |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | modules.txt | 3797 | $ python fibo.py 50 0 1 1 2 3 5 8 13 21 34 모듈이 임포트될 때, 코드는 실행되지 않습니다: >>> import fibo >>> 이것은 종종 모듈에 대한 편리한 사용자 인터페이스를 제공하거나 테스트 목적으로 사용됩니다 (모듈을 스크립트로 실행하면 테스트 스위트를 실행하 기). 6.1.2. 모듈 검색 경로 --------------------- "spam" 이라는 이름의 모듈이 임포트될 때, 인터 |
| 2 | modules.txt | 6767 | >>> import sys >>> sys.path.append('/ufs/guido/lib/python') 6.3. "dir()" 함수 ================= 내장 함수 "dir()" 은 모듈이 정의하는 이름들을 찾는 데 사용됩니다. 문자 열들의 정렬된 리스트를 돌려줍니다: |
| 3 | programming.txt | 1739 | One is to use the freeze tool, which is included in the Python source tree as Tools/freeze. It converts Python byte code to C arrays; with a C compiler you can embed all your modules into a new program, which is then linked with the standar |
| 4 | pathlib.txt | 729 | 이전에 이 모듈을 사용한 적이 없거나 어떤 클래스가 작업에 적합한지 확신 이 없다면, "Path"가 가장 적합할 가능성이 높습니다. 코드가 실행되는 플 랫폼의 구상 경로를 인스턴스화 합니다. 순수한 경로는 특별한 경우에 유용합니다; 예를 들면: 1. 유닉스 기계에서 윈도우 경로를 조작하려고 할 때 (또는 그 반대). 유닉 스에서 실행할 때는 "WindowsPath"를 인스턴스화 할 수 없지만, "PureWindowsPath"는 |

### 17. 클래스에서 밑줄로 시작하는 이름은 비공개 멤버를 뜻하나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 1 | 1.000 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | classes.txt | 17172 | 클래스-비공개 멤버들의 올바른 사례가 있으므로 (즉 서브 클래스에서 정의 된 이름들과의 충돌을 피하고자), *이름 뒤섞기 (name mangling)* 라고 불 리는 메커니즘에 대한 제한된 지원이 있습니다. "__spam" 형태의 (최소 두 개의 밑줄로 시작하고, 최대 한 개의 밑줄로 끝납니다) 모든 식별자는 "_classname__spam" 로 텍스트 적으로 치환되는데, "classname" 은 현재 클 래스 이름에서 앞에  |
| 2 | classes.txt | 593 | C++ 용어로, 보통 클래스 멤버들은 (데이터 멤버를 포함해서) *public* (예 외는 아래 비공개 변수 를 보세요) 하고, 모든 맴버 함수들은 *virtual* 입 니다. 모듈라-3처럼, 객체의 매소드에서 그 객체의 멤버를 참조하는 줄임 표현은 없습니다: 메서드 함수는 그 객체를 표현하는 명시적인 첫 번째 인 자를 선언하는데, 함수 호출 때 묵시적으로 제공됩니다. 스몰토크처럼, 클 래스 자신도 객체입니다. 이것이 임포팅과 |
| 3 | programming.txt | 45138 | 이것은 완전히 동등하지는 않지만, 실제로는 아주 가깝습니다. You could also try a variable-length argument list, for example: def __init__(self, *args): ... 같은 접근법이 모든 메서드 정의에서도 동작합니다. __spam을 사용하려고 하는데 _SomeClassName__spam에 대한 에러가 발생합니다. ---------------------------- |
| 4 | classes.txt | 16436 | 동적인 순서가 필요한 이유는, 모든 다중 상속의 경우는 하나나 그 이상의 다이아몬드 관계 (적어도 부모 클래스 중 하나가 가장 바닥 클래스들로부터 여러 경로를 통해 액세스 되는 경우) 를 만들기 때문입니다. 예를 들어, 모 든 클래스는 "object" 를 계승하기 때문에, 모든 다중 상속은 "object" 에 이르는 여러 경로를 제공합니다. 베이스 클래스들이 여러 번 액세스 되지 않게 하려고, 동적인 알고리즘이 검색 순서를 선 |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | classes.txt | 17172 | 클래스-비공개 멤버들의 올바른 사례가 있으므로 (즉 서브 클래스에서 정의 된 이름들과의 충돌을 피하고자), *이름 뒤섞기 (name mangling)* 라고 불 리는 메커니즘에 대한 제한된 지원이 있습니다. "__spam" 형태의 (최소 두 개의 밑줄로 시작하고, 최대 한 개의 밑줄로 끝납니다) 모든 식별자는 "_classname__spam" 로 텍스트 적으로 치환되는데, "classname" 은 현재 클 래스 이름에서 앞에  |
| 2 | classes.txt | 593 | C++ 용어로, 보통 클래스 멤버들은 (데이터 멤버를 포함해서) *public* (예 외는 아래 비공개 변수 를 보세요) 하고, 모든 맴버 함수들은 *virtual* 입 니다. 모듈라-3처럼, 객체의 매소드에서 그 객체의 멤버를 참조하는 줄임 표현은 없습니다: 메서드 함수는 그 객체를 표현하는 명시적인 첫 번째 인 자를 선언하는데, 함수 호출 때 묵시적으로 제공됩니다. 스몰토크처럼, 클 래스 자신도 객체입니다. 이것이 임포팅과 |
| 3 | classes.txt | 16436 | 동적인 순서가 필요한 이유는, 모든 다중 상속의 경우는 하나나 그 이상의 다이아몬드 관계 (적어도 부모 클래스 중 하나가 가장 바닥 클래스들로부터 여러 경로를 통해 액세스 되는 경우) 를 만들기 때문입니다. 예를 들어, 모 든 클래스는 "object" 를 계승하기 때문에, 모든 다중 상속은 "object" 에 이르는 여러 경로를 제공합니다. 베이스 클래스들이 여러 번 액세스 되지 않게 하려고, 동적인 알고리즘이 검색 순서를 선 |
| 4 | programming.txt | 45138 | 이것은 완전히 동등하지는 않지만, 실제로는 아주 가깝습니다. You could also try a variable-length argument list, for example: def __init__(self, *args): ... 같은 접근법이 모든 메서드 정의에서도 동작합니다. __spam을 사용하려고 하는데 _SomeClassName__spam에 대한 에러가 발생합니다. ---------------------------- |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | classes.txt | 17172 | 클래스-비공개 멤버들의 올바른 사례가 있으므로 (즉 서브 클래스에서 정의 된 이름들과의 충돌을 피하고자), *이름 뒤섞기 (name mangling)* 라고 불 리는 메커니즘에 대한 제한된 지원이 있습니다. "__spam" 형태의 (최소 두 개의 밑줄로 시작하고, 최대 한 개의 밑줄로 끝납니다) 모든 식별자는 "_classname__spam" 로 텍스트 적으로 치환되는데, "classname" 은 현재 클 래스 이름에서 앞에  |
| 2 | classes.txt | 593 | C++ 용어로, 보통 클래스 멤버들은 (데이터 멤버를 포함해서) *public* (예 외는 아래 비공개 변수 를 보세요) 하고, 모든 맴버 함수들은 *virtual* 입 니다. 모듈라-3처럼, 객체의 매소드에서 그 객체의 멤버를 참조하는 줄임 표현은 없습니다: 메서드 함수는 그 객체를 표현하는 명시적인 첫 번째 인 자를 선언하는데, 함수 호출 때 묵시적으로 제공됩니다. 스몰토크처럼, 클 래스 자신도 객체입니다. 이것이 임포팅과 |
| 3 | programming.txt | 45138 | 이것은 완전히 동등하지는 않지만, 실제로는 아주 가깝습니다. You could also try a variable-length argument list, for example: def __init__(self, *args): ... 같은 접근법이 모든 메서드 정의에서도 동작합니다. __spam을 사용하려고 하는데 _SomeClassName__spam에 대한 에러가 발생합니다. ---------------------------- |
| 4 | classes.txt | 16436 | 동적인 순서가 필요한 이유는, 모든 다중 상속의 경우는 하나나 그 이상의 다이아몬드 관계 (적어도 부모 클래스 중 하나가 가장 바닥 클래스들로부터 여러 경로를 통해 액세스 되는 경우) 를 만들기 때문입니다. 예를 들어, 모 든 클래스는 "object" 를 계승하기 때문에, 모든 다중 상속은 "object" 에 이르는 여러 경로를 제공합니다. 베이스 클래스들이 여러 번 액세스 되지 않게 하려고, 동적인 알고리즘이 검색 순서를 선 |

### 18. 제너레이터 함수에서 yield는 어떤 역할을 하나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 1 | 1.000 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | classes.txt | 21582 | 또 하나의 주요 기능은 지역 변수들과 실행 상태가 호출 간에 자동으로 보 관된다는 것입니다. 이것은 "self.index" 나 "self.data" 와 같은 인스턴스 변수를 사용하는 접근법에 비교해 함수를 쓰기 쉽고 명료하게 만듭니다. 자동 메서드 생성과 프로그램 상태의 저장에 더해, 제너레이터가 종료할 때 자동으로 "StopIteration" 을 일으킵니다. 조합하면, 이 기능들이 일반 함 수를 작성하는 것만큼 이터레이터를  |
| 2 | classes.txt | 20863 | >>> rev = Reverse('spam') >>> iter(rev) <__main__.Reverse object at 0x00A1DB50> >>> for char in rev: ... print(char) ... m a p s 9.9. 제너레이터 =============== *제너레이터* 는 이터레이터를 만드는 간단하고 강력한 도구입니다. 일반적 인 함수처럼 작성되지만 값을 돌려주고 싶을 때마다 "yield" 문을 사용합니 |
| 3 | classes.txt | 19317 | 9.8. 이터레이터 =============== 지금쯤 아마도 여러분은 대부분의 컨테이너 객체들을 "for" 문으로 루핑할 수 있음을 눈치챘을 것입니다: for element in [1, 2, 3]: print(element) for element in (1, 2, 3): print(element) for key in {'one':1, 'two':2}: print(key) for char in "123": print(char) |
| 4 | datastructures.txt | 7197 | 이것은 다시 다음과 같습니다: >>> transposed = [] >>> for i in range(4): ... # 다음 3줄은 중첩된 리스트 컴프리헨션을 구현합니다 ... transposed_row = [] ... for row in matrix: ... transposed_row.append(row[i]) ... transposed.append(transposed_row) ... >>> transposed [[1, 5,  |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | classes.txt | 21582 | 또 하나의 주요 기능은 지역 변수들과 실행 상태가 호출 간에 자동으로 보 관된다는 것입니다. 이것은 "self.index" 나 "self.data" 와 같은 인스턴스 변수를 사용하는 접근법에 비교해 함수를 쓰기 쉽고 명료하게 만듭니다. 자동 메서드 생성과 프로그램 상태의 저장에 더해, 제너레이터가 종료할 때 자동으로 "StopIteration" 을 일으킵니다. 조합하면, 이 기능들이 일반 함 수를 작성하는 것만큼 이터레이터를  |
| 2 | classes.txt | 20863 | >>> rev = Reverse('spam') >>> iter(rev) <__main__.Reverse object at 0x00A1DB50> >>> for char in rev: ... print(char) ... m a p s 9.9. 제너레이터 =============== *제너레이터* 는 이터레이터를 만드는 간단하고 강력한 도구입니다. 일반적 인 함수처럼 작성되지만 값을 돌려주고 싶을 때마다 "yield" 문을 사용합니 |
| 3 | datastructures.txt | 7197 | 이것은 다시 다음과 같습니다: >>> transposed = [] >>> for i in range(4): ... # 다음 3줄은 중첩된 리스트 컴프리헨션을 구현합니다 ... transposed_row = [] ... for row in matrix: ... transposed_row.append(row[i]) ... transposed.append(transposed_row) ... >>> transposed [[1, 5,  |
| 4 | classes.txt | 19317 | 9.8. 이터레이터 =============== 지금쯤 아마도 여러분은 대부분의 컨테이너 객체들을 "for" 문으로 루핑할 수 있음을 눈치챘을 것입니다: for element in [1, 2, 3]: print(element) for element in (1, 2, 3): print(element) for key in {'one':1, 'two':2}: print(key) for char in "123": print(char) |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | classes.txt | 21582 | 또 하나의 주요 기능은 지역 변수들과 실행 상태가 호출 간에 자동으로 보 관된다는 것입니다. 이것은 "self.index" 나 "self.data" 와 같은 인스턴스 변수를 사용하는 접근법에 비교해 함수를 쓰기 쉽고 명료하게 만듭니다. 자동 메서드 생성과 프로그램 상태의 저장에 더해, 제너레이터가 종료할 때 자동으로 "StopIteration" 을 일으킵니다. 조합하면, 이 기능들이 일반 함 수를 작성하는 것만큼 이터레이터를  |
| 2 | classes.txt | 20863 | >>> rev = Reverse('spam') >>> iter(rev) <__main__.Reverse object at 0x00A1DB50> >>> for char in rev: ... print(char) ... m a p s 9.9. 제너레이터 =============== *제너레이터* 는 이터레이터를 만드는 간단하고 강력한 도구입니다. 일반적 인 함수처럼 작성되지만 값을 돌려주고 싶을 때마다 "yield" 문을 사용합니 |
| 3 | datastructures.txt | 7197 | 이것은 다시 다음과 같습니다: >>> transposed = [] >>> for i in range(4): ... # 다음 3줄은 중첩된 리스트 컴프리헨션을 구현합니다 ... transposed_row = [] ... for row in matrix: ... transposed_row.append(row[i]) ... transposed.append(transposed_row) ... >>> transposed [[1, 5,  |
| 4 | classes.txt | 19317 | 9.8. 이터레이터 =============== 지금쯤 아마도 여러분은 대부분의 컨테이너 객체들을 "for" 문으로 루핑할 수 있음을 눈치챘을 것입니다: for element in [1, 2, 3]: print(element) for element in (1, 2, 3): print(element) for key in {'one':1, 'two':2}: print(key) for char in "123": print(char) |

### 19. 0.1 같은 십진 소수를 Python이 정확히 표현하지 못할 수 있는 이유는 무엇인가요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 1 | 1.000 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | floatingpoint.txt | 5408 | 15.1. 표현 오류 =============== 이 섹션에서는 "0.1" 예제를 자세히 설명하고, 이러한 사례에 대한 정확한 분석을 여러분이 직접 수행하는 방법을 보여줍니다. 이진 부동 소수점 표현 에 대한 기본 지식이 있다고 가정합니다. *표현 오류 (Representation error)* 는 일부 (실제로는, 대부분의) 십진 소수가 이진(밑 2) 소수로 정확하게 표현될 수 없다는 사실을 나타냅니다. 이것이 파이썬(또는  |
| 2 | floatingpoint.txt | 3439 | 정확한 십진 표현이 필요한 사용 사례의 경우, 회계 응용 프로그램 및 고정 밀 응용 프로그램에 적합한 십진 산술을 구현하는 "decimal" 모듈을 사용해 보세요. 정확한 산술의 또 다른 형태는 유리수를 기반으로 산술을 구현하는 "fractions" 모듈에 의해 지원됩니다 (따라서 1/3과 같은 숫자는 정확하게 나타낼 수 있습니다). 부동 소수점 연산을 많이 하는 사용자면 NumPy 패키지와 SciPy 프로젝트에 서 제공하는  |
| 3 | floatingpoint.txt | 1282 | >>> 1 / 10 0.1 인쇄된 결과가 정확히 1/10인 것처럼 보여도, 실제 저장된 값은 가장 가까 운 표현 가능한 이진 소수임을 기억하세요. 흥미롭게도, 가장 가까운 근사 이진 소수를 공유하는 여러 다른 십진수가 있습니다. 예를 들어, "0.1" 과 "0.10000000000000001" 및 "0.1000000000000000055511151231257827021181583404541015625" 는 모두 "3602879 |
| 4 | floatingpoint.txt | 0 | 15. 부동 소수점 산술: 문제점 및 한계 ************************************ 부동 소수점 숫자는 컴퓨터 하드웨어에서 밑(base)이 2인(이진) 소수로 표 현됩니다. 예를 들어, **십진** 소수 "0.625"는 값 6/10 + 2/100 + 5/1000 를 가지며, 같은 방식으로 **이진** 소수 "0.101" 는 값 1/2 + 0/4 + 1/8 을 가집니다. 이 두 소수는 같은 값을 가지며, |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | floatingpoint.txt | 1282 | >>> 1 / 10 0.1 인쇄된 결과가 정확히 1/10인 것처럼 보여도, 실제 저장된 값은 가장 가까 운 표현 가능한 이진 소수임을 기억하세요. 흥미롭게도, 가장 가까운 근사 이진 소수를 공유하는 여러 다른 십진수가 있습니다. 예를 들어, "0.1" 과 "0.10000000000000001" 및 "0.1000000000000000055511151231257827021181583404541015625" 는 모두 "3602879 |
| 2 | floatingpoint.txt | 5408 | 15.1. 표현 오류 =============== 이 섹션에서는 "0.1" 예제를 자세히 설명하고, 이러한 사례에 대한 정확한 분석을 여러분이 직접 수행하는 방법을 보여줍니다. 이진 부동 소수점 표현 에 대한 기본 지식이 있다고 가정합니다. *표현 오류 (Representation error)* 는 일부 (실제로는, 대부분의) 십진 소수가 이진(밑 2) 소수로 정확하게 표현될 수 없다는 사실을 나타냅니다. 이것이 파이썬(또는  |
| 3 | floatingpoint.txt | 0 | 15. 부동 소수점 산술: 문제점 및 한계 ************************************ 부동 소수점 숫자는 컴퓨터 하드웨어에서 밑(base)이 2인(이진) 소수로 표 현됩니다. 예를 들어, **십진** 소수 "0.625"는 값 6/10 + 2/100 + 5/1000 를 가지며, 같은 방식으로 **이진** 소수 "0.101" 는 값 1/2 + 0/4 + 1/8 을 가집니다. 이 두 소수는 같은 값을 가지며, |
| 4 | floatingpoint.txt | 3439 | 정확한 십진 표현이 필요한 사용 사례의 경우, 회계 응용 프로그램 및 고정 밀 응용 프로그램에 적합한 십진 산술을 구현하는 "decimal" 모듈을 사용해 보세요. 정확한 산술의 또 다른 형태는 유리수를 기반으로 산술을 구현하는 "fractions" 모듈에 의해 지원됩니다 (따라서 1/3과 같은 숫자는 정확하게 나타낼 수 있습니다). 부동 소수점 연산을 많이 하는 사용자면 NumPy 패키지와 SciPy 프로젝트에 서 제공하는  |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | floatingpoint.txt | 5408 | 15.1. 표현 오류 =============== 이 섹션에서는 "0.1" 예제를 자세히 설명하고, 이러한 사례에 대한 정확한 분석을 여러분이 직접 수행하는 방법을 보여줍니다. 이진 부동 소수점 표현 에 대한 기본 지식이 있다고 가정합니다. *표현 오류 (Representation error)* 는 일부 (실제로는, 대부분의) 십진 소수가 이진(밑 2) 소수로 정확하게 표현될 수 없다는 사실을 나타냅니다. 이것이 파이썬(또는  |
| 2 | floatingpoint.txt | 0 | 15. 부동 소수점 산술: 문제점 및 한계 ************************************ 부동 소수점 숫자는 컴퓨터 하드웨어에서 밑(base)이 2인(이진) 소수로 표 현됩니다. 예를 들어, **십진** 소수 "0.625"는 값 6/10 + 2/100 + 5/1000 를 가지며, 같은 방식으로 **이진** 소수 "0.101" 는 값 1/2 + 0/4 + 1/8 을 가집니다. 이 두 소수는 같은 값을 가지며, |
| 3 | floatingpoint.txt | 3439 | 정확한 십진 표현이 필요한 사용 사례의 경우, 회계 응용 프로그램 및 고정 밀 응용 프로그램에 적합한 십진 산술을 구현하는 "decimal" 모듈을 사용해 보세요. 정확한 산술의 또 다른 형태는 유리수를 기반으로 산술을 구현하는 "fractions" 모듈에 의해 지원됩니다 (따라서 1/3과 같은 숫자는 정확하게 나타낼 수 있습니다). 부동 소수점 연산을 많이 하는 사용자면 NumPy 패키지와 SciPy 프로젝트에 서 제공하는  |
| 4 | floatingpoint.txt | 1282 | >>> 1 / 10 0.1 인쇄된 결과가 정확히 1/10인 것처럼 보여도, 실제 저장된 값은 가장 가까 운 표현 가능한 이진 소수임을 기억하세요. 흥미롭게도, 가장 가까운 근사 이진 소수를 공유하는 여러 다른 십진수가 있습니다. 예를 들어, "0.1" 과 "0.10000000000000001" 및 "0.1000000000000000055511151231257827021181583404541015625" 는 모두 "3602879 |

### 20. venv 모듈로 새로운 가상환경을 만드는 기본 명령은 무엇인가요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 1 | 1.000 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | library_venv.txt | 1841 | 가상 환경 만들기 ================ 가상 환경은 "venv" 모듈을 실행해서 만들어집니다: python -m venv /path/to/new/virtual/environment This creates the target directory (including parent directories as needed) and places a "pyvenv.cfg" file in it with a "home" key poin |
| 2 | tutorial_venv.txt | 737 | 12.2. 가상 환경 만들기 ====================== 가상 환경을 만들고 관리하는 데 사용되는 모듈은 "venv" 라고 합니다. "venv" 는 명령이 실행된 ("--version" 옵션으로 확인할 수 있는) 파이썬 버전을 설치합니다. 예를 들어, "python3.12"로 명령을 실행하면 버전 3.12 가 설치됩니다. 가상 환경을 만들려면, 원하는 디렉터리를 결정하고, "venv" 모듈을 스크립 트로 실행하는데 |
| 3 | library_venv.txt | 0 | "venv" --- 가상 환경 생성 ************************* Added in version 3.3. **소스 코드:** Lib/venv/ ====================================================================== The "venv" module supports creating lightweight "virtual environments", each wit |
| 4 | library_venv.txt | 9547 | 셸에서 "deactivate"를 입력하여 가상 환경을 비활성화할 수 있습니다. 정 확한 메커니즘은 플랫폼에 따라 다르고 내부 구현 상세입니다 (보통, 스크 립트나 셸 함수가 사용됩니다). API === 위에서 설명한 고수준 메서드는 제삼자 가상 환경 작성자가 필요에 따라 환 경을 사용자 정의할 수 있는 메커니즘을 제공하는 간단한 API를 사용합니다 : "EnvBuilder" 클래스. class venv.EnvBuilder(sy |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | library_venv.txt | 1841 | 가상 환경 만들기 ================ 가상 환경은 "venv" 모듈을 실행해서 만들어집니다: python -m venv /path/to/new/virtual/environment This creates the target directory (including parent directories as needed) and places a "pyvenv.cfg" file in it with a "home" key poin |
| 2 | tutorial_venv.txt | 737 | 12.2. 가상 환경 만들기 ====================== 가상 환경을 만들고 관리하는 데 사용되는 모듈은 "venv" 라고 합니다. "venv" 는 명령이 실행된 ("--version" 옵션으로 확인할 수 있는) 파이썬 버전을 설치합니다. 예를 들어, "python3.12"로 명령을 실행하면 버전 3.12 가 설치됩니다. 가상 환경을 만들려면, 원하는 디렉터리를 결정하고, "venv" 모듈을 스크립 트로 실행하는데 |
| 3 | library_venv.txt | 2566 | Deprecated since version 3.6, removed in version 3.8: **pyvenv**는 파 이썬 3.3 및 3.4 용 가상 환경을 만드는 데 권장되는 도구였으며, 파이썬 3.5 에서 "venv"를 직접 실행하는 방식으로 대체되었습니다. 윈도우에서는, 다음과 같이 "venv" 명령을 호출하십시오: PS> python -m venv C:\path\to\new\virtual\environment 명령에 |
| 4 | library_venv.txt | 0 | "venv" --- 가상 환경 생성 ************************* Added in version 3.3. **소스 코드:** Lib/venv/ ====================================================================== The "venv" module supports creating lightweight "virtual environments", each wit |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | tutorial_venv.txt | 737 | 12.2. 가상 환경 만들기 ====================== 가상 환경을 만들고 관리하는 데 사용되는 모듈은 "venv" 라고 합니다. "venv" 는 명령이 실행된 ("--version" 옵션으로 확인할 수 있는) 파이썬 버전을 설치합니다. 예를 들어, "python3.12"로 명령을 실행하면 버전 3.12 가 설치됩니다. 가상 환경을 만들려면, 원하는 디렉터리를 결정하고, "venv" 모듈을 스크립 트로 실행하는데 |
| 2 | library_venv.txt | 1841 | 가상 환경 만들기 ================ 가상 환경은 "venv" 모듈을 실행해서 만들어집니다: python -m venv /path/to/new/virtual/environment This creates the target directory (including parent directories as needed) and places a "pyvenv.cfg" file in it with a "home" key poin |
| 3 | library_venv.txt | 1379 | * Considered as disposable -- it should be simple to delete and recreate it from scratch. You don't place any project code in the environment. * Not considered as movable or copyable -- you just recreate the same environment in the target l |
| 4 | library_venv.txt | 0 | "venv" --- 가상 환경 생성 ************************* Added in version 3.3. **소스 코드:** Lib/venv/ ====================================================================== The "venv" module supports creating lightweight "virtual environments", each wit |

### 21. 데이터클래스에서 order=True를 쓰면서 eq=False를 지정하면 어떻게 되나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 1 | 1.000 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | dataclasses.txt | 3339 | * *order*: 참이면 (기본값은 "False"), "__lt__()", "__le__()", "__gt__()", "__ge__()" 메서드가 생성됩니다. 이것들은 클래스를 필 드의 튜플인 것처럼 순서대로 비교합니다. 비교되는 두 인스턴스는 같 은 형이어야 합니다. *order* 가 참이고 *eq* 가 거짓이면 "ValueError" 가 발생합니다. 클래스가 이미 "__lt__()", "__le__()", "__gt__( |
| 2 | dataclasses.txt | 4867 | *eq* 와 *frozen* 이 모두 참이면, 기본적으로 "@dataclass" 는 "__hash__()" 메서드를 만듭니다. *eq* 가 참이고 *frozen* 이 거짓이 면, "__hash__()" 가 "None" 으로 설정되어 해시 불가능하다고 표시됩 니다(가변이기 때문입니다). 만약 *eq* 가 거짓이면, "__hash__()" 를 건드리지 않는데, 슈퍼 클래스의 "__hash__()" 가 사용된다는 뜻이 됩 니다 (슈 |
| 3 | dataclasses.txt | 2442 | 클래스가 이미 "__repr__()" 을 정의했으면, 이 매개변수는 무시됩니 다. * *eq*: If true (the default), an "__eq__()" method will be generated. This method compares the class by comparing each field in order. Both instances in the comparison must be of the identical  |
| 4 | dataclasses.txt | 15617 | *changes* 가 "init=False" 를 갖는 것으로 정의된 필드를 포함하는 것 은 에러입니다. 이 경우 "ValueError" 가 발생합니다. "replace()"를 호출하는 동안 "init=False" 필드가 어떻게 작동하는지 미리 경고합니다. 그것들은 소스 객체로부터 복사되는 것이 아니라, (초 기화되기는 한다면) "__post_init__()" 에서 초기화됩니다. "init=False" 필드는 거의 사용되지 않으 |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | dataclasses.txt | 3339 | * *order*: 참이면 (기본값은 "False"), "__lt__()", "__le__()", "__gt__()", "__ge__()" 메서드가 생성됩니다. 이것들은 클래스를 필 드의 튜플인 것처럼 순서대로 비교합니다. 비교되는 두 인스턴스는 같 은 형이어야 합니다. *order* 가 참이고 *eq* 가 거짓이면 "ValueError" 가 발생합니다. 클래스가 이미 "__lt__()", "__le__()", "__gt__( |
| 2 | dataclasses.txt | 4867 | *eq* 와 *frozen* 이 모두 참이면, 기본적으로 "@dataclass" 는 "__hash__()" 메서드를 만듭니다. *eq* 가 참이고 *frozen* 이 거짓이 면, "__hash__()" 가 "None" 으로 설정되어 해시 불가능하다고 표시됩 니다(가변이기 때문입니다). 만약 *eq* 가 거짓이면, "__hash__()" 를 건드리지 않는데, 슈퍼 클래스의 "__hash__()" 가 사용된다는 뜻이 됩 니다 (슈 |
| 3 | dataclasses.txt | 1619 | "@dataclass" 가 매개변수 없는 단순한 데코레이터로 사용되면, 이 서명 에 문서화 된 기본값들이 제공된 것처럼 행동합니다. 즉, 다음 "@dataclass" 의 세 가지 용법은 동등합니다: @dataclass class C: ... @dataclass() class C: ... @dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, froze |
| 4 | dataclasses.txt | 15617 | *changes* 가 "init=False" 를 갖는 것으로 정의된 필드를 포함하는 것 은 에러입니다. 이 경우 "ValueError" 가 발생합니다. "replace()"를 호출하는 동안 "init=False" 필드가 어떻게 작동하는지 미리 경고합니다. 그것들은 소스 객체로부터 복사되는 것이 아니라, (초 기화되기는 한다면) "__post_init__()" 에서 초기화됩니다. "init=False" 필드는 거의 사용되지 않으 |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | dataclasses.txt | 3339 | * *order*: 참이면 (기본값은 "False"), "__lt__()", "__le__()", "__gt__()", "__ge__()" 메서드가 생성됩니다. 이것들은 클래스를 필 드의 튜플인 것처럼 순서대로 비교합니다. 비교되는 두 인스턴스는 같 은 형이어야 합니다. *order* 가 참이고 *eq* 가 거짓이면 "ValueError" 가 발생합니다. 클래스가 이미 "__lt__()", "__le__()", "__gt__( |
| 2 | dataclasses.txt | 4867 | *eq* 와 *frozen* 이 모두 참이면, 기본적으로 "@dataclass" 는 "__hash__()" 메서드를 만듭니다. *eq* 가 참이고 *frozen* 이 거짓이 면, "__hash__()" 가 "None" 으로 설정되어 해시 불가능하다고 표시됩 니다(가변이기 때문입니다). 만약 *eq* 가 거짓이면, "__hash__()" 를 건드리지 않는데, 슈퍼 클래스의 "__hash__()" 가 사용된다는 뜻이 됩 니다 (슈 |
| 3 | dataclasses.txt | 1619 | "@dataclass" 가 매개변수 없는 단순한 데코레이터로 사용되면, 이 서명 에 문서화 된 기본값들이 제공된 것처럼 행동합니다. 즉, 다음 "@dataclass" 의 세 가지 용법은 동등합니다: @dataclass class C: ... @dataclass() class C: ... @dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, froze |
| 4 | dataclasses.txt | 2442 | 클래스가 이미 "__repr__()" 을 정의했으면, 이 매개변수는 무시됩니 다. * *eq*: If true (the default), an "__eq__()" method will be generated. This method compares the class by comparing each field in order. Both instances in the comparison must be of the identical  |

### 22. pathlib Path가 가리키는 파일이나 디렉터리가 실제로 존재하는지 어떻게 확인하나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 1 | 1.000 |
| Hybrid Regex | 1 | 1 | 1.000 |
| Hybrid Kiwi | 1 | 1 | 1.000 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | pathlib.txt | 0 | "pathlib" --- Object-oriented filesystem paths ********************************************** Added in version 3.4. **Source code:** Lib/pathlib/ ====================================================================== 이 모듈은 다른 운영 체제에 적합한 의미  |
| 2 | pathlib.txt | 27849 | This method normally follows symlinks; to check if a symlink exists, add the argument "follow_symlinks=False". >>> Path('').exists() # The current directory. True >>> Path('.').exists() True >>> Path('setup.py').exists() True >>> Path('/etc |
| 3 | pathlib.txt | 1477 | 이 디렉터리 트리에 있는 파이썬 소스 파일 나열하기: >>> list(p.glob('**/*.py')) [PosixPath('test_pathlib.py'), PosixPath('setup.py'), PosixPath('pathlib.py'), PosixPath('docs/conf.py'), PosixPath('build/lib/pathlib.py')] 디렉터리 트리 내에서 탐색하기: >>> p = Path('/etc') >> |
| 4 | pathlib.txt | 31112 | Path.is_char_device() Return "True" if the path points to a character device. "False" will be returned if the path is invalid, inaccessible or missing, or if it points to something other than a character device. Use "Path.stat()" to disting |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | pathlib.txt | 0 | "pathlib" --- Object-oriented filesystem paths ********************************************** Added in version 3.4. **Source code:** Lib/pathlib/ ====================================================================== 이 모듈은 다른 운영 체제에 적합한 의미  |
| 2 | pathlib.txt | 55680 | pathlib's path normalization may render it unsuitable for some applications: 1. pathlib normalizes "Path("my_folder/")" to "Path("my_folder")", which changes a path's meaning when supplied to various operating system APIs and command-line u |
| 3 | pathlib.txt | 729 | 이전에 이 모듈을 사용한 적이 없거나 어떤 클래스가 작업에 적합한지 확신 이 없다면, "Path"가 가장 적합할 가능성이 높습니다. 코드가 실행되는 플 랫폼의 구상 경로를 인스턴스화 합니다. 순수한 경로는 특별한 경우에 유용합니다; 예를 들면: 1. 유닉스 기계에서 윈도우 경로를 조작하려고 할 때 (또는 그 반대). 유닉 스에서 실행할 때는 "WindowsPath"를 인스턴스화 할 수 없지만, "PureWindowsPath"는 |
| 4 | pathlib.txt | 27849 | This method normally follows symlinks; to check if a symlink exists, add the argument "follow_symlinks=False". >>> Path('').exists() # The current directory. True >>> Path('.').exists() True >>> Path('setup.py').exists() True >>> Path('/etc |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | pathlib.txt | 1477 | 이 디렉터리 트리에 있는 파이썬 소스 파일 나열하기: >>> list(p.glob('**/*.py')) [PosixPath('test_pathlib.py'), PosixPath('setup.py'), PosixPath('pathlib.py'), PosixPath('docs/conf.py'), PosixPath('build/lib/pathlib.py')] 디렉터리 트리 내에서 탐색하기: >>> p = Path('/etc') >> |
| 2 | pathlib.txt | 55680 | pathlib's path normalization may render it unsuitable for some applications: 1. pathlib normalizes "Path("my_folder/")" to "Path("my_folder")", which changes a path's meaning when supplied to various operating system APIs and command-line u |
| 3 | pathlib.txt | 729 | 이전에 이 모듈을 사용한 적이 없거나 어떤 클래스가 작업에 적합한지 확신 이 없다면, "Path"가 가장 적합할 가능성이 높습니다. 코드가 실행되는 플 랫폼의 구상 경로를 인스턴스화 합니다. 순수한 경로는 특별한 경우에 유용합니다; 예를 들면: 1. 유닉스 기계에서 윈도우 경로를 조작하려고 할 때 (또는 그 반대). 유닉 스에서 실행할 때는 "WindowsPath"를 인스턴스화 할 수 없지만, "PureWindowsPath"는 |
| 4 | pathlib.txt | 0 | "pathlib" --- Object-oriented filesystem paths ********************************************** Added in version 3.4. **Source code:** Lib/pathlib/ ====================================================================== 이 모듈은 다른 운영 체제에 적합한 의미  |

### 23. try 문의 else 절은 언제 실행되나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 3 | 0.333 |
| Hybrid Regex | 1 | 2 | 0.500 |
| Hybrid Kiwi | 1 | 2 | 0.500 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | controlflow.txt | 5209 | (이것은 올바른 코드입니다. 자세히 들여다보면: "else" 절은 "if" 문이 ** 아니라** "for" 루프에 속합니다.) One way to think of the else clause is to imagine it paired with the "if" inside the loop. As the loop executes, it will run a sequence like if/if/if/else. The "if" is i |
| 2 | controlflow.txt | 0 | 4. 기타 제어 흐름 도구 ********************** 방금 소개한 "while" 문 외에도, 파이썬은 이 장에서 만나게 될 몇 가지 추 가적인 문법들을 시용합니다. 4.1. "if" 문 ============ 아마도 가장 잘 알려진 문장 형은 "if" 문일 것입니다. 예를 들어: >>> x = int(input("Please enter an integer: ")) Please enter an integer: 42 |
| 3 | errors.txt | 2330 | "try" 문은 다음과 같이 동작합니다. * 먼저, *try 절* ("try" 와 "except" 사이의 문장들) 이 실행됩니다. * 예외가 발생하지 않으면, *except 절* 을 건너뛰고 "try" 문의 실행은 종 료됩니다. * "try" 절을 실행하는 동안 예외가 발생하면, 절의 남은 부분들을 건너뜁 니다. 그런 다음, 형이 "except" 키워드 뒤에 오는 예외 이름과 매치되면 , 그 *except 절*이 실행되고, 그 |
| 4 | errors.txt | 10529 | * "except"나 "else" 절 실행 중에 예외가 발생할 수 있습니다. 다시, "finally" 절이 실행된 후 예외가 다시 발생합니다. * If the "finally" clause executes a "break", "continue" or "return" statement, exceptions are not re-raised. This can be confusing and is therefore discouraged |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | controlflow.txt | 5209 | (이것은 올바른 코드입니다. 자세히 들여다보면: "else" 절은 "if" 문이 ** 아니라** "for" 루프에 속합니다.) One way to think of the else clause is to imagine it paired with the "if" inside the loop. As the loop executes, it will run a sequence like if/if/if/else. The "if" is i |
| 2 | errors.txt | 10529 | * "except"나 "else" 절 실행 중에 예외가 발생할 수 있습니다. 다시, "finally" 절이 실행된 후 예외가 다시 발생합니다. * If the "finally" clause executes a "break", "continue" or "return" statement, exceptions are not re-raised. This can be confusing and is therefore discouraged |
| 3 | errors.txt | 2330 | "try" 문은 다음과 같이 동작합니다. * 먼저, *try 절* ("try" 와 "except" 사이의 문장들) 이 실행됩니다. * 예외가 발생하지 않으면, *except 절* 을 건너뛰고 "try" 문의 실행은 종 료됩니다. * "try" 절을 실행하는 동안 예외가 발생하면, 절의 남은 부분들을 건너뜁 니다. 그런 다음, 형이 "except" 키워드 뒤에 오는 예외 이름과 매치되면 , 그 *except 절*이 실행되고, 그 |
| 4 | controlflow.txt | 4029 | 4.5. 루프의 "else" 절 ===================== In a "for" or "while" loop the "break" statement may be paired with an "else" clause. If the loop finishes without executing the "break", the "else" clause executes. In a "for" loop, the "else" clause |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | controlflow.txt | 5209 | (이것은 올바른 코드입니다. 자세히 들여다보면: "else" 절은 "if" 문이 ** 아니라** "for" 루프에 속합니다.) One way to think of the else clause is to imagine it paired with the "if" inside the loop. As the loop executes, it will run a sequence like if/if/if/else. The "if" is i |
| 2 | errors.txt | 2330 | "try" 문은 다음과 같이 동작합니다. * 먼저, *try 절* ("try" 와 "except" 사이의 문장들) 이 실행됩니다. * 예외가 발생하지 않으면, *except 절* 을 건너뛰고 "try" 문의 실행은 종 료됩니다. * "try" 절을 실행하는 동안 예외가 발생하면, 절의 남은 부분들을 건너뜁 니다. 그런 다음, 형이 "except" 키워드 뒤에 오는 예외 이름과 매치되면 , 그 *except 절*이 실행되고, 그 |
| 3 | errors.txt | 10529 | * "except"나 "else" 절 실행 중에 예외가 발생할 수 있습니다. 다시, "finally" 절이 실행된 후 예외가 다시 발생합니다. * If the "finally" clause executes a "break", "continue" or "return" statement, exceptions are not re-raised. This can be confusing and is therefore discouraged |
| 4 | controlflow.txt | 0 | 4. 기타 제어 흐름 도구 ********************** 방금 소개한 "while" 문 외에도, 파이썬은 이 장에서 만나게 될 몇 가지 추 가적인 문법들을 시용합니다. 4.1. "if" 문 ============ 아마도 가장 잘 알려진 문장 형은 "if" 문일 것입니다. 예를 들어: >>> x = int(input("Please enter an integer: ")) Please enter an integer: 42 |

### 24. 반복 가능한 객체의 항목과 인덱스를 함께 얻으려면 어떤 함수를 사용하나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 1 | 2 | 0.500 |
| Hybrid Regex | 1 | 2 | 0.500 |
| Hybrid Kiwi | 1 | 3 | 0.333 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | programming.txt | 12074 | 그러나, 같은 연산이 때때로 형에 따라 다른 동작을 갖는 한 가지 연산 클 래스가 있습니다: 증분 대입 연산자. 예를 들어, "+="는 리스트를 변경하지 만, 튜플이나 정수는 변경하지 않습니다 ("a_list += [1, 2, 3]"은 "a_list.extend([1, 2, 3])"과 동등하고 "a_list"를 변경하지만, "some_tuple += (1, 2, 3)"과 "some_int += 1"은 새 객체를 만듭니다). 달 |
| 2 | datastructures.txt | 17964 | (1, 2, 3) < (1, 2, 4) [1, 2, 3] < [1, 2, 4] 'ABC' < 'C' < 'Pascal' < 'Python' (1, 2, 3, 4) < (1, 2, 4) (1, 2) < (1, 2, -1) (1, 2, 3) == (1.0, 2.0, 3.0) (1, 2, ('aa', 'ab')) < (1, 2, ('abc', 'a'), 4) 서로 다른 형의 객체들을 "<" 나 ">" 로 비교하는 것은, 그 객체들이 |
| 3 | programming.txt | 37300 | 한 리스트를 다른 리스트의 값으로 정렬하려면 어떻게 해야 합니까? --------------------------------------------------------------- Merge them into an iterator of tuples, sort the resulting list, and then pick out the element you want. >>> list1 = ["what", "I'm", "sortin |
| 4 | classes.txt | 593 | C++ 용어로, 보통 클래스 멤버들은 (데이터 멤버를 포함해서) *public* (예 외는 아래 비공개 변수 를 보세요) 하고, 모든 맴버 함수들은 *virtual* 입 니다. 모듈라-3처럼, 객체의 매소드에서 그 객체의 멤버를 참조하는 줄임 표현은 없습니다: 메서드 함수는 그 객체를 표현하는 명시적인 첫 번째 인 자를 선언하는데, 함수 호출 때 묵시적으로 제공됩니다. 스몰토크처럼, 클 래스 자신도 객체입니다. 이것이 임포팅과 |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | programming.txt | 12074 | 그러나, 같은 연산이 때때로 형에 따라 다른 동작을 갖는 한 가지 연산 클 래스가 있습니다: 증분 대입 연산자. 예를 들어, "+="는 리스트를 변경하지 만, 튜플이나 정수는 변경하지 않습니다 ("a_list += [1, 2, 3]"은 "a_list.extend([1, 2, 3])"과 동등하고 "a_list"를 변경하지만, "some_tuple += (1, 2, 3)"과 "some_int += 1"은 새 객체를 만듭니다). 달 |
| 2 | datastructures.txt | 17964 | (1, 2, 3) < (1, 2, 4) [1, 2, 3] < [1, 2, 4] 'ABC' < 'C' < 'Pascal' < 'Python' (1, 2, 3, 4) < (1, 2, 4) (1, 2) < (1, 2, -1) (1, 2, 3) == (1.0, 2.0, 3.0) (1, 2, ('aa', 'ab')) < (1, 2, ('abc', 'a'), 4) 서로 다른 형의 객체들을 "<" 나 ">" 로 비교하는 것은, 그 객체들이 |
| 3 | programming.txt | 37300 | 한 리스트를 다른 리스트의 값으로 정렬하려면 어떻게 해야 합니까? --------------------------------------------------------------- Merge them into an iterator of tuples, sort the resulting list, and then pick out the element you want. >>> list1 = ["what", "I'm", "sortin |
| 4 | classes.txt | 593 | C++ 용어로, 보통 클래스 멤버들은 (데이터 멤버를 포함해서) *public* (예 외는 아래 비공개 변수 를 보세요) 하고, 모든 맴버 함수들은 *virtual* 입 니다. 모듈라-3처럼, 객체의 매소드에서 그 객체의 멤버를 참조하는 줄임 표현은 없습니다: 메서드 함수는 그 객체를 표현하는 명시적인 첫 번째 인 자를 선언하는데, 함수 호출 때 묵시적으로 제공됩니다. 스몰토크처럼, 클 래스 자신도 객체입니다. 이것이 임포팅과 |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | controlflow.txt | 29511 | * 여러분의 코드를 국제적인 환경에서 사용하려고 한다면 특별한 인코딩을 사용하지 마세요. 어떤 경우에도 파이썬의 기본, UTF-8, 또는 단순 ASCII 조차, 이 최선입니다. * 마찬가지로, 다른 언어를 사용하는 사람이 코드를 읽거나 유지할 약간의 가능성만 있더라도, 식별자에 ASCII 이외의 문자를 사용하지 마세요. -[ 각주 ]- [1] 실제로, *객체 참조에 의한 호출 (call by object reference)*  |
| 2 | programming.txt | 12074 | 그러나, 같은 연산이 때때로 형에 따라 다른 동작을 갖는 한 가지 연산 클 래스가 있습니다: 증분 대입 연산자. 예를 들어, "+="는 리스트를 변경하지 만, 튜플이나 정수는 변경하지 않습니다 ("a_list += [1, 2, 3]"은 "a_list.extend([1, 2, 3])"과 동등하고 "a_list"를 변경하지만, "some_tuple += (1, 2, 3)"과 "some_int += 1"은 새 객체를 만듭니다). 달 |
| 3 | datastructures.txt | 17964 | (1, 2, 3) < (1, 2, 4) [1, 2, 3] < [1, 2, 4] 'ABC' < 'C' < 'Pascal' < 'Python' (1, 2, 3, 4) < (1, 2, 4) (1, 2) < (1, 2, -1) (1, 2, 3) == (1.0, 2.0, 3.0) (1, 2, ('aa', 'ab')) < (1, 2, ('abc', 'a'), 4) 서로 다른 형의 객체들을 "<" 나 ">" 로 비교하는 것은, 그 객체들이 |
| 4 | programming.txt | 37300 | 한 리스트를 다른 리스트의 값으로 정렬하려면 어떻게 해야 합니까? --------------------------------------------------------------- Merge them into an iterator of tuples, sort the resulting list, and then pick out the element you want. >>> list1 = ["what", "I'm", "sortin |

### 25. pathlib.Path 객체를 Amazon S3 버킷에 직접 업로드하려면 어떻게 하나요?

| Pipeline | Hit | 첫 정답 순위 | Reciprocal Rank |
|---|---:|---:|---:|
| Baseline | 평가 제외 | 평가 제외 | 평가 제외 |
| Hybrid Regex | 평가 제외 | 평가 제외 | 평가 제외 |
| Hybrid Kiwi | 평가 제외 | 평가 제외 | 평가 제외 |

#### Baseline 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | pathlib.txt | 0 | "pathlib" --- Object-oriented filesystem paths ********************************************** Added in version 3.4. **Source code:** Lib/pathlib/ ====================================================================== 이 모듈은 다른 운영 체제에 적합한 의미  |
| 2 | pathlib.txt | 6083 | >>> p = PurePath('/etc') >>> p PurePosixPath('/etc') >>> p / 'init.d' / 'apache2' PurePosixPath('/etc/init.d/apache2') >>> q = PurePath('bin') >>> '/usr' / q PurePosixPath('/usr/bin') >>> p / '/an_absolute_path' PurePosixPath('/an_absolute_ |
| 3 | pathlib.txt | 56423 | As a consequence of these differences, pathlib is not a drop-in replacement for "os.path". Corresponding tools ------------------- 아래는 다양한 "os" 함수를 해당 "PurePath"/"Path" 대응 물에 매핑하는 표 입니다. |
| 4 | pathlib.txt | 3871 | >>> PurePath('foo//bar') PurePosixPath('foo/bar') >>> PurePath('//foo/bar') PurePosixPath('//foo/bar') >>> PurePath('foo/./bar') PurePosixPath('foo/bar') >>> PurePath('foo/../bar') PurePosixPath('foo/../bar') (나이브한 접근법은 "PurePosixPath('foo/ |

#### Hybrid Regex 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | pathlib.txt | 0 | "pathlib" --- Object-oriented filesystem paths ********************************************** Added in version 3.4. **Source code:** Lib/pathlib/ ====================================================================== 이 모듈은 다른 운영 체제에 적합한 의미  |
| 2 | pathlib.txt | 6083 | >>> p = PurePath('/etc') >>> p PurePosixPath('/etc') >>> p / 'init.d' / 'apache2' PurePosixPath('/etc/init.d/apache2') >>> q = PurePath('bin') >>> '/usr' / q PurePosixPath('/usr/bin') >>> p / '/an_absolute_path' PurePosixPath('/an_absolute_ |
| 3 | pathlib.txt | 56423 | As a consequence of these differences, pathlib is not a drop-in replacement for "os.path". Corresponding tools ------------------- 아래는 다양한 "os" 함수를 해당 "PurePath"/"Path" 대응 물에 매핑하는 표 입니다. |
| 4 | pathlib.txt | 3871 | >>> PurePath('foo//bar') PurePosixPath('foo/bar') >>> PurePath('//foo/bar') PurePosixPath('//foo/bar') >>> PurePath('foo/./bar') PurePosixPath('foo/bar') >>> PurePath('foo/../bar') PurePosixPath('foo/../bar') (나이브한 접근법은 "PurePosixPath('foo/ |

#### Hybrid Kiwi 검색 결과

| 순위 | Source | 시작 위치 | 내용 미리보기 |
|---:|---|---:|---|
| 1 | pathlib.txt | 0 | "pathlib" --- Object-oriented filesystem paths ********************************************** Added in version 3.4. **Source code:** Lib/pathlib/ ====================================================================== 이 모듈은 다른 운영 체제에 적합한 의미  |
| 2 | pathlib.txt | 6083 | >>> p = PurePath('/etc') >>> p PurePosixPath('/etc') >>> p / 'init.d' / 'apache2' PurePosixPath('/etc/init.d/apache2') >>> q = PurePath('bin') >>> '/usr' / q PurePosixPath('/usr/bin') >>> p / '/an_absolute_path' PurePosixPath('/an_absolute_ |
| 3 | pathlib.txt | 56423 | As a consequence of these differences, pathlib is not a drop-in replacement for "os.path". Corresponding tools ------------------- 아래는 다양한 "os" 함수를 해당 "PurePath"/"Path" 대응 물에 매핑하는 표 입니다. |
| 4 | pathlib.txt | 3871 | >>> PurePath('foo//bar') PurePosixPath('foo/bar') >>> PurePath('//foo/bar') PurePosixPath('//foo/bar') >>> PurePath('foo/./bar') PurePosixPath('foo/bar') >>> PurePath('foo/../bar') PurePosixPath('foo/../bar') (나이브한 접근법은 "PurePosixPath('foo/ |
