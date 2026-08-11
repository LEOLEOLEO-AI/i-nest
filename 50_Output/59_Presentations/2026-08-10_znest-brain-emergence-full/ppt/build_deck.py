#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the full academic iNEST deck from the original 146-page outline."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = Path(r"C:\Users\LEO\AppData\Local\Temp\biji_note.txt")
TEMPLATE = Path(r"C:\Users\LEO\.codex\skills\guizang-ppt-skill\assets\template-swiss.html")
OUT = ROOT / "index.html"
SLIDES_OUT = ROOT / "slides_block.html"
IMAGES = ROOT / "images"
MANIFEST = IMAGES / "manifest.json"

CHAPTERS = [
    (1, 8, "序幕", "问题导入"),
    (9, 18, "第一幕", "第一性原理"),
    (19, 30, "第二幕", "互连比节点更重要"),
    (31, 42, "第三幕", "从加性到乘性"),
    (43, 56, "第四幕", "度量"),
    (57, 68, "第五幕", "智能的定义与六级量表"),
    (69, 78, "第六幕", "动力学"),
    (79, 90, "第七幕", "自组织"),
    (91, 98, "第八幕", "控制"),
    (99, 108, "第九幕", "范式"),
    (109, 120, "第十幕", "智涌脑"),
    (121, 138, "第十一幕", "协同作战"),
    (139, 146, "第十二幕", "产业与生态"),
]

TABLE_SHAPE = {
    40: (2, 3),
    61: (3, 3),
    107: (2, 2),
    121: (3, 3),
    127: (3, 3),
    133: (4, 4),
    134: (4, 4),
    135: (3, 3),
}

LAYOUTS = ["S03", "S04", "S05", "S08", "S09", "S13", "S15", "S16", "S18", "S19", "S21"]
ANIMS = [
    "grid-reveal",
    "statement",
    "stack-build",
    "duo-mirror",
    "timeline-walk",
    "matrix-fill",
    "field-notes",
    "system-diagram",
    "why-now",
    "four-cards",
    "tech-spec",
    "bar-grow",
]
CHAPTER_OPENERS = {9, 19, 31, 43, 57, 69, 79, 91, 99, 109}
TABLE_PAGES = set(TABLE_SHAPE) | {137, 138, 145}


def chapter_of(num):
    for start, end, short, title in CHAPTERS:
        if start <= num <= end:
            return f"{short} · {title}"
    return "附录"


def clean_cell(value):
    return value.strip().strip("。")

