#!/usr/bin/env python3
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime, timedelta
import urllib.request

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
OUTPUT_DIR = VAULT / "60_MOC" / "_wiki_llm_v2"
DS_API_KEY = "sk-73d73dedd19548d19d141a0c37cfd196"
DS_API_URL = "https://api.deepseek.com/v1/chat/completions"
DS_MODEL = "deepseek-chat"

def call_llm(system_prompt, user_prompt, max_tokens=800):
    payload = {
        "model": DS_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }
    req = urllib.request.Request(DS_API_URL, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {DS_API_KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return json.loads(resp.read())["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"LLM error: {e}")
        return None

def safe_parse_json(text):
    text = text.strip()
    for m in ["```json", "```"]: text = text.replace(m, "")
    s = text.find("["); e = text.rfind("]")
    if s >= 0 and e > s: text = text[s:e+1]
    else:
        s = text.find("{"); e = text.rfind("}")
        if s >= 0 and e > s: text = text[s:e+1]
    text = re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*]', ']', text)
    return json.loads(text)

def read_frontmatter(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) > 2:
            try:
                import yaml
                return yaml.safe_load(parts[1]) or {}
            except: pass
    return {}

# === EMERGENCE DETECTION ===
def detect_emerging():
    cutoff = datetime.now() - timedelta(days=30)
    recent = []
    for td in [VAULT/"30_TCC", VAULT/"40_iNEST", VAULT/"10_Library/Papers"]:
        for f in td.rglob("*.md"):
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if mtime > cutoff:
                fm = read_frontmatter(f)
                recent.append({"name": f.stem, "tags": fm.get("tags",[]), "summary": fm.get("summary","")[:80]})
    
    recent_text = json.dumps(recent[:40], ensure_ascii=False)
    prompt = f"""Analyze these {len(recent)} recent notes. Find 3-5 EMERGING CONCEPT CLUSTERS.
Output ONLY a JSON array: [{{"name":"...","desc":"...","notes":["n1","n2"],"sig":"..."}}]
Notes: {recent_text[:3500]}"""
    
    result = call_llm("You detect emerging research clusters. Output ONLY valid JSON array.", prompt, 800)
    if not result: return
    
    try:
        clusters = safe_parse_json(result)
    except:
        # Fallback: extract manually
        clusters = [{"name":"Emerging Theme", "desc":"LLM output parse issue - retry", "notes":[], "sig":""}]
    
    report = f"""---
title: "概念涌现检测报告"
date: {datetime.now().strftime('%Y-%m-%d')}
type: emergence-report
period: {cutoff.strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}
active_notes: {len(recent)}
---

# Concept Emergence Detection

> {len(recent)} active notes in last 30 days | {datetime.now().strftime('%Y-%m-%d')}

"""
    for c in clusters:
        report += f"## {c.get('name','Cluster')}\n\n"
        report += f"{c.get('desc','')}\n\n"
        notes = c.get('notes', [])
        if notes:
            report += "**Key Notes:**\n"
            for n in notes[:5]:
                report += f"- [[{n}]]\n"
        sig = c.get('sig', '')
        if sig: report += f"\n**Significance:** {sig}\n"
        report += "\n---\n\n"
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / f"emergence_{datetime.now().strftime('%Y%m%d')}.md"
    out.write_text(report, encoding="utf-8")
    print(f"Emergence report: {out.relative_to(VAULT)}")
    print(f"Clusters found: {len(clusters)}")
    for c in clusters:
        print(f"  - {c.get('name','?')}")

# === AUTO MOC ===
def generate_moc(track):
    track_map = {"TCC": ("30_TCC", "Topological Centric Computing"),
                 "iNEST": ("40_iNEST", "Intelligent Emergence System")}
    if track not in track_map: return
    td, desc = track_map[track]
    tpath = VAULT / td
    all_notes = list(tpath.rglob("*.md"))
    recent = sorted(all_notes, key=lambda p: p.stat().st_mtime, reverse=True)[:15]
    
    note_list = []
    for f in recent:
        fm = read_frontmatter(f)
        title = fm.get("title", f.stem)
        summary = fm.get("summary", "")
        l = f"- [[{f.stem}]]"
        if summary: l += f" — {summary[:80]}"
        note_list.append(l)
    
    prompt = f"""You are a research librarian. Generate a Map of Content for {desc} ({track}).
Recent notes (most active first):
{chr(10).join(note_list[:12])}

Output clean Markdown:
## Overview (2-3 sentences on current state)
## Thematic Clusters (3-5 clusters with relevant notes)
## Emerging Directions (2-3 research frontiers)
"""
    result = call_llm("Generate structured research MOC. Output clean Markdown.", prompt, 1000)
    if not result: return
    
    moc = f"""---
title: "{track} — Auto MOC"
date: {datetime.now().strftime('%Y-%m-%d')}
type: moc
auto_generated: true
track: {track}
---

# {track} — {desc}

> Auto-generated {datetime.now().strftime('%Y-%m-%d %H:%M')} | {len(all_notes)} notes

{result}

---
| Metric | Value |
|:---|:---|
| Total Notes | {len(all_notes)} |
| 7d Active | {sum(1 for f in all_notes if f.stat().st_mtime > (datetime.now()-timedelta(days=7)).timestamp())} |
| 30d Active | {sum(1 for f in all_notes if f.stat().st_mtime > (datetime.now()-timedelta(days=30)).timestamp())} |

> Wiki LLM v2.0
"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / f"{track}_MOC_auto.md"
    out.write_text(moc, encoding="utf-8")
    print(f"MOC generated: {out.relative_to(VAULT)}")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["emerge","moc","full"])
    p.add_argument("--track", default="TCC")
    args = p.parse_args()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if args.cmd in ("emerge", "full"):
        detect_emerging()
    if args.cmd in ("moc", "full"):
        generate_moc("TCC")
        generate_moc("iNEST")
