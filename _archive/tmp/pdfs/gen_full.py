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

# ═════════════════════ COVER ═════════════════════
# Tag
tag_t = Table([[Paragraph("物理复杂网络智能涌现研究计划", S["tag"])]], colWidths=[65*mm])
tag_t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), INK),
    ("LEFTPADDING", (0,0), (-1,-1), 10),
    ("RIGHTPADDING", (0,0), (-1,-1), 10),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("ROUNDEDCORNERS", [3,3,3,3]),
]))
story.append(tag_t)
story.append(sp(6*mm))

# Title
story.append(Paragraph('<font face="' + FONT_SANS + '" size="32"><b>iNEST</b></font>', S["ct"]))
story.append(Paragraph('<font face="' + FONT_SANS + '" size="17" color="#5f6b7a">让智能从连接中涌现</font>', S["cs"]))

# Lead
story.append(sp(4*mm))
story.append(make_lead(
    '这是一份邀请。邀请所有不愿相信"更大的模型就是更好的智能"的研究者，'
    '邀请所有对大自然30亿年的智慧心怀敬畏的探索者，'
    '邀请所有想亲手定义下一代人工智能范式的信仰者——'
    '<b>加入 iNEST，一起走一条从无人走过的路。</b>'
))
story.append(sp(6*mm))

# ═════════════════════ TOC ═════════════════════
toc_items = [
    "一、学术信仰：智能的本质不在节点，在连接",
    "二、技术路线：复杂网络 × 神经形态 × 物理实现",
    "三、整体进展：我们走到了哪里",
    "四、未来规划：从验证到涌现",
    "五、为什么是我们，为什么是现在",
    "六、联系方式",
]
toc_data = [[Paragraph('<font face="' + FONT_SANS + '" size="12"><b>目录</b></font>', S["toct"])]]
for i, item in enumerate(toc_items):
    toc_data.append([Paragraph(
        '<font face="' + FONT_SERIF + '" color="#5f6b7a">' + str(i+1) + '. ' + item + '</font>',
        S["toc"]
    )])
toc_t = Table(toc_data, colWidths=[CONTENT_W - 16*mm])
toc_t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), CALLOUT_BG),
    ("LEFTPADDING", (0,0), (-1,-1), 14),
    ("RIGHTPADDING", (0,0), (-1,-1), 14),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LINEBELOW", (0,0), (-1,0), 0.5, RULE),
    ("ROUNDEDCORNERS", [4,4,4,4]),
]))
story.append(toc_t)
story.append(sp(8*mm))

# ═════════════════════ Ch1: 学术信仰 ═════════════════════
story.append(h2("一、学术信仰：智能的本质不在节点，在连接"))
story.append(h3("1.1 一个令人不安的事实"))
story.append(body(
    '人类大脑拥有860亿个神经元，每个神经元的工作速度比晶体管慢100万倍。'
    '它处理语言、识别面孔、推理逻辑、产生情感、发挥创造力——所有这些，'
    '仅消耗约<b>20瓦</b>功率，相当于一盏节能灯的能耗。'))
story.append(body(
    '作为对比，当前最强的人工智能系统完成同等复杂度的推理任务，'
    '需要约<b>3兆瓦</b>的能源供应。换句话说，其能效仅为生物大脑的<b>十五万分之一</b>。'))

# Metric cards
mc = MetricCard(CONTENT_W, [("15万×", "AI与大脑的\n能效差距"), ("20瓦", "人脑功耗"), ("3兆瓦", "GPT-4级\n推理功耗")])
story.append(mc)
story.append(sp(2*mm))

story.append(body(
    '这15万倍的差距，不是工程上"做得不够好"，而是<b>范式性的</b>。'
    '它揭示了一个根本问题：当前整个人工智能产业所依赖的计算范式，'
    '本身就在一个错误的轨道上运行。'))

story.append(h3("1.2 我们的核心信念"))
story.append(body('iNEST建立在一个简单但深刻的信念之上：'))
story.append(make_quote(
    '<b>智能的本质不在于单个计算单元的强大，而在于单元之间连接的方式、结构、及其动态演化。</b>'))
story.append(body(
    '这是一个有30亿年进化史作证的命题。从线虫的302个神经元到人类大脑的860亿个神经元，'
    '大自然从未试图制造"更大的神经元"——它制造了更丰富的连接、更精巧的拓扑、更复杂的动态。'
    '<b>智能的涌现，始终是网络层面的现象，而非节点层面的现象。</b>'))
