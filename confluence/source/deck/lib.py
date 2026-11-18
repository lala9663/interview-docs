# -*- coding: utf-8 -*-
# 받은 PPT의 틀(마스터·레이아웃·표지·목차) 위에 우리 도형을 그리는 도구.
import copy
from xml.sax.saxutils import escape
from lxml import etree

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS = {'a': A, 'p': P}
EMU = 914400
FONT = 'Pretendard'

# 받은 PPT에서 쓰는 색 묶음: (바탕, 테두리, 제목 글자)
ST = {
    'green': ('EAF6EF', '9FD1B4', '22704A'),
    'blue': ('EBF2F9', 'A9C1DE', '1F3A5C'),
    'orange': ('FFF5E9', 'EBCB9F', '9A5410'),
    'yellow': ('FFF7DC', 'E6C866', '7F5F01'),
    'gray': ('F3F4F6', 'C7CCD3', '374151'),
    'white': ('FFFFFF', 'D5DCE6', '1F2937'),
    'red': ('FDECEC', 'F2B8B5', 'B42318'),
    'panel': ('F5F7FA', 'D5DCE6', '1F2937'),
}
NAVY, NAVY2, DARK, LABEL, ACC = '2E4F78', '1F3A5C', '1F3A5C', '16406A', '006CB5'
TXT, SUB, MUTE = '242D36', '4B5563', '6B7785'

WARN = []


def emu(v):
    return int(round(v * EMU))


def char_w(ch):
    o = ord(ch)
    if ch == ' ':
        return 0.27
    if o >= 0xAC00 and o <= 0xD7A3 or 0x3130 <= o <= 0x318F or 0x4E00 <= o <= 0x9FFF:
        return 0.90
    if ch in '·.,:;\'"|!()[]/':
        return 0.32
    if ch in '→←↑↓↔⇄—①②③④⑤⑥⑦⑧⑨▪':
        return 0.92
    if ch.isupper() or ch.isdigit():
        return 0.63
    return 0.54


def text_w(t, sz, bold=False):
    return sum(char_w(c) for c in t) * sz / 72.0 * (1.03 if bold else 1.0)


def norm_paras(text, sz, bold, col):
    """문단 목록으로 맞춘다. 문단 = 런 목록, 런 = (글, 크기, 굵게, 색)."""
    if text is None:
        return []
    if isinstance(text, str):
        text = text.split('\n')
    out = []
    for p in text:
        if isinstance(p, str):
            out.append([(p, sz, bold, col)])
        elif isinstance(p, tuple):
            t, s, b, c = (list(p) + [None, None, None])[:4]
            out.append([(t, s or sz, bold if b is None else b, c or col)])
        else:
            out.append([((list(r) + [None, None, None])[0], (list(r) + [None, None, None])[1] or sz,
                         bold if (list(r) + [None, None, None])[2] is None else (list(r) + [None, None, None])[2],
                         (list(r) + [None, None, None])[3] or col) for r in p])
    return out


