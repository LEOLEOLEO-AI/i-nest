# -*- coding: utf-8 -*-
"""Generate iNEST CS 团队转入指南 PDF."""

import os, sys, re, textwrap
sys.stdout.reconfigure(encoding="utf-8")

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Frame, BaseDocTemplate, PageTemplate,
    Flowable
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from markdown_it import MarkdownIt

FONT_SANS = "NotoSansSC"
FONT_SERIF = "NotoSerifSC"
FONT_MONO = "NotoSansMonoSC"
pdfmetrics.registerFont(TTFont(FONT_SANS, "C:/Windows/Fonts/NotoSansSC-VF.ttf"))
pdfmetrics.registerFont(TTFont(FONT_SERIF, "C:/Windows/Fonts/NotoSerifSC-VF.ttf"))
try:
    pdfmetrics.registerFont(TTFont(FONT_MONO, "C:/Windows/Fonts/NotoSansMonoSC-VF.ttf"))
except:
    FONT_MONO = FONT_SANS
registerFontFamily(FONT_SANS, normal=FONT_SANS)
registerFontFamily(FONT_SERIF, normal=FONT_SERIF)

INK = HexColor("#1a1a2e")
ACCENT = HexColor("#0050b3")
ACCENT_LIGHT = HexColor("#e8f0fe")
GOLD = HexColor("#c7923e")
MUTED = HexColor("#5f6b7a")
RULE = HexColor("#d0d5dd")
CALLOUT_BG = HexColor("#f0f4f8")
QUOTE_BG = HexColor("#fdfaf3")
QUOTE_TEXT = HexColor("#5c4a1f")
QUOTE_BORDER = HexColor("#e5d5a0")
TABLE_STRIPE = HexColor("#f7f9fc")
TABLE_HEADER = HexColor("#1a1a2e")
CODE_BG = HexColor("#f5f5f5")
CHECK_BOX = HexColor("#c0c4cc")

MARGIN = 25 * mm
PAGE_W, PAGE_H = A4
CONTENT_W = PAGE_W - 2 * MARGIN

normal_style = ParagraphStyle(
    "normal", fontName=FONT_SANS, fontSize=10, leading=18,
    textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6,
)

h1_style = ParagraphStyle(
    "h1", fontName=FONT_SANS, fontSize=22, leading=30,
    textColor=ACCENT, spaceAfter=10, spaceBefore=6,
    alignment=TA_LEFT,
)

h2_style = ParagraphStyle(
    "h2", fontName=FONT_SANS, fontSize=15, leading=22,
    textColor=INK, spaceAfter=8, spaceBefore=22,
    alignment=TA_LEFT,
)

h3_style = ParagraphStyle(
    "h3", fontName=FONT_SANS, fontSize=12, leading=18,
    textColor=INK, spaceAfter=6, spaceBefore=16,
    alignment=TA_LEFT,
)

h4_style = ParagraphStyle(
    "h4", fontName=FONT_SANS, fontSize=10.5, leading=16,
    textColor=MUTED, spaceAfter=4, spaceBefore=12,
    alignment=TA_LEFT,
)

quote_style = ParagraphStyle(
    "quote", fontName=FONT_SERIF, fontSize=10, leading=17,
    textColor=QUOTE_TEXT, alignment=TA_JUSTIFY, spaceAfter=4,
    leftIndent=6, rightIndent=4,
)

code_style = ParagraphStyle(
    "code", fontName=FONT_MONO, fontSize=8, leading=12.5,
    textColor=INK, alignment=TA_LEFT, spaceAfter=0,
)

list_style = ParagraphStyle(
    "list_item", fontName=FONT_SANS, fontSize=10, leading=18,
    textColor=INK, alignment=TA_JUSTIFY, spaceAfter=3,
    leftIndent=12, bulletIndent=0,
)

table_cell_style = ParagraphStyle(
    "table_cell", fontName=FONT_SANS, fontSize=8.5, leading=13,
    textColor=INK, alignment=TA_LEFT,
)

table_header_style = ParagraphStyle(
    "table_header", fontName=FONT_SANS, fontSize=9, leading=13,
    textColor=white, alignment=TA_LEFT,
)

