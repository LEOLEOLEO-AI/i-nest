"""Codex ↔ Obsidian 深度联动脚本 - 统一桥接层 (v2 fixed)"""

import os, sys, json, re, time
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT_ROOT = r"D:\Obsidian\home\work\.openclaw\workspace"
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY") or "REDACTED_DEEPSEEK_KEY"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"

try:
    from openai import OpenAI
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
except ImportError:
    client = None

ENCODINGS = ['utf-8', 'gbk', 'gb2312', 'latin-1']

def read_vault_file(rel_path):
    full = Path(VAULT_ROOT) / rel_path
    if not full.exists():
        return ""
    raw = full.read_bytes()
    for enc in ENCODINGS:
        try:
            return raw.decode(enc)
        except:
            continue
    return raw.decode('utf-8', errors='replace')

def write_vault_file(rel_path, content):
    full = Path(VAULT_ROOT) / rel_path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")

def list_vault_files(subdir="", pattern="*.md", max_depth=None):
    p = Path(VAULT_ROOT) / subdir
    if not p.exists():
        return []
    files = []
    for f in p.rglob(pattern):
        if max_depth and len(f.relative_to(p).parts) > max_depth:
            continue
        files.append(str(f.relative_to(VAULT_ROOT)))
    return files

def call_deepseek(prompt, system=""):
    if not client:
        return "[ERROR: no client]"
    try:
        resp = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role":"system","content":system or "你是iNEST/TCC研究助手，精通神经形态计算与晶圆级芯片。"},
                {"role":"user","content":prompt}
            ],
            temperature=0.7, max_tokens=2048, timeout=60
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[ERROR: {e}]"

def health_check():
    stats = {"total_md":0, "empty_files":0, "by_dir":defaultdict(int), "encoding_issues":0}
    all_files = list_vault_files(max_depth=5)
    stats["total_md"] = len(all_files)
    for f in all_files:
        parts = Path(f).parts
        if parts:
            stats["by_dir"][parts[0]] += 1
        try:
            content = read_vault_file(f)
            if len(content.strip()) < 10:
                stats["empty_files"] += 1
        except:
            stats["encoding_issues"] += 1
    stats["by_dir"] = dict(sorted(stats["by_dir"].items()))
    return stats

def update_dashboard():
    health = health_check()
    papers = len(list_vault_files("50_Output/51_Papers"))
    patents = len(list_vault_files("50_Output/52_Patents"))
    guides = len(list_vault_files("50_Output/55_Guides"))
    tcc = len(list_vault_files("30_TCC"))
    inest = len(list_vault_files("40_iNEST"))
    inbox = len(list_vault_files("00_Inbox"))
    dashboard = {
        "updated": datetime.now().isoformat(),
        "total": health["total_md"],
        "tcc": tcc, "inest": inest,
        "inbox": inbox,
        "papers": papers, "patents": patents, "guides": guides,
        "dirs": health["by_dir"]
    }
    write_vault_file("70_Dashboard/dashboard_data.json", json.dumps(dashboard, ensure_ascii=False, indent=2))
    return dashboard

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: health | dashboard | test")
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "health":
        h = health_check()
        print(json.dumps(h, ensure_ascii=False, indent=2))
    elif cmd == "dashboard":
        d = update_dashboard()
        print(json.dumps({"status":"ok","data":d}, ensure_ascii=False, indent=2))
    elif cmd == "test":
        print("[1] DeepSeek API...")
        r = call_deepseek("一句话介绍晶圆级拓扑中心计算TCC")
        print(f"  {r[:150]}")
        print("[2] Health scan...")
        h = health_check()
        print(f"  Total: {h['total_md']}, by dir: {json.dumps(h['by_dir'], ensure_ascii=False)}")
        print("[3] ✅ All systems go")