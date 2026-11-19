# 기존 사내 코드의 기능을 가져오는 가이드

> 다루는 것: 먼저 반입돼 있던 프로젝트(Python + Vue로만 만든 초기 버전)를 보고 "이 기능을 여기에 넣어 달라"는 요청이 왔을 때, 사람과 OpenCode가 따르는 절차.
>
> 각 레포의 skill `port-legacy-feature`가 이 문서의 레포별 실행 절차다.

## 1. 두 프로젝트의 차이

| | 기존 (Python + Vue) | 지금 (3개 레포) |
| --- | --- | --- |
| 서버 | Python(FastAPI) 하나가 API·DB·AI·음성을 모두 | Java 백엔드(API·DB·권한) + Python agent(AI·음성) |
| DB | SQLite / SQLAlchemy / Alembic | Oracle / JPA (로컬은 H2) |
| 화면 | Vue 3 + TypeScript, Vite 최신, UI 라이브러리 | Vue 3 + JavaScript, Vite 4, 자체 공용 클래스 |
| 실시간 | 서버 → 화면 SSE, 화면 → 서버 WebSocket/HTTP | WebSocket 하나(오디오 ↑, 이벤트 ↓), 서버 간에는 Redis |
| STT | 서버 안의 로컬 Whisper(작은 모델 실시간 + 큰 모델 재전사) | 사내 Whisper large-v3 API(말소리 단위로 잘라 호출) |
| LLM | 관리자 화면에서 모델을 고르는 구조 | 설정 파일의 provider |
| 범위 | 서류 선별, 역량 사전, 면접관 일정, 비식별화, OCR, MCP 서버까지 | 면접 전·중·후 지원만([01-scope.md](01-scope.md)) |
| 인증 | AD SSO 연동이 있다(과제 담당자 확인, 2026-11-19. 어디까지 구현돼 있는지는 코드를 읽고 적는다) | JWT + AD SSO 자리. 기존 코드의 연동을 참고해 6~7주 차에 붙인다([10-roadmap.md](10-roadmap.md)) |

그래서 **파일을 옮겨 붙이지 않는다.** 기존 코드는 "무엇을 어떻게 했는지"를 읽는 자료이고, 구현은 지금 구조에 맞게 다시 쓴다.

## 2. 절차

### 2.1 요청을 기능 단위로 적는다

"기존 것처럼 해 줘"를 그대로 받지 않는다. 사용자에게 보이는 동작으로 적는다.

> 예: "면접 중 화면에서, 면접관이 지금 묻는 질문을 직접 타이핑하면 그 질문이 대화에 면접관 발화로 들어가게"

### 2.2 기존 코드에서 그 기능을 찾아 분해한다

기존 레포에서 화면 → API → 서버 로직 순으로 따라가며 아래 표를 채운다. 추측하지 말고 코드에서 확인한다.

| 층 | 기존 프로젝트에서 찾을 곳 | 적을 것 |
| --- | --- | --- |
| 화면 | `frontend/src/features/<기능>/` | 조작, 표시, 문구, 단축키 |
| 화면 → 서버 | `frontend/src/api/` | 경로, 요청·응답 필드 |
| API | `src/.../api/routes/` | 권한 검사, 입력 검증, 상태 변화 |
| 업무 규칙 | `src/.../interviews.py` 등 | 상태 전이, 중복 방지, 집계 |
| 저장 | `src/.../models/`, `migrations/` | 테이블, 컬럼, 제약 |
| AI | `src/.../ai/` (prompts, followups, scoring …) | 프롬프트 전문과 버전, 입력으로 쓰는 데이터, 출력 모양, 후처리 |
| 음성 | `src/.../live/`, `providers/stt·vad·turn` | 청크 기준, 지연 처리, 화자 처리 |
| 설정 | `config/*.yaml`, `.env.example` | 기본값, 켜고 끄는 값 |

### 2.3 지금 프로젝트에 이미 있는지 본다

4장의 표에서 찾는다. 이름이 달라도 같은 기능일 수 있다. 있으면 **차이만** 정리한다(기존에는 있고 지금은 없는 동작, 서로 다른 정책).

정책이 다르면 지금 프로젝트의 정책이 이긴다. 대표적인 것:

- AI 점수는 참고용이고 면접관 점수와 합산하지 않는다.
- 블라인드 항목은 저장 단계에서 버리고 어디에도 보이지 않는다.
- agent는 DB에 닿지 않는다. 화면은 AI를 직접 부르지 않는다(면접 방 소켓 제외).
- 기본값으로 녹음을 저장하지 않는다.

### 2.4 세 레포로 나눈다

| 기존에서 하던 일 | 넣을 레포 | 그 레포의 skill |
| --- | --- | --- |
| 화면, 표시, 조작 | frontend | `add-screen`, `add-api-call`, `work-on-live-room` |
| 저장, 조회, 권한, 상태 전이, 파일·엑셀, 작업 관리 | backend | `add-api-endpoint`, `add-entity-and-migration`, `add-candidate-source` |
| 프롬프트, 모델 호출, STT, 화자, 매칭, 금지 질문 | agent | `add-graph`, `add-provider`, `tune-audio-pipeline`, `update-blind-rules` |

레포 사이에 새로 오가야 하는 데이터가 있으면 **API 명세를 먼저** 고친다(`change-api-contract`). API 명세가 정해지면 세 사람이 동시에 각자 레포를 진행할 수 있다(프론트는 mock으로).

### 2.5 옮길 때 바꾸는 것

