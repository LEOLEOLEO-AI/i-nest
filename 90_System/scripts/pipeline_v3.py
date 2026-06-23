#!/usr/bin/env python3
"""
iNEST+TCC Research Pipeline v3.0 — Unified Daily Crawl → Classify → Graph
Combines daily_crawl.py + iNEST_crawler.py + build_graph.py
Fixed: NoneType crash, GBK encoding, deduped sources, TCC/iNEST focus
"""
import os, sys, json, re, time, ssl
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET

# ── Config ──────────────────────────────────────────────
VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
INBOX = VAULT / "00_Inbox"
LOG_DIR = VAULT / "logs"
LOG_DIR.mkdir(exist_ok=True)

S2_API_KEY = os.environ.get("S2_API_KEY", "s2k-hUuwuX3sqJjRFbkjC6OZg4aR6yyJxkRzxcHKNJZx")
DS_API_KEY = os.environ.get("DS_API_KEY", "sk-ef017fea9cc64cbe8185061772998930")

TODAY = datetime.now().strftime("%Y-%m-%d")
ctx = ssl.create_default_context()

# ── Search Queries (TCC + iNEST) ───────────────────────
S2_QUERIES = [
    # TCC
    "topological computing wafer scale integration",
    "chiplet interconnect routing",
    "network-on-chip topology optimization",
    "software defined system on wafer",
    "variational free energy neuromorphic",
    "dark silicon manycore architecture",
    # iNEST
    "neuromorphic computing spiking neural network",
    "self-organized criticality neural systems",
    "memristor array in-memory computing",
    "emergence complex systems neural network",
    "brain-inspired computing architecture",
    "neuronal avalanche critical dynamics",
]

# iNEST-style cross-domain arXiv queries
ARXIV_QUERIES = [
    ("RG-neural", 'abs:"renormalization group" AND (abs:neural OR abs:brain OR abs:cortex)'),
    ("neural-criticality", 'abs:criticality AND (abs:neural OR abs:brain OR abs:neuronal avalanche)'),
    ("SOC-neural", 'abs:"self-organized criticality" AND (abs:neural OR abs:brain)'),
    ("complex-net-phase", 'abs:"complex network" AND abs:"phase transition" AND (abs:neural OR abs:brain)'),
    ("neuromorphic-emergence", 'abs:neuromorphic AND (abs:self-organization OR abs:emergence)'),
    ("LSM-hardware", 'abs:"liquid state machine" AND abs:hardware OR abs:"reservoir computing" AND abs:chip'),
    ("SNN-hardware", 'abs:"spiking neural network" AND (abs:chip OR abs:FPGA OR abs:memristor)'),
    ("emergence-theory", 'abs:emergence AND abs:intelligence AND (abs:theory OR abs:thermodynamics)'),
]

# Google News RSS queries (for latest news)
GN_QUERIES = [
    ("TCC", "topological+computing+OR+chiplet+interconnect+OR+network+on+chip"),
    ("iNEST", "neuromorphic+OR+spiking+neural+OR+brain-inspired+computing"),
    ("emergence", "emergence+intelligence+OR+criticality+neural+OR+self-organized+criticality"),
]

seen_titles = set()  # dedup across sources
new_count = 0

# ── Helpers ────────────────────────────────────────────
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def is_new(title):
    key = title.strip().lower()[:80]
    if key in seen_titles:
        return False
    seen_titles.add(key)
    return True

def safe_filename(s):
    return re.sub(r'[<>:"/\\|?*]', "", s)[:60]

