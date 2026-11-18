# -*- coding: utf-8 -*-
# PPT를 HTML로 옮겨 본다(도형 = div, 글은 브라우저가 실제로 줄바꿈). PowerPoint가 없는 PC에서 넘침을 눈으로 보려는 것.
# 쓰는 법: python -I -X utf8 preview.py <pptx> <출력 폴더>
import sys, os, html
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from lxml import etree

NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
prs = Presentation(src)
PX = 96 / 914400.0


def col(node):
    if node is None:
        return None
    s = node.find('a:srgbClr', NS)
    return '#' + s.get('val') if s is not None else None


def geom_of(el, sh):
    """자리표시자는 레이아웃에서 위치를 물려받는다."""
    try:
        return sh.left, sh.top, sh.width, sh.height
    except Exception:
        return None


def walk(shapes):
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            for r in walk(sh.shapes):
                yield r
        else:
            yield sh


for i, slide in enumerate(prs.slides, 1):
    bg = '#fff'
    lay = slide.slide_layout.name
    if lay in ('2_agenda',):
        bg = '#16406A'
    parts = ['<!doctype html><meta charset="utf-8"><body style="margin:0;background:%s"><div style="position:relative;width:1280px;height:720px;overflow:hidden;font-family:Pretendard,\'Malgun Gothic\',sans-serif">' % bg]
    for sh in walk(slide.shapes):
        el = sh._element
        tag = etree.QName(el).localname
        g = geom_of(el, sh)
        if g is None or g[0] is None:
            continue
        x, y, w, h = [v * PX for v in g]
        spPr = el.find('p:spPr', NS)
        if tag == 'cxnSp':
            xf = spPr.find('a:xfrm', NS)
            x1, y1, x2, y2 = x, y, x + w, y + h
            if xf.get('flipH') == '1':
                x1, x2 = x2, x1
            if xf.get('flipV') == '1':
                y1, y2 = y2, y1
            c = col(spPr.find('a:ln/a:solidFill', NS)) or '#888'
            both = spPr.find('a:ln/a:headEnd', NS) is not None
            parts.append('<svg style="position:absolute;left:0;top:0;overflow:visible" width="1280" height="720"><line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6"/>'
                         '<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>%s</svg>' % (x1, y1, x2, y2, c, x2, y2, c, '<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (x1, y1, c) if both else ''))
            continue
        if tag == 'pic':
            parts.append('<div style="position:absolute;left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx;background:#ddd;outline:1px dashed #c0c"></div>' % (x, y, w, h))
            continue
        if tag != 'sp':
            continue
        fill = col(spPr.find('a:solidFill', NS)) if spPr is not None else None
        line = col(spPr.find('a:ln/a:solidFill', NS)) if spPr is not None else None
        pg = spPr.find('a:prstGeom', NS) if spPr is not None else None
        prst = pg.get('prst') if pg is not None else 'rect'
        radius = 0
        if prst == 'roundRect':
            gd = pg.find('a:avLst/a:gd', NS)
            radius = (int(gd.get('fmla').split()[1]) if gd is not None else 16667) / 100000.0 * min(w, h)
        if prst == 'ellipse':
            radius = min(w, h) / 2
        bp = el.find('p:txBody/a:bodyPr', NS)
        ph = el.find('.//p:nvPr/p:ph', NS)
        li = int(bp.get('lIns', 91440)) * PX if bp is not None else 9.6
        ti = int(bp.get('tIns', 45720)) * PX if bp is not None else 4.8
        anchor = (bp.get('anchor') if bp is not None else None) or ('t' if ph is not None else 't')
        jc = {'ctr': 'center', 'b': 'flex-end', 't': 'flex-start'}[anchor]
        clip = ''
        if prst in ('chevron', 'homePlate'):
            clip = 'clip-path:polygon(%s 88%% 0,100%% 50%%,88%% 100%%,0 100%%%s);' % ('0 0,', ',12% 50%' if prst == 'chevron' else '')
        style = 'position:absolute;left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx;box-sizing:border-box;display:flex;flex-direction:column;justify-content:%s;padding:%.1fpx %.1fpx;border-radius:%.1fpx;%s%s%s' % (
            x, y, w, h, jc, ti, li, radius, 'background:%s;' % fill if fill else '', 'border:1px solid %s;' % line if line else '', clip)
        inner = []
        for p in el.findall('p:txBody/a:p', NS):
            pPr = p.find('a:pPr', NS)
            al = {'ctr': 'center', 'r': 'right', 'l': 'left'}.get(pPr.get('algn') if pPr is not None else None, 'left')
            sp = pPr.find('a:lnSpc/a:spcPct', NS) if pPr is not None else None
            lh = 1.2 * (int(sp.get('val')) / 100000.0 if sp is not None else 1.0)
            runs = []
            dsz = 18 if ph is not None and (ph.get('idx') == '13') else (20 if ph is not None and ph.get('type') == 'title' else 12)
            for ch in p:
                t = etree.QName(ch).localname
                if t == 'br':
                    runs.append('<br>')
                elif t in ('r', 'fld'):
                    rp = ch.find('a:rPr', NS)
                    sz = int(rp.get('sz')) / 100.0 if rp is not None and rp.get('sz') else dsz
                    c = col(rp.find('a:solidFill', NS)) if rp is not None else None
                    b = rp is not None and rp.get('b') == '1'
                    runs.append('<span style="font-size:%.2fpx;%s%s">%s</span>' % (sz * 96 / 72, 'color:%s;' % c if c else '', 'font-weight:700;' if b else '', html.escape(ch.find('a:t', NS).text or '')))
            if runs:
                inner.append('<div style="text-align:%s;line-height:%.2f;">%s</div>' % (al, lh, ''.join(runs)))
        parts.append('<div style="%s">%s</div>' % (style, ''.join(inner)))
    parts.append('</div>')
    open(os.path.join(out, 'p%02d.html' % i), 'w', encoding='utf-8').write('\n'.join(parts))
print('ok', len(prs.slides))
