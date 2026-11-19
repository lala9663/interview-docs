# 팀원 가이드

> 다루는 것: 이 프로젝트를 처음 받은 사람이 알아야 할 것을 한 장으로 모았다. 무엇을 만드는지, 지금 어디까지 됐는지, 첫날 할 일, 자리마다 먼저 할 일, 매일·매주의 흐름, 꼭 지킬 것, 막혔을 때 볼 곳.
>
> 2026-11-19에 다시 썼다(11/18 현업 회의 반영, 일정 다시 짜기). 여기는 요약이다. 규칙의 원본은 각 문서에 있고, 줄마다 어디를 보면 되는지 적었다. 이 문서와 원본이 다르면 원본이 맞다.

## 0. 처음 모여서 같이 볼 순서

1. 목업을 연다(3장 4번). 4주 차 파일로 경력 면접 한 건을 면접 전 → 중 → 후로 따라가 본다. 그다음 신입 면접 방(실시간 기능 잠금)을 본다.
2. 이 문서의 1장과 2장을 읽는다: 무엇을 만들고, 어디까지 됐고, 무엇이 안 됐는가.
3. [14-minutes-2026-11-18.md](14-minutes-2026-11-18.md)를 읽는다. 지금 방향의 근거다.
4. [10-roadmap.md](10-roadmap.md)의 2장(1단계 범위)과 3장(주별 일정, 받아야 하는 자료)을 본다.
5. 자리(A·B·C)를 정한다(4장).
6. 각자 3장대로 로컬에서 띄운다.

## 1. 한눈에

- **만드는 것**: DSInterview. 면접관이 면접 **전**에 지원자를 파악하고, 면접 **중**에 질문과 꼬리질문을 보며 진행하고, 면접 **후**에 평가와 보고서를 정리하도록 돕는 웹 서비스다. 합격 여부는 사람이 정하고 AI의 결과는 모두 참고용이다. → [01-scope.md](01-scope.md)
- **방향(11/18 회의)**: 경력 채용(화상 면접)을 먼저 만든다. 신입(대면 면접)은 녹음과 실시간 꼬리질문을 쓰지 않고, 미리 만든 질문과 예상 꼬리질문만 준다. 면접 종류는 신입도 경력도 직무 면접과 인성 면접 두 가지다. → [14-minutes-2026-11-18.md](14-minutes-2026-11-18.md)
- **레포 세 개**

  | 레포 | 맡는 것 | 스택 |
  | --- | --- | --- |
  | `interview-frontend` | 화면, 마이크 수집 | Vue 3, JavaScript, Vite 4, Tailwind 3 |
  | `interview-backend` | DB의 모든 읽기·쓰기, 인증·권한, 엑셀, 상태 관리 | Java 8, Spring Boot 2.7.5, JPA, Oracle |
  | `interview-agent` | AI와 음성(전사, 화자 구분, 꼬리질문, 평가, 보고서) | Python 3.12, FastAPI, LangGraph |

  경계는 두 줄로 기억한다: **DB는 backend만 만진다. AI는 agent만 부른다.** → [02-architecture.md](02-architecture.md)
- **API 명세**: 세 레포가 서로 주고받는 주소와 값의 이름·모양을 적은 문서다([03-api-contract.md](03-api-contract.md)). 화면, 백엔드, agent를 따로 만들어도 맞물리는 것은 모두가 이 문서대로 만들기 때문이다. 원본 하나와 세 레포의 복사본(`docs/contract/api-contract.md`)이 있고 네 개가 항상 같아야 한다. 파일 이름과 skill 이름에는 예전 이름인 contract가 남아 있다.
- **일정**: 1단계 개발은 2027-01-15에 끝내고 2단계를 1/18에 시작한다. 2월 중에 경력 채용에 오픈해 실제 면접에 쓸 예정이라, 보안과 운영 준비가 그 전에 끝나야 한다. 12/18까지 현업의 확인이 필요한 일을 끝내고, 12/24에 기능 구현을 마감한다. 매주 수요일에 현업 회의가 있다. → [10-roadmap.md](10-roadmap.md)

## 2. 지금 어디까지 됐나 (2026-11-19)