def write_paper(title, abstract, url, source, track="General", year="", authors=""):
    """Write to 00_Inbox with proper frontmatter."""
    global new_count
    if not is_new(title):
        return False
    safe = safe_filename(title)
    fp = INBOX / f"{TODAY}_{source}_{safe}.md"
    if fp.exists():
        return False
    
    content = f"""---
title: "{title}"
date: {TODAY}
source: {source}
track: {track}
authors: {authors}
year: {year}
url: {url}
tags: [from-{source.lower()}, auto-crawl, {track.lower()}]
status: inbox
---

# {title}

**Source**: {source} | **Track**: {track} | **Date**: {TODAY}
**Authors**: {authors} | **Year**: {year}
**URL**: [{url}]({url})

## Abstract

{abstract[:800] if abstract else "(no abstract)"}

## Relevance to TCC / iNEST

(TBD — process_inbox will auto-classify)

---
*Auto-crawled {TODAY} by Research Pipeline v3.0 | Inbox — needs classification*
"""
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    new_count += 1
    return True

# ── Source 1: Semantic Scholar ─────────────────────────
def crawl_semantic_scholar():
    """Search Semantic Scholar API for TCC/iNEST papers."""
    log("[S2] Searching Semantic Scholar...")
    count = 0
    for query in S2_QUERIES:
        params = {
            "query": query,
            "limit": 3,
            "fields": "title,authors,year,abstract,url,externalIds,citationCount"
        }
        url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url)
        if S2_API_KEY:
            req.add_header("x-api-key", S2_API_KEY)
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                data = json.loads(resp.read())
                for paper in data.get("data", []):
                    if paper is None:
                        continue  # ← FIX: skip None items
                    title = paper.get("title", "") or ""
                    abstract = paper.get("abstract") or "(no abstract)"
                    paper_url = paper.get("url", "") or ""
                    authors_list = paper.get("authors", []) or []
                    author_str = ", ".join(a.get("name", "") for a in authors_list[:5])
                    year = paper.get("year", "") or ""
                    track = "TCC" if any(kw in query.lower() for kw in ["topological","chiplet","noc","network-on-chip","wafer","dark silicon"]) else "iNEST"
                    if write_paper(title, abstract, paper_url, "S2", track, str(year), author_str):
                        count += 1
        except Exception as e:
            log(f"  S2 error ({query[:30]}...): {str(e)[:60]}")
        time.sleep(1.2)
    log(f"[S2] {count} new papers")
    return count

# ── Source 2: arXiv ────────────────────────────────────
def crawl_arxiv():
    """Search arXiv with intersectional TCC/iNEST queries."""
    log("[arXiv] Searching (intersectional abs: queries)...")
    count = 0
    for label, q in ARXIV_QUERIES:
        url = f"https://export.arxiv.org/api/query?search_query={q}&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
        req = urllib.request.Request(url, headers={"User-Agent": "iNEST-Pipeline/3.0"})
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
                root = ET.fromstring(resp.read().decode("utf-8"))
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                t = entry.find("atom:title", ns)
                p = entry.find("atom:published", ns)
                i = entry.find("atom:id", ns)
                s = entry.find("atom:summary", ns)
                if t is None or p is None:
                    continue
                title = t.text.strip().replace("\n", " ") if t.text else ""
                pubdate = p.text[:10] if p.text else ""
                link = i.text.strip() if i is not None and i.text else ""
                abstract = s.text.strip().replace("\n", " ")[:500] if s is not None and s.text else ""
                try:
                    pd = datetime.strptime(pubdate, "%Y-%m-%d") if pubdate else datetime.now()
                    if (datetime.now() - pd).days > 14:
                        continue
                except:
                    continue
                if is_new(title):
                    track = "TCC" if "topological" in label or "network" in label else "iNEST"
                    if write_paper(title, abstract, link, "arXiv", track, pubdate[:4]):
                        count += 1
        except urllib.error.HTTPError as e:
            log(f"  arXiv {label}: HTTP {e.code}")
            time.sleep(15)  # rate limit backoff
        except Exception as e:
            log(f"  arXiv {label}: {str(e)[:60]}")
        time.sleep(3.5)  # arXiv rate limit
    log(f"[arXiv] {count} new papers")
    return count

