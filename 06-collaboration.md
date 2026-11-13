# 협업 규칙 (반입 이후, 3명, trunk-based, OpenCode)

> 다루는 것: 세 사람이 세 레포를 동시에 고칠 때 충돌을 줄이는 방법, 계약을 바꾸는 절차, OpenCode를 쓰는 방법.

## 1. 전제

- 반입한 뒤에는 코드를 밖으로 다시 가져올 수 없다. 사내에서는 **OpenCode**로만 AI 도움을 받는다.
- 레포는 3개(frontend, backend, agent), 사람은 3명. 한 사람이 한 레포를 주로 맡되 서로의 레포도 고칠 수 있다.
- 브랜치 전략은 trunk-based다.

## 2. Trunk-based 규칙

1. `main`은 항상 빌드되고 테스트가 통과한다.
2. 브랜치는 `main`에서 따서 **하루 이틀 안에** 합친다. 이름: `feat/<짧은-설명>`, `fix/<짧은-설명>`.
3. PR은 작게(리뷰어가 15분 안에 읽을 크기). 큰 기능은 여러 PR로 쪼갠다.
4. 덜 끝난 기능은 **기능 플래그로 가린 채** 합친다. 오래 사는 브랜치를 두지 않는다.
   - frontend: `import.meta.env.VITE_FEATURE_<이름>`, 또는 라우트·메뉴에 아직 연결하지 않음
   - backend: `app.features.<이름>` (`application.yml`)
   - agent: 설정의 `features.<이름>`
5. 합치기 전에 레포의 확인 명령을 통과시킨다.
   | 레포 | 명령 |
   | --- | --- |
   | frontend | `npm run check` |
   | backend | `./gradlew build` |
   | agent | `pytest` |
6. 포맷만 바꾸는 변경, 파일 이동, 이름 바꾸기는 **기능 변경과 다른 PR**로 한다. 섞이면 충돌이 커진다.

## 3. 충돌이 나기 쉬운 곳과 피하는 법

코드는 기능 단위 폴더로 나뉘어 있어, 서로 다른 기능을 고치면 파일이 겹치지 않는다. 겹치는 곳은 아래 "등록 파일"들이다.

| 레포 | 여러 사람이 같이 건드리는 파일 | 규칙 |
| --- | --- | --- |
| frontend | `router/index.js`, `api/index.js`, `mocks/server.js`, `lib/labels.js`, `components/AppShell.vue` | 한 줄 추가만. 기존 줄의 순서·포맷을 바꾸지 않는다 |
| backend | `application*.yml`, 보안 설정, 시드 데이터, 공용 오류 코드 | 기능별 설정은 접두사를 나눠 블록 끝에 추가 |
| agent | `config/providers.yaml`, provider 레지스트리, 라우터 등록, 설정 클래스 | 위와 같음 |
| 세 레포 | `docs/contract/api-contract.md` | 4장의 절차 |

그 밖의 습관:

- 아침에 `git pull --rebase`, 작업 중에도 하루 한 번 이상 `main`을 당겨 온다.
- 같은 기능 폴더를 두 사람이 동시에 고쳐야 하면 시작 전에 파일 단위로 나눠 말한다.
- 큰 리팩터링(폴더 구조 변경)은 미리 알리고 다른 PR이 없을 때 한 번에 한다.

## 4. API 계약을 바꾸는 절차

계약은 세 레포의 `docs/contract/api-contract.md`에 같은 내용으로 있다(이 폴더의 [03-api-contract.md](03-api-contract.md)가 반입 시점의 원본).

1. 바꾸려는 사람이 변경 내용을 짧게 공유한다: 무엇을, 왜, 어느 레포가 영향받는지.
2. 될 수 있으면 **호환되는 추가**로 한다(선택 필드 추가, 새 엔드포인트). 이름 변경·삭제는 "새것 추가 → 전환 → 옛것 삭제" 두 단계.
3. 세 레포의 계약 파일을 같은 내용으로 고친다. PR 제목에 `[계약 변경]`.
4. 합치는 순서: **받는 쪽 먼저, 보내는 쪽 나중.** (새 필드를 견디는 쪽이 먼저 배포돼야 한다.)
5. 같은 날 세 PR을 모두 합친다. 세 파일이 같은지 비교한다.