전부 외부 개발 환경에서 **가짜 AI(fake)** 로 확인한 것이다. 사내 DB, 사내 LLM·Whisper, AD SSO, 개인정보 암호화는 아직 붙이지 않았다. AI 결과의 품질은 실제 모델을 붙인 뒤에 본다.

| 묶음 | 된 것 | 안 된 것 |
| --- | --- | --- |
| 경력(화상) | 면접 전(사전 리포트, 준비된 질문, 페르소나(면접관이 고르는 진행 방식) 고르기), 면접 중(전사, 질문과 꼬리질문 나무, 말로 물은 질문 인식), 면접 후(상세 보고서, 평가 의견 초안, 질문 피드백) | 실제 화상 회의에서 소리를 받는 것은 해 본 적이 없다. 채용 시스템에서 일정과 면접위원을 읽는 것은 화면 시안뿐이다 |
| 신입(대면) | 실시간 기능 잠금(백엔드 설정), 질문 화면, 예상 꼬리질문의 저장과 표시, 평가 입력 | 예상 꼬리질문을 만드는 Agent 단계. 매칭 파일 올리기는 화면 시안뿐이다 |
| 채용 담당자 | 면접자 목록과 유형 거르기, 엑셀 여러 파일 올리기, 일정 달력, 면접 페르소나 관리, 시스템 상태, AI 참고 평가(관리자만), 운영 현황, AI 품질, 면접관 편차 | 채용·직무 등록 화면, 일정·면접관 바꾸기 화면, AI 모델 바꾸기(화면 시안뿐) |
| Agent | 면접 종류 두 가지 | 11/18 회의의 나머지: 예상 꼬리질문 만들기, 페르소나와 면접자 유형을 질문에 반영, 확인할 점의 근거 문장, LLM·음성 인식 상태 알리기. 백엔드는 이 값들을 보내거나 받을 준비가 돼 있고 Agent가 무시한다 |
| 확인 | frontend 린트·테스트·빌드, backend 테스트 39개 | 11/18 반영 뒤에는 agent 테스트를 외부 PC의 정책 때문에 돌리지 못했다(그 전의 측정과 확인은 agent 문서에 있다). 사내에서 먼저 돌린다. Oracle, Redis, 리눅스 서버에서 돌려 본 적이 없다 |

- 반영 상태를 항목별로 보려면 [01-scope.md](01-scope.md) 6장, 남은 일은 [09-backlog.md](09-backlog.md) 1장의 "11/18 회의 반영" 표와 2장.
- 현업의 답을 기다리는 것은 [05-open-questions.md](05-open-questions.md), 현업에 어렵다고 말할 것은 [15-feasibility.md](15-feasibility.md).

## 3. 첫날 할 일

1. [01-scope.md](01-scope.md)와 [02-architecture.md](02-architecture.md)를 읽는다(각 10분).
2. 주로 맡을 레포의 `README.md` → `AGENTS.md` → `docs/setup.md` 순으로 읽고 로컬에서 띄운다.

   | 레포 | 띄우기 | 확인 명령(합치기 전에 통과) |
   | --- | --- | --- |
   | frontend | `npm ci` 뒤 `npm run dev` (백엔드 없이 모의 데이터) | `npm run check` |
   | backend | `./gradlew bootRun` (H2 + 시드 데이터, 8080). Agent 없이 AI 작업까지 보려면 `AGENT_MODE=fake ./gradlew bootRun` | `./gradlew build` |
   | agent | 처음 한 번 `python -m venv .venv` → `.venv/Scripts/python -m pip install -r requirements-dev.txt`. 그다음 `.venv/Scripts/python -m uvicorn app.main:app --port 8000` (fake 모델). 리눅스는 `.venv/bin/python` | `.venv/Scripts/python -m pytest` |