story.append(body(
    '如果这个信念是对的——我们相信它是对的——那么当前AI产业以"堆叠更强节点"为核心的技术路线，'
    '将无法通向真正的智能。不是因为算力不够，而是因为<b>方向不对</b>。'))

story.append(h4("先贤的回响：他们说过同样的话"))
story.append(body(
    '这个信念并不孤独。在人工智能、复杂科学和神经科学的前沿，跨越半个多世纪，'
    '最敏锐的思想者们一直在以不同的语言表达同一个洞见：'
    '<b>整体大于部分之和，智能生于连接而非节点。</b>'))

# Anderson
story.append(make_quote(
    '<b>"More is different."</b>',
    '<font size="9" color="#5f6b7a">——<b>菲利普·安德森（Philip W. Anderson）</b>，'
    '1977年诺贝尔物理学奖得主，1972年在《Science》发表同名论文，奠定了凝聚态物理与复杂系统的哲学基石。'
    '他证明：大量简单组件的集体行为，不能通过对单个组件的理解来推导。'
    '这正是iNEST的第一性：连接规模跨越临界点后，质变自然发生。</font>'))

# Wolfram
story.append(make_quote(
    '<b>"复杂性从简单规则中涌现——关键在于规则之间的相互作用，而非规则本身。"</b>',
    '<font size="9" color="#5f6b7a">——<b>斯蒂芬·沃尔弗拉姆（Stephen Wolfram）</b>，'
    '《一种新科学》作者，通过元胞自动机证明了最简单的连接规则也能产生不可约化的复杂行为。'
    'iNEST继承这一洞见：我们不需要复杂的神经元模型，我们需要正确的连接拓扑与演化规则。</font>'))

# Hawkins
story.append(make_quote(
    '<b>"智能的本质不是算法运行在计算机上，而是大脑的架构——神经元之间的连接模式。"</b>',
    '<font size="9" color="#5f6b7a">——<b>杰夫·霍金斯（Jeff Hawkins）</b>，Palm创始人、'
    'Numenta联合创始人，在《On Intelligence》和千脑理论中反复强调：'
    '皮层柱之间的连接模式——而非单个神经元或单个皮层柱——才是智能的物理基础。</font>'))

# Hinton
story.append(make_quote(
    '<b>"大脑不是一台计算机。它是连接主义者机器——知识存储在连接的权重之中。"</b>',
    '<font size="9" color="#5f6b7a">——<b>杰弗里·辛顿（Geoffrey Hinton）</b>，'
    '深度学习三巨头之一、2024年诺贝尔物理学奖得主，毕生致力于让机器通过连接权重来学习。'
    '但即使是深度学习，其"连接"仍局限于软件层面的抽象——iNEST要把它带入物理现实。</font>'))

# Prigogine
story.append(make_quote(
    '<b>"非平衡是有序之源。"</b>',
    '<font size="9" color="#5f6b7a">——<b>伊利亚·普利高津（Ilya Prigogine）</b>，'
    '1977年诺贝尔化学奖得主，耗散结构理论创始人。他证明远离平衡态的开放系统可以自发形成有序结构。'
    'iNEST视智能涌现为一种"认知耗散结构"——能量流经复杂网络，秩序与智能自然生长。</font>'))

# Friston
story.append(make_quote(
    '<b>"任何自组织系统必须最小化其自由能——这既是感知，也是行动，更是一切智能行为的统一原理。"</b>',
    '<font size="9" color="#5f6b7a">——<b>卡尔·弗里斯顿（Karl Friston）</b>，'
    '全球被引最高的神经科学家，自由能原理与主动推理框架提出者。'
    '他为涌现智能的物理学基础提供了统一的理论语言，iNEST将其作为核心理论支柱之一。</font>'))

# Minsky
story.append(make_quote(
    '<b>"大脑不过是由肉做成的机器——关键是它如何连接。"</b>',
    '<font size="9" color="#5f6b7a">——<b>马文·明斯基（Marvin Minsky）</b>，'
    '人工智能之父之一、图灵奖得主，《心智社会》作者。他最早提出智能由大量简单"智能体"的交互产生，'
    '开创了从连接与交互理解智能的先河。</font>'))

# Simon
story.append(make_quote(
    '<b>"复杂性常常采取层级结构的形式——而层级系统是由不同子系统之间的关系来定义的。"</b>',
    '<font size="9" color="#5f6b7a">——<b>赫伯特·西蒙（Herbert A. Simon）</b>，'
    '诺贝尔经济学奖得主、图灵奖得主，在《人工科学》中提出复杂性的层级结构理论：'
    '复杂系统本质上是可分解的子系统网络，其行为由子系统间的连接关系所决定。</font>'))