def parse():
    lines = SRC.read_text(encoding="utf-8").splitlines()
    pages = []
    appendix = []
    manual = []
    cur = None
    mode = "page"
    table_mode = False
    table_cells = []
    detail_mode = False
    detail_lines = []

    def flush_table(page):
        shape = TABLE_SHAPE.get(page["num"])
        if not shape or not table_cells:
            return
        header_count, row_count = shape
        headers = [clean_cell(x) for x in table_cells[:header_count]]
        rest = table_cells[header_count:]
        rows = []
        for i in range(0, len(rest) - len(rest) % row_count, row_count):
            rows.append([clean_cell(x) for x in rest[i:i + row_count]])
        page["table_headers"] = headers
        page["table_rows"] = rows

    def classify(page, text):
        nonlocal table_mode, table_cells, detail_mode, detail_lines
        if text.startswith("主标题："):
            page["blocks"].append(("title", text[len("主标题："):]))
            return
        if text.startswith("副标题："):
            page["blocks"].append(("subtitle", text[len("副标题："):]))
            return
        m = re.match(r"^主体（表格[^）]*）[：:](.*)$", text)
        if m:
            rest = m.group(1).strip()
            if rest:
                cells = [clean_cell(x) for x in rest.split("\uFF5C") if x.strip()]
                page["table_inline"] = cells
            else:
                table_mode = True
                table_cells = []
            return
        m = re.match(r"^主体（表格式[^）]*）[：:](.*)$", text)
        if m:
            table_mode = True
            table_cells = []
            return
        m = re.match(r"^主体（([^）]*)）[：:](.*)$", text)
        if m:
            page["blocks"].append(("body", m.group(2).strip()))
            return
        if text.startswith("主体："):
            page["blocks"].append(("body", text[len("主体："):]))
            return
        if text.startswith("图示："):
            page["figure_text"] = text[len("图示："):]
            return
        if text.startswith("备注：") or text.startswith("備注："):
            page["blocks"].append(("note", text.split("：", 1)[1].strip()))
            return
        if text.startswith("依据："):
            page["blocks"].append(("evidence", text.split("：", 1)[1].strip()))
            return
        if text.startswith("公式："):
            body = text.split("：", 1)[1].strip()
            if "。备注：" in body:
                formula, note = body.split("。备注：", 1)
                page["blocks"].append(("formula", formula.strip()))
                page["blocks"].append(("note", note.strip()))
            else:
                page["blocks"].append(("formula", body))
            return
        if text.startswith("$$"):
            page["blocks"].append(("formula", text))
            return
        m = re.match(r"^(符号说明（[^）]*）|说明)[：:](.*)$", text)
        if m:
            page["blocks"].append(("symbols", m.group(2).strip()))
            return
        if text.startswith("关键任务："):
            page["blocks"].append(("tasks", text.split("：", 1)[1].strip()))
            return
        if text.startswith("工程实现："):
            page["blocks"].append(("engineer", text.split("：", 1)[1].strip()))
            return
        if text.startswith("四项含义："):
            page["blocks"].append(("terms", text.split("：", 1)[1].strip()))
            return
        if text.startswith("层次结构声明："):
            page["blocks"].append(("scope", text.split("：", 1)[1].strip()))
            return
        if text.startswith("分工细化："):
            detail_mode = True
            detail_lines = []
            return
        if detail_mode:
            if text.startswith("　　") or (text and not re.match(r"^(拟报|牵头|备注|依据|图示|主体|关键|工程|层次|四项)", text)):
                detail_lines.append(text.strip())
                return
            else:
                if detail_lines:
                    page["blocks"].append(("details", list(detail_lines)))
                detail_mode = False
        if text.startswith("拟报题目：") or text.startswith("拟报方向："):
            page["blocks"].append(("proposal", text.split("：", 1)[1].strip()))
            return
        if text.startswith("牵头："):
            page["blocks"].append(("leader", text.split("：", 1)[1].strip()))
            return
        if text.startswith("（全篇"):
            page["table_note"] = text
            return
        if text.startswith("一、") or text.startswith("二、") or text.startswith("三、"):
            return
        page["blocks"].append(("extra", text))

    for raw in lines:
        line = raw.strip()
        if line.startswith("附录（"):
            mode = "appendix"
            appendix.append(line)
            continue
        if line.startswith("三点提醒"):
            mode = "manual"
            manual.append(line)
            continue
        if mode == "appendix":
            appendix.append(line)
            continue
        if mode == "manual":
            manual.append(line)
            continue
        m = re.match(r"^P(\d+)\uFF5C(.+)$", line)
        if m:
            if cur is not None:
                if table_mode:
                    flush_table(cur)
                if detail_mode and detail_lines:
                    cur["blocks"].append(("details", list(detail_lines)))
                pages.append(cur)
            cur = {"num": int(m.group(1)), "title": m.group(2), "blocks": [], "chapter": chapter_of(int(m.group(1)))}
            table_mode = False
            table_cells = []
            detail_mode = False
            detail_lines = []
            continue
        if cur is None:
            continue
        if not line or line == "\t":
            continue
        if table_mode:
            if re.match(r"^(备注|依据|图示|主体|关键任务|工程实现|四项含义|层次结构声明|分工细化|拟报题目|拟报方向|牵头)[：:]", line) or line.startswith("（全篇"):
                flush_table(cur)
                table_mode = False
                classify(cur, line)
            else:
                table_cells.append(line)
            continue
        classify(cur, line)

    if cur is not None:
        if table_mode:
            flush_table(cur)
        if detail_mode and detail_lines:
            cur["blocks"].append(("details", list(detail_lines)))
        pages.append(cur)

    # Cover page fields live in one line.
    cover = pages[0]
    raw_cover = "".join(v for k, v in cover["blocks"] if k in ("title", "subtitle", "figure", "body"))
    if not raw_cover:
        raw_cover = " ".join(cover["blocks"][i][1] for i in range(len(cover["blocks"])))
    mt = re.search(r"主标题：(.+?)副标题：", raw_cover)
    ms = re.search(r"副标题：(.+?)图示：", raw_cover)
    mf = re.search(r"图示：(.+)$", raw_cover)
    if mt:
        cover["blocks"] = [("title", mt.group(1).strip())]
    if ms:
        cover["blocks"].append(("subtitle", ms.group(1).strip()))
    if mf:
        cover["figure_text"] = mf.group(1).strip()

    appendix_text = "".join(appendix)
    manual_text = "".join(manual)
    return pages, appendix_text, manual_text


