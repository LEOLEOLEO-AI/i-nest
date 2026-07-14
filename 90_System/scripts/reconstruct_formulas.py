import re, json
from pathlib import Path
from openai import OpenAI

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
content = (VAULT / "30_TCC/31_Theory/tcc_paper_background.md").read_text(encoding="utf-8")

client = OpenAI(api_key="REDACTED_OLD_DEEPSEEK", base_url="https://api.deepseek.com/v1", timeout=60)

prompt = """你是LaTeX公式专家。以下是TCC论文背景综述的Markdown文件，其中Word公式在转换时丢失了。

请做两件事：
1. 找出文档中所有缺失公式的位置（原本应该有公式但现在只有空白/残缺的位置）
2. 根据上下文推断公式内容，用 $$...$$ (块级) 或 $...$ (行内) LaTeX格式重建

输出JSON格式：
{"fixes": [{"location_hint": "在xx段落中/yy小节之前", "formula_latex": "$$ 公式内容 $$", "context_before": "前文关键词"}, ...]}

只重建确定需要公式的地方。如果某处看起来完整不需要公式，不要强行添加。

全文如下:
""" + content

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role":"user","content": prompt}],
    temperature=0.1, max_tokens=3000
)

result = resp.choices[0].message.content
print(result[:1500])