# Closing belief
story.append(make_quote(
    '<b>我们不是在构建一个更快的计算机——我们在构建一个更接近大脑智能涌现条件的物理系统。</b>'))


# ═════════════════════ Ch2: 技术路线 ═════════════════════
story.append(h2("二、技术路线：复杂网络 × 神经形态 × 物理实现"))
story.append(body(
    'iNEST的技术理念可以凝练为一句话：<b>将类脑神经网络的连接拓扑直接映射到物理芯片的互联结构中，'
    '以真实电子信号驱动网络涌现行为。</b>'))

story.append(h3("2.1 三大支柱"))

story.append(body(
    '<font face="' + FONT_SANS + '"><b>① 复杂网络理论与拓扑演化</b></font>'))
story.append(body(
    '大脑不是前馈网络，而是一个具有小世界、无标度、社区结构和临界动力学的复杂网络。'
    'iNEST以CST（Complex Systems Topology）理论框架为核心，'
    '系统研究连接拓扑的静态规律与动态演化机制。'
    '核心成果包括：复杂网络涌现条件的形式化描述、'
    '拓扑临界阈值的第一性原理推导、以及基于信息论的最优连接度分布。'))

story.append(body(
    '<font face="' + FONT_SANS + '"><b>② 脉冲神经网络与类脑学习规则</b></font>'))
story.append(body(
    '抛弃反向传播，回归生物启发的局部学习规则。iNEST在STDP（脉冲时序依赖可塑性）基础上，'
    '发展出拓扑感知的强化学习规则（Topology-Aware STDP），'
    '使网络能同时优化"何时放电"（时序）和"与谁连接"（拓扑）两个维度。'))

story.append(body(
    '<font face="' + FONT_SANS + '"><b>③ 软件定义互连与晶上系统</b></font>'))
story.append(body(
    '以SDI（软件定义互连）技术实现神经形态连接的物理映射，'
    '以SDSoW（软件定义晶上系统）实现芯片级的超大规模集成。'
    '28nm成熟工艺已完全满足需求——我们的优势在架构，不在制程。'))

story.append(h3("2.2 核心逻辑链"))
story.append(make_quote(
    '连接拓扑的复杂度 → 网络信息处理能力 → '
    '临界动力学特征 → 涌现智能行为 → 可观测的认知能力'))
story.append(body(
    '这不是一条"算力翻倍就能逼近智能"的工程优化曲线——这是一条从物理结构到认知能力的涌现曲线。'
    '它不以FLOPS衡量，而以网络拓扑的复杂度、信息容量和临界指数来衡量。'))

# ═════════════════════ Ch3: 整体进展 ═════════════════════
story.append(h2("三、整体进展：我们走到了哪里"))

story.append(h3("3.1 理论层"))
story.append(body(
    '已完成CST理论框架的核心构建，包括：复杂网络涌现条件的形式化描述、'
    '临界点附近的标度律推导、以及基于信息瓶颈理论的拓扑优化准则。'
    '在Physical Review E、Chaos、Neural Networks等期刊发表多篇理论论文。'))

story.append(h3("3.2 仿真层"))
story.append(body(
    '自研iNEST-Sim仿真平台已实现百万级节点规模的复杂网络动力学模拟。'
    '平台支持可配置的拓扑生成器、多种SNN学习规则、'
    '以及涌现行为的自动检测与分析模块。'
    '在中等规模（10万节点）上已成功复现神经科学中的SOC（自组织临界）特征。'))

story.append(h3("3.3 硬件层"))
story.append(body(
    '基于SDI架构的验证原型已完成设计，正在推进流片。'
    '该原型以28nm工艺实现可重构的类脑连接拓扑，支持片上学习与实时拓扑重构。'))

story.append(h3("3.4 生态信号"))
story.append(body(
    '我们不是唯一看到这条路的人。2025-2026年，中国学术界和产业界正在形成显著的共振：'))
story.append(make_signals([
    ("复旦大学：",
     '已将"介观尺度开放智能计算"列为"十五五"重点建设二级学科，'
     '标志着介观智能计算正式进入中国高等教育学科体系。'),
    ("中国科协：",
     '将"类生物计算范式的第一性原理与介观尺度实现机制"列入2025年度前沿科学问题，'
     '表明国家最高学术机构已将该方向视为战略前沿。'),
    ("SDSoW专项：",
     '软件定义晶上系统列为国家、国防发展专项或重点建设方向，'
     '列入新质生产力技术备选清单——iNEST的核心硬件架构获得国家级战略背书。'),
]))
story.append(body(
    '这不仅仅是利好消息——这预示着一次系统性变革正在到来。'
    '当学科建设、前沿科学问题和国家战略三个维度同时汇聚到同一个方向时，'
    '范式转换不再是一种可能性，而是正在发生的历史。'))


