# -*- coding: utf-8 -*-
import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

def s(layout, props):
    return {"layout": layout, "props": props}

slides = []

# P1: 封面E 光带
slides.append(s("theme09_page004", {
    "kicker": "软件定义晶上系统 · 下半场",
    "year": "2026.07",
    "titleLines": ["携手定义晶上系统下半场", "探索系统级非线性增益与智能涌现"],
    "bands": [
        {"no": "I", "t": "SDSoW进展"},
        {"no": "II", "t": "TCC拓扑中心计算"},
        {"no": "III", "t": "iNEST涌现智能"},
        {"no": "IV", "t": "战略合作"},
        {"no": "V", "t": "总结展望"}
    ],
    "footnote": "邬江兴院士带队·复旦大学·天津大学·NDSC"
}))

# P2: 标语字阵
slides.append(s("theme09_page042", {
    "lead": {"tag": "CONTENTS", "text": "报告目录"},
    "words": [
        {"text": "SDSoW进展", "en": "Part I"},
        {"text": "TCC拓扑中心计算", "en": "Part II"},
        {"text": "iNEST涌现智能", "en": "Part III"},
        {"text": "战略合作设想", "en": "Part IV"},
        {"text": "总结与展望", "en": "Summary"},
        {"text": "35页深度报告", "en": "2026.07"}
    ]
}))

# P3: 报告摘要
slides.append(s("theme09_page008", {
    "heading": "交流背景",
    "subEN": "Background & Goals",
    "pill": "核心目标",
    "summary": "推动基于SDSoW的TCC与iNEST项目合作，从第一性原理到工程落地的完整技术路线",
    "bars": [
        {"label": "理论深度", "pct": 90},
        {"label": "工程成熟度", "pct": 75},
        {"label": "合作空间", "pct": 95},
        {"label": "战略价值", "pct": 98}
    ],
    "stats": [
        {"value": "300+", "unit": "家", "label": "联盟成员"},
        {"value": "7.2T", "unit": "bps", "label": "SDI带宽"},
        {"value": "16", "unit": "个", "label": "TCC原语"},
        {"value": "6", "unit": "级", "label": "智能等级"}
    ],
    "tags": ["SDSoW", "TCC", "iNEST", "SDI", "晶上系统"],
    "barsSectionLabel": "项目评估",
    "barsTotalLabel": "综合"
}))

# P4: 金句主张
slides.append(s("theme09_page053", {
    "name": "核心命题",
    "role": "中国计算产业的换道超车",
    "tag": "战略判断",
    "badge": "P4",
    "segments": [
        {"text": "三流材料二流工艺"},
        {"text": "先进制程长期受限"},
        {"text": "单点突破难弥差距"},
        {"text": "还原论天花板已现"},
        {"text": "必须走系统论新路"}
    ]
}))

# P5: 交叉透视
slides.append(s("theme09_page051", {
    "rowHeader": "评估维",
    "unit": "",
    "note": "邬江兴院士：用超限创新解耦硬件算力与制程工艺的强绑定关系",
    "head": {"no": "P5", "en": "System-Level Gain", "cn": "系统级增益四类路线"},
    "columns": ["亚线性1+1<2", "线性1+1=2", "超线性1+1>2", "涌现1+1>N"],
    "rows": [
        {"label": "范式归属", "values": [1, 1, 5, 5]},
        {"label": "中国选择", "values": [0, 0, 5, 5]},
        {"label": "增益机制", "values": [1, 2, 5, 5]},
        {"label": "工艺依赖", "values": [5, 5, 2, 1]},
        {"label": "战略优先级", "values": [1, 1, 5, 5]},
        {"label": "代表方向", "values": [1, 1, 5, 5]}
    ]
}))

