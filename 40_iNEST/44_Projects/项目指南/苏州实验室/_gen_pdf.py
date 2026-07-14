import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FN = 'SimSun'
FB = 'SimHei'
try:
    pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc', subfontIndex=0))
    pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))
except:
    FN = 'Helvetica'; FB = 'Helvetica-Bold'

W, H = A4
C_DARK = HexColor('#1a1a2e')
C_BLUE = HexColor('#1e3799')
C_ACCENT = HexColor('#c0392b')
C_GREY = HexColor('#7f8c8d')
C_LIGHT = HexColor('#f5f6fa')
C_WHITE = white

sTitle = ParagraphStyle('T', fontName=FB, fontSize=20, leading=28, textColor=C_DARK, alignment=TA_CENTER, spaceAfter=4*mm)
sH1 = ParagraphStyle('H1', fontName=FB, fontSize=14, leading=20, textColor=C_BLUE, spaceBefore=8*mm, spaceAfter=3*mm)
sH2 = ParagraphStyle('H2', fontName=FB, fontSize=11, leading=16, textColor=C_DARK, spaceBefore=4*mm, spaceAfter=2*mm)
sBody = ParagraphStyle('B', fontName=FN, fontSize=9.5, leading=15, textColor=black, spaceAfter=2*mm, alignment=TA_JUSTIFY)
sBullet = ParagraphStyle('BL', parent=sBody, leftIndent=8*mm, bulletIndent=3*mm, spaceBefore=1*mm, spaceAfter=1*mm)
sMeta = ParagraphStyle('M', fontName=FN, fontSize=9, leading=13, textColor=C_GREY, alignment=TA_CENTER)
sCell = ParagraphStyle('C', fontName=FN, fontSize=8, leading=11, textColor=black)
sHead = ParagraphStyle('CH', fontName=FB, fontSize=8.5, leading=11, textColor=C_WHITE)
sQuote = ParagraphStyle('Q', fontName=FN, fontSize=9.5, leading=15, textColor=C_BLUE, leftIndent=8*mm, rightIndent=8*mm, backColor=C_LIGHT, borderPadding=6, spaceBefore=3*mm, spaceAfter=3*mm)

def mt(headers, rows, cw=None):
    hdr = [Paragraph(h, sHead) for h in headers]
    data = [hdr] + [[Paragraph(str(c), sCell) for c in r] for r in rows]
    if not cw:
        cw = [W*0.85/len(headers)]*len(headers)
    t = Table(data, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),C_BLUE), ('TEXTCOLOR',(0,0),(-1,0),C_WHITE),
        ('ALIGN',(0,0),(-1,0),'CENTER'), ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('GRID',(0,0),(-1,-1),0.5,HexColor('#dcdde1')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[C_WHITE,C_LIGHT]),
        ('TOPPADDING',(0,0),(-1,-1),3), ('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('LEFTPADDING',(0,0),(-1,-1),4), ('RIGHTPADDING',(0,0),(-1,-1),4),
    ]))
    return t

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=HexColor('#dcdde1'), spaceBefore=2*mm, spaceAfter=2*mm)

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(HexColor('#dcdde1'))
    canvas.setLineWidth(0.5)
    canvas.line(18*mm, H-15*mm, W-18*mm, H-15*mm)
    canvas.setFont(FN, 7)
    canvas.setFillColor(C_GREY)
    canvas.drawString(18*mm, H-13*mm, 'Suzhou National Materials Lab iNEST Pilot Project')
    canvas.drawRightString(W-18*mm, H-13*mm, 'Confidential - Internal Review')
    canvas.drawCentredString(W/2, 10*mm, '- %d -' % doc.page)
    canvas.restoreState()

outdir = r'D:\Obsidian\home\work\.openclaw\workspace\40_iNEST\44_Projects\项目指南\苏州实验室'
outpath = os.path.join(outdir, 'iNEST_Briefing_XuNanping_v1.0.pdf')

story = []
story.append(Spacer(1, 12*mm))
story.append(Paragraph('Suzhou National Materials Lab', sMeta))
story.append(Paragraph('iNEST Pilot Project', sTitle))
story.append(Paragraph('Briefing for Director Xu Nanping', sMeta))
story.append(Spacer(1, 2*mm))
story.append(hr())
story.append(Spacer(1, 3*mm))
story.append(Paragraph('Reporter: Tong Yi, Researcher  |  June 23, 2026  |  v1.0 Executive Briefing', sMeta))
story.append(Spacer(1, 6*mm))

# Section 1
story.append(Paragraph('1. Project Positioning: Why Must Suzhou Lab Act Now?', sH1))
story.append(Paragraph('1.1 Global AI Computing Faces a Paradigm-Level Inflection', sH2))
story.append(mt(['Bottleneck','Current Status','Source'],
    [['Thermal Limit','H100 700W to B200 1000W+, liquid cooling at physical limit','NVIDIA TDP 2024-2025'],
     ['Interconnect Gap','IBM bandwidth lags behind model parameter growth','IBM HFI Report 2025'],
     ['Diminishing Returns','GPT-5 training cost >, performance curve flattening','Epoch AI 2025'],
     ['Von Neumann Bottleneck','90%+ energy consumed in data movement, not compute','Horowitz ISSCC 2014']],
    [W*0.18, W*0.42, W*0.25]))