class Slide(object):
    def __init__(self, slide, no):
        self.s = slide
        self.no = no
        self.tree = slide.shapes._spTree
        self.nid = 100

    # ---------- 틀 다루기 ----------
    def clear_body(self):
        for el in list(self.tree):
            tag = etree.QName(el).localname
            if tag in ('sp', 'grpSp', 'cxnSp', 'pic', 'graphicFrame'):
                if el.find('.//p:nvPr/p:ph', NS) is None or tag == 'grpSp':
                    self.tree.remove(el)

    def shape(self, sid):
        for el in self.tree.iter('{%s}sp' % P):
            if el.find('p:nvSpPr/p:cNvPr', NS).get('id') == str(sid):
                return el
        raise KeyError(sid)

    def ph(self, typ, idx=None):
        for el in self.tree.findall('p:sp', NS):
            ph = el.find('.//p:nvPr/p:ph', NS)
            if ph is not None and (ph.get('type') or 'body') == typ and (idx is None or ph.get('idx') == str(idx)):
                return el
        raise KeyError((typ, idx))

    @staticmethod
    def set_lines(sp, lines):
        """글만 바꾸고 서식은 그대로 둔다. 문단 수가 같으면 문단마다, 문단이 하나면 줄바꿈으로."""
        paras = sp.findall('p:txBody/a:p', NS)
        paras = [p for p in paras if p.find('a:r', NS) is not None]
        if len(paras) == len(lines):
            for p, line in zip(paras, lines):
                Slide._set_runs(p, [line])
        elif len(paras) == 1:
            Slide._set_runs(paras[0], lines)
        else:
            raise ValueError('문단 수가 맞지 않는다: %d vs %d' % (len(paras), len(lines)))

    @staticmethod
    def _set_runs(p, lines):
        first = p.find('a:r', NS)
        tmpl = copy.deepcopy(first)
        pos = list(p).index(first)
        for el in list(p):
            if etree.QName(el).localname in ('r', 'br'):
                p.remove(el)
        for i, line in enumerate(lines):
            if i:
                br = etree.SubElement(p, '{%s}br' % A)
                p.remove(br)
                p.insert(pos, br)
                pos += 1
            r = copy.deepcopy(tmpl)
            r.find('a:t', NS).text = line
            p.insert(pos, r)
            pos += 1

    def head(self, title, lead, crumb):
        self.set_lines(self.ph('title'), [title])
        self.set_lines(self.ph('body', 13), lead)
        self.set_lines(self.ph('body', 14), crumb)
        for l in lead:
            if text_w(l, 18) > 12.0:
                WARN.append('s%02d 한 줄 설명이 길다(%.1f"): %s' % (self.no, text_w(l, 18), l))

    # ---------- 그리기 ----------
    def _add(self, xml):
        self.tree.append(etree.fromstring(xml))

    def _id(self):
        self.nid += 1
        return self.nid

    def box(self, x, y, w, h, fill=None, line=None, text=None, sz=11, bold=False, col=TXT, al='ctr',
            anchor='ctr', r=0.06, ins=(0.07, 0.03), lw=0.75, geom=None, sp=100, name='Box'):
        paras = norm_paras(text, sz, bold, col)
        i = self._id()
        if geom is None:
            geom = 'roundRect' if r else 'rect'
        av = ''
        if geom == 'roundRect':
            av = '<a:gd name="adj" fmla="val %d"/>' % min(50000, int(r / max(0.01, min(w, h)) * 100000))
        fx = '<a:solidFill><a:srgbClr val="%s"/></a:solidFill>' % fill if fill else '<a:noFill/>'
        lx = ('<a:ln w="%d"><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:ln>' % (int(lw * 12700), line)) if line else '<a:ln><a:noFill/></a:ln>'
        body = []
        for runs in paras:
            rx = ''.join(
                '<a:r><a:rPr lang="ko-KR" altLang="en-US" sz="%d" b="%d"><a:solidFill><a:srgbClr val="%s"/></a:solidFill>'
                '<a:latin typeface="%s"/><a:ea typeface="%s"/><a:cs typeface="%s"/></a:rPr><a:t>%s</a:t></a:r>' % (
                    int(s * 100), 1 if b else 0, c, FONT, FONT, FONT, escape(t)) for t, s, b, c in runs)
            body.append('<a:p><a:pPr algn="%s"><a:lnSpc><a:spcPct val="%d"/></a:lnSpc></a:pPr>%s</a:p>' % (al, sp * 1000, rx))
        if not body:
            body = ['<a:p><a:pPr algn="ctr"/><a:endParaRPr lang="ko-KR" altLang="en-US"/></a:p>']
        self._add(
            '<p:sp xmlns:a="%s" xmlns:p="%s"><p:nvSpPr><p:cNvPr id="%d" name="%s %d"/><p:cNvSpPr%s/><p:nvPr/></p:nvSpPr>'
            '<p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="%s"><a:avLst>%s</a:avLst></a:prstGeom>%s%s</p:spPr>'
            '<p:txBody><a:bodyPr wrap="square" lIns="%d" tIns="%d" rIns="%d" bIns="%d" rtlCol="0" anchor="%s"><a:noAutofit/></a:bodyPr><a:lstStyle/>%s</p:txBody></p:sp>' % (
                A, P, i, name, i, ' txBox="1"' if not fill and not line else '', emu(x), emu(y), emu(w), emu(h), geom, av, fx, lx,
                emu(ins[0]), emu(ins[1]), emu(ins[0]), emu(ins[1]), anchor, ''.join(body)))
        # 넘침 확인(어림)
        if paras:
            avail_w = w - 2 * ins[0] - (0.25 if geom in ('chevron', 'homePlate') else 0)
            need = 0.0
            for runs in paras:
                pw = sum(text_w(t, s, b) for t, s, b, c in runs)
                ms = max(s for t, s, b, c in runs)
                n = max(1, int(pw / max(0.05, avail_w) + 0.999))
                need += n * ms * 1.22 * sp / 100.0 / 72.0
            if need > h - 2 * ins[1] + 0.02:
                WARN.append('s%02d 넘침 %.2f > %.2f : %s' % (self.no, need, h - 2 * ins[1], ' / '.join(''.join(r[0] for r in p) for p in paras)[:60]))

    def txt(self, x, y, w, h, text, sz=11, bold=False, col=TXT, al='l', anchor='ctr', sp=100, ins=(0.02, 0.01)):
        self.box(x, y, w, h, None, None, text, sz, bold, col, al, anchor, r=0, ins=ins, sp=sp, name='Text')

    def item(self, x, y, w, h, title, sub=None, style='white', al='ctr', tsz=11, ssz=10, tb=True, anchor='ctr', ins=(0.07, 0.03)):
        f, l, c = ST[style]
        paras = [(title, tsz, tb, c)]
        if sub:
            for s in (sub if isinstance(sub, list) else [sub]):
                paras.append((s, ssz, False, SUB))
        self.box(x, y, w, h, f, l, paras, al=al, anchor=anchor, ins=ins)

    def hdr(self, x, y, w, h, text, fill=NAVY, sz=11, al='l', sub=None):
        paras = [(text, sz, True, 'FFFFFF')]
        if sub:
            paras.append((sub, 10, False, 'DCE6F2'))
        self.box(x, y, w, h, fill, None, paras, al=al, ins=(0.12, 0.03))

    def panel(self, x, y, w, h):
        self.box(x, y, w, h, 'F5F7FA', 'D5DCE6', r=0)

    def arrow(self, x1, y1, x2, y2, col=NAVY, both=False, lw=1.3):
        i = self._id()
        fl = (' flipH="1"' if x2 < x1 else '') + (' flipV="1"' if y2 < y1 else '')
        self._add(
            '<p:cxnSp xmlns:a="%s" xmlns:p="%s"><p:nvCxnSpPr><p:cNvPr id="%d" name="Arrow %d"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr>'
            '<p:spPr><a:xfrm%s><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="straightConnector1"><a:avLst/></a:prstGeom>'
            '<a:ln w="%d"><a:solidFill><a:srgbClr val="%s"/></a:solidFill>%s<a:tailEnd type="triangle" w="med" len="med"/></a:ln></p:spPr></p:cxnSp>' % (
                A, P, i, i, fl, emu(min(x1, x2)), emu(min(y1, y2)), emu(abs(x2 - x1)), emu(abs(y2 - y1)), int(lw * 12700), col,
                '<a:headEnd type="triangle" w="med" len="med"/>' if both else ''))

    def pill(self, x, y, w, h, text, style='green'):
        f, l, c = ST[style]
        self.box(x, y, w, h, f, l, text, sz=9, bold=True, col=c, r=h / 2, ins=(0.02, 0.0))

    def note(self, x, y, w, h, label, lines, style='orange', sz=11):
        f, l, c = ST[style]
        paras = []
        if label:
            paras.append((label, sz, True, c))
        for t in (lines if isinstance(lines, list) else [lines]):
            paras.append(t if isinstance(t, list) else (t, sz, False, TXT))
        self.box(x, y, w, h, f, l, paras, al='l', ins=(0.18, 0.05), sp=108)

    def navy_bar(self, x, y, w, h, lines, sz=11):
        self.box(x, y, w, h, NAVY2, None, [(t, sz, i == 0, 'FFFFFF' if i == 0 else 'DCE6F2') for i, t in enumerate(lines)], al='l', ins=(0.2, 0.05), sp=108)

    def table(self, x, y, colw, head, rows, rh=0.44, hh=0.36, sz=10.5, first_bold=True, head_fill=NAVY2):
        w = sum(colw)
        self.box(x, y, w, hh, head_fill, None, r=0)
        cx = x
        for cw, t in zip(colw, head):
            self.txt(cx + 0.12, y, cw - 0.2, hh, t, sz=11, bold=True, col='FFFFFF', al='l')
            cx += cw
        cy = y + hh
        for ri, row in enumerate(rows):
            self.box(x, cy, w, rh, 'FFFFFF' if ri % 2 == 0 else 'F5F7FA', 'D5DCE6', r=0)
            cx = x
            for ci, (cw, cell) in enumerate(zip(colw, row)):
                if isinstance(cell, dict):
                    self.pill(cx + 0.12, cy + (rh - 0.24) / 2, 0.62, 0.24, cell['pill'], cell.get('style', 'green'))
                else:
                    b = first_bold and ci == 0
                    self.txt(cx + 0.12, cy, cw - 0.2, rh, cell, sz=sz + (0.5 if b else 0), bold=b, col='1F2937' if b else TXT, al='l')
                cx += cw
            cy += rh
        return cy

    def flow(self, x, y, w, h, steps, gap=0.2, style='blue', tsz=11, ssz=9.5):
        """가로로 이어지는 상자들. steps = (제목, 설명[, 색 묶음])"""
        n = len(steps)
        bw = (w - gap * (n - 1)) / n
        for i, st in enumerate(steps):
            t, s = st[0], st[1]
            sty = st[2] if len(st) > 2 else style
            bx = x + i * (bw + gap)
            self.item(bx, y, bw, h, t, s.split('\n') if s else None, sty, tsz=tsz, ssz=ssz, ins=(0.04, 0.03))
            if i:
                self.arrow(bx - gap + 0.02, y + h / 2, bx - 0.02, y + h / 2)
        return bw


def cols(n, gap, x0=0.61, w=12.11):
    cw = (w - gap * (n - 1)) / n
    return [(x0 + i * (cw + gap), cw) for i in range(n)]