# ═════════════════════ Ch4: 未来规划 ═════════════════════
story.append(h2("四、未来规划：从验证到涌现"))

story.append(body(
    'iNEST制定了从感知到超级智能的<b>智涌脑（Emergent Brain）</b>演进路线图。'
    '我们的核心指标不是传统意义上的"算力"——而是<b>网络连接规模和拓扑复杂度</b>。'
    '每一代升级的不是算力翻倍，而是网络的拓扑复杂度跨越新的临界阈值。'))

# Roadmap table
def th_cell(text):
    return Paragraph('<font face="' + FONT_SANS + '"><b>' + text + '</b></font>', S["th"])

def td_cell(text, bold=False):
    face = FONT_SANS if bold else FONT_SERIF
    b1, b2 = ("<b>", "</b>") if bold else ("", "")
    return Paragraph('<font face="' + face + '">' + b1 + text + b2 + '</font>', S["tc"])

roadmap_header = [
    th_cell("发展阶段"), th_cell("时间"), th_cell("核心特征"),
    th_cell("网络规模"), th_cell("智能级别"), th_cell("标志性能力"),
]
roadmap_rows = [
    ["感知",    "2025-2026", "类脑感知", "10⁶~10⁷连接",   "初级感知",  "视觉/听觉模式识别"],
    ["认知",    "2026-2028", "涌现认知", "10⁷~10⁸连接",   "认知级",    "逻辑推理、语言理解"],
    ["通用",    "2029-2031", "通用涌现", "10⁹~10¹⁰连接",  "通用级",    "多模态、迁移学习、元认知萌芽"],
    ["超人",    "2032-2035", "超人涌现", "10¹¹~10¹²连接", "超人级",    "创造性思维、自主科研探索"],
    ["超级智能","2035+",     "超级涌现", ">10¹⁴连接",     "超越人类级","跨领域知识整合，自主科学探索"],
]

col_w = [CONTENT_W*0.10, CONTENT_W*0.10, CONTENT_W*0.13,
         CONTENT_W*0.16, CONTENT_W*0.12, CONTENT_W*0.39]
data = [roadmap_header]
for row in roadmap_rows:
    data.append([td_cell(row[0], True)] + [td_cell(x) for x in row[1:]])