3. 세 서비스를 함께 띄워 한 바퀴 돌려 본다: 백엔드 → agent → 프런트(`npm run dev:api`).
   - **Agent는 환경변수 `BACKEND_MODE=http`로 띄운다.** 기본값은 가짜 백엔드라, 그대로 띄우면 면접 방은 열리지만 전사와 꼬리질문이 백엔드에 저장되지 않는다(agent `docs/setup.md` 3장).
   - 로그인은 임시 로그인이다. 시드 사번은 backend `docs/setup.md`에 있다.
   - **전사와 보고서까지 보려면 경력 채용의 시드 면접으로 들어간다**: 사전 리포트 → 면접 방 → 종료 → 보고서.
   - 신입 채용에서는 엑셀 업로드 → 매칭 → 사전 리포트 → 질문 화면 → 종료 → 평가 입력까지다. 신입은 기본 설정에서 실시간 기능이 꺼져 있어 전사와 보고서가 없다(backend `app.live.new-grad-enabled`). 샘플 엑셀은 신입 공채용이다.
   - 예전에 띄운 적이 있어 backend에 `data/` 폴더가 남아 있으면 지우고 다시 띄운다(표와 열이 바뀌었다. backend `docs/setup.md`).
4. 목업을 열어 본다: frontend `dist-demo/`의 HTML을 더블클릭한다. 현업 회의에서 보여 주는 화면이 이것이고 주차마다 파일이 다르다.
   - 11/25 회의에 보여 줄 것은 `interview-mockup-2026-w48.html`(4주 차)이다. 11/18 회의의 의견이 들어 있다.
   - 11/18 회의에서 보여 준 예전 화면은 `…-2026-w47.html`, 모든 화면이 켜진 것은 `…-2027-w02.html`이다.
5. 레포 루트에서 OpenCode를 열고 "이 레포의 skill 목록을 알려 줘"라고 물어 `AGENTS.md`와 skill이 읽히는지 본다.
6. [06-collaboration.md](06-collaboration.md)를 읽고 작은 것 하나를 골라 첫 PR을 낸다.

## 4. 누가 무엇을

레포가 아니라 흐름으로 나눈다. 세 명 모두 세 레포를 고친다.

| 자리 | 맡는 흐름 | 주로 고치는 곳 | 겸하는 역할 |
| --- | --- | --- | --- |
| A | 데이터와 운영(등록, 매칭 파일, 채용 시스템 연결, 일정, 관리 화면) | 백엔드, 관리 화면 | 병합 담당 |
| B | AI와 실시간(전사, 화자, 꼬리질문, 보고서) | Agent, 면접 방 | AI 품질 담당 |
| C | 면접관 화면과 평가(준비, 평가, 보고서 화면) | 프런트엔드, 평가 쪽 백엔드 | 현업 소통·시연 담당 |

자리마다 먼저 할 일이다. 주별 전체는 [10-roadmap.md](10-roadmap.md) 3장에 있다.

| 자리 | 이번 주(3주 차, ~11/20) | 다음 주(4주 차, 11/23~27) | 먼저 읽을 것 |
| --- | --- | --- | --- |
| A | 11/18 반영분을 사내 레포에 올리기. Oracle에 스키마 올리기(새 표와 열 포함), Redis 연결 | Oracle·Redis로 전체 흐름 확인. 임시 로그인. 면접 대상자 엑셀 샘플을 받으면 올려 보기. 보안 7 · 9 · 13번: 사내 개발 서버의 키를 환경변수로, 임시 로그인을 열면 접속할 수 있는 곳 제한, HTTPS와 WebSocket 설정 확인([10-roadmap.md](10-roadmap.md) 3장의 "보안에서 할 일") | backend `docs/database.md`, `docs/excel-upload.md`, [08-import-checklist.md](08-import-checklist.md) 3장 |
| B | 사내 LLM·Whisper에 접속되는지 확인. Agent 문서를 11/18 반영 상태로 맞추기. agent 테스트 돌리기 | 사내 LLM으로 사전 리포트 만들기. Agent에 예상 꼬리질문 만들기, 페르소나와 면접자 유형 반영. 보안 7 · 8 · 10번: Agent에 개발용 기본 키 검사, API 문서 화면 끄기, 사내 AI에 자료를 보내도 되는지 확인([10-roadmap.md](10-roadmap.md) 3장의 "보안에서 할 일") | agent `docs/providers.md`, `docs/prompts.md`, `docs/open-questions.md`, API 명세 4.1 |
| C | 4주 차 목업 확인. 1단계 범위 자료와 [15-feasibility.md](15-feasibility.md) 다듬기. 현업에 받을 자료 다시 요청 | 11/25 회의 시연과 1단계 범위 합의. 회의 의견을 [09-backlog.md](09-backlog.md)에 적기 | frontend `docs/setup.md`의 "주차별 목업", [05-open-questions.md](05-open-questions.md) |