def esc(value):
    return html.escape(value, quote=False)


def math_html(raw):
    s = esc(raw.strip())
    s = re.sub(r"^\$\$|\$\$$", "", s)
    def ub(m):
        inner, label = m.group(1), m.group(2)
        return f'<span class="ub">{inner}<span class="ub-lb">{label}</span></span>'
    s = re.sub(r"\\underbrace\{([^{}]+)\}\{\\text\{([^{}]+)\}\}", ub, s)
    s = s.replace("\\cdot", "·")
    s = s.replace("\\partial", "∂")
    s = s.replace("\\sum", "Σ")
    s = s.replace("\\alpha", "α")
    s = s.replace("\\gamma", "γ")
    s = s.replace("\\tau", "τ")
    s = s.replace("\\eta", "η")
    s = s.replace("\\lambda", "λ")
    s = s.replace("\\Gamma", "Γ")
    s = s.replace("\\mathcal{M}", "M")
    s = s.replace("\\mathcal{T}", "𝒯")
    s = s.replace("\\Pi", "Π")
    s = s.replace("\\max", "max")
    s = s.replace("\\left", "")
    s = s.replace("\\right", "")
    s = s.replace("\\quad", " ")
    s = s.replace("\\text", "")
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"_([A-Za-z0-9]+)", r"<sub>\1</sub>", s)
    s = re.sub(r"\^([A-Za-z0-9·αΓ]+)", r"<sup>\1</sup>", s)
    return s


def render_table(page):
    headers = page.get("table_headers", [])
    rows = page.get("table_rows", [])
    inline = page.get("table_inline", [])
    if not headers and not rows and inline:
        cells = "".join(f'<td>{esc(c)}</td>' for c in inline)
        return f'<div class="ac-table-wrap"><table class="ac-table"><tr>{cells}</tr></table></div>'
    if not headers:
        return ""
    th = ""
    if page["num"] == 40:
        th = "<th></th>"
    th += "".join(f"<th>{esc(h)}</th>" for h in headers)
    trs = []
    for row in rows:
        tds = "".join(f"<td>{esc(c)}</td>" for c in row)
        trs.append(f"<tr>{tds}</tr>")
    note = ""
    if page.get("table_note"):
        note = f'<div class="ac-table-note">{esc(page["table_note"])}</div>'
    return f'<div class="ac-table-wrap"><table class="ac-table"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table>{note}</div>'


