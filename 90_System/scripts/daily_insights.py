"""Daily DeepSeek Insight Generator - named by date"""
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from openai import OpenAI

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
KEY = os.environ.get("DEEPSEEK_API_KEY") or "REDACTED_DEEPSEEK_KEY"
client = OpenAI(api_key=KEY, base_url="https://api.deepseek.com/v1")
today = datetime.now().strftime("%Y-%m-%d")

def scan_recent():
    """Scan recently modified high-value files"""
    files = []
    for d in ["30_TCC", "40_iNEST"]:
        for f in sorted((VAULT / d).rglob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
            try:
                c = f.read_text(encoding="utf-8", errors="replace")
                if len(c.strip()) > 300:
                    files.append((str(f.relative_to(VAULT)), c[:2000], f.stat().st_mtime))
            except:
                pass
    return files

def scan_inspiration_counts():
    """Count inspiration-tagged files"""
    tcc_c, tcc_h = 0, 0
    inest_c, inest_h = 0, 0
    for f in (VAULT / "30_TCC").rglob("*.md"):
        try:
            c = f.read_text(encoding="utf-8", errors="replace")[:500].lower()
            if any(kw in c for kw in ['灵感', 'inspiration', '洞察', 'insight']):
                tcc_c += 1
                if len(f.read_text(encoding="utf-8", errors="replace")) > 500:
                    tcc_h += 1
        except:
            pass
    for f in (VAULT / "40_iNEST").rglob("*.md"):
        try:
            c = f.read_text(encoding="utf-8", errors="replace")[:500].lower()
            if any(kw in c for kw in ['灵感', 'inspiration', '洞察', 'insight']):
                inest_c += 1
                if len(f.read_text(encoding="utf-8", errors="replace")) > 500:
                    inest_h += 1
        except:
            pass
    return {"tcc_count": tcc_c, "tcc_high": tcc_h, "inest_count": inest_c, "inest_high": inest_h}

def generate_insights(files, counts):
    """Generate insight report via DeepSeek"""
    file_list = "\n".join([f"- {s[0][:80]}" for s in files[:12]])
    
    prompt = f"""你是iNEST/TCC的首席研究分析官。基于知识库最新文件生成今日洞察。

最新文件:
{file_list}

灵感统计: TCC {counts['tcc_count']}篇(高价值{counts['tcc_high']}), iNEST {counts['inest_count']}篇(高价值{counts['inest_high']})

输出Markdown:

# DeepSeek 每日洞察 — {today}

## 1. TCC 关键进展
(基于最新文件的2-3条实质分析)

## 2. iNEST 关键进展
(基于最新文件的2-3条实质分析)

## 3. 今日论文灵感
(2-3个具体方向，含创新点和可投期刊)

## 4. 专利与技术点
(2-3个可布局方向)

## 5. 下一步行动建议"""

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7, max_tokens=3072, timeout=120
    )
    return resp.choices[0].message.content

def update_home_md(counts):
    """Update Home.md inspiration counts"""
    hp = VAULT / "Home.md"
    content = hp.read_text(encoding="utf-8")
    # Find and update the counts
    import re
    content = re.sub(r'\|\s*🧠\s*TCC\s*\|\s*\*\*\d+\*\*\s*\|\s*\*\*\d+\*\*\s*\|', 
                     f'| 🧠 TCC | **{counts["tcc_count"]}** | **{counts["tcc_high"]}** |', content)
    content = re.sub(r'\|\s*🧬\s*iNEST\s*\|\s*\*\*\d+\*\*\s*\|\s*\*\*\d+\*\*\s*\|',
                     f'| 🧬 iNEST | **{counts["inest_count"]}** | **{counts["inest_high"]}** |', content)
    hp.write_text(content, encoding="utf-8")

def main():
    print(f"Daily Insight Generator - {today}")
    
    # Scan
    print("[1/4] Scanning recent files...")
    files = scan_recent()
    print(f"  Found {len(files)} recent files")
    
    # Count inspirations
    print("[2/4] Counting inspirations...")
    counts = scan_inspiration_counts()
    print(f"  TCC: {counts['tcc_count']}/{counts['tcc_high']}, iNEST: {counts['inest_count']}/{counts['inest_high']}")
    
    # Generate insights
    print("[3/4] Generating insights via DeepSeek...")
    report = generate_insights(files, counts)
    
    # Save with date name
    out_path = VAULT / "60_MOC" / f"02_DeepSeek_Insights_{today}.md"
    out_path.write_text(report, encoding="utf-8")
    
    # Also save as latest symlink copy
    latest_path = VAULT / "60_MOC" / "02_DeepSeek_Insights.md"
    latest_path.write_text(report, encoding="utf-8")
    print(f"  Saved: {out_path.name} ({len(report)} chars)")
    
    # Update Home.md
    print("[4/4] Updating Home.md counts...")
    update_home_md(counts)
    print("  Done!")
    
    print(f"\nDone: {today}")

if __name__ == "__main__":
    main()