story.append(Paragraph('<b>Conclusion:</b> The pure scale-up/scale-out path is approaching its engineering limit.', sBody))

story.append(Paragraph('1.2 TCC Paradigm: From Compute-Centric to Topology-Centric', sH2))
for item in [
    '<b>Route-Transform Isomorphism</b>: Communication = Computation. Network connections are themselves computing resources.',
    '<b>SDI Compound Bonds</b>: Software-Defined Interconnect (FUSE+MAPS+GEMM+LINK), network topology is programmable.',
    '<b>CST Theoretical Metric</b>: Coordination Spatiotemporal Complexity is a threshold detector for intelligence emergence; CST formula does NOT contain connection-count variable.'
]:
    story.append(Paragraph('\\u2022 ' + item, sBullet))

story.append(Paragraph('1.3 Suzhou Lab Irreplaceable Strategic Position', sH2))
story.append(mt(['Layer','Content','Lead Unit','Suzhou Role'],
    [['L5 Emergence Verify','Six-level intelligence emergence physical verification','All seven units','Participant'],
     ['<b>L4 System Integration</b>','<b>SDSoW wafer-level system</b>','<b>Suzhou(Tong Yi) + TJU(Yu Hesan)</b>','<b>Co-Lead</b>'],
     ['L3 Emergence Arch','TCC-11 accelerator / CST IP / toolchain','FDU(Zhang Fan) + ZJU(Pan Gang) + NDSC(Li Peijie)','Adaptation'],
     ['L2 Nonlinear Device','Memristor crossbar / multi-scale dynamics','PKU(Yang Yuchao) + TJU(Yu Hesan)','Test coordination'],
     ['<b>L1 Material Innovation</b>','<b>SDI compound bond / TCC-Link physical layer</b>','<b>Suzhou Lab(Tong Yi)</b>','<b>SOLE unit</b>']],
    [W*0.16, W*0.32, W*0.24, W*0.13]))
story.append(Paragraph('<i>One-line positioning: Without material-layer breakthroughs, everything above is castles in the air.</i>', sQuote))

# Section 2
story.append(Paragraph('2. Seven-Unit Synergistic Team', sH1))
story.append(Paragraph('<b>Leadership:</b> Academicians Wu Jiangxing + Xu Nanping  |  <b>Executive Lead:</b> Liu Qinrang', sBody))
story.append(mt(['Unit','Lead','Core Strength','Authority'],
    [['<b>Suzhou Lab</b>','<b>Tong Yi (Lead)</b>','Functional oxides + memristors + wafer integration','28nm domestic tape-out (2025)'],
     ['Peking University','Prof. Yang Yuchao','Dual ferroelectric-gate tunable memristor','InfoMat 2026'],
     ['Tianjin University','Assoc. Yu Hesan','Device fabrication + wafer-level test','TJU Microelectronics'],
     ['Fudan University','Prof. Zhang Fan','Emergence architecture + toolchain','FDU Chip Frontier Center'],
     ['Zhejiang University','Prof. Pan Gang','Darwin3 neuromorphic chip + SNN ecosystem','NSR 2025'],
     ['NDSC','Res. Li Peijie','SDI standards + SDSoW architecture','NDSC Reports 2025-2026'],
     ['Haihe Lab','Prof. Li Tao','TCC-11 FPGA full-chain verification','Haihe Lab 2026']],
    [W*0.16, W*0.18, W*0.32, W*0.19]))

# Section 3
story.append(Paragraph('3. Four-Year Technical Roadmap', sH1))
story.append(Paragraph('Core Innovation: Device Philosophy Correction', sH2))
story.append(mt(['Dimension','Traditional Precision Computing','iNEST Emergence Computing'],
    [['Device Goal','Resistance uniformity (6-8 bit)','<b>ON/OFF switch (1 bit)</b>'],
     ['Primary Contradiction','Device uniformity','<b>Nonlinear I-V mapping with network dynamics</b>'],
     ['Process Node','7nm/5nm advanced','<b>28nm/12nm mature - sufficient</b>'],
     ['Clock Speed','GHz high-frequency','<b>MHz (matching biological timescales)</b>'],
     ['Device Variability','Bug (must eliminate)','<b>Feature (physical driver of emergence)</b>']],
    [W*0.22, W*0.33, W*0.30]))