roadmap_t = Table(data, colWidths=col_w, repeatRows=1)
style_cmds = [
    ("BACKGROUND", (0,0), (-1,0), INK),
    ("TEXTCOLOR", (0,0), (-1,0), white),
    ("ALIGN", (0,0), (-1,-1), "LEFT"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
    ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("GRID", (0,0), (-1,-1), 0.5, RULE),
]
for i in range(1, len(roadmap_rows) + 1):
    if i % 2 == 0:
        style_cmds.append(("BACKGROUND", (0,i), (-1,i), TABLE_STRIPE))
roadmap_t.setStyle(TableStyle(style_cmds))
story.append(roadmap_t)
story.append(sp(2*mm))

story.append(body(
    '<b>核心逻辑：每一代升级的不是"算力翻倍"，而是网络的拓扑复杂度跨越新的临界阈值。</b>'
    '这不是在做更大的计算机——这是在做更接近生物智能涌现条件的物理网络。'))
story.append(make_quote(
    '<b>我们走的不是一条捷径。我们走的是一条在本质意义上更正确的路。</b>'))

# ═════════════════════ Ch5: 为什么是我们 ═════════════════════
story.append(h2("五、为什么是我们，为什么是现在"))

story.append(h3("5.1 非对称优势"))
story.append(body('在中国，我们拥有这个方向上独特的位置：'))

advantages = [
    '<b>工艺中立</b>：不依赖极限半导体工艺。28nm起步即可，'
    '当对手在2nm以下越跑越贵的时候，我们可以用成熟工艺走出自己的路。',
    '<b>理论先发</b>：在"物理复杂网络智能涌现"这一方向上，'
    '我们的CST理论框架和跨学科方法论体系处于全球领先水平。'
    '目前全球尚无其他团队在同一维度上建立起完整的"理论→仿真→硬件"闭环。',
    '<b>赛道转换</b>：这不是在同一个维度上追赶对手，而是开辟一个全新的竞争维度。'
    '不是"弯道超车"，而是<b>"换道前行"</b>。',
]
for adv in advantages:
    story.append(body(adv))

story.append(body(
    '全球AI界刚刚开始意识到算力路线的天花板，但绝大多数团队仍然在原有范式内寻找突破。'
    '正是这个"大多数还在原来的路上"的时刻，给了先行者最大的时间窗口。'
    '范式转换从来不是从旧范式的领先者那里发生的——'
    '它总是来自那些愿意回到第一性、愿意走不同路的人。'))

story.append(h3("5.2 我们寻找什么样的伙伴"))
story.append(body('我们最需要的东西不是经费，不是设备，而是<b>人</b>。'))
story.append(body(
    '我们需要的人，不一定是已经功成名就的教授或论文等身的学者——'
    '当然，我们也非常欢迎他们。我们更需要的是：'))

traits = [
    '在深夜读Beggs & Plenz的SOC论文读到心跳加速的博士生——'
    '因为你知道这不仅仅是一篇神经科学论文，而是蕴含着更深刻的物理原理',
    '对"更大的模型就是更好的智能"这句话本能地感到不安的研究者——'
    '因为你的直觉告诉你，大自然是不会用1.8万亿参数和1亿美元电费来产生智能的',
    '被自由能原理的优雅所击中、但又苦恼于不知道如何将其工程化的青年学者——'
    '因为你觉得理论和实践之间应该有一座桥，只是还没找到桥的位置',
    '相信复杂系统科学能改变世界、但在这个"深度学习统治一切"的时代里感到孤独的人——'
    '因为你看到了一条不同的路，只是一个人走有点寂寞',
    '愿意把自己的学术生涯押在一个"非共识"方向上的冒险者——'
    '因为你知道，所有真正重要的工作在刚开始时都是"非共识"的',
]
for t in traits:
    story.append(body('• ' + t))

story.append(sp(2*mm))
story.append(make_callout(
    '<font face="' + FONT_SANS + '"><b>如果你读到这里，内心产生了一种'
    '"这就是我一直想说但不知道该怎么说的东西"的感觉——那么，请相信你的直觉。</b>'
    '这种直觉比任何简历和推荐信都重要。'
    '因为它意味着你已经看到了那条不同的路，'
    '你缺少的可能只是一个团队、一个平台、一个和你一样相信这条路的人。</font>'
    '<br/><br/>'
    '<font face="' + FONT_SANS + '"><b>来加入我们吧。</b>一起回到第一性，'
    '一起从无到有地构建一套全新的智能范式，'
    '一起在人类研究智能的历史上留下你的名字。</font>'
))


# ═════════════════════ Ch6: 联系方式 ═════════════════════
story.append(h2("六、联系方式"))
story.append(body(
    'iNEST探索团队正在开放招收博士研究生、博士后和访问学者。'
    '我们也欢迎跨机构的联合研究合作，涵盖理论、仿真、工程、应用等各个层面。',
    "bni"))
story.append(make_callout(
    '<font face="' + FONT_SANS + '"><b>署名</b>：iNEST探索团队</font><br/>'
    '<font face="' + FONT_SANS + '"><b>研究方向</b>：物理复杂网络智能涌现——'
    '软件定义互连（SDI）与晶上系统（SDSoW）</font>'
))
story.append(body('具体联系方式请关注相关学术平台获取团队信息。', "bni"))
story.append(sp(4*mm))
story.append(HRFlowable(CONTENT_W))

# Footer
story.append(Paragraph(
    '<font face="' + FONT_SANS + '"><b>"这不是在已有路线上做更好，这是开辟一条新路线。"</b></font>',
    S["footer"]))
story.append(Paragraph("来和我们一起，把这条路走出来。", S["footer"]))
story.append(Paragraph(
    '因为有些事情，只靠一群人中的一个人是做不成的——它需要一群人，而且必须是"对的人"。',
    S["footer"]))
story.append(Paragraph("如果你觉得自己可能就是对的人，请联系我们。", S["footer"]))
story.append(sp(3*mm))
story.append(Paragraph("iNEST探索团队 · 2026年6月", S["footer"]))

# ═════════════════════ BUILD ═════════════════════
print("Building PDF with " + str(len(story)) + " flowables...")
doc.build(story)
size_kb = os.path.getsize(OUTPUT_PATH) / 1024
print("PDF generated: " + OUTPUT_PATH)
print("Size: " + str(int(size_kb)) + " KB")