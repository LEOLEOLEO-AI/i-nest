# -*- coding: utf-8 -*-
"""DeepSeek deep analysis of core TCC+iNEST research files - v2"""

import json, time, re, os
from pathlib import Path
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

VAULT = Path(r"D:\Obsidian\vault")
load_dotenv(VAULT / ".env", override=True)
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com/v1", timeout=60)

# Find files by glob + size filter
def find_research_files(directory, patterns, min_kb=5, max_files=10):
    found = []
    d = VAULT / directory
    if not d.exists():
        return found
    for pat in patterns:
        for f in d.rglob(pat):
            if f.stat().st_size > min_kb * 1024:
                rel = str(f.relative_to(VAULT))
                if rel not in [x[0] for x in found]:
                    found.append((rel, f.stat().st_size))
    found.sort(key=lambda x: -x[1])
    return found[:max_files]

# TCC: SDI, CST, topology, paradigm, chiplet, architecture
tcc_files = find_research_files("30_TCC/31_Theory", ["*SDI*", "*CST*", "*拓扑*", "*范式*", "*定理*", "*复杂度*", "*连通*"], min_kb=5)
tcc_files += find_research_files("30_TCC/32_Technology", ["*SDSoW*", "*Chiplet*", "*互联*", "*晶圆*", "*封装*", "*架构*"], min_kb=5)
tcc_files += find_research_files("30_TCC/34_Projects", ["*项目*", "*指南*", "*海河*", "*布局*"], min_kb=5)

# iNEST: emergence, complexity, neuromorphic, SNN, brain
inest_files = find_research_files("40_iNEST/41_Theory", ["*涌现*", "*复杂度*", "*理论*", "*框架*", "*因果*", "*智能*", "*意识*"], min_kb=5)
inest_files += find_research_files("40_iNEST/42_Technology", ["*神经*", "*SNN*", "*忆阻*", "*脉冲*", "*类脑*", "*突触*"], min_kb=5)

# Dedup + take top 20
seen = set()
all_files = []
for f, s in tcc_files + inest_files:
    if f not in seen:
        seen.add(f)
        all_files.append(f)

all_files = all_files[:20]

print(f"Files to analyze: {len(all_files)}")
for f in all_files:
    size = (VAULT / f).stat().st_size / 1024
    print(f"  [{size:.1f}KB] {f}")

# === Analysis ===
SYSTEM_PROMPT = """你是TCC(拓扑中心计算/晶圆级互联)和iNEST(神经形态/类脑计算)的科研分析专家。

深度分析以下文档，提取可反哺知识库的内容。输出JSON:
{
  "direction": "TCC/iNEST/both",
  "type": "原创研究/综述/转载",
  "theoretical_claims": [{"claim":"理论主张","evidence":"支撑证据","confidence":"高/中/低"}],
  "technical_methods": [{"method":"方法","maturity":"概念/仿真/实验/工程"}],
  "key_data": [{"point":"数据点","value":"数值","source":"来源"}],
  "gaps": ["知识空白"],
  "next_steps": ["下一步建议"],
  "keywords": ["关键词"],
  "summary": "一段话总结"
}
规则: 不确定就写"文档未提供"，严禁编造。区分理论推导/仿真/实验/工程。"""

results = []
for i, rel_path in enumerate(all_files):
    fpath = VAULT / rel_path
    if not fpath.exists():
        continue
    content = fpath.read_text(encoding="utf-8", errors="ignore")[:5000]
    print(f"\n[{i+1}/{len(all_files)}] {fpath.name[:50]}...")
    
    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role":"system","content":SYSTEM_PROMPT},
                      {"role":"user","content":f"文件:{fpath.name}\n\n{content}"}],
            temperature=0.1, max_tokens=1500)
        text = resp.choices[0].message.content
        m = re.search(r"\{.*\}", text, re.DOTALL)
        r = json.loads(m.group()) if m else {"error":"no json","raw":text[:100]}
        r["file"] = rel_path
        r["filename"] = fpath.name
        results.append(r)
        print(f"  -> {r.get('direction','?')} | {r.get('type','?')}")
    except Exception as e:
        results.append({"file":rel_path,"error":str(e)})
        print(f"  ERR: {e}")
    time.sleep(0.4)

out = {"timestamp":datetime.now().strftime("%Y%m%d_%H%M%S"),"total":len(results),"results":results}
(VAULT/"60_MOC"/"deep_research_analysis.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"\nDone: {len(results)} results -> 60_MOC/deep_research_analysis.json")
