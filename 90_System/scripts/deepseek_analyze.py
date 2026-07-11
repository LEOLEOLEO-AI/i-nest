# -*- coding: utf-8 -*-
"""DeepSeek V4 Pro batch analysis of 10_Inbox files"""

import json, shutil, time, re
from pathlib import Path
from openai import OpenAI
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
INBOX = VAULT / "10_Inbox"
API_KEY = "REDACTED_DEEPSEEK_KEY"

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com/v1", timeout=30)

SYSTEM_PROMPT = """你是TCC（拓扑中心计算/晶圆级互联）和iNEST（神经形态/类脑计算）科研分析专家。

对每条笔记输出JSON行（每行一个JSON对象，用换行分隔）：
{"file":"文件名","direction":"TCC/iNEST/both","keywords":["k1","k2"],"insight_tcc":"对TCC启迪(一句话)","insight_inest":"对iNEST启迪(一句话)","paper":"高/中/低/无","patent":"高/中/低/无","simulation":"高/中/低/无","code":"高/中/低/无","summary":"一句话摘要"}

判定标准：
- TCC: 晶圆级互联/SDSoW/Chiplet/存算一体/先进封装/片上网络/并行计算/交换芯片/3DIC/PCIe
- iNEST: 神经形态/类脑/脉冲神经网络/涌现/认知计算/脑启发AI/复杂网络动力学/意识
- both: 同时涉及两个方向"""

def analyze_batch(files_batch):
    """Send batch of files to DeepSeek for analysis"""
    user_content = "分析以下笔记，每行输出一个JSON：\n\n"
    for i, (fpath, fname, content) in enumerate(files_batch):
        truncated = content[:800].replace("\n", " ")
        user_content += f"--- 笔记{i+1}: {fname} ---\n{truncated}\n\n"
    
    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            temperature=0.2,
            max_tokens=2000,
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"  API Error: {e}")
        return None

def parse_results(text, files_batch):
    """Parse LLM output into structured results"""
    results = []
    lines = text.strip().split("\n")
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("{"):
            try:
                r = json.loads(line)
                if i < len(files_batch):
                    r["path"] = str(files_batch[i][0].relative_to(VAULT))
                results.append(r)
            except:
                pass
    return results

# Collect all md files
all_files = []
for f in INBOX.rglob("*.md"):
    content = f.read_text(encoding="utf-8", errors="ignore")
    if "可能重复" in content and len(content) < 200:
        continue  # skip dedup stubs
    if len(content) < 50:
        continue  # skip nearly empty
    all_files.append((f, f.name, content))

print(f"Files to analyze: {len(all_files)}")

# Process in batches of 8
BATCH_SIZE = 8
all_results = []
processed = 0

for i in range(0, len(all_files), BATCH_SIZE):
    batch = all_files[i:i+BATCH_SIZE]
    batch_num = i // BATCH_SIZE + 1
    
    output = analyze_batch(batch)
    if output:
        results = parse_results(output, batch)
        all_results.extend(results)
        processed += len(batch)
    
    if batch_num % 5 == 0:
        print(f"  Progress: {processed}/{len(all_files)}")
    time.sleep(0.5)

print(f"Processed: {processed}/{len(all_files)}, results: {len(all_results)}")

# Save results
out = {
    "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
    "total_files": len(all_files),
    "analyzed": len(all_results),
    "results": all_results
}
(VAULT / "60_MOC" / "deepseek_analysis.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved to 60_MOC/deepseek_analysis.json")