# P6: 投资展望
slides.append(s("theme09_page028", {
    "groups": [
        {"title": "诞生逻辑", "en": "SD x Wafer", "sign": "SDSoW", "items": [
            {"label": "软件定义增益", "note": "SDI六正交原语集"},
            {"label": "晶上集成增益", "note": "Chiplet+晶圆级互连"},
            {"label": "连乘纽带效应", "note": "1+1>2系统级增益"}
        ]},
        {"title": "关键突破", "en": "Breakthrough", "sign": "SDI", "items": [
            {"label": "互连=计算资源", "note": "从被动管道到一级资产"},
            {"label": "可编程神经网络", "note": "六原语实时拓扑重构"},
            {"label": "纳秒级重构", "note": "硬件原生拓扑切换"}
        ]}
    ],
    "phases": [{"time": "2019"}, {"time": "2024"}, {"time": "2027"}]
}))

# P7: 数字对决
slides.append(s("theme09_page041", {
    "note": "晶上系统已是国际共识。分水岭：用什么软件来定义",
    "badge": "P7",
    "kicker": "全球态势",
    "left": {"value": "4万亿", "unit": "晶体管", "label": "Cerebras WSE-3", "desc": "2024量产46,225mm²", "bar": 92},
    "right": {"value": "2.39x", "unit": "提升", "label": "清华映山湖", "desc": "ISCA 2025训练吞吐超Dojo", "bar": 78}
}))

# P8: 区间对比
slides.append(s("theme09_page084", {
    "endLabels": ["Gen1 2019", "Gen3 2027"],
    "unit": "倍",
    "head": {"no": "P8", "en": "SDI Chip Evolution", "cn": "SDI芯片三代跃升"},
    "items": [
        {"label": "总带宽", "a": 0.4, "b": 7.2, "sub": "400G to 7.2T 18x"},
        {"label": "Lane数量", "a": 32, "b": 128, "sub": "32 to 128 Lane 4x"},
        {"label": "单Lane速率", "a": 12.5, "b": 56, "sub": "12.5 to 56 Gbps"},
        {"label": "时延压缩", "a": 20, "b": 8, "sub": "20ns to sub-10ns"},
        {"label": "协议生态", "a": 3, "b": 6, "sub": "多模态统一承载"},
        {"label": "联盟成员", "a": 30, "b": 300, "sub": "SDSoW联盟300+"}
    ]
}))

# P9: 研究方法
slides.append(s("theme09_page011", {
    "sectionNo": "I",
    "titleCN": "SDSoW下半场",
    "titleEN": "The Second Half",
    "bubbleText": "TCC+iNEST",
    "bubbleColor": "#0E58DE",
    "stackLabels": ["TCC拓扑增益", "iNEST智能涌现", "1+1>2", "1+1>N", "系统级创新"]
}))

# P10: 篇章卡 TCC
slides.append(s("theme09_page101", {
    "chapterNo": "II",
    "titleCN": "TCC拓扑中心计算",
    "titleEN": "Topology-Centric Computing",
    "lead": "拓扑即计算 用物理网络拓扑替代冯诺依曼范式",
    "items": [
        {"label": "核心命题", "sub": "互连从管道升级为计算资源"},
        {"label": "三层正交架构", "sub": "16原语覆盖620+映射点"},
        {"label": "液态拓扑织构", "sub": "图积运算实时生成最优拓扑"},
        {"label": "先导项目验证", "sub": "FPGA原型 ASIC流片"}
    ]
}))

print("Halfway...")
# P11: 市场全景
slides.append(s("theme09_page012", {
    "quarter": [
        {"label": "Q1", "amt": 22, "cnt": 5},
        {"label": "Q2", "amt": 28, "cnt": 7},
        {"label": "Q3", "amt": 35, "cnt": 8},
        {"label": "Q4", "amt": 42, "cnt": 9}
    ],
    "month": [
        {"label": "1月"},{"label": "2月"},{"label": "3月"},{"label": "4月"},
        {"label": "5月"},{"label": "6月"},{"label": "7月"},{"label": "8月"},
        {"label": "9月"},{"label": "10月"},{"label": "11月"},{"label": "12月"}
    ],
    "summaryStats": [
        {"v": "Route=Transform", "u": "第一性原理", "l": "路由即变换"},
        {"v": "0.1pJ", "u": "拓扑边能耗", "l": "降低100倍"},
        {"v": "16+620+", "u": "原语+映射点", "l": "全场景覆盖"}
    ]
}))

