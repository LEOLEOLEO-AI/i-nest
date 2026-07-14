# -*- coding: utf-8 -*-
"""Local LLM-free classifier for 20_Processing ambiguous files"""

import json, shutil, re
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
PROC = VAULT / "20_Processing"

# === Expanded classification rules ===
TCC_KW = {
    "architecture": ["wafer", "晶圆", "sdsow", "chiplet", "2.5d", "3dic", "3d-ic",
                     "封装", "packaging", "pcie", "cxl", "ucc", "noc", "片上网络",
                     "network-on-chip", "互联", "interconnect", "交换芯片", "switch",
                     "router", "路由", "先进计算", "微纳电子", "晶上", "晶上系统"],
    "compute": ["算力", "comput", "并行", "parallel", "数据中心", "datacenter",
                "存算一体", "processing-in-memory", "pim", "near-memory",
                "集合通信", "collective", "ccu", "tcc", "拓扑中心"],
    "system": ["sdi", "软件定义", "software-defined", "dtco", "stco", "协同设计",
               "co-design", "井芯", "国产芯片", "自主可控"],
}

INEST_KW = {
    "neuroscience": ["神经", "neuron", "类脑", "brain", "neuromorphic", "突触",
                     "synapse", "脉冲", "spike", "snn", "认知", "cognitive",
                     "意识", "consciousness", "脑科学", "神经科学"],
    "emergence": ["涌现", "emergence", "复杂度", "complexity", "复杂网络",
                  "complex network", "临界", "critical", "分形", "fractal",
                  "自组织", "self-organiz", "动力学", "dynamics", "混沌", "chaos"],
    "ai_bio": ["inest", "哈密顿", "hamiltonian", "hnn", "物理信息",
               "physics-informed", "pinn", "liquid", "可塑", "plasticity",
               "hebbian", "拓扑深度", "几何约束", "介观", "mesoscopic"],
}

VALUE_KW = {
    "paper": ["论文", "paper", "发表", "publish", "理论", "theory", "框架", "framework",
              "模型", "model", "综述", "survey", "review", "方法", "method"],
    "patent": ["专利", "patent", "发明", "invent", "方法", "装置", "系统", "架构",
               "芯片", "电路", "设计", "实现"],
    "simulation": ["仿真", "simulat", "实验", "experiment", "验证", "verif",
                   "测试", "test", "数据", "data", "cst", "spice", "建模", "model"],
    "code": ["代码", "code", "算法", "algorithm", "实现", "implement",
             "编程", "program", "开发", "develop", "框架", "sdk", "api"],
}

def classify_by_content(content, filename):
    cl = content.lower()
    fn = filename.lower()
    
    tcc_score = 0
    inest_score = 0
    
    for category, kws in TCC_KW.items():
        for kw in kws:
            if kw in cl or kw in fn:
                tcc_score += 1
    
    for category, kws in INEST_KW.items():
        for kw in kws:
            if kw in cl or kw in fn:
                inest_score += 1
    
    if tcc_score > inest_score:
        return "TCC", tcc_score
    elif inest_score > tcc_score:
        return "iNEST", inest_score
    else:
        return "both", 0

def extract_insights(content, direction):
    """Extract key sentences as insights"""
    lines = [l.strip() for l in content.split("\n") if len(l.strip()) > 20]
    insights = []
    for line in lines[:10]:
        line = re.sub(r'^#+\s*', '', line)
        line = re.sub(r'\[.*?\]\(.*?\)', '', line)
        line = re.sub(r'[>\-\*\|\`]', '', line).strip()
        if len(line) > 15 and len(line) < 200:
            insights.append(line)
    return insights[:3] if insights else ["内容较短，无法提取关键句"]

def assess_value(content):
    scores = {}
    cl = content.lower()
    for cat, kws in VALUE_KW.items():
        score = sum(1 for kw in kws if kw in cl)
        if score >= 4:
            scores[cat] = "高"
        elif score >= 2:
            scores[cat] = "中"
        elif score >= 1:
            scores[cat] = "低"
        else:
            scores[cat] = "无"
    return scores

# === Process ===
ambig = json.loads((VAULT / "60_MOC" / "ambig_files.json").read_text(encoding="utf-8"))

results = []
tcc_count = 0
inest_count = 0
both_count = 0

for item in ambig:
    fpath = VAULT / item["path"]
    if not fpath.exists():
        continue
    
    content = fpath.read_text(encoding="utf-8", errors="ignore")
    direction, score = classify_by_content(content, fpath.name)
    insights = extract_insights(content, direction)
    value = assess_value(content)
    
    result = {
        "file": item["path"],
        "filename": fpath.name,
        "direction": direction,
        "score": score,
        "insights": insights,
        "paper_value": value["paper"],
        "patent_value": value["patent"],
        "sim_value": value["simulation"],
        "code_value": value["code"],
    }
    results.append(result)
    
    # Move file
    if direction == "TCC":
        dst = VAULT / "30_TCC" / "32_Tech" / fpath.name
        tcc_count += 1
    elif direction == "iNEST":
        dst = VAULT / "40_iNEST" / "42_Tech" / fpath.name
        inest_count += 1
    else:
        dst = VAULT / "30_TCC" / "32_Tech" / fpath.name
        both_count += 1
    
    if not dst.exists():
        shutil.move(str(fpath), str(dst))

print(f"TCC: {tcc_count}, iNEST: {inest_count}, Both: {both_count}")

# Save results
out = {
    "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
    "total": len(results),
    "summary": {"TCC": tcc_count, "iNEST": inest_count, "both": both_count},
    "results": results
}
(VAULT / "60_MOC" / "classify_results.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Results saved: 60_MOC/classify_results.json")
