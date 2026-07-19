import json, os, re
from pathlib import Path
from datetime import datetime, timedelta

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
DASHBOARD_DIR = VAULT / "70_Dashboard"
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

def count_md(*dirs):
    n = 0
    for d in dirs:
        p = VAULT / d
        if p.exists():
            n += len([f for f in p.rglob("*.md") if ".git" not in f.parts and ".obsidian" not in f.parts and "80_Archive" not in f.parts])
    return n

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

out = DASHBOARD_DIR / "dashboard_data.json"
out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

today = data["date"]

djson = {
    "generated": data["generated"], "date": today,
    "vault": {"total_md": data["counts"]["total"], "tcc_total": data["counts"]["tcc"],
              "tcc_theory": count_md("30_TCC/31_Theory"), "tcc_tech": count_md("30_TCC/32_Tech"),
              "tcc_eng": count_md("30_TCC/33_Dev"), "inest_total": data["counts"]["inest"],
              "inest_theory": count_md("40_iNEST/41_Theory"), "inest_tech": count_md("40_iNEST/42_Tech"),
              "inest_eng": count_md("40_iNEST/43_Engineering")},
    "inbox": {"new_24h": 0, "pending": count_md("10_Inbox"), "processing": count_md("20_Processing")},
    "output": {"papers": data["counts"]["papers"], "patents": data["counts"]["patents"],
               "monographs": count_md("50_Output/53_Monographs"), "code": data["counts"]["code"],
               "guides": data["counts"]["guides"]},
    "recent_changes": [], "tasks": {"today": [], "active": [], "papers": [], "patents": [], "code": []},
    "insights": {"tcc": [], "inest": [], "cross": []}
}
(DASHBOARD_DIR / "data.json").write_text(json.dumps(djson, ensure_ascii=False, indent=2), encoding="utf-8")
nl = chr(10)
js = "// Unified Data Bus - generated " + data["generated"] + nl + "var UNIFIED_DATA = " + json.dumps(djson, ensure_ascii=False) + ";"
(DASHBOARD_DIR / "data.js").write_text(js, encoding="utf-8")

home = VAULT / "Home.md"
if home.exists():
    c = home.read_text(encoding="utf-8", errors="replace")
    c = re.sub(r'>2026-07-\d{2}<', ">" + today + "<", c)
    for key in ["total","tcc","inest","inbox","papers","patents"]:
        pat = '(data-key="' + key + '">)\\d+<'
        repl = "\\g<1>" + str(data["counts"][key]) + "<"
        c = re.sub(pat, repl, c)
    home.write_text(c, encoding="utf-8")

ts = datetime.now().strftime("%H:%M:%S")
print(f"[{ts}] Refresh Dashboard v2.0")
print(f"  dashboard_data.json + data.json + data.js + Home.md")
print(f"  TCC: {data['counts']['tcc']} | iNEST: {data['counts']['inest']} | Inbox: {data['counts']['inbox']} | Papers: {data['counts']['papers']}")