def render_blocks(page):
    parts = []
    details = []
    for kind, value in page.get("blocks", []):
        if kind in ("title", "subtitle", "figure"):
            continue
        if kind == "body":
            parts.append(f'<div class="ac-body">{esc(value)}</div>')
        elif kind == "note":
            parts.append(f'<div class="ac-note"><span class="tag">备注</span>{esc(value)}</div>')
        elif kind == "evidence":
            parts.append(f'<div class="ac-ref"><span class="tag">[引用] 依据</span>{esc(value)}</div>')
        elif kind == "formula":
            parts.append(f'<div class="ac-formula">{math_html(value)}</div>')
        elif kind == "symbols":
            parts.append(f'<div class="ac-symbols"><span class="tag">符号说明</span>{esc(value)}</div>')
        elif kind == "terms":
            parts.append(f'<div class="ac-note"><span class="tag">四项含义</span>{esc(value)}</div>')
        elif kind == "tasks":
            parts.append(f'<div class="ac-note"><span class="tag">关键任务</span>{esc(value)}</div>')
        elif kind == "engineer":
            parts.append(f'<div class="ac-ref"><span class="tag">工程实现</span>{esc(value)}</div>')
        elif kind == "scope":
            parts.append(f'<div class="ac-note"><span class="tag">层次结构声明</span>{esc(value)}</div>')
        elif kind == "proposal":
            parts.append(f'<div class="ac-note"><span class="tag">拟报题目 / 方向</span>{esc(value)}</div>')
        elif kind == "leader":
            parts.append(f'<div class="ac-ref"><span class="tag">牵头</span>{esc(value)}</div>')
        elif kind == "details":
            details = value
        elif kind == "extra":
            parts.append(f'<div class="ac-body">{esc(value)}</div>')
    if details:
        cards = []
        for d in details:
            name = d.split("——", 1)[0].strip()
            body = d.split("——", 1)[1].strip() if "——" in d else d
            cards.append(f'<div class="ac-detail-card"><div class="ac-detail-name">{esc(name)}</div><div class="ac-detail-body">{esc(body)}</div></div>')
        parts.append(f'<div class="ac-detail-grid">{"".join(cards)}</div>')
    table_html = render_table(page)
    if table_html:
        parts.append(table_html)
    return "\n".join(parts)


def diagram_pattern(page):
    fig = page.get("figure_text", "")
    text = " ".join(v for k, v in page.get("blocks", []) if k in ("body", "terms", "tasks"))
    if "雷达" in fig:
        return "radar"
    if "柱" in fig or "对比" in fig or "瀑布" in fig:
        return "bars"
    if "曲线" in fig or "双曲线" in fig or "幂律" in fig or "阶梯" in fig or "台阶" in fig:
        return "curve" if "曲线" in fig or "幂律" in fig else "ladder"
    if "数轴" in fig or "标记点" in fig:
        return "scale"
    if "树状" in fig:
        return "tree"
    if "泳道" in fig or "甘特" in fig:
        return "gantt"
    if "环" in fig or "回路" in fig or "闭环" in fig or "嵌套" in fig:
        return "loop"
    if "网络" in fig or "拓扑" in fig or "连接" in fig or "节点" in fig or "晶格" in fig:
        return "network"
    if "仪表" in fig:
        return "gauges"
    if "时间轴" in fig:
        return "timeline"
    if "矩阵" in fig or "卡片" in fig or "扇形" in fig:
        return "matrix"
    if "框" in fig or "墙" in fig:
        return "pipeline"
    return ["network", "bars", "matrix", "rings", "ladder", "scale", "curve", "pipeline"][page["num"] % 8]