# P12: 评级矩阵
slides.append(s("theme09_page067", {
    "rowHeader": "范式",
    "note": "TCC是第三代计算范式：拓扑即计算",
    "head": {"no": "P12", "en": "Three Paradigms", "cn": "三种计算范式对比"},
    "criteria": ["计算模型", "能耗主因", "扩展瓶颈", "智能适配", "互连角色", "中国机会"],
    "rows": [
        {"label": "冯诺依曼", "sub": "指令驱动存算分离", "grades": ["指令驱动", "数据搬移", "存算墙", "低", "被动管道", "受制程"]},
        {"label": "数据流", "sub": "数据驱动流式计算", "grades": ["数据驱动", "数据搬移", "通信墙", "中", "被动管道", "受带宽"]},
        {"label": "TCC", "sub": "拓扑驱动原位计算", "grades": ["拓扑驱动", "拓扑变换", "拓扑增益", "高", "一级资源", "换道超车"]}
    ]
}))

# P13: 数字海报
slides.append(s("theme09_page064", {
    "lines": ["TCC核心架构", "16原语 | 620+映射点"],
    "ticker": ["Rx6路由", "Tx6变换", "Cx4计算", "三层正交", "液态拓扑", "纳秒重构"]
}))

# P14: 阶梯递进
slides.append(s("theme09_page093", {
    "head": {"no": "P14", "en": "Three-Layer Orthogonal", "cn": "TCC三层正交架构"},
    "steps": [
        {"label": "拓扑层", "sub": "R原语定义网络连接"},
        {"label": "映射层", "sub": "T原语定义任务嵌入"},
        {"label": "执行层", "sub": "C原语定义驻留计算"},
        {"label": "正交性", "sub": "每层独立层间标准接口"},
        {"label": "液态切换", "sub": "纳秒级任务间拓扑重构"},
        {"label": "目标", "sub": "拓扑计算数据完全解耦"}
    ]
}))

# P15: 核心要点
slides.append(s("theme09_page102", {
    "head": {"no": "P15", "en": "Liquid Topology Fabric", "cn": "液态拓扑织构LTF"},
    "lead": {"tag": "核心创新", "text": "芯片拓扑像液体一样流动适配"},
    "items": [
        {"title": "元拓扑集合", "desc": "K2,Pn,Cn,Sn,Tk五类基本结构"},
        {"title": "图积运算", "desc": "笛卡尔积 张量积 强积组合"},
        {"title": "实时生成", "desc": "任意CST最优拓扑实时计算"},
        {"title": "纳秒重构", "desc": "SDI硬件原生支持"},
        {"title": "覆盖范围", "desc": "完整图 环 树 格栅 全谱系"}
    ]
}))

# P16: 关键问答
slides.append(s("theme09_page105", {
    "head": {"no": "P16", "en": "Route=Transform", "cn": "Route=Transform定理"},
    "items": [
        {"q": "核心发现？", "a": "路由操作=图拓扑变换"},
        {"q": "关键机制？", "a": "数据不必搬移拓扑原地变形"},
        {"q": "能耗量化？", "a": "拓扑边能耗约0.1pJ"},
        {"q": "对比优势？", "a": "比传统数据搬移降低100倍"},
        {"q": "物理意义？", "a": "从第一性打破冯诺依曼瓶颈"},
        {"q": "工程验证？", "a": "SDI v31硬件实测确认"}
    ]
}))

# P17: 实施路径
slides.append(s("theme09_page104", {
    "head": {"no": "P17", "en": "P-Mapping", "cn": "P-Mapping全息映射"},
    "outcome": {"tag": "成果", "text": "620+计算映射点覆盖主流AI/HPC算子"},
    "steps": [
        {"title": "算子分析", "desc": "分解计算图为拓扑模式"},
        {"title": "模式匹配", "desc": "匹配最优元拓扑模板"},
        {"title": "图积生成", "desc": "组合生成专用拓扑织构"},
        {"title": "SDI部署", "desc": "纳秒级加载到硬件拓扑层"}
    ]
}))

