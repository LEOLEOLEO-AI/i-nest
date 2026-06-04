import os, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont("SimSun", "C:/Windows/Fonts/simsun.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("SimHei", "C:/Windows/Fonts/simhei.ttf"))
pdfmetrics.registerFont(TTFont("SimKai", "C:/Windows/Fonts/simkai.ttf"))
pdfmetrics.registerFont(TTFont("SimFang", "C:/Windows/Fonts/simfang.ttf"))

PRIMARY = HexColor("#1a365d")
ACCENT = HexColor("#2b6cb0")
LIGHT_BG = HexColor("#ebf4ff")
DARK_TEXT = HexColor("#1a202c")
MED_TEXT = HexColor("#4a5568")
BORDER = HexColor("#cbd5e0")
TABLE_HEADER = HexColor("#2b6cb0")
TABLE_ALT = HexColor("#f7fafc")

W, H = A4
MARGIN = 25 * mm

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved = []
    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        for s in self._saved:
            self.__dict__.update(s)
            self.setFont("SimSun", 8)
            self.setFillColor(MED_TEXT)
            self.drawCentredString(W/2, 15*mm, "\u2014 {} \u2014".format(self._pageNumber))
            self.setStrokeColor(BORDER); self.setLineWidth(0.5)
            self.line(MARGIN, H-20*mm, W-MARGIN, H-20*mm)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

def mkstyle(name, **kw):
    kw.setdefault("fontName", "SimSun")
    kw.setdefault("fontSize", 10)
    kw.setdefault("leading", 18)
    kw.setdefault("textColor", DARK_TEXT)
    kw.setdefault("alignment", TA_LEFT)
    return ParagraphStyle(name, **kw)

S = {}
S["title"] = mkstyle("T", fontName="SimHei", fontSize=22, leading=30, textColor=PRIMARY, spaceAfter=6*mm)
S["h1"] = mkstyle("H1", fontName="SimHei", fontSize=15, leading=22, textColor=PRIMARY, spaceBefore=8*mm, spaceAfter=4*mm)
S["h2"] = mkstyle("H2", fontName="SimHei", fontSize=12.5, leading=19, textColor=ACCENT, spaceBefore=6*mm, spaceAfter=3*mm)
S["h3"] = mkstyle("H3", fontName="SimHei", fontSize=11, leading=17, spaceBefore=4*mm, spaceAfter=2*mm)
S["body"] = mkstyle("B", fontSize=10, leading=18, alignment=TA_JUSTIFY, spaceBefore=1*mm, spaceAfter=1.5*mm, firstLineIndent=20)
S["body_ni"] = mkstyle("BN", fontSize=10, leading=18, alignment=TA_JUSTIFY, spaceBefore=1*mm, spaceAfter=1.5*mm)
S["bullet"] = mkstyle("BL", fontSize=10, leading=18, spaceBefore=0.5*mm, spaceAfter=0.5*mm, leftIndent=8*mm, bulletIndent=3*mm)
S["bullet2"] = mkstyle("B2", fontSize=10, leading=18, spaceBefore=0.3*mm, spaceAfter=0.3*mm, leftIndent=14*mm, bulletIndent=8*mm)
S["quote"] = mkstyle("Q", fontName="SimKai", fontSize=10.5, leading=19, textColor=MED_TEXT, leftIndent=12*mm, rightIndent=8*mm, spaceBefore=3*mm, spaceAfter=3*mm, backColor=LIGHT_BG)
S["code"] = mkstyle("C", fontSize=8, leading=12, leftIndent=8*mm, rightIndent=4*mm, spaceBefore=2*mm, spaceAfter=2*mm, backColor=HexColor("#f0f0f0"))
S["meta"] = mkstyle("M", fontName="SimFang", fontSize=9, leading=14, textColor=MED_TEXT, alignment=TA_CENTER)
S["check"] = mkstyle("CK", fontSize=10, leading=20, leftIndent=8*mm)

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def process(md):
    story = []
    lines = md.split("\n")
    i = 0
    in_table = False; table_rows = []
    in_code = False; code_lines = []
    in_quote = False; quote_lines = []
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if in_code:
                ct = "\n".join(code_lines)
                story.append(Paragraph("<pre>{}</pre>".format(esc(ct)), S["code"]))
                code_lines = []; in_code = False
            else:
                in_code = True
            i += 1; continue
        if in_code:
            code_lines.append(line); i += 1; continue
        if line.strip().startswith("> "):
            if not in_quote: quote_lines = []; in_quote = True
            quote_lines.append(line.strip()[2:]); i += 1; continue
        elif in_quote:
            in_quote = False
            if quote_lines:
                story.append(Paragraph("<br/>".join(quote_lines), S["quote"]))
            quote_lines = []
        if "|" in line and line.strip().startswith("|"):
            if not in_table: table_rows = []; in_table = True
            table_rows.append([c.strip() for c in line.strip().strip("|").split("|")])
            if i+1 < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i+1].strip()):
                i += 2; continue
            i += 1; continue
        elif in_table:
            in_table = False
            if len(table_rows) >= 2:
                render_tbl(story, table_rows)
            table_rows = []; continue
        if line.startswith("# ") and not line.startswith("## "):
            story.append(Paragraph(line[2:].strip(), S["title"]))
        elif line.startswith("## ") and not line.startswith("### "):
            story.append(Paragraph(line[3:].strip(), S["h1"]))
        elif line.startswith("### ") and not line.startswith("#### "):
            story.append(Paragraph(line[4:].strip(), S["h2"]))
        elif line.startswith("#### "):
            story.append(Paragraph(line[5:].strip(), S["h3"]))
        elif line.strip() == "---":
            story.append(HRFlowable(width="60%", thickness=0.3, color=BORDER, spaceBefore=4*mm, spaceAfter=4*mm))
        elif line.startswith("- [ ]"):
            story.append(Paragraph("\u2610 " + line[5:].strip(), S["check"]))
        elif line.startswith("- [x]"):
            story.append(Paragraph("\u2611 " + line[6:].strip(), S["check"]))
        elif line.startswith("- "):
            story.append(Paragraph("\u2022 " + line[2:].strip(), S["bullet"]))
        elif line.startswith("    - "):
            story.append(Paragraph("\u2013 " + line[6:].strip(), S["bullet2"]))
        elif re.match(r'^\d+\. ', line):
            m = re.match(r'^(\d+)\. ', line)
            story.append(Paragraph("{}.".format(m.group(1)) + " " + line[m.end():].strip(), S["bullet"]))
        elif line.strip():
            story.append(Paragraph(line.strip(), S["body"]))
        else:
            story.append(Spacer(1, 2*mm))
        i += 1
    if in_quote and quote_lines:
        story.append(Paragraph("<br/>".join(quote_lines), S["quote"]))
    if in_table and len(table_rows) >= 2:
        render_tbl(story, table_rows)
    return story