def diagram_html(pattern):
    if pattern == "bars":
        return (
            '<div class="dg dg-bars">'
            '<div class="bar"><i style="width:16%"></i></div>'
            '<div class="bar"><i style="width:34%"></i></div>'
            '<div class="bar"><i style="width:58%"></i></div>'
            '<div class="bar"><i style="width:86%"></i></div>'
            '</div>'
        )
    if pattern == "curve":
        return (
            '<div class="dg dg-curve">'
            '<svg viewBox="0 0 300 150" preserveAspectRatio="none" aria-hidden="true">'
            '<path class="c-a" d="M10,130 C90,120 130,95 290,62" fill="none" stroke-width="4"/>'
            '<path class="c-b" d="M10,130 C80,70 150,40 290,8" fill="none" stroke-width="4"/>'
            '</svg></div>'
        )
    if pattern == "network":
        return (
            '<div class="dg dg-network">'
            '<span class="n n1"></span><span class="n n2"></span><span class="n n3"></span>'
            '<span class="n n4"></span><span class="n c"></span><span class="n n5"></span>'
            '<span class="n n6"></span><span class="n n7"></span><span class="n n8"></span>'
            '</div>'
        )
    if pattern == "rings":
        return '<div class="dg dg-rings"><span class="r r1"></span><span class="r r2"></span><span class="r r3"></span><span class="r core"></span></div>'
    if pattern == "ladder":
        return '<div class="dg dg-ladder"><span class="step s1"></span><span class="step s2"></span><span class="step s3"></span><span class="step s4"></span></div>'
    if pattern == "scale":
        return '<div class="dg dg-scale"><span class="tick t1"></span><span class="tick t2"></span><span class="tick t3"></span><span class="tick t4"></span><span class="tick t5"></span><span class="tick t6"></span><span class="needle"></span></div>'
    if pattern == "matrix":
        return '<div class="dg dg-matrix"><span class="cell"></span><span class="cell hot"></span><span class="cell"></span><span class="cell"></span><span class="cell"></span><span class="cell hot"></span></div>'
    if pattern == "pipeline":
        return '<div class="dg dg-pipeline"><span class="node"></span><span class="arrow"></span><span class="node"></span><span class="arrow"></span><span class="node"></span><span class="arrow"></span><span class="node hot"></span></div>'
    if pattern == "loop":
        return '<div class="dg dg-loop"><span class="ring"></span><span class="ring inner"></span><span class="core"></span><span class="arrow a1"></span><span class="arrow a2"></span></div>'
    if pattern == "radar":
        return (
            '<div class="dg dg-radar">'
            '<svg viewBox="0 0 200 150" preserveAspectRatio="none" aria-hidden="true">'
            '<polygon points="100,15 170,60 150,130 50,130 30,60" fill="rgba(18,59,125,.10)" stroke="#123b7d" stroke-width="3"/>'
            '<polygon points="100,15 170,60 150,130 50,130 30,60" fill="none" stroke="#9aa7b8" stroke-width="1" stroke-dasharray="4 5" transform="scale(.72) translate(39,19)"/>'
            '</svg></div>'
        )
    if pattern == "gauges":
        return '<div class="dg dg-gauges"><span class="gauge"></span><span class="gauge hot"></span><span class="gauge"></span></div>'
    if pattern == "timeline":
        return '<div class="dg dg-timeline"><span class="tl t1"></span><span class="tl t2"></span><span class="tl t3"></span><span class="tl t4"></span><span class="tl t5"></span><span class="tl t6"></span></div>'
    if pattern == "tree":
        return '<div class="dg dg-tree"><span class="root"></span><span class="branch b1"></span><span class="branch b2"></span><span class="branch b3"></span><span class="branch b4"></span></div>'
    if pattern == "gantt":
        return '<div class="dg dg-gantt"><span class="g-row"><i style="width:30%"></i></span><span class="g-row"><i style="width:55%"></i></span><span class="g-row"><i style="width:78%"></i></span></div>'
    return '<div class="dg dg-rings"><span class="r r1"></span><span class="r r2"></span><span class="r r3"></span></div>'


def cover_bg(num, manifest):
    item = manifest.get(str(num))
    if not item:
        return ""
    local = IMAGES / item["local"]
    if not local.exists():
        return ""
    src = "images/" + item["local"].replace("\\", "/")
    return f'<img class="ac-cover-bg" src="{src}" alt="" data-image-slot="s22-hero-21x9">'

