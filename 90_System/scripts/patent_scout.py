#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patent_scout.py — 专利侦察：从假设和桥接中识别可专利方向

规则：
1. 只分析 status != "proven" 的假设（已证的是论文方向，不是专利）
2. 涉及"新颖硬件配置/方法/算法"的假设有专利潜力
3. 产出专利披露草案（不是正式申请文件）
"""
import json, re, sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
VAULT = Path(r"D:\Obsidian\vault")
META = VAULT / "99_Meta"
OUT_DIR = META / "patent_disclosures"
HYP_FILE = META / "hypothesis_registry.json"

# 假设 → 专利可行性评估规则
PATENT_CRITERIA = {
    "hardware": ["chiplet", "互连", "晶圆", "3D", "集成", "memristor", "crossbar", "NoC"],
    "method": ["算法", "路由", "拓扑", "调度", "映射"],
    "system": ["架构", "框架", "系统", "平台"],
}

def assess_patentability(hyp):
    """评估一个假设的专利潜力"""
    title = hyp.get("title", "").lower()
    scores = {}
    for category, keywords in PATENT_CRITERIA.items():
        score = sum(1 for kw in keywords if kw in title)
        if score > 0:
            scores[category] = score
    
    total = sum(scores.values())
    if total >= 2:
        return "HIGH", scores
    elif total == 1:
        return "MEDIUM", scores
    return "LOW", scores


def generate_disclosure(hyp, level, scores):
    """生成专利披露草案"""
    hid = hyp.get("id", "?")
    title = hyp.get("title", "")
    rationale = hyp.get("rationale", "")
    test = hyp.get("test_method", "")
    bridge = hyp.get("source_bridge", "")
    
    # 从标题提取技术领域
    tech_field = "计算机体系结构 / 智能计算"
    if any(kw in title for kw in ["互连", "NoC", "路由"]):
        tech_field = "片上网络 / 互连架构"
    elif any(kw in title for kw in ["忆阻", "memristor", "神经形态"]):
        tech_field = "神经形态计算硬件"
    elif any(kw in title for kw in ["chiplet", "集成", "晶圆"]):
        tech_field = "异构集成封装"
    elif any(kw in title for kw in ["涌现", "临界", "emergence"]):
        tech_field = "复杂系统智能"
    
    disclosure = f"""---
title: "专利披露·{hid}"
hypothesis: "{hid}"
date: {datetime.now().strftime("%Y-%m-%d")}
patentability: {level}
categories: {json.dumps(list(scores.keys()))}
type: patent-disclosure
---

# 专利披露草案 · {hid}

> **可专利性**: {'🟢 ' + level if level == 'HIGH' else '🟡 ' + level} | **技术领域**: {tech_field}
> 本文件由 patent_scout 自动生成，需专利代理人审核后方可申请。

## 一、发明名称

{title}

## 二、技术领域

{tech_field}

## 三、要解决的技术问题

{rationale or title}

## 四、技术方案（核心权利要求方向）

基于假设 {hid} 和跨域桥接 {bridge}：

1. **核心方法**: {title}
2. **验证方式**: {test}
3. **创新点**: 将TCC×iNEST交叉方法应用于{tech_field}

## 五、有益效果

- 突破传统计算架构限制
- 为TCC/iNEST交叉领域提供新的硬件/软件协同设计路径

## 六、后续行动

- [ ] 补充具体实施例（仿真数据或原型实验结果）
- [ ] 检索现有专利（CNKI/Derivative/USPTO）
- [ ] 联系专利代理人评估
- [ ] 与相关论文发表策略协调（先申专再发论文）

---
*由 patent_scout.py 于 {datetime.now().isoformat()} 自动生成*
*来源假设: {hid} | 来源桥接: {bridge}*
"""
    return disclosure


def main():
    try:
        data = json.loads(HYP_FILE.read_text(encoding="utf-8"))
        hyps = data.get("hypotheses", [])
    except:
        print("[patent_scout] 无法读取假设注册表")
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    results = []
    for h in hyps:
        if h.get("status") == "proven":
            continue  # 已证的写论文，不申专利
        
        level, scores = assess_patentability(h)
        if level in ("HIGH", "MEDIUM"):
            disclosure = generate_disclosure(h, level, scores)
            outfile = OUT_DIR / f"{h['id']}_disclosure.md"
            outfile.write_text(disclosure, encoding="utf-8")
            results.append((h["id"], level, str(outfile.name)))
            print(f"  [{level}] {h['id']}: {h.get('title','')[:50]} → {outfile.name}")
    
    print(f"\n[patent_scout] 扫描完成: {len(hyps)} 个假设中识别出 {len(results)} 个可专利方向")
    if results:
        summary_lines = [f"- {r[0]} ({r[1]}): `{r[2]}`" for r in results]
        (OUT_DIR / "_index.md").write_text(
            "# 可专利方向索引\n\n" + "\n".join(summary_lines) + "\n",
            encoding="utf-8"
        )


if __name__ == "__main__":
    main()