def render_tbl(story, rows):
    usable = W - 2*MARGIN
    nc = max(len(r) for r in rows)
    cw = [usable/nc]*nc
    formatted = []
    for row in rows:
        fs = [Paragraph(c, mkstyle("tc", fontSize=9, leading=14)) for c in row]
        formatted.append(fs)
    t = Table(formatted, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0,0),(-1,0),"SimHei"),("FONTSIZE",(0,0),(-1,0),9),
        ("TEXTCOLOR",(0,0),(-1,0),white),("BACKGROUND",(0,0),(-1,0),TABLE_HEADER),
        ("FONTNAME",(0,1),(-1,-1),"SimSun"),("FONTSIZE",(0,1),(-1,-1),9),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("GRID",(0,0),(-1,-1),0.5,BORDER),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[white,TABLE_ALT]),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
    ]))
    story.append(Spacer(1,2*mm)); story.append(t); story.append(Spacer(1,3*mm))

md_path = r"D:\Obsidian\iNEST_CS团队转入指南.md"
out = r"D:\Obsidian\output\iNEST_CS团队转入指南.pdf"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(md_path, "r", encoding="utf-8") as f:
    md = f.read()
doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                        topMargin=28*mm, bottomMargin=25*mm,
                        title="iNEST Guide", author="iNEST Team")
story = process(md)
story.append(Spacer(1, 8*mm))
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
story.append(Paragraph("iNEST\u63a2\u7d22\u56e2\u961f \u00b7 2026\u5e746\u6708", S["meta"]))
doc.build(story, canvasmaker=NumberedCanvas)
print("OK: " + out)