def render_visual(page, manifest):
    fig = page.get("figure_text", "")
    cap = f'<div class="ac-fig-cap">图示 · {esc(fig)}</div>' if fig else ""
    item = manifest.get(str(page["num"]))
    if item:
        local = IMAGES / item["local"]
        if local.exists():
            title = item["title"]
            page_url = item["page_url"]
            src = "images/" + item["local"].replace("\\", "/")
            return (
                f'<div class="ac-visual">'
                f'<img src="{src}" alt="{esc(title)}" data-image-slot="s16-brief-21x9">'
                f'<div class="ac-img-cap"><span>图源</span><a href="{esc(page_url)}" target="_blank" rel="noopener">{esc(title)}</a></div>'
                f'{cap}</div>'
            )
    pattern = diagram_pattern(page)
    return f'<div class="ac-visual"><div class="ac-diagram">{diagram_html(pattern)}</div>{cap}</div>'


def opener_title(title):
    m = re.match(r"^幕首[：:]?主体（[^）]*）[—–-]+(.+)$", title)
    if m:
        return m.group(1).strip()
    m = re.match(r"^幕首[：:]?(.+)$", title)
    if m:
        return m.group(1).strip()
    return title


def render_slide(page, manifest, idx):
    num = page["num"]
    total = 148
    if num == 1:
        layout = "SWISS-COVER-ASCII"
        anim = "hero"
    elif num == 146:
        layout = "SWISS-CLOSING-ASCII"
        anim = "split-statement"
    elif num in CHAPTER_OPENERS:
        layout = "S09"
        anim = "statement"
    elif num in TABLE_PAGES:
        layout = "S04"
        anim = "matrix-fill"
    else:
        layout = LAYOUTS[idx % len(LAYOUTS)]
        anim = ANIMS[idx % len(ANIMS)]

    chrome = (
        f'<div class="ac-chrome"><span class="chapter">{esc(page["chapter"])}</span>'
        f'<span class="page">P{num} / 146</span></div>'
    )
    title = opener_title(page["title"]) if num in CHAPTER_OPENERS else page["title"]
    title_html = f'<h2 class="ac-title">{esc(title)}</h2>'
    blocks = render_blocks(page)
    table_html = render_table(page)
    if table_html:
        blocks = blocks.replace(table_html, "") if table_html in blocks else blocks
        blocks += table_html
    main = f'<div class="ac-main">{blocks}</div>'
    visual = render_visual(page, manifest)

    if num == 1:
        body = (
            '<section class="slide accent academic-cover" data-layout="SWISS-COVER-ASCII" data-animate="hero">'
            '<div class="canvas-card">'
            '<canvas class="ascii-bg" aria-hidden="true"></canvas>'
            + cover_bg(1, manifest) +
            '<div class="ac-cover-inner">'
            f'<div class="ac-cover-chrome">{esc(page["chapter"])}</div>'
            f'<h1 class="ac-cover-title">智涌脑 · iNEST<br/><span>网络时空协同复杂度涌现智能</span></h1>'
            '<div class="ac-cover-sub">从第一性原理到工程实现的完整推演：理论 — 技术 — 工程 — 产业闭环</div>'
            '<div class="ac-cover-foot">智涌脑 Z-Brain Ⅰ / Ⅱ / Ⅲ · iNEST 全景报告</div>'
            '</div></div></section>'
        )
    elif num == 146:
        body = (
            '<section class="slide academic-cover academic-closing" data-layout="SWISS-CLOSING-ASCII" data-animate="split-statement">'
            '<div class="canvas-card">'
            + cover_bg(146, manifest) +
            '<div class="ac-cover-inner">'
            f'<div class="ac-cover-chrome">{esc(page["chapter"])} · 收官</div>'
            '<h1 class="ac-cover-title">智能不是算出来的，<br/><span>是长出来的</span></h1>'
            '<div class="ac-cover-sub">我们要做的，是造一片能长出智能的土壤。</div>'
            '<div class="ac-cover-foot">P146 · 晶圆上生长的神经网络，中心一点临界辉光</div>'
            '</div></div></section>'
        )
    elif num in CHAPTER_OPENERS:
        body = (
            f'<section class="slide academic-cover" data-layout="S09" data-animate="statement">'
            f'<div class="canvas-card">' + cover_bg(num, manifest) + '<div class="ac-cover-inner">'
            f'<div class="ac-cover-chrome">{esc(page["chapter"])} · 幕首</div>'
            f'<h1 class="ac-cover-title">{esc(title)}</h1>'
            f'<div class="ac-cover-foot">P{num} / 146 · 保留原提纲每页表述</div>'
            '</div></div></section>'
        )
    else:
        body = (
            f'<section class="slide academic" data-layout="{layout}" data-animate="{anim}">'
            f'<div class="canvas-card">{chrome}{title_html}<div class="ac-grid">{main}{visual}</div></div></section>'
        )
    return body