def esc_xml(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

def parse_inline_tokens(tokens):
    parts = []
    for tok in tokens:
        if tok is None:
            continue
        t = tok.type
        if t == "text":
            parts.append(esc_xml(tok.content))
        elif t == "strong_open":
            parts.append("<b>")
        elif t == "strong_close":
            parts.append("</b>")
        elif t == "em_open":
            parts.append("<i>")
        elif t == "em_close":
            parts.append("</i>")
        elif t == "code_inline":
            parts.append(f'<font face="{FONT_MONO}" color="#c7254e" size="9">{esc_xml(tok.content)}</font>')
        elif t == "link_open":
            href = tok.attrs.get("href", "")
            parts.append(f'<a href="{esc_xml(href)}" color="#0050b3"><u>')
        elif t == "link_close":
            parts.append("</u></a>")
        elif t == "softbreak":
            parts.append(" ")
        elif t == "hardbreak":
            parts.append("<br/>")
        elif t == "image":
            pass
        else:
            if hasattr(tok, "content") and tok.content:
                parts.append(esc_xml(str(tok.content)))
    return "".join(parts)

def parse_inline(text):
    tokens = MarkdownIt().parseInline(text, {})
    return parse_inline_tokens(tokens)

INPUT_MD = r"D:\Obsidian\iNEST_CS团队转入指南.md"
OUTPUT_PDF = r"D:\Obsidian\iNEST_CS团队转入指南.pdf"

print("Reading markdown...")
with open(INPUT_MD, "r", encoding="utf-8") as f:
    md_text = f.read()

md = MarkdownIt()
tokens = md.parse(md_text, {})

story = []

state = {
    "in_para": False,
    "in_list": False,
    "list_type": None,
    "list_counter": 0,
    "in_quote": False,
    "quote_buffer": [],
    "in_table": False,
    "table_rows": [],
    "in_thead": False,
    "in_tbody": False,
    "current_row": [],
    "heading_level": 0,
    "in_code_block": False,
    "code_lines": [],
    "code_lang": "",
    "ordered_counter": 0,
}

def flush_quote():
    if state["quote_buffer"]:
        quote_text = " ".join(state["quote_buffer"])
        parsed = parse_inline(quote_text)
        qp = Paragraph(parsed, quote_style)
        qt = Table([[qp]], colWidths=[CONTENT_W - 10])
        qt.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("BACKGROUND", (0, 0), (-1, -1), QUOTE_BG),
            ("LINEBEFORE", (0, 0), (0, 0), 3, GOLD),
        ]))
        story.append(Spacer(1, 4))
        story.append(qt)
        story.append(Spacer(1, 6))
        state["quote_buffer"] = []

def render_table():
    rows = state["table_rows"]
    if not rows:
        return
    num_cols = max(len(r) for r in rows)
    col_w = CONTENT_W / num_cols
    data = []
    for i, row in enumerate(rows):
        while len(row) < num_cols:
            row.append("")
        para_row = []
        for cell in row:
            inline_xml = parse_inline(cell)
            if i == 0:
                para_row.append(Paragraph(inline_xml, table_header_style))
            else:
                para_row.append(Paragraph(inline_xml, table_cell_style))
        data.append(para_row)

    t = Table(data, colWidths=[col_w]*num_cols, repeatRows=1)
    tbl_style = [
        ("FONTNAME", (0, 0), (-1, -1), FONT_SANS),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, ACCENT),
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
    ]
    for i in range(2, len(data), 2):
        tbl_style.append(("BACKGROUND", (0, i), (-1, i), TABLE_STRIPE))
    t.setStyle(TableStyle(tbl_style))
    story.append(Spacer(1, 6))
    story.append(t)
    story.append(Spacer(1, 8))

def render_code_block():
    lines = state["code_lines"]
    story.append(Spacer(1, 4))
    for line in lines:
        if not line.strip():
            story.append(Paragraph("&nbsp;", code_style))
        else:
            story.append(Paragraph("<![CDATA[" + esc_xml(line.rstrip()) + "]]>", code_style))
    story.append(Spacer(1, 4))

