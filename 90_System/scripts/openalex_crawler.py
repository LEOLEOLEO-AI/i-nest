#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAlex Crawler — Fast, free, no rate-limit replacement for S2+arXiv.
Covers both TCC and iNEST queries. Outputs Markdown to _pipeline_insights.
"""
import os, sys, json, re, time, urllib.request, urllib.parse
from datetime import datetime
from pathlib import Path

VAULT = Path(r"D:\Obsidian\vault")
INBOX = VAULT / "00_Inbox" / "_pipeline_insights"
INBOX.mkdir(parents=True, exist_ok=True)
UA = "mailto:qinrangliu@tju.edu.cn"

QUERIES = [
    # TCC
    ("TCC", "chiplet wafer-scale interconnect topology routing"),
    ("TCC", "network-on-chip small-world topology optimization"),
    ("TCC", "dark silicon manycore energy optimization"),
    ("TCC", "memristor ferroelectric crossbar array VLSI"),
    ("TCC", "3D-IC TSV hybrid bonding advanced packaging"),
    ("TCC", "photonic interconnect silicon photonics network"),
    # iNEST
    ("iNEST", "self-organized criticality neuronal avalanche"),
    ("iNEST", "edge of chaos reservoir computing dynamics"),
    ("iNEST", "complex network phase transition emergence"),
    ("iNEST", "free energy principle active inference neural"),
    ("iNEST", "neuromorphic spiking neural network memristor"),
    ("iNEST", "C. elegans connectome computation network"),
    # Bridge
    ("Bridge", "network topology intelligence emergence scaling"),
    ("Bridge", "higher-order network simplicial hypergraph dynamics"),
    ("Bridge", "integrated information causal emergence neural"),
]

def search_openalex(query, per_page=10, year=None):
    """Search OpenAlex API."""
    params = {"search": query, "per_page": per_page, "sort": "cited_by_count:desc"}
    if year:
        params["filter"] = f"publication_year:{year}"
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=30).read())
        return data.get("results", [])
    except Exception as e:
        print(f"  [ERR] {e}")
        return []

def paper_to_md(paper, track, query):
    """Convert OpenAlex paper to Markdown note."""
    title = paper.get("title", "Untitled")
    safe_title = re.sub(r'[<>:"/\\|?*]', "", title)[:80]
    doi = paper.get("doi", "").replace("https://doi.org/", "") if paper.get("doi") else ""
    year = paper.get("publication_year", "")
    cited = paper.get("cited_by_count", 0)
    
    authors = paper.get("authorships", [])
    author_names = [a.get("author", {}).get("display_name", "") for a in authors[:5]]
    
    # Get abstract
    abstract = ""
    if paper.get("abstract_inverted_index"):
        try:
            idx = paper["abstract_inverted_index"]
            words = sorted([(pos, w) for w, positions in idx.items() for pos in positions])
            abstract = " ".join(w for _, w in words)
        except:
            pass
    
    # Topics
    topics = [t.get("display_name", "") for t in paper.get("topics", [])[:3]]
    
    # Journal
    journal = ""
    if paper.get("primary_location") and paper["primary_location"].get("source"):
        journal = paper["primary_location"]["source"].get("display_name", "")
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_OA_{safe_title}.md"
    
    md = f"""---
title: "{title}"
authors: {author_names}
year: {year}
doi: "{doi}"
journal: "{journal}"
cited_by: {cited}
track: {track}
source: openalex
query: "{query}"
date: {date_str}
topics: {topics}
---

# {title}

**{', '.join(author_names[:3])}** ({year}) | *{journal}* | Cited: {cited}

## Abstract

{abstract[:1500]}

## Topics

{', '.join(topics)}

## Links

- [OpenAlex](https://openalex.org/{paper.get('id','').split('/')[-1]})
- [DOI](https://doi.org/{doi}) (if doi else '')
"""
    return filename, md

def main(limit_per_query=5, year=None, dry_run=False):
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"OpenAlex Crawler — {today}")
    print("=" * 50)
    
    total = 0
    logs = []
    seen_titles = set()
    
    # Load existing titles for dedup
    log_file = INBOX / "_oa_seen.json"
    if log_file.exists():
        try:
            seen_titles = set(json.loads(log_file.read_text(encoding="utf-8")))
        except:
            pass
    
    for track, query in QUERIES:
        print(f"\n[{track}] {query[:60]}...")
        papers = search_openalex(query, per_page=limit_per_query, year=year)
        new_count = 0
        
        for paper in papers:
            title = paper.get("title", "")
            if not title or title in seen_titles:
                continue
            
            fname, md = paper_to_md(paper, track, query)
            if not dry_run:
                (INBOX / fname).write_text(md, encoding="utf-8")
            seen_titles.add(title)
            new_count += 1
            total += 1
            doi = paper.get("doi", "") or ""
            print(f"  + {title[:70]} [{paper.get('publication_year','?')}]")
        
        logs.append({"track": track, "query": query, "new": new_count})
        time.sleep(0.3)  # Polite delay
    
    # Save seen titles
    if not dry_run:
        log_file.write_text(json.dumps(list(seen_titles), ensure_ascii=False), encoding="utf-8")
    
    print(f"\n{'='*50}")
    print(f"Total new papers: {total} | Queries: {len(QUERIES)}")
    return total

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--year", type=int, default=2026)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    main(limit_per_query=args.limit, year=args.year, dry_run=args.dry_run)