# ── Source 3: Google News RSS ──────────────────────────
def crawl_google_news():
    """Fetch latest tech/science news from Google News RSS."""
    log("[GN] Google News RSS...")
    count = 0
    for track, q in GN_QUERIES:
        url = f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
                root = ET.fromstring(resp.read().decode("utf-8"))
            for item in root.findall(".//item"):
                t = item.find("title")
                l = item.find("link")
                p = item.find("pubDate")
                if t is None:
                    continue
                title = t.text or ""
                link = l.text if l is not None and l.text else ""
                pubdate = p.text[:22] if p is not None and p.text else ""
                try:
                    pd = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M") if pubdate else datetime.now()
                    if (datetime.now() - pd).days > 7:
                        continue
                except:
                    continue
                if is_new(title):
                    if write_paper(title, "", link, "GoogleNews", track):
                        count += 1
        except Exception as e:
            log(f"  GN error ({track}): {str(e)[:60]}")
        time.sleep(1)
    log(f"[GN] {count} new articles")
    return count

# ── Stage 2: Process Inbox (classify with LLM) ─────────
def call_deepseek(prompt, max_tokens=300):
    """Call DeepSeek V4 API."""
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a research assistant. Output ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.1
    }
    req = urllib.request.Request(
        "https://api.deepseek.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {DS_API_KEY}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())["choices"][0]["message"]["content"]
    except Exception as e:
        log(f"  LLM: {str(e)[:60]}")
        return None

def classify_and_move(fp):
    """Classify a single inbox file and move to correct directory."""
    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    prompt = f"""Classify this research note. JSON only:
{{"track":"TCC"|"iNEST"|"General", "category":"Paper"|"Article"|"Concept"|"Insight"|"Fleeting",
  "tags":["tag1","tag2"], "summary":"one sentence Chinese", "quality":"high"|"medium"|"low"}}

Title: {fp.name}
Content: {content[:1500]}"""
    result = call_deepseek(prompt, 200)
    if not result:
        return
    m = re.search(r'\{.*\}', result, re.DOTALL)
    if not m:
        return
    try:
        cls = json.loads(m.group())
    except:
        return
    
    track = cls.get("track", "General")
    category = cls.get("category", "Other")
    quality = cls.get("quality", "medium")
    tags = cls.get("tags", [])
    summary = cls.get("summary", "")
    
    if quality == "low":
        target = VAULT / "_archive" / "low_quality" / fp.name
        target.parent.mkdir(parents=True, exist_ok=True)
        os.rename(fp, target)
        log(f"  → ARCHIVE {fp.name}")
        return
    
    # Map to directory
    dir_map = {"Paper": "Papers", "Article": "Articles", "Concept": "Concepts",
               "Insight": "Insights", "Fleeting": "Fleeting"}
    sub = dir_map.get(category, "Inbox")
    target_dir = VAULT / "10_Knowledge" / sub if category in dir_map else (
        VAULT / "20_Projects" / f"_{track}" if track in ("TCC", "iNEST") else VAULT / "Inbox")
    
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / fp.name
    if target.exists():
        target = target_dir / f"{fp.stem}_dup.md"
    
    # Update frontmatter
    tags_fix = tags + ["classified", track.lower()]
    tags_line = "tags: [" + ", ".join(tags_fix) + "]"
    content = re.sub(r'tags:\s*\[.*?\]', tags_line, content)
    if summary and "## AI Summary" not in content and "## AI 摘要" not in content:
        content += f"\n\n## AI 摘要\n\n{summary}\n"
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    
    os.rename(fp, target)
    log(f"  → {target.relative_to(VAULT)} [{track}]")

def process_inbox(limit=15):
    """Classify and organize inbox items."""
    log("[Process] Classifying inbox items...")
    files = sorted(
        [f for f in INBOX.glob("*.md") if f.name != ".gitkeep"],
        key=lambda f: f.stat().st_mtime
    )[:limit]
    if not files:
        log("[Process] No files to process")
        return 0
    for fp in files:
        classify_and_move(fp)
        time.sleep(0.5)
    log(f"[Process] {len(files)} processed")
    return len(files)

# ── Stage 3: Build Knowledge Graph ─────────────────────
def scan_and_build_graph():
    """Scan all .md files, extract [[wikilinks]], build graph, suggest backlinks."""
    log("[Graph] Scanning wiki links...")
    EXCLUDE = {".git", ".obsidian", ".venv", ".trash", "node_modules", "_archive"}
    links = defaultdict(set)
    backlinks = defaultdict(set)
    files = {}
    
    for root, dirs, fns in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE and not d.startswith(".")]
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            full = Path(root) / fn
            try:
                rel = str(full.relative_to(VAULT)).replace("\\", "/")
            except:
                continue
            name = fn[:-3]
            files[rel] = name
            try:
                with open(full, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except:
                continue
            for target in set(re.findall(r'\[\[([^\]|#]+)', content)):
                if target.strip() and target.strip() != name:
                    links[rel].add(target.strip())
                    backlinks[target.strip()].add(rel)
    
    log(f"[Graph] {len(files)} files, {sum(len(v) for v in links.values())} links")
    
    # Export graph JSON
    nodes = [{"id": fp, "label": name,
              "out_degree": len(links.get(fp, set())),
              "in_degree": len(backlinks.get(fp, set()))}
             for fp, name in files.items()]
    edges = []
    for src, tgts in links.items():
        for t in tgts:
            tgt_file = next((fp for fp, n in files.items() if n == t), None)
            if tgt_file:
                edges.append({"source": src, "target": tgt_file})
    
    out = VAULT / "knowledge_graph" / "graph_data.json"
    out.parent.mkdir(exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"nodes": nodes, "edges": edges}, f, ensure_ascii=False, indent=2)
    log(f"[Graph] Exported: {len(nodes)} nodes, {len(edges)} edges")
    
    # Suggest missing backlinks
    suggestions = []
    for src, tgts in links.items():
        src_name = files.get(src, "")
        for t in tgts:
            if src_name and src not in backlinks.get(t, set()):
                tgt_file = next((fp for fp, n in files.items() if n == t), None)
                if tgt_file:
                    suggestions.append({
                        "action": f"Add [[{src_name}]] to {tgt_file}",
                        "source": src, "target": tgt_file
                    })
    log(f"[Graph] {len(suggestions)} missing backlinks")
    return len(nodes), len(edges), len(suggestions)