- 리뷰는 영역이 다른 사람이 본다. → [10-roadmap.md](10-roadmap.md) 4장
- 받을 자료가 와야 시작할 수 있는 일이 많다(신입 엑셀·매칭 파일, 경력 DB 테이블, 평가 양식, 질문 가이드, 용어집). 무엇을 누구에게 받는지와 오지 않았을 때의 대안은 [10-roadmap.md](10-roadmap.md) 3장의 "받아야 하는 자료"와 [15-feasibility.md](15-feasibility.md) 2장에 있다. 오기 전에는 가상 데이터로 만든다.

## 5. 매일의 흐름

```
dev에서 작업 브랜치를 딴다 → 고친다 → 확인 명령 통과 → PR → 리뷰 → dev에 스쿼시 병합
```

- 아침에 `git pull --rebase`로 `dev`를 당겨 온다.
- 작업 브랜치는 `feat/<짧은-설명>`, `fix/<짧은-설명>`. **하루 이틀 안에** 합친다. 오래 들고 있지 않는다.
- PR은 작게 낸다(리뷰하는 사람이 15분 안에 읽을 크기). 포맷 바꾸기·파일 이동은 기능 변경과 다른 PR로 낸다.
- PR 제목(= 커밋 메시지)은 `<영역>: <무엇을 왜>` 한 줄, 한국어. 예: `speaker: 되묻기 구간 규칙 추가`. API 명세를 바꾸면 앞에 `[API 변경]`.
- PR에 확인 명령을 돌린 결과를 붙인다. API 명세를 건드렸으면 네 파일이 같은지 비교한 결과도 붙인다.
- 리뷰는 1명, 영역이 다른 사람이 본다. API 명세를 바꾸는 PR은 세 명 모두 확인한다.
- `main`에는 직접 커밋하지 않는다.
- `dev`가 깨졌으면 새 작업보다 복구가 먼저다.
- 덜 끝난 기능은 기능 플래그로 가린 채 합친다. → [06-collaboration.md](06-collaboration.md) 2장

지금까지는 한 사람이 `main`에서 작업했다. 사내 레포에 `dev`가 없으면 `main`에서 `dev`를 만드는 것부터 한다.

## 6. 매주의 흐름

| 요일 | 하는 일 |
| --- | --- |
| 월 | 지난 회의의 의견을 후보에서 골라 이번 주 할 일을 정한다. 받아야 하는 자료가 왔는지 본다 |
| 화 | 오전에 합치기 마감. 세 서비스를 띄워 통합 확인 → `dev`를 `main`으로 올리고 태그(예: `2026-w48`). 세 레포를 같은 날 같은 태그로. 큰 변경은 이날 합치지 않는다 |
| 수 | 현업 회의. 그 주차의 목업으로 시연하고, 사내 연결 결과는 개발 서버에서 보여 준다. 나온 의견은 받아 적고 그 자리에서 날짜를 약속하지 않는다. 어려운 것은 그 자리에서 어렵다고 말한다([15-feasibility.md](15-feasibility.md)) |
| 목·금 | 개발 |

현업 의견과 작업 중에 나온 아이디어는 [09-backlog.md](09-backlog.md)에 후보로 넣고(적는 법은 그 문서 맨 위), 다음 월요일에 넣을지 정한다. → [10-roadmap.md](10-roadmap.md) 5·6장

## 7. 꼭 지킬 것

어기면 다른 두 사람이 멈추거나, 되돌리기 어려운 것들이다.

