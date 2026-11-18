// 컨플루언스 자료를 PPT로 만든다. 제목과 한 줄 설명은 고칠 수 있는 글자, 그림은 PNG.
// 쓰는 법: node build.js <그림 폴더(meta.tsv + PNG)> <출력.pptx> <apply_theme.js 경로>
const fs = require('fs')
const path = require('path')
const pptxgen = require('pptxgenjs')

const [imgDir, outFile, themeScript] = process.argv.slice(2)
const { applyTheme } = require(themeScript)

const THEME = {
  name: 'DSInterview',
  headFontFace: 'Malgun Gothic',
  bodyFontFace: 'Malgun Gothic',
  colors: {
    dk1: '191F28', lt1: 'FFFFFF', dk2: '4E5968', lt2: 'F4F5F7',
    accent1: '1428A0', accent2: 'C98A00', accent3: '1A7F5A', accent4: '8B95A1', accent5: 'D5DAE0', accent6: '0C1A6B',
    hlink: '1428A0', folHlink: '4E5968',
  },
}

const rows = fs.readFileSync(path.join(imgDir, 'meta.tsv'), 'utf8').split('\n').filter(Boolean).map((l) => {
  const [id, group, no, title, line, tag] = l.split('\t')
  return { id, group, no, title, line, tag }
})

async function main() {
  const pres = new pptxgen()
  pres.layout = 'LAYOUT_WIDE' // 13.33 x 7.5
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace }
  pres.title = 'DSInterview 시스템 구성 · 처리 흐름'
  pres.author = 'DSInterview'
  const C = pres.SchemeColor
  const W = 13.33
  const MX = 0.6

  // 표지와 구분 장: 파란 바탕
  pres.defineSlideMaster({
    title: 'COVER',
    background: { color: C.accent1 },
    objects: [
      { placeholder: { options: { name: 'title', type: 'title', x: MX, y: 2.55, w: W - MX * 2, h: 1.3, fontSize: 44, bold: true, color: C.background1, align: 'left', valign: 'bottom', margin: 0 }, text: '' } },
      { placeholder: { options: { name: 'body', type: 'body', x: MX, y: 4.0, w: W - MX * 2, h: 1.2, fontSize: 20, color: C.background1, align: 'left', valign: 'top', margin: 0 }, text: '' } },
    ],
  })
  // 내용 장: 흰 바탕, 위에 구분·제목·한 줄, 아래에 그림
  pres.defineSlideMaster({
    title: 'CONTENT',
    background: { color: C.background1 },
    objects: [
      { placeholder: { options: { name: 'kicker', type: 'body', x: MX, y: 0.42, w: W - MX * 2, h: 0.32, fontSize: 13, bold: true, color: C.accent1, align: 'left', valign: 'middle', margin: 0 }, text: '' } },
      { placeholder: { options: { name: 'title', type: 'title', x: MX, y: 0.74, w: W - MX * 2, h: 0.72, fontSize: 32, bold: true, color: C.text1, align: 'left', valign: 'middle', margin: 0 }, text: '' } },
      { placeholder: { options: { name: 'body', type: 'body', x: MX, y: 1.5, w: W - MX * 2, h: 0.62, fontSize: 15, color: C.text2, align: 'left', valign: 'top', margin: 0 }, text: '' } },
      { text: { text: 'DSInterview', options: { x: MX, y: 7.02, w: 3, h: 0.3, fontSize: 10, bold: true, color: C.text2, margin: 0, isTextBox: true } } },
    ],
    slideNumber: { x: W - MX - 0.6, y: 7.02, w: 0.6, h: 0.3, fontSize: 10, color: C.text2, align: 'right' },
  })

  const SEC0 = '표지'
  pres.addSection({ title: SEC0 })
  const cover = pres.addSlide({ masterName: 'COVER', sectionTitle: SEC0 })
  cover.addText('DSInterview 시스템 구성 · 처리 흐름', { placeholder: 'title' })
  cover.addText('면접관이 면접 전·중·후에 AI의 도움을 받는 웹 서비스\n시스템 구성 5장 · 처리 흐름과 구조 15장', { placeholder: 'body' })
  cover.addNotes('"제안"이 붙은 장(Deep Agent 구조, 분리 구성·판단 기준, 질문 페르소나)은 아직 만들지 않은 것이다. 나머지는 지금 코드에 있는 그대로다.')

  let section = null
  for (const r of rows) {
    const secTitle = r.id.startsWith('s') ? '시스템 구성' : '처리 흐름 · 구조 통합본'
    if (secTitle !== section) {
      section = secTitle
      pres.addSection({ title: section })
      const d = pres.addSlide({ masterName: 'COVER', sectionTitle: section })
      d.addText(section, { placeholder: 'title' })
      d.addText(r.id.startsWith('s')
        ? '과제 요약 · Overall 아키텍처 · 구성요소와 통신 · 주요 기능 영역 · 설계 원칙'
        : '면접 진행 흐름부터 AI 처리 구성, 음성 스트림, 속도 개선, 기술 스택까지 15가지', { placeholder: 'body' })
    }
    const s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: section })
    const kicker = [{ text: `${r.group} · ${r.no}`, options: {} }]
    if (r.tag === 'p') kicker.push({ text: '  ·  제안', options: { color: C.accent2 } })
    s.addText(kicker, { placeholder: 'kicker' })
    s.addText(r.title, { placeholder: 'title' })
    s.addText(r.line, { placeholder: 'body' })
    // 그림: 1600x640 비율(2.5:1). 폭 12.13" → 높이 4.852"
    const iw = W - MX * 2
    const ih = iw / 2.5
    s.addImage({ path: path.join(imgDir, r.id + '.png'), x: MX, y: 2.12, w: iw, h: ih, altText: `${r.title}: ${r.line}`, objectName: `그림 ${r.id}` })
    s.addNotes(r.line + (r.tag === 'p' ? ' (제안: 아직 만들지 않은 내용이다.)' : ''))
  }

  await pres.writeFile({ fileName: outFile })
  await applyTheme(outFile, THEME)
  console.log('slides', rows.length + 3, '→', outFile)
}

main().catch((e) => { console.error(e); process.exit(1) })