# P18: 批注精读
slides.append(s("theme09_page054", {
    "head": {"no": "P18", "en": "FFT-AllReduce Isomorphism", "cn": "FFT-AllReduce图同构定理"},
    "segments": [
        {"text": "FFT蝶形网络等价于AllReduce归约树"},
        {"text": "同一拓扑硬件同时服务AI和雷达"},
        {"text": "图同构发现 硬件复用 成本降半"},
        {"text": "SDI实现动态拓扑角色切换"},
        {"text": "一芯多用军民融合典型范例"},
        {"text": "TCC-Link标准统一承载"},
        {"text": "已通过CST仿真验证"}
    ],
    "notes": [
        {"lead": "应用1", "text": "大模型分布式训练"},
        {"lead": "应用2", "text": "相控阵雷达信号处理"},
        {"lead": "应用3", "text": "5G Massive MIMO"},
        {"lead": "应用4", "text": "卫星通信波束赋形"}
    ]
}))

# P19: 影像纪程
slides.append(s("theme09_page082", {
    "head": {"no": "P19", "en": "TCC Pilot Roadmap", "cn": "TCC先导项目路线"},
    "nodes": [
        {"date": "2024", "caption": "SDI v31技术验证"},
        {"date": "2025Q2", "caption": "FPGA原型平台搭建"},
        {"date": "2025Q4", "caption": "ResNet-50 BERT验证"},
        {"date": "2026Q2", "caption": "PyiNEST SDK发布"},
        {"date": "2026Q4", "caption": "ASIC流片准备"},
        {"date": "2027", "caption": "Gen3+量产验证"}
    ]
}))

# P20: 全幅图景
slides.append(s("theme09_page097", {
    "badge": "III",
    "kicker": "iNEST",
    "title": "涌现智能",
    "titleEN": "Emergent Intelligence",
    "paragraph": "极简规则xSDI韧带 硅基网络自主涌现智能。复杂网络自组织临界态是智能涌现的物理基础。",
    "tags": ["复杂网络", "自组织临界", "C.elegans 302", "六大智能等级"]
}))

# P21: 图说特写
slides.append(s("theme09_page025", {
    "points": [
        {"label": "能效鸿沟", "value": "150000x", "caption": "人脑20W vs GPU 3MW"},
        {"label": "科学问题", "value": "临界动力学", "caption": "关键不在神经元数量"},
        {"label": "自组织临界", "value": "SOC相变点", "caption": "智能涌现的物理基础"},
        {"label": "SDI使命", "value": "可编程突触", "caption": "硅基网络突触可塑性"}
    ]
}))

# P22: 景气仪表
slides.append(s("theme09_page085", {
    "badge": "P22",
    "headEn": "Six Intelligence Levels",
    "headCn": "六大智能等级",
    "items": [
        {"cn": "L1 反射 0.707", "en": "Feigenbaum alpha", "value": 15, "note": "基本反射响应"},
        {"cn": "L2 感知 1.618", "en": "Golden Ratio phi", "value": 30, "note": "环境感知能力"},
        {"cn": "L3 学习 2.718", "en": "Natural e", "value": 52, "note": "自适应学习"},
        {"cn": "L4 推理 3.142", "en": "Pi", "value": 72, "note": "逻辑推理能力"}
    ]
}))

# P23: 资本排行
slides.append(s("theme09_page035", {
    "unit": "分",
    "badge": "P23",
    "headEn": "Trinity Methodology",
    "headCn": "三位一体方法论",
    "items": [
        {"name": "物理第一性", "en": "FEP+STDP", "value": 95, "meta": "自由能最小化", "tag": "理论根基"},
        {"name": "生物启迪", "en": "C.elegans 302", "value": 88, "meta": "连接组标度律", "tag": "验证来源"},
        {"name": "SDI利剑", "en": "6 Primitives", "value": 92, "meta": "可编程突触", "tag": "工程实现"},
        {"name": "涌现机制", "en": "SOC Phase Trans", "value": 85, "meta": "自组织临界相变", "tag": "核心假说"},
        {"name": "标度律", "en": "sigma~N^0.398", "value": 78, "meta": "跨物种普适规律", "tag": "CST发现"},
        {"name": "验证手段", "en": "CST Simulation", "value": 90, "meta": "实验事实级别", "tag": "仿真平台"},
        {"name": "最终目标", "en": "Silicon Brain", "value": 80, "meta": "第一代硅基大脑", "tag": "工程愿景"}
    ]
}))