1. **API 명세가 먼저다.** 경로·필드·열거형·WebSocket 이벤트는 `docs/contract/api-contract.md`를 따른다. 필요한 값이 API 명세에 없으면 임의로 만들지 않는다. 바꿀 때는 먼저 공유하고 합의한 뒤, 원본([03-api-contract.md](03-api-contract.md))과 세 레포의 복사본을 **같은 날 같은 내용으로** 고친다. 네 파일이 같아야 한다. → [06-collaboration.md](06-collaboration.md) 4장, 각 레포의 skill `change-api-contract`
2. **블라인드 항목을 저장·응답·AI 입력에 넣지 않는다.** 성별, 생년월일, 가족, 주소, 출신 지역 등이다. agent로 가는 자료에는 면접자 이름과 수험번호도 넣지 않는다.
3. **실제 사람의 정보, 사내 주소, 비밀키를 코드·테스트·문서에 쓰지 않는다.** 시드와 샘플은 가상의 인물만. 비밀값은 환경변수 이름만 적는다. 현업에게 받은 파일(엑셀 샘플, 매칭 파일, 양식)은 레포에 넣지 않는다.
4. **개인정보 암호화가 붙기 전에는 개발 DB에 실제 개인정보를 넣지 않는다.** 가린 샘플이나 가상 데이터만 넣는다. 보안에서 할 일 전체는 [10-roadmap.md](10-roadmap.md) 3장의 "보안에서 할 일"에 있다
5. **녹음을 임의로 저장하지 않는다.** 기본은 메모리에만 두고 사후 정리 뒤 버린다. 디버깅용으로도 디스크에 쓰지 않는다.
6. **AI가 합격·불합격을 정하게 하지 않는다.** AI 점수와 면접관 점수를 합산하지 않는다. AI 참고 평가는 관리자만 본다.
7. **스택을 바꾸지 않는다.** frontend는 JavaScript(타입스크립트 아님), backend는 Java 8 문법과 `javax.*`, 네이티브 SQL 금지. 사내에는 인터넷이 없어 새 의존성은 사내 미러에 있는지부터 확인한다.
8. **여러 사람이 같이 건드리는 파일은 한 줄 추가만 한다.** frontend의 `router/index.js`, `api/index.js`, `mocks/server.js`, `lib/labels.js`, `AppShell.vue`, backend의 `application.yml`·`build.gradle`·`SecurityConfig`·`LocalSeedRunner`·`excel-mapping.yml`·`schema.sql`·`AGENTS.md`, agent의 `container.py`·`providers/registry.py`·`providers/fake_responses.py`·`settings/sections.py`·README의 환경변수 표다. 기존 줄의 순서나 포맷을 바꾸지 않는다. backend의 파일들은 다른 변경과 섞지 않고 작은 PR로 먼저 합치고, `schema.sql`은 손으로 고치지 않고 다시 만든다. → [06-collaboration.md](06-collaboration.md) 3장

레포별 금지 사항 전체는 각 레포 `AGENTS.md`에 있다.

## 8. OpenCode로 일하는 법

사내에서는 OpenCode로만 AI 도움을 받는다.

- **레포 루트에서 연다.** 그래야 그 레포의 `AGENTS.md`와 skill이 잡힌다. 두 레포에 걸친 일은 레포마다 따로 시킨다.
- 요청에 **무엇을, 어디에, 끝난 모습**을 적는다. API 명세가 바뀌는 일이면 "API 변경 포함"이라고 적는다.
- 끝나면 **확인 명령을 돌린 결과**를 보여 달라고 한다. 통과하지 않은 변경은 합치지 않는다.
- 자주 하는 일은 skill이 절차를 안다.

  | 하려는 일 | 레포 | skill |
  | --- | --- | --- |
  | 화면 추가 | frontend | `add-screen` |
  | 백엔드 호출 추가 | frontend | `add-api-call` |
  | 면접 방(실시간) 수정 | frontend | `work-on-live-room` |
  | 엔드포인트 추가 | backend | `add-api-endpoint` |
  | 테이블·컬럼 추가 | backend | `add-entity-and-migration` |
  | 엑셀 양식 변경, 다른 입력 통로 추가(매칭 파일, 채용 시스템 DB) | backend | `add-candidate-source` |
  | LLM·STT 교체 | agent | `add-provider` |
  | 새 AI 작업 | agent | `add-graph` |
  | 전사 지연·잘림 조정 | agent | `tune-audio-pipeline` |
  | 블라인드 기준 반영 | agent | `update-blind-rules` |
  | API 변경 | 세 레포 | `change-api-contract` |
  | 기존 사내 코드의 기능 가져오기 | 세 레포 | `port-legacy-feature` |

