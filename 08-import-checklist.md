# 반입 체크리스트

> 다루는 것: 외부에서 만든 세 레포를 사내로 들여갈 때 챙길 것, 들어간 뒤 사내 자원에 붙이는 순서.
>
> 한 번 들어가면 다시 꺼낼 수 없다. **반입 전에** 1장을 끝낸다.
>
> **지금 상태(2026-11-19)**: 반입은 1주 차에 끝났다. 11/18 회의를 반영한 변경은 3주 차에 들여간다([10-roadmap.md](10-roadmap.md) 3장). 1장과 2장은 다음에 다시 들여갈 때를 위한 기록으로 둔다. 그 뒤에 바뀐 것은 주차별로 사내 레포에 올린다. 지금 볼 것은 3장(사내 자원에 붙이기)이다.

## 1. 반입 전 (외부에서)

### 코드와 문서

- [ ] 세 레포 각각 확인 명령 통과: frontend `npm run check`, backend `./gradlew build`, agent `pytest`
- [ ] fake AI로 처음부터 끝까지 한 번. 경력 채용의 시드 면접: 사전 리포트 → 면접 방(전사·꼬리질문) → 종료 → 초안 보고서 → 보정본. 신입 채용: 엑셀 업로드 → 매칭 → 사전 리포트 → 질문 화면 → 종료 → 평가 입력(신입은 기본 설정에서 실시간 기능이 꺼져 있어 전사와 보고서가 없다). Agent는 `BACKEND_MODE=http`로 띄운다
- [ ] 세 레포의 `docs/contract/api-contract.md`가 서로 같고 이 폴더의 `03-api-contract.md`와 같다
- [ ] 이 `docs/` 폴더(별도 git 레포)를 함께 넣는다. 사내 레포를 3개로 유지해야 하면 backend 레포의 `docs/project/`로 옮기거나 사내 위키에 올린다
- [ ] 레포에 실제 개인정보, 외부 서비스 키, 외부 주소가 없다(시드·모의 데이터는 모두 가상의 인물)
- [ ] 외부 전용 코드가 없다(외부 LLM 서비스용 provider 등). agent의 provider 목록 확인

### 의존성 (사내에는 인터넷이 없다)

- [ ] **frontend**: `package-lock.json` 포함. 사내 npm 미러에 모든 패키지·버전이 있는지 목록으로 확인(`npm ls --all`). 글꼴(Pretendard)은 npm 패키지로 번들돼 있어 CDN이 필요 없다
- [ ] **backend**: Gradle wrapper(`gradlew`, `gradle/wrapper/`) 포함. 사내에서 Gradle 7.5.1 배포본을 받을 주소로 `gradle-wrapper.properties`의 `distributionUrl`을 바꿔야 할 수 있다. 의존성 목록(`./gradlew dependencies`)을 사내 Maven 미러와 대조
- [ ] **agent**: `requirements.txt`(고정 버전) 포함. 사내 pip 미러와는 간접 의존성까지 든 `requirements.lock.txt`로 대조한다(agent `docs/setup.md`). 무거운 패키지(torch 등)는 쓰지 않는다
- [ ] 사내 미러에 없는 것이 있으면 반입 전에 대체하거나 반입 신청 목록에 넣는다

### 반입 신청에 필요한 정보

- [ ] 세 레포의 오픈소스 라이선스 목록(패키지 관리 도구로 추출)
- [ ] 서버 자원 요청 근거: [02-architecture.md](02-architecture.md) 4장, agent `docs/concurrency.md`

## 2. 반입 직후 (사내, 아직 사내 자원에 붙이기 전)

- [ ] 세 레포를 사내 Git에 올린다. 반입한 코드가 `main`의 시작점이다
- [ ] 세 레포 각각 `main`에서 `dev`를 만들어 올린다(`git switch -c dev && git push -u origin dev`). 이후 작업 브랜치는 모두 `dev`에서 딴다([06-collaboration.md](06-collaboration.md) 2장)
- [ ] 사내 Git에서 기본 브랜치를 `dev`로 바꾼다. 새로 받은 사람이 `dev`에서 시작하고 PR의 대상도 `dev`가 되게 하기 위해서다
- [ ] 세 `main`에 같은 시작 태그를 붙인다(예: `import-2026-11`). 나중에 "반입 때 상태"와 비교할 기준이 된다
- [ ] `main`에 직접 푸시하지 않기로 세 명이 확인한다. 사내 Git에 브랜치 보호 기능이 있으면 `main`에 걸고, 없으면 약속으로 지킨다(올리는 사람은 병합 담당 한 명)
- [ ] 각 레포 루트에서 OpenCode를 열어 `AGENTS.md`와 skill이 읽히는지 확인("이 레포의 skill 목록을 알려 줘")
- [ ] 사내 미러로 의존성 설치: `npm ci` / `./gradlew build` / `pip install -r requirements.txt`
- [ ] fake 설정 그대로 세 서비스를 띄워 1장의 "처음부터 끝까지"를 사내 PC에서 다시 확인

## 3. 사내 자원에 붙이기 (권장 순서)

한 번에 하나씩 바꾸고, 바꿀 때마다 처음부터 끝까지 돌려 본다. 표의 순서는 권장이고, 언제 하는지는 [10-roadmap.md](10-roadmap.md) 3장이 정한다(3~4주 차 DB·LLM, 5주 차 Whisper와 받은 데이터, 6~7주 차 AD SSO, 8주 차 KMS). 순서는 "위험이 작고 다른 것의 전제가 되는 것부터".