def render_appendix_slide(appendix_text):
    items = [x.strip() for x in re.split(r"\uFF5C", appendix_text) if x.strip() and not x.startswith("附录")]
    cards = "".join(f'<div class="appendix-item">{esc(x)}</div>' for x in items)
    return (
        '<section class="slide academic" data-layout="S15" data-animate="matrix-fill">'
        '<div class="canvas-card">'
        '<div class="ac-chrome"><span class="chapter">附录</span><span class="page">A1–A10</span></div>'
        '<h2 class="ac-title">附录 · 十项支撑材料</h2>'
        f'<div class="ac-grid full"><div class="ac-appendix-grid">{cards}</div></div>'
        '</div></section>'
    )


def render_manual_slide(manual_text):
    paras = [x.strip() for x in manual_text.splitlines() if x.strip()]
    cards = []
    for p in paras[1:]:
        title = p.split("。", 1)[0]
        body = p.split("。", 1)[1] if "。" in p else ""
        cards.append(f'<div class="manual-card"><div class="manual-title">{esc(title)}。</div><div class="manual-body">{esc(body)}</div></div>')
    return (
        '<section class="slide academic" data-layout="S16" data-animate="field-notes">'
        '<div class="canvas-card">'
        '<div class="ac-chrome"><span class="chapter">讲者手册</span><span class="page">SPEAKER</span></div>'
        '<h2 class="ac-title">三点提醒 · 讲者手册首页</h2>'
        f'<div class="ac-grid full"><div class="ac-manual-grid">{"".join(cards)}</div></div>'
        '</div></section>'
    )


def build():
    pages, appendix_text, manual_text = parse()
    manifest = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8")).get("items", {})
    slides = []
    for idx, page in enumerate(pages):
        slides.append(render_slide(page, manifest, idx))
    slides.append(render_appendix_slide(appendix_text))
    slides.append(render_manual_slide(manual_text))
    slides_html = "\n\n".join(slides)

    template = TEMPLATE.read_text(encoding="utf-8")
    marker_start = template.find("<!-- SLIDES_HERE")
    marker_end = template.find("-->", marker_start) + 3
    deck_close = template.find("\n</div>", marker_end)
    deck = template[:marker_start] + slides_html + "\n</div>" + template[deck_close + len("\n</div>"):]

    css_path = ROOT / "academic.css"
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        deck = deck.replace("</style>", "\n" + css + "\n</style>", 1)
    deck = deck.replace(
        "[必填] 替换为 PPT 标题 · Deck Title",
        "智涌脑 · iNEST 全景报告（详细版）· 学术风格 146 页",
    )
    deck = deck.replace("#deck{position:fixed;inset:0;width:10000vw;", "#deck{position:fixed;inset:0;width:15000vw;")

    OUT.write_text(deck, encoding="utf-8")
    SLIDES_OUT.write_text(slides_html, encoding="utf-8")
    print(f"Built {len(slides)} slides -> {OUT}")
    print(f"Slide block written -> {SLIDES_OUT}")


if __name__ == "__main__":
    build()