- 코드 구조를 바꾸면 같은 PR에서 `AGENTS.md`·skill·`docs/`를 같이 고친다. 문서가 틀리면 OpenCode가 틀린 곳을 고친다. → [06-collaboration.md](06-collaboration.md) 5장
- 작업하다가 범위 밖의 아이디어가 나오면 그 자리에서 만들지 않고 [09-backlog.md](09-backlog.md)에 적는다.

## 9. 목업과 주차별 기능

- 현업 시연은 서버 없이 여는 목업(HTML 한 파일)으로 한다. 3~11주 차 회의용이 주차마다 하나씩 있다(`2026-w47` ~ `2027-w02`). 주차가 올라갈수록 보이는 화면이 늘어난다: 4주 차에 11/18 회의 반영, 6주 차 운영 현황, 7주 차 AI 품질, 8주 차 면접관 편차. 5·9·10·11주 차는 새 화면이 없다.
- 코드는 한 벌이다. 기능은 모두 들어 있고, 주차별 목업에서만 그 주차에 보여 줄 것을 켠다. 개발 서버와 실제 배포에서는 전부 보인다(API 명세에 없는 화면 시안인 AI 모델 바꾸기, 매칭 파일 올리기, 채용 시스템에서 불러오기만 가짜 데이터로 돌 때 보인다).
- **프런트에 화면이나 기능을 더하면** 몇 주 차 목업부터 보일지 정한다: `src/lib/features.js`에 주차를 적고, `src/mocks/changelog.js`의 그 주차에 한 줄 적는다. 정하지 않으면 3주 차 목업부터 보인다.
- 이미 회의에서 보여 준 주차의 변경 요약은 고치지 않는다. 아직 보여 주지 않은 주차는 그 주의 일이 정해지면 고쳐서 다시 빌드한다.
- 다시 만들기: frontend에서 `npm run build:demo`. → frontend `docs/setup.md`의 "주차별 목업"

## 10. 막혔을 때

| 궁금한 것 | 볼 곳 |
| --- | --- |
| 이 값·이 경로가 맞나 | 그 레포의 `docs/contract/api-contract.md` |
| 왜 이렇게 만들었나, 가정이 뭔가 | [05-open-questions.md](05-open-questions.md), 그 레포의 `docs/open-questions.md` |
| 현업이 뭐라고 했나 | [14-minutes-2026-11-18.md](14-minutes-2026-11-18.md), [13-minutes-2026-11-11.md](13-minutes-2026-11-11.md) |
| 이 기능은 할 예정인가 | [09-backlog.md](09-backlog.md), [10-roadmap.md](10-roadmap.md) |
| 현업이 요구했는데 할 수 있나 | [15-feasibility.md](15-feasibility.md) |
| 화자 구분이 왜 틀리나, 어떻게 나아지나 | [04-speaker-separation.md](04-speaker-separation.md) |
| 사내 자원(DB, LLM, Whisper, SSO)에 어떻게 붙이나 | [08-import-checklist.md](08-import-checklist.md) 3장, 각 레포 `docs/` |
| 기존 사내 코드의 기능을 옮기려면 | [07-legacy-porting-guide.md](07-legacy-porting-guide.md) |
| 화면을 어떻게 그리나 | frontend `docs/ui-guide.md` |

## 11. 아직 정하지 않은 것

합류한 사람이 "규칙이 없네"라고 느낄 수 있는 곳이다. 정해지면 이 절에서 지우고 해당 문서에 적는다.

- A·B·C 자리에 누가 앉는지
- 1단계의 범위(11/25 회의에서 현업과 정한다)
- 합치기 전 확인을 사내에서 자동으로 돌릴지
- 세 레포 공통 문서(이 폴더)를 사내에서 어디에 둘지. API 명세 원본의 위치가 여기에 달려 있다([06-collaboration.md](06-collaboration.md) 6장)
- 공식 레포로 올리는 시점과 방식

→ [10-roadmap.md](10-roadmap.md) 7장
