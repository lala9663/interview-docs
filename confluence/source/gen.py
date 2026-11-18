# -*- coding: utf-8 -*-
"""사내 컨플루언스용 그림 20장을 HTML로 만든다(한 장 = 한 파일, 1600x900). 뒤에 브라우저로 PNG로 찍는다.
쓰는 법: python gen.py <출력 폴더>"""
import io
import os
import sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1600px;height:900px;background:#fff;color:#191f28;font-family:'Pretendard','Malgun Gothic','맑은 고딕',sans-serif;-webkit-font-smoothing:antialiased}
body{padding:52px 64px 40px;display:flex;flex-direction:column}
.kicker{font-size:19px;font-weight:700;color:#1428a0;letter-spacing:-.01em}
h1{font-size:44px;font-weight:800;letter-spacing:-.03em;margin-top:6px}
.line{font-size:24px;color:#4e5968;margin-top:12px;line-height:1.45;letter-spacing:-.01em}
.body{flex:1;display:flex;flex-direction:column;justify-content:center;gap:22px;margin-top:26px;min-height:0}
.foot{display:flex;justify-content:space-between;font-size:16px;color:#8b95a1;border-top:1px solid #e5e8eb;padding-top:12px}
.foot b{color:#191f28}.foot b span{color:#1428a0}
.row{display:flex;align-items:stretch;gap:0}
.box{flex:1;border:1.5px solid #d5dae0;border-radius:10px;padding:16px 18px;background:#fff;min-width:0;display:flex;flex-direction:column;justify-content:center}
.box .t{font-size:23px;font-weight:700;letter-spacing:-.02em;line-height:1.3}
.box .s{font-size:17.5px;color:#4e5968;margin-top:6px;line-height:1.42}
.box.ai{border-color:#1428a0;border-left-width:6px}
.box.user{background:#f4f5f7;border-color:#f4f5f7}
.box.store{border-style:dashed}
.box.key{background:#1428a0;border-color:#1428a0;color:#fff}.box.key .s{color:#d6dcf5}
.box.opt{border-color:#c98a00;border-left-width:6px}
.no{font-size:15px;font-weight:700;color:#8b95a1;margin-bottom:4px}
.box.key .no{color:#aab6ee}
.arr{flex:0 0 46px;display:flex;align-items:center;justify-content:center;color:#8b95a1;font-size:28px;font-weight:700}
.arr small{display:block;font-size:13px;font-weight:600;color:#8b95a1;text-align:center;line-height:1.2}
.cards{display:grid;gap:18px}
.card{border:1.5px solid #d5dae0;border-radius:10px;padding:20px 22px;min-width:0}
.card h3{font-size:25px;font-weight:800;letter-spacing:-.02em;display:flex;align-items:center;gap:10px}
.card h3 i{font-style:normal;font-size:14px;font-weight:700;color:#1428a0;border:1.5px solid #1428a0;border-radius:5px;padding:2px 8px}
.card h3 i.w{color:#a06a00;border-color:#c98a00}
.card ul{list-style:none;margin-top:12px}
.card li{font-size:19px;color:#333d4b;line-height:1.5;padding-left:16px;position:relative;margin-top:5px}
.card li:before{content:'';position:absolute;left:0;top:.72em;width:6px;height:6px;border-radius:50%;background:#1428a0}
.card.w li:before{background:#c98a00}
.card.top{border-top:6px solid #1428a0}.card.top.w{border-top-color:#c98a00}
.band{display:grid;grid-template-columns:230px 1fr;border:1.5px solid #d5dae0;border-radius:10px;overflow:hidden}
.band .lab{background:#f4f5f7;padding:16px 20px;display:flex;flex-direction:column;justify-content:center}
.band .lab b{font-size:23px;font-weight:800;letter-spacing:-.02em}.band .lab span{font-size:16px;color:#4e5968;margin-top:3px}
.band .items{display:flex;gap:12px;padding:14px 16px;align-items:stretch}
.chip{flex:1;border:1.5px solid #d5dae0;border-radius:8px;padding:10px 14px;min-width:0}
.chip b{display:block;font-size:19px;font-weight:700;letter-spacing:-.01em}.chip span{display:block;font-size:15.5px;color:#4e5968;margin-top:3px;line-height:1.35}
.down{text-align:center;color:#8b95a1;font-size:22px;font-weight:700;line-height:.6}
.note{font-size:19px;color:#4e5968;border-left:4px solid #1428a0;padding:4px 0 4px 16px;line-height:1.5}
.note.w{border-left-color:#c98a00}
.note b{color:#191f28}
table{width:100%;border-collapse:collapse}
th{font-size:17px;color:#8b95a1;font-weight:700;text-align:left;padding:10px 14px;border-bottom:1.5px solid #d5dae0}
td{font-size:20px;padding:15px 14px;border-bottom:1px solid #e5e8eb;line-height:1.4;vertical-align:middle}
td b{font-weight:700}td.m{color:#1428a0;font-weight:700;white-space:nowrap}td.g{color:#4e5968}
.grid5{display:grid;grid-template-columns:1fr 150px 1fr 150px 1fr;column-gap:0;row-gap:10px;align-items:stretch}
.conn{display:flex;flex-direction:column;align-items:center;justify-content:center;color:#4e5968;font-size:15.5px;font-weight:600;text-align:center;line-height:1.3;padding:0 6px}
.conn b{font-size:28px;color:#8b95a1;line-height:1}
.conn.v{padding:10px 0}
"""


def page(fid, group, no, title, line, body, tag=''):
    kick = '%s · %s' % (group, no) + (' · <span style="color:#a06a00">제안</span>' if tag == 'p' else '')
    html = ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>%s</style></head><body>'
            '<div class="kicker">%s</div><h1>%s</h1><p class="line">%s</p><div class="body">%s</div>'
            '<div class="foot"><b>DS<span>Interview</span></b><span>%s</span></div></body></html>') % (CSS, kick, title, line, body, group)
    io.open(os.path.join(OUT, fid + '.html'), 'w', encoding='utf-8').write(html)
    META.append((fid, group, no, title, line, tag))


META = []


def box(t, s='', kind='', no=''):
    return '<div class="box %s">%s<div class="t">%s</div>%s</div>' % (
        kind, '<div class="no">%s</div>' % no if no else '', t, '<div class="s">%s</div>' % s if s else '')


def arr(label=''):
    return '<div class="arr"><div>→%s</div></div>' % ('<small>%s</small>' % label if label else '')


def flow(steps, per_row=4, numbered=True):
    rows = []
    n = 0
    for i in range(0, len(steps), per_row):
        cells = []
        for st in steps[i:i + per_row]:
            n += 1
            t, s, kind = (list(st) + ['', ''])[:3]
            if cells:
                cells.append(arr())
            cells.append(box(t, s, kind, str(n) if numbered else ''))
        # 줄 수를 맞춰 상자 폭이 같게
        for _ in range(per_row - len(steps[i:i + per_row])):
            cells.append('<div class="arr" style="visibility:hidden">→</div><div class="box" style="visibility:hidden"></div>')
        rows.append('<div class="row">%s</div>' % ''.join(cells))
    return '<div class="down">↓</div>'.join(rows) if len(rows) > 1 else rows[0]


def cards(items, cols, top=False):
    out = []
    for it in items:
        t, bullets, tag = (list(it) + [''])[:3]
        w = ' w' if tag in ('제안', '검토') else ''
        badge = '<i class="%s">%s</i>' % ('w' if w else '', tag) if tag else ''
        out.append('<div class="card%s%s"><h3>%s%s</h3><ul>%s</ul></div>' % (
            ' top' if top else '', w, t, badge, ''.join('<li>%s</li>' % b for b in bullets)))
    return '<div class="cards" style="grid-template-columns:repeat(%d,1fr)">%s</div>' % (cols, ''.join(out))


def band(label, sub, items):
    return '<div class="band"><div class="lab"><b>%s</b><span>%s</span></div><div class="items">%s</div></div>' % (
        label, sub, ''.join('<div class="chip"><b>%s</b><span>%s</span></div>' % (a, b) for a, b in items))


def note(text, w=False):
    return '<p class="note%s">%s</p>' % (' w' if w else '', text)


G1, G2 = '시스템 구성', '처리 흐름 · 구조'

# ================= 시스템 구성 =================
page('s1', G1, '1', '과제 요약',
     '면접관이 면접 전·중·후에 AI의 도움을 받는 웹 서비스다. 합격 여부는 사람이 정하고 AI의 결과는 모두 참고용이다.',
     cards([
         ('면접 전', ['이력서와 JD를 읽고 만든 <b>사전 리포트</b>', '면접에서 물을 <b>준비된 질문</b>', '면접 대상자 엑셀 올리기, 면접관 매칭']),
         ('면접 중', ['대화를 <b>글로 옮기기</b>', '면접관과 지원자 <b>말 구분</b>', '답변이 끝나면 <b>꼬리질문 제안</b>']),
         ('면접 후', ['기준별 <b>AI 참고 평가</b>', '<b>보고서</b> 초안 → 보정본', '면접관 평가 정리·복사']),
     ], 3, top=True)
     + band('대상', '한 벌의 코드', [('신입 공채', '대면 · 동시 20개 방 이상 · 보고서는 1~2분 안에'), ('경력 채용', '화상 · 여러 차수 · 상세 보고서')]))

arch = ('<div class="grid5">'
        + box('화면', 'Vue 3 · JavaScript<br>마이크 수집, 표시', 'key')
        + '<div class="conn"><b>→</b>REST /api/v1<br>JWT</div>'
        + box('백엔드', 'Spring Boot · JPA<br>기록의 주인, 인증·권한, 엑셀', 'key')
        + '<div class="conn"><b>→</b>JPA</div>'
        + box('Oracle', '모든 기록', 'store')
        + '<div class="conn v"><b>↕</b>WebSocket · 방 입장권(5분)<br>오디오 ↑ · 실시간 이벤트 ↓</div><div></div>'
        + '<div class="conn v"><b>↕</b>내부 REST · X-Internal-Key<br>AI 작업 요청 ↓ · 저장 요청 ↑</div><div></div>'
        + box('Redis', '토큰 · 방 상태 · 이벤트 중계', 'store')
        + '<div style="grid-column:1 / span 3">' + box('Agent', 'FastAPI · LangGraph &nbsp;|&nbsp; 전사, 화자 구분, 꼬리질문, 사전 리포트, 평가, 보고서', 'ai') + '</div>'
        + '<div class="conn"><b>→</b>모델 호출</div>'
        + box('사내 LLM · Whisper large-v3', '설정으로 교체', 'store')
        + '</div>')
page('s2', G1, '2', 'Overall 아키텍처',
     '화면 · 백엔드 · Agent 세 서비스다. DB는 백엔드만 만지고, AI는 Agent만 부른다. 신입(대면)과 경력(화상)이 같은 구성을 쓴다.',
     arch
     + band('음성 입력', '신입과 경력의 차이', [
         ('신입 · 대면', '면접실의 면접관 노트북 마이크가 방의 소리를 받아 Agent로 보낸다'),
         ('경력 · 화상 (지금)', '신입과 같은 길이다. 면접관 노트북이 화상 회의에서 나오는 소리를 받아 보낸다'),
         ('경력 · 화상 (미정)', 'Knox Teams에서 참가자별 음성이나 자막을 받을 수 있으면 그 길을 더한다. 현업 확인 중'),
     ])
     + note('세 서비스의 구성은 신입과 경력이 같고, 다른 것은 <b>음성이 들어오는 길</b>뿐이다. 오디오만 예외로 화면 → Agent 직접이다. 백엔드를 거치면 지연과 부하가 늘기 때문이고, 백엔드가 발급한 입장권으로만 붙을 수 있다.'))

page('s3', G1, '3', '구성요소 · 통신',
     '통신 길은 다섯 가지이고, 길마다 인증 방식이 정해져 있다.',
     '<table><tr><th>누가 → 누구에게</th><th>방식</th><th>인증</th><th>무엇을</th></tr>'
     '<tr><td><b>화면 → 백엔드</b></td><td class="m">REST /api/v1</td><td>로그인 토큰(JWT)</td><td class="g">모든 조회와 저장</td></tr>'
     '<tr><td><b>화면 ↔ Agent</b></td><td class="m">WebSocket</td><td>방 입장권(백엔드 발급, 5분)</td><td class="g">마이크 음성 ↑, 전사·꼬리질문 이벤트 ↓</td></tr>'
     '<tr><td><b>백엔드 → Agent</b></td><td class="m">내부 REST</td><td>X-Internal-Key</td><td class="g">사전 리포트·평가·보고서 생성, 방 마무리</td></tr>'
     '<tr><td><b>Agent → 백엔드</b></td><td class="m">내부 REST</td><td>X-Internal-Key</td><td class="g">전사·꼬리질문 저장, 보정 전사 전달</td></tr>'
     '<tr><td><b>백엔드 · Agent → 저장소</b></td><td class="m">JPA · Redis</td><td>계정·비밀번호(환경변수)</td><td class="g">Oracle은 백엔드만. Redis는 토큰, 방 상태, 이벤트 중계</td></tr>'
     '</table>'
     + note('주고받는 값의 이름과 모양은 <b>API 명세</b> 한 문서에 적혀 있고, 세 서비스가 그 문서대로 만든다.'))

page('s4', G1, '4', '주요 기능 영역',
     '면접 전 · 중 · 후의 면접관 화면과, 채용 담당자가 쓰는 관리 화면으로 나뉜다.',
     cards([
         ('면접 전', ['오늘의 면접, 다음 면접', '면접자 목록·상세(블라인드 제외)', '사전 리포트, 준비된 질문']),
         ('면접 중', ['실시간 대화 기록, 화자 구분', '준비한 질문 자동 체크', '꼬리질문 제안, 메모']),
         ('면접 후', ['AI 참고 평가', '보고서 초안 → 보정본', '내 평가, 물은 질문을 질문 은행에']),
         ('관리', ['엑셀 올리기, 면접관 매칭', '진행 현황, 당일 운영 현황', 'AI 품질, 면접관 편차']),
     ], 4, top=True))

page('s5', G1, '5', '설계 원칙',
     '바꿔 끼우기 쉽게, 면접이 멈추지 않게, 사람이 판단하게 만든다.',
     cards([
         ('DB는 백엔드만', ['DB 교체와 개인정보 통제가 한 서비스에서 끝난다']),
         ('AI는 Agent만', ['모델 교체가 한 서비스에서 끝난다', '모델은 인터페이스 뒤에 있고 설정으로 바꾼다']),
         ('API 명세가 먼저', ['값의 이름과 모양을 문서에 먼저 적고 만든다', '세 사람이 따로 만들어도 맞물린다']),
         ('면접이 멈추지 않게', ['AI가 늦거나 죽어도 화면은 계속 쓴다', '놓친 부분은 면접 뒤 다시 정리해 채운다']),
         ('블라인드', ['성별·나이·가족 등은 저장 단계에서 버린다', 'AI가 낸 글도 금지 항목을 한 번 더 검사한다']),
         ('AI는 참고용', ['AI 점수와 면접관 점수를 합산하지 않는다', '합격·불합격은 사람이 정한다']),
     ], 3))

# ================= 처리 흐름 · 구조 =================
page('p01', G2, '1', '면접 진행 흐름',
     '엑셀을 올리는 것부터 면접관이 평가를 내는 것까지 한 줄로 이어진다.',
     flow([
         ('엑셀 올리기', '면접 대상자 등록<br>블라인드 항목 제외', 'user'),
         ('면접관 매칭', '면접과 면접관 배정', 'user'),
         ('사전 리포트', '요약과 준비된 질문', 'ai'),
         ('면접 방 입장', '마이크 켜고 시작', 'user'),
         ('실시간 지원', '전사 · 화자 구분<br>꼬리질문 제안', 'ai'),
         ('면접 종료', 'AI 참고 평가<br>보고서 초안', 'ai'),
         ('면접 뒤 정리', '전체 음성 다시 전사<br>보고서 보정본', 'ai'),
         ('면접관 평가', '점수·등급 정리<br>채용 시스템에 복사', 'user'),
     ], 4)
     + note('<b>파란 선</b>은 AI가 하는 일, <b>회색 바탕</b>은 사람이 하는 일이다. 신입 면접의 보고서 초안은 종료 뒤 1~2분 안에 나온다.'))

page('p02', G2, '2', '레이어드 구조',
     '세 서비스 모두 기능 단위로 폴더를 나누고, 그 안에서 위에서 아래로만 부른다.',
     band('화면', 'Vue 3', [('화면(features)', '오늘 · 면접자 · 면접 전·중·후 · 관리'), ('상태(stores)', '로그인, 채용 선택'), ('호출(api)', 'REST 한 곳, 모의 서버 전환')])
     + '<div class="down">↓</div>'
     + band('백엔드', 'Spring Boot', [('Controller', '주소와 권한'), ('Service', '업무 규칙, AI 작업 관리'), ('Repository', 'JPA, 표준 쿼리만')])
     + '<div class="down">↓ ↑</div>'
     + band('Agent', 'FastAPI', [('API · WebSocket', '내부 REST, 방 연결'), ('그래프(LangGraph)', '작업의 순서와 검증'), ('프롬프트 · Provider', '지시문, 모델 호출')])
     + '<div class="down">↓</div>'
     + band('바깥', '설정으로 교체', [('Oracle', '기록'), ('Redis', '토큰, 방 상태'), ('사내 LLM', '글 생성'), ('Whisper', '음성 → 글')]))

page('p03', G2, '3', 'AI 처리 구성',
     'AI 작업은 다섯 가지 그래프로 나뉘고, 빠른 모델과 품질 모델을 일에 따라 나눠 쓴다.',
     cards([
         ('사전 리포트', ['요약과 질문 생성', '품질 모델', '면접 전'], ''),
         ('문장 다듬기', ['군말 지우기, 띄어쓰기', '빠른 모델', '면접 중'], ''),
         ('꼬리질문', ['답변을 더 깊이 묻는 질문', '빠른 모델', '면접 중'], ''),
         ('참고 평가', ['기준별 점수와 근거 발화', '품질 모델', '면접 후'], ''),
         ('보고서', ['신입 간단 / 경력 상세', '품질 모델', '면접 후'], ''),
     ], 5, top=True)
     + band('공통', '모든 그래프', [('금지 항목 필터', '입력에서 지우고 출력을 다시 검사'), ('출력 검증', '형식이 틀리면 한 번 다시 시킴'), ('동시 호출 제한', '모델별 한도, 제한 시간, 재시도'), ('음성 → 글', 'Whisper, 화자 구분 체인')]))

deep = ('<div class="row" style="justify-content:center"><div style="flex:0 0 520px">' + box('조율 에이전트', '할 일을 계획하고, 하위 에이전트에 나눠 맡기고, 결과를 보고 계획을 고친다', 'key') + '</div></div>'
        '<div class="down">↓ ↑</div>'
        + '<div class="row" style="gap:16px">'
        + box('자료 읽기', '이력서 · JD · 질문 은행에서<br>필요한 부분을 찾아 읽는다', 'opt')
        + box('질문 설계', '직무·경험에 맞는 질문과<br>꼬리질문을 만든다', 'opt')
        + box('검증', '금지 항목, 중복, 근거가<br>자료에 있는지 따진다', 'opt')
        + box('평가 · 정리', '답변을 기준에 대어 보고<br>보고서로 정리한다', 'opt')
        + '</div>')
page('p04', G2, '4', 'Deep Agent 구조',
     '지금은 순서가 정해진 그래프다. 에이전트가 스스로 계획을 세우고 하위 에이전트에 일을 나눠 맡기는 구조를 제안한다.',
     deep + band('갖춰야 할 것', '네 가지', [('계획', '할 일 목록을 만들고 고쳐 간다'), ('하위 에이전트', '일을 나눠 맡기고 결과만 받는다'), ('작업 메모', '중간 결과를 파일처럼 적어 두고 다시 읽는다'), ('자세한 지시문', '언제 무엇을 쓸지 구체적으로 적는다')])
     + note('<b>지금</b>: 요약 → JD 질문 → 이력서 질문 → 검사처럼 순서가 고정돼 있어 빠르고 예측하기 쉽다. <b>제안</b>: 결과가 얕으면 자료를 더 읽고 다시 만드는 식으로 스스로 반복한다. 모델 호출이 늘어 느려지므로 시간 여유가 있는 사전 리포트와 경력 상세 보고서부터 적용한다.', True), 'p')

page('p05', G2, '5', '질문 추천 상세 과정',
     'JD와 질문 은행에서 직무 질문을, 이력서에서 경험 질문을 만들고 금지 항목을 걸러 낸다.',
     flow([
         ('자료 준비', '프로필(블라인드 제외)<br>JD · 질문 은행', 'store'),
         ('금지 항목 지우기', '프로필의 금지 내용 삭제', ''),
         ('JD 기반 질문', 'JD에 맞는 질문 생성<br>질문 은행에서 고르기', 'ai'),
         ('이력서 기반 질문', '경험·프로젝트를<br>확인하는 질문', 'ai'),
         ('금지 항목 검사', '있으면 한 번 다시 생성', ''),
         ('정리', '남은 금지 질문은 통째로 뺀다<br>출처 표시: JD · 이력서 · 질문 은행', ''),
         ('저장', '백엔드가 준비된 질문으로 저장', 'store'),
         ('면접관 손질', '빼기 · 직접 추가', 'user'),
     ], 4)
     + note('질문마다 출처가 남아, 어느 쪽 질문이 실제로 더 쓰였는지를 관리 화면에서 볼 수 있다.'))

page('p06', G2, '6', '브리핑 생성 상세 과정',
     '면접관 매칭이 끝나면 사전 리포트(브리핑) 작업이 자동으로 걸리고, 다 되면 화면에 나타난다.',
     flow([
         ('작업 접수', '매칭 직후 자동<br>또는 "다시 만들기"', 'user'),
         ('백엔드: AI 작업 등록', '상태를 저장하고<br>바로 응답한다', 'store'),
         ('Agent 호출', '프로필 · JD · 질문 은행 전달', ''),
         ('금지 항목 지우기', '모델에 넣기 전에 삭제', ''),
         ('요약 생성', '한 줄 총평 · 핵심<br>강점 · 확인할 점 · 이력', 'ai'),
         ('질문 생성', 'JD 기반 · 이력서 기반', 'ai'),
         ('금지 항목 검사', '있으면 한 번 다시 생성', ''),
         ('저장 · 표시', '백엔드 저장<br>화면이 2초마다 확인', 'store'),
     ], 4)
     + note('오래 걸리는 AI 호출은 요청을 붙잡고 기다리지 않는다. 작업으로 등록해 뒤에서 돌리고, 실패하면 화면에서 다시 요청한다.'))

page('p07', G2, '7', '꼬리질문 흐름',
     '지원자의 답이 끝나고 잠깐 조용하면, 방금 한 답을 더 깊이 묻는 질문 2~3개를 제안한다.',
     flow([
         ('지원자 답 확정', '말이 글로 바뀌고<br>지원자 말로 판정', ''),
         ('만들 때인가', '1.5초 조용하고<br>답이 20자 이상', ''),
         ('재료 모으기', '최근 문답 · 지원자 요약<br>이미 물은 질문', 'store'),
         ('질문 생성', '빠른 모델 · 2~3개<br>사담이면 만들지 않음', 'ai'),
         ('걸러 내기', '금지 항목 · 이미 한 질문<br>서로 겹치는 후보', ''),
         ('화면에 제안', '오른쪽 칸에 표시<br>이유도 한 줄', 'key'),
         ('채택', '누르거나, 말로 물으면<br>질문 목록에 올라간다', 'user'),
         ('저장', '채택 여부까지 기록', 'store'),
     ], 4)
     + note('다음 말이 먼저 시작되면 만들지 않는다. "지금 만들기"를 누르면 기다리지 않고 바로 만든다.'))

page('p08', G2, '8', 'JD 기반 분석',
     'JD를 따로 분석하는 단계는 없고, JD 글을 각 AI 작업의 재료로 넣는다. 쓰이는 곳은 다섯 군데다.',
     cards([
         ('사전 리포트 요약', ['JD에 비추어 강점과 확인할 점을 뽑는다'], '면접 전'),
         ('JD 기반 질문', ['JD의 필수 지식을 묻는 질문을 만든다', '질문 은행에서 직무에 맞는 것을 고른다'], '면접 전'),
         ('AI 참고 평가', ['평가 기준과 함께 JD를 넣어 점수의 근거로 삼는다'], '면접 후'),
         ('상세 보고서', ['JD와 평가 항목으로 역량 3~6개를 골라 분석한다'], '면접 후'),
         ('면접관 매칭(임시)', ['직무 코드가 같은 면접관을 배정한다', '현업 매칭 결과가 오면 바꾼다'], '관리'),
     ], 3)
     + note('JD는 직무마다 한 번 등록하고, 그 직무의 모든 면접이 같은 글을 쓴다.'))

page('p09', G2, '9', '턴 디텍션 · 의도 분석',
     '말의 끝은 침묵으로 잡고, 누가 무엇을 말했는지는 글 내용으로 판정한다. 의도 분류 모델은 따로 없다.',
     flow([
         ('음성 조각 받기', '16kHz · 0.1초 단위', 'store'),
         ('말소리인가', '소리 크기로 판단<br>주변 소음에 맞춰 조정', ''),
         ('말 한 덩어리', '침묵이 이어지면 끊는다<br>너무 길면 강제로 자른다', 'key'),
         ('글로 바꾸기', 'Whisper', 'ai'),
         ('누가 말했나', '사람 지정 → 채널 → 질문과 일치<br>→ 말투 규칙 → AI 문맥 판정', ''),
         ('무엇을 물었나', '준비된 질문 · 꼬리질문과<br>얼마나 비슷한지 비교', ''),
         ('다음 동작', '질문이면 "물었음" 표시<br>답이면 꼬리질문 준비', 'key'),
     ], 4)
     + note('"의도"는 <b>화자 판정</b>(질문하는 사람인가, 답하는 사람인가)과 <b>질문 일치</b>(준비한 질문 가운데 어느 것인가) 두 가지로 대신한다. 바꿔 말한 질문은 지금 방식으로 못 잡아 임베딩 모델을 검토한다.'))

ws = ('<div class="grid5" style="grid-template-columns:1fr 260px 1fr 200px 1fr">'
      + box('마이크 노트북', '방에 한 대<br>음성을 보낸다', 'key')
      + '<div class="conn"><b>⇄</b>WebSocket 하나<br>음성 ↑ (PCM 16비트 · 16kHz)<br>이벤트 ↓ (JSON)</div>'
      + box('Agent', '말 덩어리로 자르기 → 전사<br>→ 다듬기 · 화자 판정', 'ai')
      + '<div class="conn"><b>→</b>이벤트 중계<br>(Redis)</div>'
      + box('다른 면접관 노트북', '듣기 전용<br>같은 이벤트를 받는다', 'user')
      + '</div>')
page('p10', G2, '10', '음성 스트림 처리',
     'SSE가 아니라 WebSocket을 쓴다. 음성을 올리고 결과를 내려받는 일을 연결 하나로 하기 때문이다.',
     ws + cards([
         ('내려오는 이벤트', ['임시 글자 → 확정 문장(화자 포함)', '질문 일치, 꼬리질문 제안·채택', '모델 상태, 오류']),
         ('끊겼을 때', ['1.6초부터 간격을 늘려 다시 붙는다', '놓친 구간은 백엔드에서 채운다', '입장권은 5분짜리라 매번 새로 받는다']),
         ('밀릴 때', ['보낼 음성이 2초 넘게 쌓이면 버린다', '서버는 임시 글자를 건너뛴다', '빠진 부분은 면접 뒤 다시 전사한다']),
     ], 3)
     + note('SSE는 서버에서 화면으로만 흐른다. 음성을 올리는 길을 따로 만들어야 해서 쓰지 않았다.'))

cmp_html = ('<div class="row" style="gap:28px">'
            '<div style="flex:1"><div class="card top"><h3>지금: 나누지 않음<i>적용</i></h3><ul>'
            '<li>Agent 한 서비스가 음성 스트림과 AI 작업을 함께 한다</li>'
            '<li>방 상태와 이벤트가 Redis에 있어 <b>Agent를 여러 대</b>로 늘릴 수 있다</li>'
            '<li>실시간 작업과 면접 뒤 작업은 호출 한도를 따로 둔다</li>'
            '<li>배포와 운영이 한 벌이라 단순하다</li></ul></div></div>'
            '<div style="flex:1"><div class="card top w"><h3>나눈다면<i class="w">검토</i></h3><ul>'
            '<li>스트림 서버: 음성 받기, 자르기, 전사, 이벤트 보내기</li>'
            '<li>AI 작업 서버: 사전 리포트, 평가, 보고서</li>'
            '<li>보고서가 몰려도 실시간 전사가 밀리지 않는다</li>'
            '<li>서비스와 배포 설정이 하나 늘어난다</li></ul></div></div></div>')
page('p11', G2, '11', '스트림 서버 분리 여부',
     '지금은 나누지 않는다. Agent를 여러 대로 늘리는 것으로 먼저 대응하고, 사내 AI로 부하를 잰 뒤 다시 판단한다.',
     cmp_html + note('방 20개를 동시에 돌린 부하 확인은 가짜 AI 기준으로만 했다. 사내 LLM·Whisper의 실제 속도와 동시 호출 한도를 재야 판단할 수 있다(6주 차).'))

page('p12', G2, '12', '분리 구성 · 판단 기준',
     '나눌 때의 구성과, 나눌지 말지를 정할 때 볼 네 가지 숫자를 정리했다.',
     flow([
         ('화면', '음성 ↑ 이벤트 ↓', 'user'),
         ('스트림 서버', '받기 · 자르기 · 전사<br>화자 판정 · 꼬리질문', 'opt'),
         ('Redis', '방 상태 · 이벤트 · 작업 대기열', 'store'),
         ('AI 작업 서버', '사전 리포트 · 평가 · 보고서<br>면접 뒤 다시 전사', 'opt'),
     ], 4, numbered=False)
     + cards([
         ('전사 지연', ['말이 끝나고 글이 뜨기까지', '보고서가 몰릴 때 늘어나는가'], '기준'),
         ('동시 방 수', ['한 대가 버티는 방의 수', '20개 방에서 대기열이 쌓이는가'], '기준'),
         ('장애 영향', ['보고서 작업이 죽으면', '진행 중인 면접도 끊기는가'], '기준'),
         ('배포 주기', ['프롬프트를 고칠 때마다', '진행 중인 방을 끊어야 하는가'], '기준'),
     ], 4)
     + note('네 가지 가운데 하나라도 문제가 되면 나눈다. 코드는 이미 폴더가 나뉘어 있어(실시간 / 그래프) 서비스로 떼어 내기 쉽다.', True), 'p')

page('p13', G2, '13', 'LLM 속도 개선 방안',
     '면접 흐름이 멈추지 않는 것이 우선이다. 이미 넣은 것 다섯 가지와 사내 모델을 붙인 뒤 검토할 것 네 가지다.',
     '<div class="row" style="gap:28px"><div style="flex:1.15">'
     + cards([('이미 넣은 것', [
         '<b>모델을 나눠 쓴다</b>: 면접 중에는 빠른 모델, 면접 전·후에는 품질 모델',
         '<b>기다리지 않는다</b>: 다듬기가 늦으면 원문을 그대로 확정한다',
         '<b>밀리면 덜어 낸다</b>: 임시 글자를 건너뛰고 확정 문장을 먼저 낸다',
         '<b>죽은 모델은 부르지 않는다</b>: 연속 3번 실패하면 30초 쉬었다가 시험 호출',
         '<b>신입 보고서는 호출을 최소로</b>: 1~2분 안에 초안을 낸다',
     ], '적용')], 1, top=True)
     + '</div><div style="flex:1">'
     + cards([('검토할 것', [
         '<b>글자를 받는 대로 보여 주기</b>: 보고서와 요약을 다 될 때까지 기다리지 않는다',
         '<b>지시문 줄이기</b>: 꼬리질문에 넣는 문답 수와 요약 길이',
         '<b>같은 입력은 다시 만들지 않기</b>: 사전 리포트 재요청',
         '<b>한꺼번에 부르기</b>: 상세 보고서의 부분들을 동시에',
     ], '검토')], 1, top=True)
     + '</div></div>'
     + note('사내 LLM의 실제 응답 시간과 동시 호출 한도를 아직 모른다. 붙인 뒤 재서 어느 것부터 할지 정한다.', True))

page('p14', G2, '14', '질문 페르소나 설정',
     '지금은 면접 종류와 상관없이 같은 말투로 질문을 만든다. 면접 종류마다 면접관의 관점을 정해 주는 것을 제안한다.',
     cards([
         ('PT 면접', ['<b>관점</b>: 같은 직무의 선임', '<b>묻는 것</b>: 근거, 대안, 한계', '<b>말투</b>: 구체적이고 짧게'], '제안'),
         ('인성 면접', ['<b>관점</b>: 함께 일할 팀의 리더', '<b>묻는 것</b>: 실제 행동, 그때의 판단', '<b>말투</b>: 열린 질문, 경험 중심'], '제안'),
         ('직무 면접(경력)', ['<b>관점</b>: 실무 책임자', '<b>묻는 것</b>: 맡은 범위, 결과, 수치', '<b>말투</b>: 이력의 주장을 확인'], '제안'),
         ('포트폴리오(경력)', ['<b>관점</b>: 결과물을 검토하는 사람', '<b>묻는 것</b>: 본인 기여, 설계 이유', '<b>말투</b>: 결과물의 한 부분을 짚어'], '제안'),
     ], 4, top=True)
     + note('<b>지금 있는 것</b>: 면접 종류에 따라 사담을 다루는 규칙만 다르다(인성 면접은 사담에서 드러난 태도도 본다). <b>넣는 곳</b>: 질문과 꼬리질문 지시문의 첫머리. 금지 항목 규칙은 어느 페르소나에서나 그대로 적용한다.', True), 'p')

page('p15', G2, '15', '기술 스택',
     '사내에 인터넷이 없어, 모든 라이브러리를 사내 미러에서 받을 수 있는 것으로만 골랐다.',
     cards([
         ('화면', ['Vue 3 · JavaScript', 'Vite 4 · Tailwind CSS 3', 'vue-router 4 · pinia', '마이크: AudioWorklet (PCM 16비트)', '테스트: vitest'], ''),
         ('백엔드', ['Java 8 · Spring Boot 2.7.5', 'Spring Data JPA · Oracle', 'Redis Sentinel · JWT', '엑셀: Apache POI', '테스트: JUnit 5'], ''),
         ('Agent', ['Python 3.12 · FastAPI', 'LangChain · LangGraph', 'WebSocket · Redis', '사내 LLM · Whisper large-v3', '테스트: pytest'], ''),
     ], 3, top=True)
     + band('공통', '세 서비스', [('API 명세', '주고받는 값의 약속'), ('가짜 AI', '모델 없이 전체 흐름 확인'), ('OpenCode', '사내 AI 코딩 도구용 규칙·절차'), ('주차별 목업', '서버 없이 여는 시연 파일')]))

io.open(os.path.join(OUT, 'meta.tsv'), 'w', encoding='utf-8').write('\n'.join('\t'.join(m) for m in META))
print(len(META), 'pages')
