# -*- coding: utf-8 -*-
"""DeepSeek deep analysis of core TCC+iNEST research files"""

import json, time, os
from pathlib import Path
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

VAULT = Path(r"D:\Obsidian\vault")
load_dotenv(VAULT / ".env", override=True)
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com/v1", timeout=60)

# === Top TCC research files ===
TCC_FILES = [
    "30_TCC/31_Theory/SDI_Paper_Draft.md",
    "30_TCC/31_Theory/时空复杂度乘积定理的推导.md",
    "30_TCC/31_Theory/从冯诺依曼到网络中心_计算范式迁移的第一性原理综述.md",
]

# === Top iNEST research files ===
INEST_FILES = [
    "40_iNEST/41_Theory/网络时空协同复杂度涌现智能：一个整合性理论框架.md",
]

# Find more by scanning
for pattern, limit in [("30_TCC/31_Theory/*CST*", 3), ("30_TCC/32_Tech/*SDSoW*", 2),
                        ("30_TCC/34_Projects/*项目*", 2), ("40_iNEST/41_Theory/*涌现*", 3),
                        ("40_iNEST/42_Tech/*神经*", 2), ("40_iNEST/41_Theory/*因果*", 1)]:
    for f in sorted(VAULT.glob(pattern), key=lambda x: -x.stat().st_size)[:limit]:
        rel = str(f.relative_to(VAULT))
        if rel not in TCC_FILES + INEST_FILES:
            if "TCC" in rel:
                TCC_FILES.append(rel)
            else:
                INEST_FILES.append(rel)

all_files = TCC_FILES + INEST_FILES
print(f"Files to analyze: {len(all_files)} ({len(TCC_FILES)} TCC + {len(INEST_FILES)} iNEST)")
for f in all_files:
    size = (VAULT / f).stat().st_size / 1024
    print(f"  [{size:.1f}KB] {f}")

SYSTEM_PROMPT = """你是TCC(拓扑中心计算/晶圆级互联)和iNEST(神经形态/类脑计算)的资深研究科学家。

深度分析以下研究文档，提取可存入知识库的实质性内容。输出JSON:

{
  "direction": "TCC或iNEST",
  "theoretical_breakthroughs": [
    {"claim": "理论命题", "evidence": "推导依据或实验证据", "confidence": "高/中/低"}
  ],
  "technical_methods": [
    {"method": "技术方法名称", "description": "方法描述", "maturity": "概念/仿真验证/实验验证/工程落地"}
  ],
  "engineering_insights": [
    {"insight": "工程洞察", "applicability": "可应用场景"}
  ],
  "objective_data": [
    {"data_point": "客观数据点", "value": "具体数值", "source": "来源"}
  ],
  "knowledge_gaps": ["待填补的知识空白1", "空白2"],
  "actionable_suggestions": ["可执行的下一步建议1", "建议2"],
  "keywords": ["关键词1", "关键词2", "关键词3"],
  "summary": "一段话总结核心贡献"
}

严格准则:
- 每个claim必须有证据支撑，无证据则标注confidence为低
- 区分理论推导/仿真结果/实验数据/工程估算
- 客观数据必须给出具体数值和来源
- 不要编造任何内容，不确定就写"文档未提供"
- 如果内容是非原创综述/转载他人文章，标注"非原创综述"并降低权重"""

results = []

for i, rel_path in enumerate(all_files):
    fpath = VAULT / rel_path
    if not fpath.exists():
        continue
    
    content = fpath.read_text(encoding="utf-8", errors="ignore")
    # Truncate for API - take first 6000 chars
    content_sample = content[:6000]
    
    print(f"\n[{i+1}/{len(all_files)}] Analyzing: {fpath.name[:60]}...")
    
    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"文件: {fpath.name}\n\n内容样本(前6000字):\n{content_sample}"}
            ],
            temperature=0.15,
            max_tokens=2000,
        )
        
        text = resp.choices[0].message.content.strip()
        # Extract JSON
        import re
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            result = json.loads(m.group())
        else:
            result = {"error": "No JSON", "raw": text[:200]}
        
        result["file"] = rel_path
        result["filename"] = fpath.name
        result["size_kb"] = fpath.stat().st_size / 1024
        results.append(result)
        
        print(f"  OK - direction: {result.get('direction', '?')}")
        
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append({"file": rel_path, "error": str(e)})
    
    time.sleep(0.5)

# Save
out = {
    "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
    "total": len(results),
    "results": results
}
(VAULT / "60_MOC" / "deep_research_analysis.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nSaved: 60_MOC/deep_research_analysis.json ({len(results)} results)")
