# -*- coding: utf-8 -*-
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

FONT_SANS = 'NotoSansSC'
FONT_SERIF = 'NotoSerifSC'
pdfmetrics.registerFont(TTFont(FONT_SANS, 'C:/Windows/Fonts/NotoSansSC-VF.ttf'))
pdfmetrics.registerFont(TTFont(FONT_SERIF, 'C:/Windows/Fonts/NotoSerifSC-VF.ttf'))
registerFontFamily(FONT_SANS, normal=FONT_SANS)
registerFontFamily(FONT_SERIF, normal=FONT_SERIF)
print('OK')