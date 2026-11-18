# DSInterview — 프로젝트 문서

서비스 이름은 **DSInterview**다(면접 지원 서비스). 화면 이름과 디자인 방향은 frontend `docs/ui-guide.md`에 있다.

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
| 6 | [06-collaboration.md](06-collaboration.md) | 3명 브랜치 규칙(`dev` + `main`), API 변경 절차, OpenCode 사용법과 skill 목록 |
| 7 | [07-legacy-porting-guide.md](07-legacy-porting-guide.md) | 기존 사내 코드(Python + Vue)의 기능을 가져오는 절차, 기능 대응표 |
| 8 | [08-import-checklist.md](08-import-checklist.md) | 반입 전·후 체크리스트, 사내 자원에 붙이는 순서 |
| 9 | [09-backlog.md](09-backlog.md) | 기능 후보 목록: 면접관·현업 입장에서 더 필요한 것, 우선순위 |
| 먼저 | [11-team-guide.md](11-team-guide.md) | 팀원 가이드: 새로 합류한 사람이 첫 주에 알아야 할 것 한 장. 첫날 할 일, 매일·매주의 흐름, 꼭 지킬 것, 막혔을 때 볼 곳 |
| 회의 | [12-meeting-2026-11-18.md](12-meeting-2026-11-18.md) | 11/18 현업 회의 질문지: 물어볼 여덟 가지, 왜 묻는지, 답에 따라 달라지는 것. 받은 답을 적는 칸이 있다 |
| 회의 | [13-minutes-2026-11-11.md](13-minutes-2026-11-11.md) | 11/11 현업 회의록: 과제 범위, 필요한 데이터, 위험, 현업 희망 일정. 11/18에 바뀐 것을 표로 붙였다 |
| 회의 | [14-minutes-2026-11-18.md](14-minutes-2026-11-18.md) | 11/18 현업 회의록: 목업에 대한 의견, 정한 방향(경력 위주, 신입은 실시간 잠금), 각자 할 일. 지금 기준이다 |
| 자료 | [confluence/README.md](confluence/README.md) | 사내 컨플루언스에 올릴 자료: 시스템 구성 5장, 처리 흐름·구조 15장. 항목마다 한 줄 설명과 그림 한 장 |
| 10 | [10-roadmap.md](10-roadmap.md) | 개발 일정: 주별 목표, 세 명의 담당, 주간 흐름, 일정을 바꾸는 방법. 매주 바뀐다 |

## 처음 온 사람

[11-team-guide.md](11-team-guide.md)에 첫 주에 알아야 할 것이 한 장으로 있다. 요약하면:

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

세 레포 모두 `docs/contract/api-contract.md`(API 명세 복사본)와 `.opencode/skills/`(OpenCode용 작업 절차)가 있다.

## 지금 상태

- 반입은 1주 차에 끝났다. 그 뒤에 바뀐 것은 주차별로 사내 레포에 올린다.
- **fake AI**(가짜 LLM·STT)로 전체 흐름이 돈다. 실제 사내 LLM·Whisper·Oracle·Redis Sentinel·AD SSO는 사내에서 설정을 바꿔 붙인다(08).
- 개인정보 암호화(KMS)는 아직 없다. 적용 방식이 나오면 6주 차에 붙인다(10).
- AI 결과의 **품질**은 실제 모델을 붙인 뒤에 검증한다. fake는 모양과 흐름만 맞춘다.
- 현업 시연은 서버 없이 여는 목업(HTML 한 파일)으로 한다. 3~6주 차 회의용 목업이 주차마다 하나씩 만들어져 있고, 주차가 올라갈수록 보이는 기능이 늘어난다. 목업 안의 "달라진 것"이 그 주차에 더해진 것을 보여 준다(frontend `docs/setup.md`의 "주차별 목업").
