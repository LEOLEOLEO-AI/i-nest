# -*- coding: utf-8 -*-
"""Phase 2: LLM classify ambiguous files + extract insights"""

import json, shutil, time, re
from pathlib import Path
from openai import OpenAI
from datetime import datetime

VAULT = Path(r"D:\Obsidian\vault")
API_KEY = "REDACTED_LEAKED_SILICONFLOW"
BASE_URL = "https://api.siliconflow.cn/v1"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Load ambiguous files
ambig = json.loads((VAULT / "60_MOC" / "ambig_files.json").read_text(encoding="utf-8"))
print(f"Total ambiguous files: {len(ambig)}")

SYSTEM_PROMPT = """你是TCC（拓扑中心计算/晶圆级互联）和iNEST（神经形态/类脑计算）两个前沿方向的科研分类专家。

分析以下笔记内容，输出JSON（仅JSON，不要其他文字）：
{
  "direction": "TCC" 或 "iNEST" 或 "both",
  "confidence": 0.0-1.0,
  "keywords": ["关键词1", "关键词2", "关键词3"],
  "insight_tcc": "对TCC研究的启迪（1-2句，无启迪则写'无直接关联'）",
  "insight_inest": "对iNEST研究的启迪（1-2句，无启迪则写'无直接关联'）",
  "paper_value": "论文产出价值：高/中/低/无",
  "patent_value": "专利产出价值：高/中/低/无",
  "sim_value": "仿真验证价值：高/中/低/无",
  "code_value": "核心代码价值：高/中/低/无",
  "summary": "一句话摘要"
}

判定标准：
- TCC = 晶圆级互联/拓扑中心计算/SDSoW/Chiplet/存算一体/先进封装/片上网络/并行计算架构
- iNEST = 神经形态/类脑计算/脉冲神经网络/涌现智能/认知计算/脑启发AI/复杂网络动力学
- both = 同时涉及两个方向"""

results = []
errors = []

for i, item in enumerate(ambig):
    fpath = VAULT / item["path"]
    if not fpath.exists():
        continue
    
    try:
        content = fpath.read_text(encoding="utf-8", errors="ignore")
        # Truncate to ~3000 chars for API
        content_short = content[:3000]
        
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V4-Pro",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"文件名: {fpath.name}\n\n内容:\n{content_short}"}
            ],
            temperature=0.1,
            max_tokens=500,
        )
        
        result_text = response.choices[0].message.content.strip()
        # Extract JSON
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = {"direction": "unknown", "confidence": 0, "error": "No JSON found"}
        
        result["file"] = item["path"]
        result["filename"] = fpath.name
        results.append(result)
        
        # Move file based on classification
        direction = result.get("direction", "unknown")
        if direction == "TCC":
            dst = VAULT / "30_TCC" / "32_Tech" / fpath.name
        elif direction == "iNEST":
            dst = VAULT / "40_iNEST" / "42_Tech" / fpath.name
        else:
            dst = VAULT / "30_TCC" / "32_Tech" / fpath.name  # default to TCC
        
        if not dst.exists():
            shutil.move(str(fpath), str(dst))
        
        if (i + 1) % 10 == 0:
            print(f"  Progress: {i+1}/{len(ambig)}")
        
        time.sleep(0.3)  # rate limit
        
    except Exception as e:
        errors.append({"file": item["path"], "error": str(e)})
        print(f"  Error {i+1}: {item['path']} - {e}")

# Save results
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
out = {
    "timestamp": timestamp,
    "total": len(ambig),
    "processed": len(results),
    "errors": errors,
    "results": results
}
(VAULT / "60_MOC" / "llm_classify_results.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

# Stats
tcc = sum(1 for r in results if r.get("direction") == "TCC")
inest = sum(1 for r in results if r.get("direction") == "iNEST")
both = sum(1 for r in results if r.get("direction") == "both")

print(f"\nDone! TCC: {tcc}, iNEST: {inest}, Both: {both}, Errors: {len(errors)}")