print("Part 2 done")
# P24: 同比对望
slides.append(s("theme09_page037", {
    "endLabels": ["C.elegans 302", "Hemibrain 130K"],
    "unit": "",
    "head": {"no": "P24", "en": "Cross-Species Scaling", "cn": "跨物种标度律"},
    "items": [
        {"label": "小世界系数", "sub": "4.2 C.elegans to 8.9 Hemibrain"},
        {"label": "幂律指数", "sub": "1.35 C.elegans to 2.42 Hemibrain"},
        {"label": "SC-FC耦合比", "sub": "1.8x C.elegans to 2.3x Hemibrain"},
        {"label": "雪崩KS p值", "sub": "0.22 C.elegans to 0.48 Hemibrain"},
        {"label": "同步比例", "sub": "15% C.elegans to 62% Hemibrain"},
        {"label": "信息效率", "sub": "0.70 C.elegans to 1.90 Hemibrain"}
    ]
}))

# P25: 单笔分布
slides.append(s("theme09_page090", {
    "head": {"no": "P25", "en": "CST Key Metrics", "cn": "CST仿真关键指标"},
    "axisTicks": ["0", "20", "40", "60", "80", "100", "120"],
    "rows": [
        {"label": "小世界系数", "peak": 0.72, "amp": 0.90},
        {"label": "幂律指数", "peak": 0.55, "amp": 0.88},
        {"label": "雪崩KS检验", "peak": 0.48, "amp": 0.75},
        {"label": "同步比例", "peak": 0.65, "amp": 0.85},
        {"label": "信息传输效率", "peak": 0.70, "amp": 0.92}
    ]
}))

# P26: 排名变迁
slides.append(s("theme09_page083", {
    "periodLeft": "Phase 1",
    "periodRight": "Phase 4",
    "unit": "成熟度",
    "badge": "P26",
    "headEn": "iNEST Pilot Projects",
    "headCn": "iNEST先导项目",
    "legendUp": "提升",
    "legendDown": "待推进",
    "unitLabel": "TRL",
    "items": [
        {"cn": "C.elegans 302建模"},
        {"cn": "拓扑扫描分析"},
        {"cn": "雪崩临界验证"},
        {"cn": "同步涌现观测"},
        {"cn": "忆阻器原型"},
        {"cn": "SDI-SNN融合"},
        {"cn": "CST V31仿真"},
        {"cn": "5/5生物指标"}
    ]
}))

# P27: 影像卡集
slides.append(s("theme09_page087", {
    "head": {"no": "P27", "en": "SDI + SNN Fusion", "cn": "SDI与SNN融合路径"},
    "cards": [
        {"title": "SDI角色", "caption": "可编程突触网络 六原语实时重构"},
        {"title": "SNN角色", "caption": "脉冲神经元阵列 忆阻器+CMOS"},
        {"title": "融合路径", "caption": "SDI互连xSNN计算=晶圆级集成"},
        {"title": "目标系统", "caption": "第一代中国硅基大脑原型"}
    ]
}))

# P28: 影像便当
slides.append(s("theme09_page039", {
    "head": {"no": "P28", "en": "National Strategy", "cn": "国家战略引领与合作"},
    "items": [
        {"label": "十五五布局", "sub": "发改委 科技委 重点专项"},
        {"label": "王恩东院士", "sub": "晶上训推一体服务器"},
        {"label": "李国齐团队", "sub": "内生复杂性xSDI融合"},
        {"label": "四层协同", "sub": "理论 技术 工程 生态"},
        {"label": "工作节奏", "sub": "半月联席 季度PI汇报"},
        {"label": "第二曲线", "sub": "系统级增益新赛道"}
    ]
}))