story.append(Paragraph('Four-Year Milestones', sH2))
for title, detail in [
    ('<b>Y1 (2026Q4-2027Q3): Material to Device</b>',
     'SDI compound bond material formula (5 MPW rounds) | Memristor I-V characterization (alpha=2.8-4.5) | Milestone M1: Single-node ON/OFF switching verified'),
    ('<b>Y2 (2027Q4-2028Q3): Device to Array</b>',
     '128x128 memristor crossbar | SDI switch matrix FPGA IP core | PKU/TJU process solidification | Milestone M2: Array-level nonlinear mapping verified'),
    ('<b>Y3 (2028Q4-2029Q3): Array to System</b>',
     'SDSoW prototype (>10K nodes) | II-III grade emergence physical verification | CST-material reverse mapping model | Milestone M3: Physical emergence verified'),
    ('<b>Y4 (2029Q4-2030Q3): System to Emergence</b>',
     '10K-node SDSoW wafer system | IV-V grade emergence verification | iNEST open-source community + TCC-Link standard | Milestone M4: Four-grade emergence verified'),
]:
    story.append(Paragraph(title, sH2))
    story.append(Paragraph(detail, sBody))

# Section 4
story.append(Paragraph('4. Budget (2 Billion RMB / 4 Years)', sH1))
story.append(mt(['Unit','Budget (10K RMB)','Share','Core Tasks'],
    [['<b>Suzhou Lab (Tong Yi, Lead)</b>','<b>7,000</b>','<b>35%</b>','L1 materials + L4 system integration + 30-50 staff'],
     ['Tianjin University (Yu Hesan)','2,800','14%','L2 device fab/test + L4 system test'],
     ['Fudan University (Zhang Fan)','2,800','14%','L3 emergence architecture + toolchain'],
     ['PKU + ZJU + NDSC','4,000','20%','L2 devices + L3 toolchain + SDI standards'],
     ['Seven-unit emergence verification','1,300','6.5%','L5 physical verification + cross-unit data'],
     ['Suzhou team salary + student stipends + exchange','2,200','11%','30-50 staff + 8 postdocs + 15 PhD + 15 MS'],
     ['<b>Total</b>','<b>20,000</b>','<b>100%</b>','<b>7 units, 4 years, annual review rolling allocation</b>']],
    [W*0.28, W*0.15, W*0.10, W*0.32]))
story.append(Paragraph('<b>Suzhou Key Spending:</b> Materials R&D (5 MPW rounds) ~2,500 | Array tape-out ~1,500 | SDSoW integration ~1,800 | Team hiring (30-50) ~1,200 (10K RMB)', sBody))

# Section 5
story.append(Paragraph('5. Existing Validation Foundation', sH1))
story.append(mt(['Dimension','Evidence','Source'],
    [['<b>Theory</b>','CST V25 40-system cross-species/architecture test rho=0.92 tau=0.83','CST V25 Paper 2026'],
     ['<b>Simulation</b>','SDI six-grade emergence simulation full-chain passed (V9 to L6)','SDI Experiment-3 2025-2026'],
     ['<b>Device</b>','Dual ferroelectric-gate memristor I-V nonlinear mapping','Yang Yuchao, InfoMat 2026'],
     ['<b>Architecture</b>','Darwin3 commercial-grade SNN toolchain','Pan Gang, NSR 2025'],
     ['<b>Process</b>','28nm domestic memristor crossbar tape-out','Suzhou Lab internal 2025'],
     ['<b>Standards</b>','TCC-Link framework + SDSoW architecture design','NDSC Reports 2025-2026']],
    [W*0.14, W*0.51, W*0.20]))

# Section 6
story.append(Paragraph('6. Recommendations', sH1))
for item in [
    '<b>Occupy track definition rights:</b> SDI compound bond functional materials will define the material basis for post-Moore intelligent computing.',
    '<b>Build irreplaceability:</b> The dual role of L1 materials + L4 system integration ensures Suzhou Lab central hub position in the full technology stack.',
    '<b>Form talent high ground:</b> 30-50 dedicated staff + seven-unit national synergy creates China first-tier neuromorphic emergence computing team.',
]:
    story.append(Paragraph('\\u2022 ' + item, sBullet))
story.append(Spacer(1, 3*mm))
story.append(Paragraph('<b>Recommendation:</b> Approve this pilot project at highest priority, with 4-year 200M RMB full funding, and include it in Suzhou National Materials Lab 15th Five-Year Plan major directions.', sQuote))

# Footer
story.append(Spacer(1, 8*mm))
story.append(hr())
story.append(Paragraph('Full Project Guide: [V3] Suzhou Lab iNEST Pilot Project Guide - Materials and Network Foundation v3.0 Final Release', sMeta))
story.append(Paragraph('Suzhou National Materials Lab  |  iNEST Pilot Project  |  Confidential - Internal Review Only', sMeta))

doc = SimpleDocTemplate(outpath, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=22*mm, bottomMargin=18*mm,
    title='Suzhou Lab iNEST Pilot Briefing', author='Tong Yi')
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print('OK: ' + outpath)
print('Size: %.1f KB' % (os.path.getsize(outpath)/1024))
