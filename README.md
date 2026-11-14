# 면접 어시스턴트 — 프로젝트 문서

세 레포(frontend, backend, agent)에 걸친 문서다. 한 레포 안의 구조·설정·실행은 그 레포의 `docs/`에 있다.

```
interview/
  docs/                 ← 여기 (세 레포 공통)
  interview-frontend/   Vue 3 · JavaScript · Vite 4            화면
  interview-backend/    Java 8 · Spring Boot 2.7.5 · JPA       기록의 주인, 인증, 엑셀
  interview-agent/      Python · FastAPI · LangChain/LangGraph  AI, 음성
```

## 읽는 순서

| 순서 | 문서 | 내용 |
| --- | --- | --- |
| 1 | [01-scope.md](01-scope.md) | 무엇을 만드는가. 신입/경력 차이, 면접 전·중·후 단계별 범위, 과제와 기존 시스템의 경계 |
| 2 | [02-architecture.md](02-architecture.md) | 세 레포의 역할과 연결, 교체 지점 표, 동시 20개 방 대응, 보안 |
| 3 | [03-api-contract.md](03-api-contract.md) | REST · WebSocket · 내부 API의 정확한 모양(원본) |
| 4 | [04-speaker-separation.md](04-speaker-separation.md) | Whisper에 화자분리가 없을 때의 대응책과 측정 결과 |
| 5 | [05-open-questions.md](05-open-questions.md) | 현업 확인이 필요한 것, 가정으로 만든 것, 답이 오면 바꿀 위치 |
| 6 | [06-collaboration.md](06-collaboration.md) | 3명 trunk-based 규칙, 계약 변경 절차, OpenCode 사용법과 skill 목록 |
| 7 | [07-legacy-porting-guide.md](07-legacy-porting-guide.md) | 기존 사내 코드(Python + Vue)의 기능을 가져오는 절차, 기능 대응표 |
| 8 | [08-import-checklist.md](08-import-checklist.md) | 반입 전·후 체크리스트, 사내 자원에 붙이는 순서 |
| 9 | [09-backlog.md](09-backlog.md) | 기능 후보 목록: 면접관·현업 입장에서 더 필요한 것, 우선순위 |

## 처음 온 사람

1. 01, 02를 읽는다.
2. 맡을 레포의 `README.md` → `AGENTS.md` → `docs/setup.md` 순으로 읽고 로컬에서 띄운다.
3. 세 서비스를 함께 띄워 한 바퀴 돌려 본다(02의 6장).
4. 06의 규칙을 읽고 첫 PR을 낸다.

## 레포별 문서

| 레포 | 먼저 볼 것 | 그 밖 |
| --- | --- | --- |
| frontend | `README.md`, `AGENTS.md` | `docs/architecture.md`, `realtime-room.md`, `ui-guide.md`, `setup.md`, `auth.md`, `open-questions.md` |
| backend | `README.md`, `AGENTS.md` | `docs/architecture.md`, `setup.md`, `database.md`, `auth.md`, `excel-upload.md`, `open-questions.md` |
| agent | `README.md`, `AGENTS.md` | `docs/architecture.md`, `setup.md`, `providers.md`, `audio-pipeline.md`, `speaker-separation.md`, `concurrency.md`, `blind-rules.md`, `prompts.md`, `open-questions.md` |

세 레포 모두 `docs/contract/api-contract.md`(계약 복사본)와 `.opencode/skills/`(OpenCode용 작업 절차)가 있다.

## 지금 상태

- 외부 개발 환경에서 **fake AI**(가짜 LLM·STT)로 전체 흐름이 돈다. 실제 사내 LLM·Whisper·Oracle·Redis Sentinel·AD SSO는 사내에서 설정을 바꿔 붙인다(08).
- AI 결과의 **품질**은 실제 모델을 붙인 뒤에 검증한다. fake는 모양과 흐름만 맞춘다.