# P29: 估值梯队
slides.append(s("theme09_page058", {
    "badge": "P29",
    "headEn": "National Strategy Layout",
    "headCn": "国家战略布局",
    "tiers": [
        {"band": "国家发改委", "en": "NDRC", "count": 95, "range": "十五五规划", "reps": ["晶上系统方向", "重点专项支持"]},
        {"band": "科技委", "en": "MOST", "count": 90, "range": "前沿布局", "reps": ["重点研发计划", "军科委项目", "NSF重大"]},
        {"band": "SDSoW联盟", "en": "Alliance", "count": 300, "range": "产业生态", "reps": ["300+成员", "全产业链覆盖", "产学研协同"]},
        {"band": "SDI芯片", "en": "SDI Chips", "count": 85, "range": "三代验证", "reps": ["Gen1量产", "Gen2批产", "Gen3研发"]},
        {"band": "合作窗口", "en": "Window", "count": 98, "range": "2026-2027", "reps": ["十五五开局", "NSF申报季", "ASIC流片窗"]}
    ]
}))

# P30: 双联对照
slides.append(s("theme09_page060", {
    "head": {"no": "P30", "en": "Wang Endong Cooperation", "cn": "与王恩东院士团队合作"},
    "panels": [
        {"title": "王院士优势", "sub": "高效能服务器与存储技术重点实验室", "caption": "定义了中国服务器产业旗帜", "label": "产业引领"},
        {"title": "合作方向", "sub": "晶上训推一体高效能服务器", "caption": "SDSoW+TCC重塑AI服务器架构", "label": "技术融合"},
        {"title": "核心价值", "sub": "系统级增益工程落地", "caption": "SDI互连嵌入主板实现拓扑原生计算", "label": "工程突破"}
    ]
}))

# P31: 区域画像
slides.append(s("theme09_page066", {
    "head": {"no": "P31", "en": "Li Guoqi Cooperation", "cn": "与李国齐研究员团队合作"},
    "axes": [
        {"label": "理论深度", "max": 5, "unit": "级"},
        {"label": "工程转化", "max": 5, "unit": "级"},
        {"label": "互补性", "max": 5, "unit": "级"},
        {"label": "创新潜力", "max": 5, "unit": "级"},
        {"label": "战略价值", "max": 5, "unit": "级"}
    ],
    "objects": [
        {"label": "内生复杂性理论", "vals": [5, 2, 5, 5, 5]},
        {"label": "瞬悉大模型", "vals": [4, 3, 4, 4, 4]},
        {"label": "SDI互连架构", "vals": [3, 5, 5, 5, 5]},
        {"label": "CST仿真平台", "vals": [4, 4, 5, 4, 4]},
        {"label": "晶圆级集成", "vals": [2, 5, 4, 5, 5]}
    ]
}))

print("Part 3 done")
# P32: 公司版图
slides.append(s("theme09_page072", {
    "badge": "P32",
    "headEn": "Four Cooperation Directions",
    "headCn": "四大合作方向",
    "items": [
        {"name": "类脑理论", "sector": "基础研究", "val": 95, "round": "Phase1"},
        {"name": "晶圆系统", "sector": "工程研制", "val": 88, "round": "Phase2"},
        {"name": "国防项目", "sector": "应用落地", "val": 82, "round": "Phase2"},
        {"name": "NSF重大", "sector": "项目申报", "val": 90, "round": "2026.09"},
        {"name": "工具共建", "sector": "平台建设", "val": 78, "round": "Phase1"},
        {"name": "原型研制", "sector": "硬件验证", "val": 75, "round": "Phase3"},
        {"name": "论文联合", "sector": "学术产出", "val": 92, "round": "持续"},
        {"name": "专利布局", "sector": "知识产权", "val": 85, "round": "持续"},
        {"name": "人才培养", "sector": "队伍建设", "val": 80, "round": "持续"},
        {"name": "开源社区", "sector": "生态建设", "val": 70, "round": "Phase2"},
        {"name": "标准制定", "sector": "行业引领", "val": 72, "round": "Phase3"},
        {"name": "产业推广", "sector": "商业转化", "val": 68, "round": "Phase4"}
    ]
}))

