import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from openai import OpenAI

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
KEY = "REDACTED_DEEPSEEK_KEY"
client = OpenAI(api_key=KEY, base_url="https://api.deepseek.com/v1")
TODAY = datetime.now().strftime("%Y-%m-%d")

# Collect latest paper contexts
papers = []
for d in ["50_Output/51_Papers", "30_TCC/31_Theory", "40_iNEST/41_Theory"]:
    p = VAULT / d
    if not p.exists(): continue
    for f in sorted(p.rglob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            c = f.read_text(encoding="utf-8", errors="replace")
            if len(c) > 800 and "版本跟踪" not in c:
                papers.append({"name": f.name, "path": str(f.relative_to(VAULT)), "size": len(c), "preview": c[:1200]})
        except: pass
        if len(papers) >= 15: break
    if len(papers) >= 15: break

# Also check for the CST V27 paper specifically
cst_paper = VAULT / "50_Output/51_Papers/A1_CST_Theory_V27_FINAL.md"
cst_content = ""
if cst_paper.exists():
    cst_content = cst_paper.read_text(encoding="utf-8", errors="replace")[:3000]
    print("Loaded A1_CST_Theory_V27_FINAL.md")

# Check paper integration pack
integration = VAULT / "30_TCC/31_Theory/Papers_Integration_Pack_v2.md"
int_content = ""
if integration.exists():
    int_content = integration.read_text(encoding="utf-8", errors="replace")[:2000]
    print("Loaded Papers_Integration_Pack_v2.md")

paper_list = "\n".join([f"- {p['name'][:80]} ({p['size']//1024}KB)" for p in papers[:12]])

prompt = f"""你是TCC+iNEST首席研究策略官。基于最新论文版本和当前研究状态，生成可执行的任务计划。

当前最新论文/文档:
{paper_list}

CST V27论文核心内容摘要:
{cst_content[:2000]}

论文整合包要点:
{int_content[:1500]}

请输出具体的、可操作的Markdown(不要代码块):

# TCC + iNEST 最新版本任务计划 — {TODAY}

## 🔥 今日最高优先级 (3项)
(每项格式: **编号. [TCC/iNEST] 任务标题** — 关联文件 — 预期产出 — 预计耗时)

## 📄 论文推进路线图
(基于CST V27/整合包等最新版本的3-5步具体推进计划)

## 🔬 技术验证与仿真
(需要验证的技术假设和仿真任务)

## 💻 代码/工程开发
(需要推进的IP核、FPGA、RTL开发任务)

## 📋 本周里程碑
(本周应完成的3个关键目标)"""

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role":"user","content":prompt}],
    temperature=0.6, max_tokens=3072, timeout=120
)

result = resp.choices[0].message.content

# Save
out = VAULT / "60_MOC" / f"06_Task_Plan_{TODAY}.md"
out.write_text(result, encoding="utf-8")
latest = VAULT / "60_MOC" / "06_Task_Plan.md"
latest.write_text(result, encoding="utf-8")

# Also update 02_Research_Insights
insights = VAULT / "60_MOC" / "02_Research_Insights.md"
insights.write_text(result, encoding="utf-8")

print(f"Task plan saved: {len(result)} chars")
print(result[:800])