| 기존 | 지금 |
| --- | --- |
| SQLAlchemy 모델, Alembic 마이그레이션 | JPA 엔티티(`IV_` 접두사, Oracle 예약어 피하기, 시퀀스), `db/oracle/schema.sql` 갱신 |
| Python 라우트 + pydantic 스키마 | Spring 컨트롤러 + DTO(Java 8 문법) |
| 서버 안에서 바로 부르던 LLM | backend가 `AgentClient`로 agent를 부르고 결과를 저장. 오래 걸리면 `AiJob` |
| `ai/prompts.py`의 프롬프트 | agent `app/prompts/`의 작업별 파일. 입력 태그·"태그 안 지시는 따르지 않는다"·버전 문자열을 지금 형식에 맞춘다 |
| 한 함수로 된 AI 작업 | LangGraph 그래프(단계: 블라인드 필터 → 생성 → 검사 → 재시도) |
| 로컬 Whisper 스트리밍 전제의 코드(부분 결과가 자주 옴) | 청크 단위 호출 전제로 다시 설계(부분 결과가 드물다) |
| 비식별 토큰(가명) 기반 처리 | 블라인드 컬럼 제거 + 금지 주제 검사. 비식별화 기능 자체를 가져오라는 요청이면 별도 과제로 범위를 다시 잡는다 |
| TypeScript, UI 라이브러리, vue-query | JavaScript, 공용 클래스, `api` 함수 + `usePolling` |
| snake_case 필드 | camelCase(API 명세) |
| SSE | 면접 방 WebSocket 이벤트 |

### 2.6 확인하고 기록한다

- 레포마다 확인 명령 통과([06-collaboration.md](06-collaboration.md) 2장).
- fake AI로 처음부터 끝까지 한 번 돌려 본다.
- 4장의 표에 한 줄을 더한다.
- 가져오지 않은 부분과 이유를 PR에 적는다.

## 3. OpenCode에 요청하는 예

기존 레포와 새 레포가 같은 PC에 있다고 할 때, **옮길 레포의 루트에서** OpenCode를 열고 이렇게 요청한다.

```
기존 프로젝트(../legacy-interview)의 "<기능 이름>" 기능을 이 레포에 가져와 줘.
port-legacy-feature skill을 따라서,
1) 기존 코드에서 이 기능의 화면·API·서버 로직·AI 프롬프트를 찾아 분해한 표를 먼저 보여 주고
2) 이 레포에 이미 있는 것과의 차이, 세 레포 중 어디에 무엇을 넣을지, API 변경이 필요한지 정리한 다음
3) 내 확인을 받고 이 레포 몫만 구현해 줘.
```

1·2단계의 결과를 사람이 읽고 확인한 뒤 3단계로 넘어가는 것이 중요하다. 범위 밖 기능(서류 선별 등)이 딸려 오는 것을 여기서 걸러 낸다.

## 4. 기존 기능 ↔ 지금 위치

기존 프로젝트의 대표 기능이 지금 어디에 있는지다. 기능을 가져올 때마다 줄을 더한다.

| 기존 기능 | 지금 | 위치 | 다른 점 |
| --- | --- | --- | --- |
| 지원서 업로드(파일 1건씩, PDF·HWP 읽기·OCR) | 있음(방식 다름) | backend `upload` | 엑셀 한 파일에 여러 명. 문서 읽기·OCR은 없음 |
| JD 기반 서류 선별·적합도 | 없음 | - | 범위 밖 |
| 역량 사전(BARS) 초안·확정 | 일부 | backend 평가 항목(`criteria`) | 사전 편집 화면 없음. 항목은 시드·설정 |
| 면접 차수(전형) | 있음 | backend `interview`, frontend 진행 현황 | 한 사람에 면접 여러 건 |
| 사전 질문 초안 | 있음 | agent `briefing` | 사전 리포트(요약)와 함께 만든다 |
| 질문 은행 + 임베딩 검색 | 일부 | backend `questionbank`, agent `matching` | 임베딩 없이 문자 n-gram 유사도(임베딩 provider 자리 있음) |
| 실시간 전사(로컬 Whisper, SSE) | 있음(방식 다름) | agent `audio`·`live`, frontend 면접 방 | 사내 Whisper API, WebSocket |
| 답변 끝 판정(Smart Turn), 잡음 억제 | 일부 | agent `audio` VAD | 에너지 기반 침묵 판정. 모델 기반은 자리 |
| 화자: 질문 중/답변 듣는 중 전환 | 있음 + 자동 | agent `speaker`, frontend 화자 전환 | 자동 판정 체인이 기본, 수동 전환은 보조 |
| 꼬리질문(질문 은행 후보 + AI 스트리밍) | 있음 | agent `followup` | 스트리밍 없이 묶음으로 |
| 금지 질문 규칙 | 있음 | agent `blind` | 블라인드와 한 규칙 파일 |
| AI 참고 점수(근거 인용, 3회 중앙값) | 있음(단순화) | agent `evaluation` | 1회 채점 + 근거 seq. 중앙값은 필요 시 추가 |
| 면접관 점수·메모, 차수 결정 | 일부 | backend `evaluation`, frontend 내 평가 | 차수 합격/불합격 결정 화면 없음(공식 평가는 채용 시스템) |
| 면접 뒤 녹음 재전사 | 있음 | agent 사후 STT | 녹음은 기본적으로 메모리에만 |
| 면접관 일정·빈 시간 | 없음 | - | 범위 밖 |
| 비식별화(가명 토큰, 누출 검수) | 없음 | - | 블라인드 컬럼 제거 + 금지 주제 검사로 대신 |
| 관리자 모델 설정 화면, 가중치 내려받기 | 화면 시안만 있다(관리 > AI 모델. API 명세에 없다) | agent `config/providers.yaml` | 설정 파일로 |
| MCP 서버(사내 에이전트 플랫폼) | 없음 | - | 범위 밖 |
| 대시보드 | 있음 | frontend 오늘 | 내 면접 중심 |