# P33: 层级冰柱
slides.append(s("theme09_page073", {
    "rootLabel": "SDSoW生态",
    "rootValue": "35",
    "unit": "项",
    "head": {"no": "P33", "en": "Key Projects", "cn": "重点项目策划"},
    "groups": [
        {"label": "理论联合", "sub": "涌现动力学统一框架", "value": 8, "children": [
            {"label": "联合发表", "value": 3}, {"label": "专利申请", "value": 2}, {"label": "理论自洽", "value": 3}
        ]},
        {"label": "工具共建", "sub": "CST+瞬悉+PyiNEST", "value": 7, "children": [
            {"label": "CST仿真", "value": 3}, {"label": "PyiNEST SDK", "value": 2}, {"label": "瞬悉集成", "value": 2}
        ]},
        {"label": "原型研制", "sub": "FPGA ASIC流片", "value": 8, "children": [
            {"label": "FPGA验证", "value": 3}, {"label": "忆阻器阵列", "value": 2}, {"label": "ASIC流片", "value": 3}
        ]},
        {"label": "生态推广", "sub": "开源+产业+人才", "value": 7, "children": [
            {"label": "开源社区", "value": 2}, {"label": "产业资源", "value": 3}, {"label": "人才培养", "value": 2}
        ]},
        {"label": "项目申报", "sub": "NSF+军科委+重点研发", "value": 5, "children": [
            {"label": "NSF重大", "value": 2}, {"label": "军科委", "value": 2}, {"label": "重点研发", "value": 1}
        ]}
    ],
    "rootBadgeLabel": "总计",
    "axisLabelL0": "合作领域",
    "axisLabelL1": "子任务数",
    "axisLabelL2": "细分项"
}))

# P34: 月度热力
slides.append(s("theme09_page077", {
    "rows": [
        {"cn": "理论合作", "vals": [90,85,80,88,92,95,88,82,86,90,94,92]},
        {"cn": "技术合作", "vals": [75,78,82,85,88,90,85,80,83,86,88,85]},
        {"cn": "工程合作", "vals": [60,65,70,72,75,78,72,68,70,73,76,78]},
        {"cn": "生态合作", "vals": [55,58,62,65,68,70,65,60,63,66,68,70]},
        {"cn": "半月联席", "vals": [95,95,95,95,95,95,95,95,95,95,95,95]},
        {"cn": "季度汇报", "vals": [80,80,85,85,90,90,85,85,90,90,95,95]}
    ]
}))

# P35: 结语
slides.append(s("theme09_page111", {
    "brand": "SDSoW",
    "headline": "携手开辟第二曲线",
    "headlineEN": "Create the Second Curve",
    "statement": "在工艺受限的十年窗口，路B是唯一能赢的路",
    "contact": [
        {"label": "邬江兴院士团队", "value": "复旦大学"},
        {"label": "SDSoW联盟", "value": "300+"}
    ]
}))

# --- BUILD ---
goal = {
    "title": "SDSoW下半场：TCC与iNEST",
    "goal": "推动基于SDSoW的TCC与iNEST项目合作，探索系统级非线性增益与智能涌现",
    "audience": "王恩东院士实验室 / 中科院自动化所李国齐团队",
    "owner": "邬江兴院士团队 复旦大学 天津大学 NDSC",
    "randomSeed": "sdsow-tcc-inest-20260713-d4",
    "pageCount": 35,
    "themePack": "theme09",
    "slides": slides
}

out = r"D:\Obsidian\home\work\.openclaw\workspace\50_Output\59_Presentations\SDSoW_TCC_iNEST_20260713\goal.json"
with open(out, 'w', encoding='utf-8') as f:
    json.dump(goal, f, ensure_ascii=False, indent=2)

print(f"OK: {len(slides)} slides written to goal.json")
print(f"Title: {goal['title']}")