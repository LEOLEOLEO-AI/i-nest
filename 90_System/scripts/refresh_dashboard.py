# TCC+iNEST 自进化看板刷新脚本 v1.0
# 用途: 每日自动同步 任务计划→看板数据→Home 入口
# 调度: 每日 06:00 / 每次启动 Obsidian

import json, os
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")

def count_md(*dirs):
    n = 0
    for d in dirs:
        p = VAULT / d
        if p.exists(): n += len(list(p.rglob("*.md")))
    return n

# 1. Generate dashboard data
data = {
    "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "date": datetime.now().strftime("%Y-%m-%d"),
    "counts": {
        "total": count_md("30_TCC","40_iNEST","50_Output","60_MOC","10_Inbox","20_Processing"),
        "tcc": count_md("30_TCC"),
        "inest": count_md("40_iNEST"),
        "inbox": count_md("10_Inbox"),
        "papers": count_md("50_Output/51_Papers"),
        "patents": count_md("50_Output/52_Patents"),
        "guides": count_md("50_Output/55_Guides"),
        "code": count_md("50_Output/54_Code"),
    },
    "pipeline": {
        "last_sync": datetime.now().strftime("%H:%M"),
        "getnote_inbox": count_md("10_Inbox"),
        "processing": count_md("20_Processing"),
        "archive": count_md("80_Archive"),
    }
}

out = VAULT / "70_Dashboard/dashboard_data.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# 2. Update Home.md date stamp
home = VAULT / "Home.md"
if home.exists():
    c = home.read_text(encoding="utf-8", errors="replace")
    today = datetime.now().strftime("%Y-%m-%d")
    c = c.replace('data-key="total"', f'data-key="total"').replace('>更新</span>: <span', f'>更新</span>: <span').replace('2026-07-15', today)
    home.write_text(c, encoding="utf-8")

print(f"[{datetime.now().strftime('%H:%M:%S')}] Dashboard refreshed")
print(f"  TCC: {data['counts']['tcc']} | iNEST: {data['counts']['inest']} | Inbox: {data['counts']['inbox']}")
