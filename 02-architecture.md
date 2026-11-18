# 전체 구조

> 다루는 것: 세 레포가 무엇을 맡고 어떻게 이어지는가, 교체 지점, 동시 20개 방을 어떻게 받는가.
>
> 메시지의 정확한 모양은 [03-api-contract.md](03-api-contract.md).
>
> 이 문서는 지금 코드의 구조다. 2026-11-18 회의로 바뀌는 방향(경력 우선, 신입은 실시간 녹음을 하지 않음, 자동 매칭 없음, 경력 데이터는 채용 시스템의 DB 테이블에서)은 [01-scope.md](01-scope.md) 6장에 있고, 코드에는 아직 반영하지 않았다. 세 서비스의 경계와 통신 방식은 그대로다.

## 1. 구성

```
┌────────────────────┐   REST /api/v1 (JWT)    ┌────────────────────────┐   JPA    ┌─────────┐
│ interview-frontend │ ──────────────────────▶ │ interview-backend      │ ───────▶ │ Oracle  │
│ Vue 3 · JS · Vite 4│                         │ Java 8 · Spring 2.7.5  │          └─────────┘
│                    │                         │ 기록의 주인, 인증, 엑셀 │ ───────▶ Redis (토큰, 캐시)
│                    │                         └───────┬────────▲───────┘
│                    │              내부 REST          │        │ 내부 REST (콜백)
│                    │              X-Internal-Key     ▼        │
│                    │   WebSocket (방 입장권)  ┌────────────────────────┐
│                    │ ──────────────────────▶ │ interview-agent        │ ───────▶ 사내 LLM (DS API Hub)
└────────────────────┘   오디오 ↑ / 이벤트 ↓    │ Python · FastAPI       │ ───────▶ Whisper large-v3
                                               │ LangChain / LangGraph  │ ───────▶ Redis (방 상태, 이벤트 중계)
                                               └────────────────────────┘
```

| 레포 | 맡는 것 | 맡지 않는 것 |
| --- | --- | --- |
| frontend | 화면, 마이크 수집, 표시 | 업무 규칙, 권한 판단 |
| backend | DB의 모든 읽기·쓰기, 인증·권한, 엑셀 처리, 면접·방·평가·보고서의 상태, AI 작업 관리 | 모델 호출, 프롬프트, 오디오 처리 |
| agent | STT, 전사 다듬기, 화자 판정, 질문 매칭, 요약·질문·꼬리질문·평가·보고서 생성, 블라인드 검사 | DB 접근, 사용자 인증(입장권 검증만) |

경계의 이유:

- **backend가 DB를 독점**해야 DB 교체(H2 → Oracle)와 개인정보 통제가 한 레포에서 끝난다.
- **agent가 AI를 독점**해야 모델 교체가 한 레포에서 끝나고, Python 생태계(LangGraph)를 그대로 쓴다.
- 오디오만 예외로 **브라우저 → agent 직접**이다. 20개 방의 오디오를 Java를 거쳐 중계하면 지연과 부하만 는다. 대신 backend가 발급한 5분짜리 입장권으로만 붙을 수 있다.

## 2. 데이터가 흐르는 길

### 면접 전

```
엑셀 ─▶ backend upload ─▶ 행 검증 · 블라인드 컬럼 제거 ─▶ 면접자 저장 (실패 행은 오류 목록)
                                   │
자동 매칭 ─▶ 면접 + 면접관 배정 ─▶ 브리핑 작업(AiJob) ─▶ agent /briefings ─▶ 요약 · 질문 저장
```

### 면접 중

```
마이크 ─PCM16 16kHz─▶ agent ─▶ 말소리 구간으로 자름 ─▶ Whisper ─▶ (partial 이벤트)
                               ─▶ LLM 다듬기 ─▶ 화자 판정 ─▶ (final 이벤트) ─▶ backend에 저장
                               ─▶ 면접관 말이면 준비된 질문·제안한 꼬리질문과 매칭 ─▶ (question.matched / followup.matched 이벤트)
                               ─▶ 지원자 답이 끝나면 꼬리질문 ─▶ (followup 이벤트) ─▶ backend에 저장
```

### 면접 후

```
종료 ─▶ backend ─▶ agent finalize ─┬─▶ (즉시) AI 평가 ─▶ 보고서 v1 (LIVE 초안)       ← 신입: 1~2분 안
                                   └─▶ (뒤에서) 방 전체 음성 사후 STT ─▶ backend 콜백 ─▶ AI 평가 다시
                                         ─▶ 전사 교체 ─▶ 보고서 v2 (REFINED 보정본) ─▶ 음성 폐기
```

## 3. 교체 지점

