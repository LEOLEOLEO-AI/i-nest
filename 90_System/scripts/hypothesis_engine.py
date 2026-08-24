#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hypothesis_engine.py — 从跨域桥接自动生成研究假设
读取 cross_domain_insights.md 中的高强度桥接，
转换为正式假设提案写入 hypothesis_registry.json。

规则（防失控）：
1. 只新增 status="proposed" 的假设，不修改已有假设
2. 桥接强度 >= 100 才值得生成假设
3. 去重：同名桥接不重复生成
"""
import json, re, sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
VAULT = Path(r"D:\Obsidian\vault")
META = VAULT / "99_Meta"
BRIDGE_FILE = VAULT / "wiki" / "cross_domain_insights.md"
HYP_FILE = META / "hypothesis_registry.json"

STRENGTH_THRESHOLD = 100

# 桥接名 → 假设模板映射（可人工扩展）
HYPOTHESIS_TEMPLATES = {
    "SDI_Plastic_Interconnect": {
        "title": "TCC×iNEST: SDI软件定义互连可实现类突触可塑性拓扑重构",
        "rationale": "将STDP权重更新规则映射到NoC路由表更新，实现互连拓扑按负载自适应调整",
        "test": "在sdi_network仿真框架中对比固定拓扑vs可塑拓扑的吞吐/延迟",
    },
    "Chiplet_Heterogeneous_Neuromorphic": {
        "title": "TCC×iNEST: Chiplet异构集成CMOS+忆阻器crossbar可实现存算一体神经形态加速",
        "rationale": "1M1T1R突触神经元阵列通过3DHI堆叠与逻辑chiplet集成，消除von Neumann瓶颈",
        "test": "估算面积/能耗/延迟 vs GPU baseline，验证超加性增益(H1)",
    },
    "NoC_Spiking_Routing": {
        "title": "TCC×iNEST: NoC路由算法为事件驱动spike包重设计可降低延迟一个数量级",
        "rationale": "spike稀疏性+异步性使传统同步流水线浪费严重，event-driven路由可大幅提升效率",
        "test": "在仿真中实现async路由协议，对比packet latency分布",
    },
    "WaferScale_Neuromorphic": {
        "title": "TCC×iNEST: 晶圆级集成可在单die上实现百万级神经元实时仿真",
        "rationale": "Cerebras CS-2已证明晶圆级AI推理可行，扩展至SNN域",
        "test": "映射Izhikevich神经元阵列到wafer-scale mesh，评估通信瓶颈",
    },
    "3DIC_Neural_Stacking": {
        "title": "TCC×iNEST: 3D-IC堆叠模拟皮层柱状架构可实现密集神经处理层",
        "rationale": "皮层的垂直柱状结构与3D堆叠的层间TSV连接天然对应",
        "test": "建立层间连接模型，对比2D平面布局的信息传递效率",
    },
    "Topology_Brain_Connectome": {
        "title": "TCC×iNEST: 脑连接组拓扑模式可启发晶圆级NoC最优拓扑设计",
        "rationale": "大脑的小世界/模块化拓扑是亿年优化的结果，直接移植到芯片设计",
        "test": "用连接组数据生成NoC拓扑，vs mesh/torus对比性能",
    },
    "Memory_Wall_Neuromorphic_Solution": {
        "title": "TCC×iNEST: 神经形态内存内计算可突破晶圆级系统的memory wall",
        "rationale": "存算一体消除数据搬运开销，解决大规模SNN的访存瓶颈",
        "test": "建模memristor crossbar的能效比 vs SRAM cache方案",
    },
}


def parse_bridges():
    txt = BRIDGE_FILE.read_text(encoding="utf-8", errors="ignore") if BRIDGE_FILE.exists() else ""
    bridges = {}
    for m in re.finditer(r"### (\S+)\s*\(Strength: (\d+)\)", txt):
        name, strength = m.group(1), int(m.group(2))
        if strength >= STRENGTH_THRESHOLD and name in HYPOTHESIS_TEMPLATES:
            bridges[name] = strength
    return bridges


def load_hypotheses():
    if HYP_FILE.exists():
        try:
            return json.loads(HYP_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"hypotheses": [], "last_updated": ""}


def generate():
    bridges = parse_bridges()
    registry = load_hypotheses()
    existing = {h.get("id"): h for h in registry.get("hypotheses", [])}
    existing_titles = {h.get("title", "") for h in existing.values()}

    # 找到最大编号
    max_num = 0
    for h in existing.values():
        hid = h.get("id", "")
        m = re.match(r"H(\d+)", hid)
        if m:
            max_num = max(max_num, int(m.group(1)))

    added = []
    next_id = max_num + 1
    for name, strength in sorted(bridges.items(), key=lambda x: -x[1]):
        tpl = HYPOTHESIS_TEMPLATES[name]
        title = tpl["title"]
        if title in existing_titles:
            continue  # 已有，跳过
        hid = f"H{next_id}"
        entry = {
            "id": hid,
            "title": title,
            "status": "proposed",
            "evidence": f"Cross-domain bridge: {name} (strength={strength})",
            "rationale": tpl.get("rationale", ""),
            "test_method": tpl.get("test", ""),
            "created": datetime.now().strftime("%Y-%m-%d"),
            "source_bridge": name,
        }
        registry["hypotheses"].append(entry)
        added.append(f"{hid}: {title}")
        next_id += 1
        print(f"  + [{hid}] {title} (bridge={name}, strength={strength})")

    if added:
        registry["last_updated"] = datetime.now().isoformat()
        HYP_FILE.parent.mkdir(parents=True, exist_ok=True)
        HYP_FILE.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[hypothesis_engine] 新增 {len(added)} 条假设 → {HYP_FILE}")
    else:
        print("[hypothesis_engine] 无新假设需添加")
    return len(added)


if __name__ == "__main__":
    n = generate()
    sys.exit(0 if n >= 0 else 1)
