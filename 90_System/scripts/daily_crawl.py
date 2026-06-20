#!/usr/bin/env python3
"""
Daily Crawl Pipeline — 8:00 AM automated literature & news crawl.
Fetches from Semantic Scholar, arXiv RSS, and selected neuroscience/ML sources.
Outputs to 00_Inbox with proper frontmatter.
"""
import os, json, time, re
from datetime import datetime, timezone, timedelta
from pathlib import Path
import urllib.request
import urllib.parse

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
INBOX = VAULT / "00_Inbox"
LOG_DIR = VAULT / "logs"

# Semantic Scholar API key
S2_API_KEY = "s2k-hUuwuX3sqJjRFbkjC6OZg4aR6yyJxkRzxcHKNJZx"

# Search queries for TCC and iNEST
QUERIES = {
    "TCC": [
        "topological computing wafer scale integration",
        "chiplet interconnect routing algorithm",
        "network-on-chip topology optimization",
        "software defined system on wafer",
        "variational free energy neuromorphic",
    ],
    "iNEST": [
        "neuromorphic computing spiking neural network",
        "self-organized criticality neural systems",
        "memristor array in-memory computing",
        "emergence complex systems neural network",
        "brain-inspired computing architecture 2025",
    ],
}

def search_semantic_scholar(query, limit=5):
    """Search Semantic Scholar API."""
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,abstract,url,externalIds,citationCount"
    }
    headers = {"x-api-key": S2_API_KEY} if S2_API_KEY else {}
    req_url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(req_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("data", [])
    except Exception as e:
        print(f"  S2 error: {e}")
        return []

def search_arxiv(query, max_results=3):
    """Search arXiv API."""
    base = "http://export.arxiv.org/api/query"
    params = {
        "search_query": query,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    req_url = base + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(req_url)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
            entries = re.findall(r"<entry>(.*?)</entry>", raw, re.DOTALL)
            results = []
            for entry in entries:
                title = re.search(r"<title>(.*?)</title>", entry)
                summary = re.search(r"<summary>(.*?)</summary>", entry)
                link = re.search(r'<id>(.*?)</id>', entry)
                published = re.search(r"<published>(.*?)</published>", entry)
                results.append({
                    "title": title.group(1).strip() if title else "",
                    "abstract": summary.group(1).strip()[:300] if summary else "",
                    "url": link.group(1).strip() if link else "",
                    "year": published.group(1)[:4] if published else "",
                })
            return results
    except Exception as e:
        print(f"  arXiv error: {e}")
        return []

def write_note(track, source, paper):
    """Write a paper note to 00_Inbox."""
    today = datetime.now().strftime("%Y-%m-%d")
    title = paper.get("title", "Untitled")[:80]
    # Sanitize filename
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)[:60]
    filename = f"{today}_{track}_{source}_{safe_title}.md"
    filepath = INBOX / filename
    
    if filepath.exists():
        return False
    
    authors = paper.get("authors", [])
    author_str = ", ".join([a.get("name", "") for a in authors[:5]])
    
    content = f"""---
title: "{title}"
date: {today}
track: {track}
source: {source}
authors: {author_str}
year: {paper.get('year', '')}
url: {paper.get('url', '')}
citations: {paper.get('citationCount', '')}
tags: [from-{source.lower()}, inbox, {track.lower()}]
---

# {title}

**来源**: {source}
**作者**: {author_str}
**年份**: {paper.get('year', '')}
**引用数**: {paper.get('citationCount', '')}

## 摘要

{paper.get('abstract', 'No abstract available.')[:500]}

## 链接

[{paper.get('url', '#')}]({paper.get('url', '#')})

---
*自动抓取于 {datetime.now().strftime("%Y-%m-%d %H:%M")} | 待分类处理*
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True

def main():
    print(f"\n{'='*60}")
    print(f"Daily Crawl Pipeline — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    
    total_new = 0
    
    for track, queries in QUERIES.items():
        print(f"\n[{track}] Searching...")
        for query in queries:
            print(f"  Query: {query[:60]}...")
            
            # Semantic Scholar
            papers = search_semantic_scholar(query, limit=3)
            for paper in papers:
                if write_note(track, "S2", paper):
                    total_new += 1
                    print(f"    + {paper.get('title','')[:60]}")
            time.sleep(1.5)  # Rate limit
            
            # arXiv
            arxiv_papers = search_arxiv(query, max_results=2)
            for paper in arxiv_papers:
                if write_note(track, "arXiv", paper):
                    total_new += 1
                    print(f"    + {paper.get('title','')[:60]}")
            time.sleep(0.5)
    
    print(f"\n{'='*60}")
    print(f"Done. {total_new} new papers added to 00_Inbox.")
    
    # Write log
    LOG_DIR.mkdir(exist_ok=True)
    logfile = LOG_DIR / f"crawl_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(logfile, "w") as f:
        json.dump({"date": datetime.now().isoformat(), "new_papers": total_new}, f)

if __name__ == "__main__":
    main()
