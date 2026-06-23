
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
