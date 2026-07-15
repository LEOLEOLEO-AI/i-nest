"""Frontmatter Booster — Add YAML frontmatter to files with links but no frontmatter"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")

def infer_direction(path_str, content):
    """Infer TCC/iNEST from path or content"""
    path_lower = path_str.lower()
    if "inest" in path_lower or "40_inest" in path_lower: return "iNEST"
    if "tcc" in path_lower or "30_tcc" in path_lower: return "TCC"
    # Guess from content
    if "神经形态" in content or "脉冲" in content or "SNN" in content: return "iNEST"
    if "拓扑" in content or "Chiplet" in content or "晶圆" in content: return "TCC"
    return "TCC"

def boost_frontmatter():
    count = 0
    for f in list((VAULT/"30_TCC").rglob("*.md"))[:1000] + list((VAULT/"40_iNEST").rglob("*.md"))[:1000]:
        try:
            c = f.read_text(encoding="utf-8", errors="replace")
            if c.startswith("---"): continue  # Already has frontmatter
            if len(c) < 200: continue  # Too short
            
            direction = infer_direction(str(f), c[:500])
            title = f.stem.replace("_", " ")[:80]
            
            fm = f"""---
direction: {direction}
title: "{title}"
created: {datetime.fromtimestamp(f.stat().st_ctime).strftime("%Y-%m-%d")}
modified: {datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")}
---
"""
            f.write_text(fm + c, encoding="utf-8")
            count += 1
            if count % 100 == 0:
                print(f"  {count} files boosted...")
        except Exception as e:
            pass
    
    print(f"Frontmatter boosted: {count} files")
    return count

if __name__ == "__main__":
    boost_frontmatter()
