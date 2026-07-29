"""Generate DeepSeek Insight Report from vault content"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

VAULT = Path(r"D:\Obsidian\vault")
load_dotenv(VAULT / ".env")
KEY = os.environ.get("DEEPSEEK_API_KEY", "")
client = OpenAI(api_key=KEY, base_url="https://api.deepseek.com/v1")

# Scan recent files
recent = []
for d in ["30_TCC", "40_iNEST"]:
    for f in sorted((VAULT / d).rglob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:15]:
        try:
            c = f.read_text(encoding="utf-8", errors="replace")
            if len(c.strip()) > 200:
                recent.append((str(f.relative_to(VAULT)), c[:1500]))
        except:
            pass

files_list = "\n".join([f"- {s[0][:80]}" for s in recent[:15]])
print(f"Collected {len(recent)} files")

prompt = f"""你是iNEST/TCC神经形态计算与拓扑中心计算的首席研究分析官。请根据知识库最新文件列表，生成一份有实质洞察的研究报告。

最新研究文件:
{files_list}

请按以下结构输出Markdown:

# DeepSeek 深度洞察报告
**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 1. TCC 理论突破（拓扑中心计算）
从理论层面分析当前TCC研究的最新进展和关键突破方向（至少3条实质观点）

## 2. iNEST 技术进展（神经形态计算）
从技术层面分析iNEST的最新进展和关键技术节点（至少3条实质观点）

## 3. 论文灵感产出
基于当前研究状态，提出有价值的论文方向（至少3个方向，每个包含核心创新点和可投期刊建议）

## 4. 专利布局建议
基于技术进展，建议可申请的专利方向（至少3个方向，每个包含技术方案要点）

## 5. 工程开发与仿真建议
需要优先开展的仿真验证和代码开发任务

## 6. 跨方向协同机会
TCC与iNEST的交叉融合创新点"""

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.8, max_tokens=4096, timeout=120
)
report = resp.choices[0].message.content

out_path = VAULT / "60_MOC" / "02_DeepSeek_Insights.md"
out_path.write_text(report, encoding="utf-8")
print(f"Saved: {len(report)} chars")