| 바꾸려는 것 | 손대는 곳 | 방법 |
| --- | --- | --- |
| LLM | agent `config/providers.yaml` | `impl`과 주소·모델 이름을 바꾼다. 형식이 다르면 provider 한 파일 추가 |
| STT(Whisper) | agent `config/providers.yaml`, `app/providers/`(`whisper_http.py`) | 위와 같음. DS API Hub 규격은 어댑터 한 파일 |
| DB | backend `application-<profile>.yml` | 프로파일 전환. 엔티티·쿼리는 그대로 |
| Redis (단일 ↔ Sentinel) | backend·agent 설정 | 설정만 |
| 인증(개발용 ↔ AD SSO) | backend `auth`, frontend 로그인 화면 | `AuthProvider` 구현 추가 |
| 면접자 데이터 통로(엑셀 ↔ API) | backend `CandidateSource` | 구현 추가. 저장 로직은 공용 |
| 엑셀 컬럼 | backend `excel-mapping.yml` | 설정만 |
| 블라인드·금지 질문 기준 | backend `excel-mapping.yml`(컬럼), agent `config/blind_rules.yaml`(주제·표현) | 설정만 |
| 면접관 매칭 방식 | backend `InterviewerMatcher` | 구현 추가 |
| 녹음 보관(안 함 ↔ 보관) | agent `audio.retention`, `audio.store` | 설정. 파일 저장 구현이 들어 있음(기본 꺼짐) |
| 화자 판정 방식 | agent `app/speaker/` | 판정기 추가·순서 변경 |
| 음성 입력(브라우저 마이크 ↔ Knox Teams) | agent 오디오 입력, frontend `audioOwner` | 미확정. Knox가 전사를 주면 STT 단계를 건너뛰는 입력을 더한다 |

## 4. 동시 20개 이상의 방 (신입 공채)

| 걱정 | 대응 |
| --- | --- |
| Whisper·LLM API가 한꺼번에 몰림 | agent가 프로세스 전역 동시 호출 수를 제한하고 방마다 큐를 둔다. 밀리면 임시 글자(partial)를 건너뛰고 확정 전사를 우선한다 |
| LLM 다듬기가 늦음 | 제한 시간을 넘으면 다듬지 않은 문장을 그대로 확정한다. 면접 흐름이 멈추지 않는 것이 우선 |
| agent 한 대로 부족 | 방 상태와 이벤트 중계가 Redis에 있어 agent를 여러 대 띄울 수 있다. 한 방의 오디오 소켓은 한 대에 붙고, 같은 방의 다른 단말은 어느 대에 붙어도 이벤트를 받는다 |
| 사후 STT가 몰림(면접이 같은 시각에 끝남) | 사후 STT는 실시간보다 낮은 우선순위의 별도 제한으로 돈다. 초안 보고서는 사후 STT를 기다리지 않는다 |
| Whisper·LLM이 죽음 | 연속 3번 실패하면 그 모델을 30초 동안 부르지 않고 바로 실패로 처리한다(죽은 모델을 기다리느라 큐가 밀리지 않게). 30초 뒤 한 번만 시험 호출해 되면 다시 연다. 화면에는 무엇이 멈췄고 무엇을 계속 쓸 수 있는지 안내가 뜬다. 음성은 계속 받아 두어 사후 STT가 채운다 (agent `docs/providers.md`, frontend `docs/realtime-room.md`) |
| 사후 STT 실패 | 음성을 바로 버리지 않고 기본 30분 동안 들고 1분마다 다시 시도한다. 그 안에 안 되면 버리고 실패를 알린다. 30분이라는 값은 현업·보안 확인이 필요하다([05-open-questions.md](05-open-questions.md) 12번) |
| 방 음성의 메모리 | 16kHz PCM16은 분당 약 1.9MB. 30분 방 20개면 약 1.2GB. 방당 상한을 두고 넘으면 오래된 구간부터 버린다 |
| 보고서 1~2분 | 신입(`BRIEF`)은 모델 호출 수를 최소로 한 그래프를 쓴다. backend가 제한 시간(기본 120초)을 건다 |
| DB 쓰기 | 전사는 발화 단위 묶음 저장. backend는 무상태라 여러 대로 늘릴 수 있다 |

실제 수치(지연, 큐 깊이, 증설 기준)는 agent 레포 `docs/concurrency.md`에 부하 테스트 결과와 함께 있다. **사내 Whisper·LLM의 실제 처리 속도와 동시 호출 한도는 사내에서 다시 재야 한다**([08-import-checklist.md](08-import-checklist.md)).

## 5. 보안과 개인정보

- 블라인드 컬럼은 backend가 저장 단계에서 버린다. agent는 블라인드 제외본만 받는다. agent는 출력(요약·질문·보고서)을 금지 주제 규칙으로 한 번 더 검사한다.
- 음성은 agent 밖으로 나가는 곳이 사내 Whisper뿐이다. 기본 설정에서 디스크에 쓰지 않는다.
- 서비스 간 호출은 `X-Internal-Key`, 브라우저 → agent는 방 입장권(JWT, 5분, 방 id 고정).
- 비밀값(JWT 키, 내부 키, 모델 API 키, DB 비밀번호)은 환경변수로만 넣는다. 레포의 기본값은 개발용이다.
- 운영 DB의 개인정보 암호화(KMS)는 아직 적용하지 않았고 꽂을 자리도 없다. backend의 컬럼 변환기로 붙일 계획이다(일정은 [10-roadmap.md](10-roadmap.md) 6주 차).

## 6. 포트와 실행 순서 (로컬)

| 서비스 | 포트 | 실행 |
| --- | --- | --- |
| backend | 8080 | `./gradlew bootRun` (프로파일 `local`: H2, 시드 데이터) |
| agent | 8000 | `uvicorn app.main:app --port 8000` (fake provider) |
| frontend | 5173 | `npm run dev:api` (또는 백엔드 없이 `npm run dev`) |