# ── Main ────────────────────────────────────────────────
def main():
    print(f"\n{'='*60}")
    print(f"  iNEST + TCC Research Pipeline v3.0")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    
    start = time.time()
    
    # Stage 1: Crawl
    c1 = crawl_semantic_scholar()
    c2 = crawl_arxiv()
    c3 = crawl_google_news()
    
    print(f"\n  Stage 1 Complete: {c1+c2+c3} new items to inbox")
    
    # Stage 2: Process
    processed = process_inbox(limit=20)
    
    # Stage 3: Build graph
    nodes, edges, missing = scan_and_build_graph()
    
    elapsed = time.time() - start
    print(f"\n{'='*60}")
    print(f"  Pipeline v3.0 Complete")
    print(f"  New: {c1}(S2) + {c2}(arXiv) + {c3}(GN) = {c1+c2+c3}")
    print(f"  Classified: {processed} | Graph: {nodes}N {edges}E | Missing BL: {missing}")
    print(f"  Time: {elapsed:.0f}s")
    print(f"{'='*60}")
    
    # Log
    log_data = {
        "date": datetime.now().isoformat(),
        "new_papers": c1+c2+c3,
        "classified": processed,
        "graph_nodes": nodes, "graph_edges": edges,
        "elapsed_s": round(elapsed, 1)
    }
    with open(LOG_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M')}.json", "w") as f:
        json.dump(log_data, f, indent=2)

if __name__ == "__main__":
    main()

