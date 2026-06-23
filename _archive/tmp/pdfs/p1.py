# -*- coding: utf-8 -*-
"""Generate iNEST invitation PDF with professional Chinese typography."""

import os, sys
sys.stdout.reconfigure(encoding='utf-8')

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ═════════════════════ Fonts ═════════════════════
FONT_SANS = "NotoSansSC"
FONT_SERIF = "NotoSerifSC"
pdfmetrics.registerFont(TTFont(FONT_SANS, "C:/Windows/Fonts/NotoSansSC-VF.ttf"))
pdfmetrics.registerFont(TTFont(FONT_SERIF, "C:/Windows/Fonts/NotoSerifSC-VF.ttf"))
registerFontFamily(FONT_SANS, normal=FONT_SANS)
registerFontFamily(FONT_SERIF, normal=FONT_SERIF)

# ═════════════════════ Colors ═════════════════════
INK = HexColor("#1a1a2e")
ACCENT = HexColor("#0050b3")
ACCENT_LIGHT = HexColor("#e8f0fe")
GOLD = HexColor("#c7923e")
MUTED = HexColor("#5f6b7a")
RULE = HexColor("#d0d5dd")
CALLOUT_BG = HexColor("#f0f4f8")
QUOTE_BG = HexColor("#fdfaf3")
QUOTE_TEXT = HexColor("#5c4a1f")
TABLE_STRIPE = HexColor("#f7f9fc")

CONTENT_W = A4[0] - 36 * mm
OUTPUT_PATH = r"D:\Obsidian\iNEST对外合作介绍材料.pdf"

# ═════════════════════ Styles ═════════════════════
S = {}
S["ct"] = ParagraphStyle("ct", fontName=FONT_SANS, fontSize=28, leading=36, textColor=INK, alignment=TA_LEFT, spaceAfter=4*mm)
S["cs"] = ParagraphStyle("cs", fontName=FONT_SANS, fontSize=14, leading=20, textColor=MUTED, alignment=TA_LEFT, spaceAfter=8*mm)
S["h2"] = ParagraphStyle("h2", fontName=FONT_SANS, fontSize=17, leading=24, textColor=ACCENT, alignment=TA_LEFT, spaceBefore=12*mm, spaceAfter=4*mm)
S["h3"] = ParagraphStyle("h3", fontName=FONT_SANS, fontSize=13, leading=19, textColor=INK, alignment=TA_LEFT, spaceBefore=6*mm, spaceAfter=2*mm)
S["h4"] = ParagraphStyle("h4", fontName=FONT_SANS, fontSize=11.5, leading=17, textColor=INK, alignment=TA_LEFT, spaceBefore=4*mm, spaceAfter=1.5*mm)
S["body"] = ParagraphStyle("body", fontName=FONT_SERIF, fontSize=10.5, leading=18, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=3*mm, firstLineIndent=21)
S["bni"] = ParagraphStyle("bni", fontName=FONT_SERIF, fontSize=10.5, leading=18, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=3*mm)
S["lead"] = ParagraphStyle("lead", fontName=FONT_SANS, fontSize=11.5, leading=20, textColor=ACCENT, alignment=TA_LEFT, spaceAfter=2*mm)
S["quote"] = ParagraphStyle("qt", fontName=FONT_SERIF, fontSize=10.5, leading=18, textColor=QUOTE_TEXT, alignment=TA_LEFT, spaceAfter=2*mm)
S["qs"] = ParagraphStyle("qs", fontName=FONT_SERIF, fontSize=9, leading=14, textColor=MUTED, alignment=TA_LEFT)
S["callout"] = ParagraphStyle("co", fontName=FONT_SANS, fontSize=10.5, leading=19, textColor=INK, alignment=TA_LEFT, spaceAfter=1*mm)
S["footer"] = ParagraphStyle("ft", fontName=FONT_SANS, fontSize=9, leading=15, textColor=MUTED, alignment=TA_CENTER, spaceAfter=1*mm)
S["toc"] = ParagraphStyle("toc", fontName=FONT_SERIF, fontSize=11, leading=22, textColor=MUTED, alignment=TA_LEFT)
S["toct"] = ParagraphStyle("toct", fontName=FONT_SANS, fontSize=12, leading=18, textColor=ACCENT, alignment=TA_LEFT, spaceAfter=3*mm)
S["tag"] = ParagraphStyle("tag", fontName=FONT_SANS, fontSize=9, leading=13, textColor=white, alignment=TA_LEFT)
S["th"] = ParagraphStyle("th", fontName=FONT_SANS, fontSize=9, leading=13, textColor=white, alignment=TA_LEFT)
S["tc"] = ParagraphStyle("tc", fontName=FONT_SERIF, fontSize=9, leading=14, textColor=INK, alignment=TA_LEFT)
S["sig"] = ParagraphStyle("sig", fontName=FONT_SERIF, fontSize=10, leading=16, textColor=INK, alignment=TA_LEFT)