| 순서 | 붙일 것 | 레포 | 문서 | 확인할 것 |
| --- | --- | --- | --- | --- |
| 1 | Oracle | backend | `docs/database.md` | 스키마 생성(`db/oracle/schema.sql`), 한글·CLOB 저장, 시퀀스 권한 |
| 2 | Redis(Sentinel) | backend, agent | 각 `docs/` | 토큰 저장, 방 이벤트가 agent 두 대 사이에 중계되는지 |
| 3 | 사내 LLM | agent | `docs/providers.md` | 주소·인증 헤더·모델 이름, 한국어 출력, JSON 형식 출력이 되는지, 응답 시간, 동시 호출 한도 |
| 4 | 사내 Whisper large-v3 | agent | `docs/providers.md`, `docs/audio-pipeline.md` | 요청 형식(파일 형식, 필드 이름), 응답에 구간 시각·화자 정보가 있는지, 30초 음성의 처리 시간, 동시 호출 한도 |
| 5 | AD SSO (6~7주 차, [10-roadmap.md](10-roadmap.md)) | backend, frontend | 각 `docs/auth.md` | 사내에 일부 구현된 AD SSO 연동 코드를 참고한다. 로그인 흐름, 사번·이름·부서 매핑, 관리자 권한을 주는 방법. 붙기 전까지는 임시 로그인 |
| 6 | 실제 엑셀(마스킹 샘플) | backend | `docs/excel-upload.md` | 컬럼 이름을 `excel-mapping.yml`에 맞추기, 블라인드 컬럼 표시, DRM 해제본으로 올리기 |
| 7 | 블라인드·금지 질문 기준(현업 제공) | backend, agent | agent `docs/blind-rules.md` | 기준을 YAML에 반영, 검수 스크립트 |
| 8 | 배포(PaaS, 서비스별 config 레포를 거친 자동 배포) | 세 레포 + 각 config 레포 | 각 레포 `docs/setup.md` | config 레포에 넣을 빌드·실행 명령과 환경변수, HTTPS(마이크는 HTTPS에서만), WebSocket 프록시. 세 레포에는 CI/CD 파일이 없다 |

### 3·4번(모델)을 붙인 뒤 꼭 재야 하는 것

fake로는 알 수 없는 값들이다. 결과에 따라 설정값과 서버 수가 정해진다.

- [ ] 말이 끝난 뒤 확정 전사가 화면에 뜨기까지의 시간(목표: 수 초 이내)
- [ ] 답변이 끝난 뒤 꼬리질문이 뜨기까지의 시간
- [ ] 방 20개를 동시에 돌렸을 때 위 두 값과 큐 깊이(agent `scripts/load_test.py`를 실제 provider로)
- [ ] 신입 보고서(`BRIEF`)가 1~2분 안에 나오는지(신입 실시간 기능을 열었을 때만 해당한다)
- [ ] 화자 판정 정확도: 실제(동의받은) 면접 녹음 몇 건으로 agent `scripts/eval_speaker.py` 방식의 측정
- [ ] 질문 자동 매칭의 정확도와 임계값

### 운영 전 보안 점검

- [ ] 모든 비밀값을 환경변수로 교체(JWT 키, `INTERNAL_API_KEY`, `ROOM_TICKET_SECRET`, DB·Redis 비밀번호, 모델 API 키). 레포의 개발용 기본값이 운영에 남아 있지 않은지
- [ ] backend의 개발용 로그인(`/auth/dev-login`)이 운영 프로파일에서 닫혀 있는지
- [ ] agent의 내부 API(`/internal/v1`)가 사내망 안에서 backend만 부를 수 있는지
- [ ] 개인정보 암호화(KMS) 적용. 8주 차에 붙인다([10-roadmap.md](10-roadmap.md) 3장). 붙이기 전에 넣은 데이터는 지우고 다시 넣는다
- [ ] 사후 STT 실패 시 음성을 메모리에 30분 들고 있는 것이 괜찮은지 확인([05-open-questions.md](05-open-questions.md) 12번)
- [ ] 녹음 보관 정책 확정(기본: 보관 안 함)과 지원자 동의 문구

## 4. 현업에 받아야 하는 것

[05-open-questions.md](05-open-questions.md)에 질문 목록과 답에 따라 바꿀 위치가 있다. 반입 일정에 영향을 주는 것:

- 신입 면접 대상자 엑셀의 실제 포맷(마스킹 샘플). 11/11에 요청. 2026-11-19 현재 받은 기록이 없다
- 현업이 가진 직무별 면접 질문 목록의 형식(05의 1장 18번). 11/18 답: 경력 유형별 질문 가이드를 주기로 했다
- 화자 구분이 얼마나 맞아야 쓸 수 있는가(05의 1장 26번). 11/18 회의에서 답이 나오지 않았다
- 블라인드·금지 질문 기준
- 평가 항목과 채용 시스템 입력 화면 캡처. 11/18: 평가 의견란의 초안은 DS 전사 공통 양식의 항목에 맞추기로 했다. 양식은 아직 받지 못했다(05의 1장 9 · 33번)
- Knox Teams 음성·자막 API 가능 여부
- 직무 면접과 인성 면접의 진행 방식(동시 / 차수). 11/18 회의에서도 답이 없었다(05의 1장 1번)
- 면접 방의 마이크 구성(한 대 / 지원자용·면접관용 분리). 11/18: 신입은 실시간 녹음을 하지 않기로 해 지금은 정할 필요가 없다(05의 1장 8번)
