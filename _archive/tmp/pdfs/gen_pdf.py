# -*- coding: utf-8 -*-
"""Generate iNEST PDF."""

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

# Fonts
FONT_SANS = "NotoSansSC"
FONT_SERIF = "NotoSerifSC"
pdfmetrics.registerFont(TTFont(FONT_SANS, "C:/Windows/Fonts/NotoSansSC-VF.ttf"))
pdfmetrics.registerFont(TTFont(FONT_SERIF, "C:/Windows/Fonts/NotoSerifSC-VF.ttf"))
registerFontFamily(FONT_SANS, normal=FONT_SANS)
registerFontFamily(FONT_SERIF, normal=FONT_SERIF)
print("Fonts OK")

# Colors
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

CONTENT_W = A4[0] - 36*mm
OUTPUT_PATH = r"D:\Obsidian\iNEST对外合作介绍材料.pdf"