print("Processing tokens...")
for tok in tokens:
    t = tok.type

    if t == "heading_open":
        state["heading_level"] = int(tok.tag[1])
    elif t == "heading_close":
        state["heading_level"] = 0
    elif t == "inline" and state["heading_level"] > 0:
        level = state["heading_level"]
        content = tok.content.strip()
        if not content:
            continue
        if level == 1:
            story.append(Paragraph(parse_inline(content), h1_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=8))
        elif level == 2:
            story.append(Spacer(1, 4))
            story.append(Paragraph(parse_inline(content), h2_style))
        elif level == 3:
            story.append(Paragraph(parse_inline(content), h3_style))
        elif level == 4:
            story.append(Paragraph(parse_inline(content), h4_style))
        else:
            story.append(Paragraph(parse_inline(content), normal_style))

    elif t == "paragraph_open":
        state["in_para"] = True
    elif t == "paragraph_close":
        state["in_para"] = False
    elif t == "inline" and state["in_para"] and not state["in_list"] and not state["heading_level"]:
        content = tok.content.strip()
        if not content:
            continue
        if state["in_quote"]:
            state["quote_buffer"].append(content)
        elif state["in_table"] and (state["in_thead"] or state["in_tbody"]):
            state["current_row"].append(content)
        else:
            story.append(Paragraph(parse_inline(content), normal_style))

    elif t == "blockquote_open":
        state["in_quote"] = True
        state["quote_buffer"] = []
    elif t == "blockquote_close":
        state["in_quote"] = False
        flush_quote()

    elif t == "bullet_list_open":
        state["in_list"] = True
        state["list_type"] = "bullet"
    elif t == "bullet_list_close":
        state["in_list"] = False
        state["list_type"] = None
        story.append(Spacer(1, 4))
    elif t == "list_item_open":
        pass
    elif t == "list_item_close":
        pass
    elif t == "inline" and state["in_list"] and state["list_type"] == "bullet":
        story.append(Paragraph("&#x2022; " + parse_inline(tok.content.strip()), list_style))
    elif t == "inline" and state["in_list"] and state["list_type"] == "ordered":
        state["ordered_counter"] += 1
        story.append(Paragraph(f"{state['ordered_counter']}. " + parse_inline(tok.content.strip()), list_style))

    elif t == "ordered_list_open":
        state["in_list"] = True
        state["list_type"] = "ordered"
        state["ordered_counter"] = 0
    elif t == "ordered_list_close":
        state["in_list"] = False
        state["list_type"] = None
        story.append(Spacer(1, 4))

    elif t == "fence":
        state["code_lines"] = tok.content.split("\n")
        state["code_lang"] = tok.info.strip()
        render_code_block()

    elif t == "table_open":
        state["in_table"] = True
        state["table_rows"] = []
        state["in_thead"] = False
        state["in_tbody"] = False
    elif t == "table_close":
        state["in_table"] = False
        render_table()
    elif t == "thead_open":
        state["in_thead"] = True
    elif t == "thead_close":
        state["in_thead"] = False
    elif t == "tbody_open":
        state["in_tbody"] = True
    elif t == "tbody_close":
        state["in_tbody"] = False
    elif t == "tr_open":
        state["current_row"] = []
    elif t == "tr_close":
        if state["current_row"]:
            state["table_rows"].append(state["current_row"])
        state["current_row"] = []
    elif t == "th_open" or t == "td_open":
        pass
    elif t == "th_close" or t == "td_close":
        pass

    elif t == "hr":
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="40%", thickness=0.5, color=RULE, spaceAfter=4))

print(f"Building PDF with {len(story)} flowables...")

class CSGuideDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        frame = Frame(MARGIN, 22*mm, CONTENT_W, PAGE_H - 2*MARGIN - 8*mm, id="main")
        self.addPageTemplates([
            PageTemplate(id="main", frames=[frame], onPage=self._on_page)
        ])

    def _on_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT_SANS, 8)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(PAGE_W - MARGIN, 15*mm, f"\u2014 {doc.page} \u2014")
        canvas.drawString(MARGIN, 15*mm, "iNEST \u00b7 CS\u56e2\u961f\u8f6c\u5165\u6307\u5357")
        if doc.page > 1:
            canvas.setStrokeColor(RULE)
            canvas.setLineWidth(0.3)
            canvas.line(MARGIN, PAGE_H - MARGIN + 10*mm, PAGE_W - MARGIN, PAGE_H - MARGIN + 10*mm)
        canvas.restoreState()

doc = CSGuideDoc(OUTPUT_PDF, pagesize=A4, title="iNEST CS\u56e2\u961f\u8f6c\u5165\u6307\u5357", author="iNEST\u63a2\u7d22\u56e2\u961f")
doc.build(story)
print(f"Done! PDF: {OUTPUT_PDF}")