# ═════════════════════ Flowables ═════════════════════
class HRFlowable(Flowable):
    def __init__(self, width, color=RULE):
        Flowable.__init__(self)
        self.width = width; self.color = color; self.height = 5*mm
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(0.5)
        self.canv.line(0, 2.5*mm, self.width, 2.5*mm)

class MetricCard(Flowable):
    def __init__(self, width, metrics):
        Flowable.__init__(self)
        self.width = width; self.metrics = metrics
        self.height = 30*mm; self.card_w = (width - 12*mm) / 3
    def draw(self):
        for i, (num, label) in enumerate(self.metrics):
            x = i * (self.card_w + 6*mm)
            self.canv.setFillColor(ACCENT_LIGHT)
            self.canv.roundRect(x, 0, self.card_w, self.height, 4*mm, fill=1, stroke=0)
            self.canv.setFillColor(ACCENT)
            self.canv.setFont(FONT_SANS, 20)
            self.canv.drawCentredString(x + self.card_w/2, self.height - 14*mm, num)
            self.canv.setFont(FONT_SANS, 7.5)
            self.canv.setFillColor(MUTED)
            for j, line in enumerate(label.split("\n")):
                self.canv.drawCentredString(x + self.card_w/2, self.height - 22*mm - j*4*mm, line)

# ═════════════════════ Helpers ═════════════════════
def body(text, style="body"):
    return Paragraph(text, S[style])

def h2(text):
    return Paragraph(text, S["h2"])

def h3(text):
    return Paragraph(text, S["h3"])

def h4(text):
    return Paragraph(text, S["h4"])

def sp(h=3*mm):
    return Spacer(1, h)

def make_callout(text):
    inner = Paragraph(text, S["callout"])
    t = Table([[inner]], colWidths=[CONTENT_W - 16*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CALLOUT_BG),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [3,3,3,3]),
    ]))
    return t

def make_quote(text, attr=None):
    inner = [Paragraph(text, S["quote"])]
    if attr:
        inner.append(Paragraph(attr, S["qs"]))
    t = Table([[inner]], colWidths=[CONTENT_W - 16*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), QUOTE_BG),
        ("LEFTPADDING", (0,0), (-1,-1), 14),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LINEBEFORE", (0,0), (0,0), 2.5, GOLD),
        ("ROUNDEDCORNERS", [0,3,3,0]),
    ]))
    return t

def make_lead(text):
    inner = Paragraph(text, S["lead"])
    t = Table([[inner]], colWidths=[CONTENT_W - 16*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), ACCENT_LIGHT),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LINEBEFORE", (0,0), (0,0), 3, ACCENT),
        ("ROUNDEDCORNERS", [0,3,3,0]),
    ]))
    return t

def make_signals(signals):
    rows = []
    for inst, txt in signals:
        inner = Paragraph(
            '<font face="' + FONT_SANS + '" color="#0050b3"><b>' + inst + '</b></font>' +
            '<font face="' + FONT_SERIF + '">' + txt + '</font>',
            S["sig"]
        )
        rows.append([inner])
    t = Table(rows, colWidths=[CONTENT_W])
    cmds = [
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("ROUNDEDCORNERS", [3,3,3,3]),
    ]
    for i in range(len(signals)):
        cmds.append(("BACKGROUND", (0,i), (-1,i), CALLOUT_BG))
        if i < len(signals) - 1:
            cmds.append(("LINEBELOW", (0,i), (-1,i), 0.5, RULE))
    t.setStyle(TableStyle(cmds))
    return t

# ═════════════════════ BUILD ═════════════════════
print("Building PDF...")
doc = SimpleDocTemplate(
    OUTPUT_PATH, pagesize=A4,
    leftMargin=18*mm, rightMargin=18*mm,
    topMargin=20*mm, bottomMargin=20*mm,
    title="iNEST · 让智能从连接中涌现",
    author="iNEST探索团队",
)
story = []