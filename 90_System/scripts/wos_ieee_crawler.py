#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WoS + IEEE Xplore Crawler Integration
Requires: WOS_API_KEY and IEEE_API_KEY environment variables.
Usage: python wos_ieee_crawler.py --dry-run   (test)
       python wos_ieee_crawler.py             (live)
"""
import os, sys, json, re, time, urllib.request, urllib.parse
from datetime import datetime
from pathlib import Path

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
INBOX = VAULT / "00_Inbox" / "_pipeline_insights"
INBOX.mkdir(parents=True, exist_ok=True)
TODAY = datetime.now().strftime("%Y-%m-%d")

WOS_KEY = os.environ.get("WOS_API_KEY", "")
IEEE_KEY = os.environ.get("IEEE_API_KEY", "")

# ============================================================
# Web of Science API
# ============================================================
WOS_QUERIES_TCC = [
    "TS=(chiplet AND interconnect AND wafer)",
    "TS=(network-on-chip AND topology AND optimization)",
    "TS=(dark silicon AND manycore AND energy)",
    "TS=(memristor AND crossbar AND neuromorphic)",
    "TS=(3D-IC OR TSV AND hybrid bonding AND packaging)",
]
WOS_QUERIES_INEST = [
    "TS=(self-organized criticality AND neuronal)",
    "TS=(avalanche AND brain AND critical)",
    "TS=(edge of chaos AND reservoir computing)",
    "TS=(free energy principle AND active inference)",
    "TS=(connectome AND computation AND network)",
]

def search_wos(query, limit=10):
    """Search Web of Science API."""
    if not WOS_KEY:
        print("  [WoS] SKIP: No WOS_API_KEY env var")
        return []
    url = f"https://api.clarivate.com/apis/wos/wok/search/v1/query"
    params = {
        "databaseId": "WOS",
        "usrQuery": query,
        "count": limit,
        "firstRecord": 1
    }
    headers = {"X-ApiKey": WOS_KEY, "Accept": "application/json"}
    try:
        req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params), headers=headers)
        data = json.loads(urllib.request.urlopen(req, timeout=30).read())
        return data.get("Records", {}).get("records", {}).get("REC", [])
    except Exception as e:
        print(f"  [WoS ERR] {e}")
        return []

# ============================================================
# IEEE Xplore API
# ============================================================
IEEE_QUERIES = [
    ("TCC", "chiplet interconnect wafer scale"),
    ("TCC", "network on chip topology"),
    ("iNEST", "neuromorphic criticality"),
    ("iNEST", "spiking neural network memristor"),
    ("iNEST", "connectome topology computation"),
]

def search_ieee(query, limit=10):
    """Search IEEE Xplore API."""
    if not IEEE_KEY:
        print("  [IEEE] SKIP: No IEEE_API_KEY env var")
        return []
    url = "https://ieeexploreapi.ieee.org/api/v1/search/articles"
    params = {
        "apikey": IEEE_KEY,
        "format": "json",
        "max_records": limit,
        "sort_field": "publication_year",
        "sort_order": "desc",
        "querytext": query
    }
    try:
        req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params))
        data = json.loads(urllib.request.urlopen(req, timeout=30).read())
        return data.get("articles", [])
    except Exception as e:
        print(f"  [IEEE ERR] {e}")
        return []

# ============================================================
# Write to Markdown
# ============================================================
def wos_to_md(rec, track):
    """Convert WoS record to Markdown."""
    title = rec.get("title", [{}])[0].get("content", "Untitled")
    safe = re.sub(r'[<>:"/\\|?*]', "", title)[:80]
    authors = [a.get("content","") for a in rec.get("author", {}).get("authors", [])][:5]
    journal = rec.get("source", {}).get("sourceTitle", [{}])[0].get("content", "")
    doi = rec.get("other", {}).get("identifier", {}).get("doi", "")
    year = rec.get("source", {}).get("sourceMeta", {}).get("pubyear", "")
    
    return f"""---
title: "{title}"
authors: {authors}
year: {year}
doi: "{doi}"
journal: "{journal}"
track: {track}
source: wos
date: {TODAY}
---

# {title}
**{', '.join(authors[:3])}** ({year}) | {journal}
""", f"{TODAY}_WOS_{safe}.md"

def ieee_to_md(art, track):
    """Convert IEEE article to Markdown."""
    title = art.get("title", "Untitled")
    safe = re.sub(r'[<>:"/\\|?*]', "", title)[:80]
    authors = [a.get("full_name","") for a in art.get("authors",{}).get("authors",[])]
    journal = art.get("publication_title", "")
    doi = art.get("doi", "")
    year = art.get("publication_year", "")
    abstract = art.get("abstract", "")[:1500]
    
    return f"""---
title: "{title}"
authors: {authors}
year: {year}
doi: "{doi}"
journal: "{journal}"
track: {track}
source: ieee
date: {TODAY}
---

# {title}
**{', '.join(authors[:3])}** ({year}) | {journal}

## Abstract
{abstract}
""", f"{TODAY}_IEEE_{safe}.md"

# ============================================================
# Main
# ============================================================
def main(dry_run=False):
    total = 0
    
    # WoS
    if WOS_KEY:
        print("=== Web of Science ===")
        for q in WOS_QUERIES_TCC + WOS_QUERIES_INEST:
            track = "TCC" if q in WOS_QUERIES_TCC else "iNEST"
            records = search_wos(q, limit=5)
            for rec in records:
                md, fname = wos_to_md(rec, track)
                if not dry_run:
                    (INBOX / fname).write_text(md, encoding="utf-8")
                total += 1
                print(f"  + {rec.get('title',[{}])[0].get('content','')[:70]}")
            time.sleep(0.5)
    else:
        print("[WoS] Set WOS_API_KEY to enable")
    
    # IEEE
    if IEEE_KEY:
        print("\n=== IEEE Xplore ===")
        for track, q in IEEE_QUERIES:
            articles = search_ieee(q, limit=5)
            for art in articles:
                md, fname = ieee_to_md(art, track)
                if not dry_run:
                    (INBOX / fname).write_text(md, encoding="utf-8")
                total += 1
                print(f"  + {art.get('title','')[:70]}")
            time.sleep(1)
    else:
        print("[IEEE] Set IEEE_API_KEY to enable")
    
    print(f"\nTotal new: {total}")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    main(dry_run=args.dry_run)