각 레포의 skill `change-api-contract`에 레포별 손댈 파일이 적혀 있다.

## 5. OpenCode 쓰는 법

### 5.1 준비돼 있는 것

| 파일 | 역할 |
| --- | --- |
| 레포 루트 `AGENTS.md` | OpenCode가 세션을 시작할 때 읽는 규칙. 스택, 금지 사항, 폴더 규칙, 명령어, 작업 순서 |
| `.opencode/skills/<이름>/SKILL.md` | 자주 하는 작업의 절차서. OpenCode가 설명(description)을 보고 맞는 것을 불러 쓴다 |
| `docs/` | 구조·설정·미확정 사항. skill과 AGENTS.md가 이 문서들을 가리킨다 |

### 5.2 skill 목록

| 레포 | skill | 쓰는 때 |
| --- | --- | --- |
| frontend | `add-screen` | 화면 추가 |
| | `add-api-call` | 백엔드 호출 추가(모의 서버 포함) |
| | `work-on-live-room` | 면접 방(실시간) 수정 |
| backend | `add-api-endpoint` | 엔드포인트 추가 |
| | `add-entity-and-migration` | 테이블·컬럼 추가(Oracle 주의점) |
| | `add-candidate-source` | 엑셀 컬럼 변경, API 입력 추가 |
| agent | `add-provider` | LLM·STT 교체·추가 |
| | `add-graph` | 새 AI 작업(프롬프트 → 그래프 → 테스트) |
| | `tune-audio-pipeline` | 청크·지연·VAD 조정 |
| | `update-blind-rules` | 블라인드·금지 질문 기준 반영 |
| 세 레포 공통 | `change-api-contract` | 계약 변경 |
| | `port-legacy-feature` | 기존 사내 코드의 기능 가져오기 ([07](07-legacy-porting-guide.md)) |

### 5.3 요청하는 요령

- **레포 루트에서 OpenCode를 연다.** 그래야 그 레포의 `AGENTS.md`와 skill이 잡힌다. 두 레포에 걸친 작업은 레포마다 따로 요청한다.
- 요청에 **무엇을, 어디에, 끝난 모습**을 적는다. 예: "면접자 목록에 '학교' 열을 더해 줘. 계약의 Candidate 목록 항목에 `school`을 선택 필드로 더하고, mock도 맞추고, `npm run check`까지."
- 계약이 바뀌는 일이면 요청에 그렇게 적는다("계약 변경 포함"). OpenCode가 `change-api-contract` 절차를 따른다.
- 끝나면 **확인 명령을 돌린 결과**를 보여 달라고 한다. 통과하지 않은 변경은 합치지 않는다.
- 규칙이 반복해서 어겨지면 `AGENTS.md`에 한 줄을 더한다. 자주 하는 작업이 생기면 skill을 더한다(폴더 하나 + `SKILL.md`, 맨 위에 `name`과 `description`).

### 5.4 AGENTS.md와 skill을 고칠 때

- 이 파일들도 코드다. PR로 고치고 리뷰를 받는다.
- `AGENTS.md`는 짧게 유지한다(200줄 안쪽). 길어지는 설명은 `docs/`로 보내고 링크만 둔다.
- 코드 구조를 바꾸면 같은 PR에서 `AGENTS.md`·skill·`docs/`를 같이 고친다. 문서와 코드가 어긋나면 OpenCode가 틀린 곳을 고친다.

## 6. 문서를 두는 곳

| 내용 | 위치 |
| --- | --- |
| 한 레포 안의 구조·설정·실행 | 그 레포의 `docs/` |
| 세 레포에 걸친 것(범위, 전체 구조, 계약 원본, 화자분리, 미확정 사항, 협업, 이식 가이드, 반입 체크리스트) | 이 폴더(`docs/`). 외부에서는 별도 git 레포로 관리한다. 반입할 때는 문서 레포로 그대로 넣거나, 레포를 3개로 유지해야 하면 세 레포 중 하나(권장: backend)의 `docs/project/`로 옮기거나 사내 위키에 올린다 |
| 현업 확인이 필요한 것 | [05-open-questions.md](05-open-questions.md) + 각 레포의 `docs/open-questions.md` |
