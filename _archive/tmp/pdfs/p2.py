
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
