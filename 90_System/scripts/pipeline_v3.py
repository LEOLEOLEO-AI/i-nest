#!/usr/bin/env python3
"""
iNEST+TCC Research Pipeline v3.0 閿?Unified Daily Crawl 閿?Classify 閿?Graph
Combines daily_crawl.py + iNEST_crawler.py + build_graph.py
Fixed: NoneType crash, GBK encoding, deduped sources, TCC/iNEST focus
"""
import os, sys, json, re, time, ssl
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import urllib.request, urllib.parse, urllib.error
import time
import sys
sys.path.insert(0, r"D:\\Obsidian\\scripts")
from llm_router import llm_call
sys.path.insert(0, r'D:\Obsidian\home\work\.openclaw\workspace\90_System\scripts')
from enhance_papers import is_duplicate_crossday, mark_as_seen, enrich_paper_file, extract_s2_id_from_url, enrich_with_s2_detail
import xml.etree.ElementTree as ET

# 閳光偓閳光偓 Config 閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓
VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
INBOX = VAULT / "00_Inbox" / "_pipeline_insights"
LOG_DIR = VAULT / "logs"
LOG_DIR.mkdir(exist_ok=True)

S2_API_KEY = os.environ.get("S2_API_KEY", "REDACTED_S2_KEY")

TODAY = datetime.now().strftime("%Y-%m-%d")
ctx = ssl.create_default_context()

# S2 API Config

# 閳光偓閳光偓 S2 API Config 閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓
S2_DELAY = 1           # seconds between S2 queries (free tier: 1 req/s)
S2_RETRY_DELAY = 5    # seconds to wait on HTTP 429
S2_MAX_RETRIES = 1

# 閳光偓閳光偓 Search Queries (TCC + iNEST) 閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓
S2_QUERIES = [
    # === TCC: Topological/Spatial Computing ===
    "network-on-chip topology small-world complex network",
    "chiplet interconnect wafer-scale routing topology optimization",
    "temporal network dynamic topology reconfigurable computing",
    # === iNEST: Criticality & Emergence ===
    "self-organized criticality neuronal avalanche information capacity",
    "edge of chaos neuromorphic computing reservoir dynamics",
    "neuromorphic memristor spiking neural network critical",
    # === Bridge: Complex Network Theory 閳?Computation ===
    "complex network phase transition information processing emergence",
    "free energy principle self-organization neural computation",
    "integrated information causal emergence neural network",
    # === Higher-Order & Structural ===
    "higher-order network simplicial complex hypergraph information propagation",
    "multilayer network multiplex temporal dynamics synchronization",
    "network spatiotemporal coordination pattern formation self-organization",
    # === Emergence & Intelligence ===
    "causal emergence integrated information neural intelligence",
    "multiplicative interaction nonlinear synergy complex system emergence",
    "intrinsic motivation active inference free energy intelligence emergence",
    # === Complex Network Theory & Application ===
    "network geometry hyperbolic embedding complex network topology",
    "percolation phase transition complex network robustness resilience",
    # === Benchmarks ===
    "C. elegans connectome small-world network computation",
    "Drosophila connectome network topology computation emergence",
]

# iNEST-style cross-domain arXiv queries
ARXIV_QUERIES = [
    # ============ TCC: Topology-Centric Computing ============
    # Scale-up/out interconnect + NoC
    ("TCC-scale-noc", 'abs:(scale-up OR scale-out OR "network-on-chip" OR NoC) AND abs:(interconnect OR routing OR topology OR arbitration)'),
    # Wafer-scale / chiplet integration
    ("TCC-wafer-chiplet", 'abs:("wafer-scale" OR chiplet OR "2.5D" OR "3D-IC") AND abs:(integration OR interconnect OR network OR packaging)'),
    # Reconfigurable network
    ("TCC-reconfigurable", 'abs:(reconfigurable OR "software-defined" OR programmable) AND abs:(network OR interconnect OR routing OR topology)'),
    # Higher-order network topology
    ("TCC-higher-order", 'abs:("higher-order" OR simplicial OR hypergraph OR "multilayer network") AND abs:(topology OR network OR interconnect OR computing)'),
    # Network simulation + compilation
    ("TCC-sim-compile", 'abs:(simulation OR compiler OR "design space exploration" OR "cycle-accurate" OR SystemC) AND abs:("network-on-chip" OR NoC OR interconnect)'),
    # Network topology optimization
    ("TCC-topology-opt", 'abs:(topology AND (optimization OR synthesis OR "design automation")) AND abs:(network OR interconnect OR NoC)'),
    # Deadlock / congestion / QoS
    ("TCC-qos", 'abs:(deadlock OR congestion OR "quality-of-service" OR QoS OR "flow control") AND abs:(network OR interconnect OR NoC OR routing)'),

    # ============ iNEST: intelligent Neural Emergence SysTems ============
    # Self-organization + criticality
    ("iNEST-selforg-critical", 'abs:("self-organization" OR "self-organised" OR criticality OR "critical state") AND abs:(neural OR network OR dynamics OR emergence)'),
    # Nonlinear dynamics + complexity
    ("iNEST-nonlinear", 'abs:("nonlinear dynamics" OR "complex system" OR "complexity science") AND abs:(emergence OR "phase transition" OR bifurcation OR chaos)'),
    # Spatiotemporal coordination
    ("iNEST-spatiotemporal", 'abs:(spatiotemporal OR "spatial-temporal") AND abs:(coordination OR synchronization OR "pattern formation") AND abs:(neural OR network OR dynamics)'),
    # Neural networks (spiking, SNN)
    ("iNEST-snn", 'abs:("spiking neural" OR SNN OR "leaky integrate-and-fire" OR "neuromorphic") AND abs:(learning OR plasticity OR STDP OR architecture)'),
    # Intelligent emergence
    ("iNEST-emergence", 'abs:(emergence OR "emergent behavior" OR "collective intelligence") AND abs:(neural OR network OR agent OR "multi-agent")'),
    # Asynchronous + event-triggered
    ("iNEST-async", 'abs:(asynchronous OR "event-triggered" OR "event-driven" OR "clockless") AND abs:(circuit OR neural OR network OR computing)'),
    # Spatial + functional structure
    ("iNEST-structure", 'abs:("spatial structure" OR "functional connectivity" OR "network motif" OR "community structure") AND abs:(neural OR brain OR emergence OR dynamics)'),
    # Higher-order in iNEST context
    ("iNEST-higher-order", 'abs:("higher-order interaction" OR "simplicial complex" OR hypergraph) AND abs:(neural OR brain OR dynamics OR synchronization)'),
    # Free energy + active inference
    ("iNEST-free-energy", 'abs:("free energy principle" OR "active inference" OR "predictive coding") AND abs:(neural OR emergence OR self-organization)'),
    # Reservoir computing
    ("iNEST-reservoir", 'abs:("reservoir computing" OR "echo state" OR "liquid state machine") AND abs:(dynamics OR emergence OR criticality OR neuromorphic)'),

    # ============ Bridge: TCC <-> iNEST ============
    # Network science meets computation
    ("bridge-network-comp", 'abs:("complex network" OR "network science") AND abs:(computing OR architecture OR chip OR hardware)'),
    # Information theory + emergence
    ("bridge-info-emergence", 'abs:("information theory" OR "integrated information" OR "mutual information") AND abs:(emergence OR criticality OR "complex network")'),
]

# Google News RSS queries (for latest news)
GN_QUERIES = [
    ("TCC", "topological+computing+OR+chiplet+interconnect+OR+network+on+chip+OR+wafer-scale+integration"),
    ("iNEST", "neuromorphic+OR+spiking+neural+OR+brain-inspired+computing+OR+complex+network+emergence"),
    ("emergence", "emergence+intelligence+OR+criticality+neural+OR+self-organized+criticality+OR+causal+emergence"),
    ("complex-networks", "higher-order+network+OR+simplicial+complex+OR+multilayer+network+OR+temporal+network"),
]

seen_titles = set()  # dedup across sources
new_count = 0

# 閳光偓閳光偓 Helpers 閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def is_new(title):
    key = title.strip().lower()[:80]
    if key in seen_titles:
        return False
    seen_titles.add(key)
    return True

def generate_deep_insight(title, text, detail):
    """LLM-powered deep TCC/iNEST insight generation."""
    abstract = detail.get('abstract', text[:1000]) if detail else text[:1000]
    citations = detail.get('citations', 0) if detail else 0
    fields = detail.get('fields', '') if detail else ''

    prompt = "Analyze this paper for TCC (NoC/chiplet/interconnect) and iNEST (criticality/emergence/neural) projects.\nTitle: " + title + "\nAbstract: " + abstract[:800] + "\n\nOutput JSON: {relevance_score:0-3, tcc:connection or empty, inest:connection or empty, actionable:suggestion, track:TCC|iNEST|Bridge|General}. Be specific, in Chinese."

    try:
        result = llm_call(prompt, system='Analyze research papers for TCC+iNEST. Output pure JSON only.', task_type='insight', max_tokens=500)
        if result:
            result = result.strip()
            if result.startswith('```'):
                result = result.replace('```json', '').replace('```', '').strip()
            import json as _json
            try:
                data = _json.loads(result)
                data['relevance_score'] = data.get('relevance_score', 1)
                return data
            except _json.JSONDecodeError:
                pass
    except Exception:
        pass

    # Keyword fallback
    text_lower = text.lower()
    kw_tcc = ['noc','network-on-chip','chiplet','wafer','interconnect','topolog','routing','scale-up','scale-out']
    kw_inest = ['neural','emergence','critical','self-organiz','bifurcation','nonlinear','spiking','reservoir','dynamics','phase transition']
    tcc_hits = [kw for kw in kw_tcc if kw in text_lower]
    inest_hits = [kw for kw in kw_inest if kw in text_lower]

    if not tcc_hits and not inest_hits:
        return {'relevance_score': 0}

    return {
        'relevance_score': min(len(tcc_hits) + len(inest_hits), 3),
        'tcc': 'Keyword: ' + ', '.join(tcc_hits[:3]) if tcc_hits else '',
        'inest': 'Keyword: ' + ', '.join(inest_hits[:3]) if inest_hits else '',
        'actionable': 'Review for relevance to TCC/iNEST.',
        'track': 'iNEST' if len(inest_hits) > len(tcc_hits) else 'TCC'
    }

def safe_filename(s):
    return re.sub(r'[<>:"/\\|?*]', "", s)[:60]

def write_insight(title, abstract, url, source, track="General", year="", authors="", s2_detail=None):
    """Write an insight note to inbox with enrichment from S2 detail."""
    global new_count
    if not is_new(title):
        return False
    safe = safe_filename(title)
    fp = INBOX / f"{TODAY}_{source}_{safe}.md"
    if fp.exists():
        return False
    s2_id = extract_s2_id_from_url(url) if source == 'S2' else None
    is_dup, reason = is_duplicate_crossday(title, s2_id)
    if is_dup:
        log(f"  鐠哄疇绻?闁插秴顦?: {title[:50]}... [{reason}]")
        return False
    
    detail = s2_detail or {}
    if source == 'S2' and s2_id and not detail:
        try:
            detail = enrich_with_s2_detail({'s2_id': s2_id, 'url': url}) or {}
        except:
            detail = {}
    
    full_text = (title + " " + detail.get('abstract', abstract or "")).lower()
    insight = generate_deep_insight(title, full_text, detail)
    
    if not insight or insight.get('relevance_score', 0) == 0:
        log(f"  鐠哄疇绻?瀵京娴夐崗?: {title[:50]}...")
        return False
    
    tcc_block = ""
    if insight.get('tcc'):
        tcc_block = f"## TCC Insights\n\n{insight['tcc']}\n"
    inest_block = ""
    if insight.get('inest'):
        inest_block = f"## iNEST Insights\n\n{insight['inest']}\n"
    actionable = ""
    if insight.get('actionable'):
        actionable = f"## Actionable\n\n{insight['actionable']}\n"
    
    citations = detail.get('citations', 0)
    refs = detail.get('refs', 0)
    fields = detail.get('fields', "")
    journal = detail.get('journal', "")
    doi = detail.get('doi', "")
    tldr = detail.get('tldr', "")
    
    parts = []
    parts.append("---")
    parts.append(f'title: "{title}"')
    parts.append(f"date: {TODAY}")
    parts.append(f"source: {source}")
    parts.append(f"track: {track}")
    parts.append(f"authors: {authors}")
    parts.append(f"year: {detail.get('year', year)}")
    parts.append(f"url: {url}")
    parts.append(f"tags: [inbox, {track.lower()}, {source.lower()}]")
    parts.append(f"citations: {citations}")
    parts.append(f"relevance: {insight.get('relevance_score', 1)}")
    parts.append("status: inbox")
    parts.append("---")
    parts.append("")
    parts.append(f"# {title}")
    parts.append("")
    parts.append(f"**{authors}** ({detail.get('year', year)}) | *{journal or 'N/A'}*")
    parts.append(f"**Citations**: {citations} | **References**: {refs}")
    if fields:
        parts.append(f"**妫板棗鐓?*: {fields}")
    if doi:
        parts.append(f"**DOI**: {doi}")
    parts.append(f"**闁剧偓甯?*: [{url}]({url})")
    parts.append("")
    if tldr:
        parts.append(f"## Summary")
        parts.append("")
        parts.append(tldr)
        parts.append("")
    if detail.get('abstract') or abstract:
        parts.append(f"## Abstract")
        parts.append("")
        txt = detail.get('abstract', abstract or "")
        parts.append(txt[:1200])
        parts.append("")
    if tcc_block:
        parts.append("## TCC Insights")
        parts.append("")
        parts.append(insight['tcc'])
        parts.append("")
    if inest_block:
        parts.append("## iNEST Insights")
        parts.append("")
        parts.append(insight['inest'])
        parts.append("")
    if actionable:
        parts.append("## Actionable")
        parts.append("")
        parts.append(insight['actionable'])
        parts.append("")
    parts.append("---")
    parts.append(f"*{TODAY} 缁夋垹鐖虹粻锛勫殠v3.1閼奉亜濮╅幓鎰仹 | 閻╃鍙ф惔? {insight.get('relevance_score', 1)}/3*")
    
    content = "\n".join(parts)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    new_count += 1
    mark_as_seen(title, s2_id=s2_id, filepath=str(fp))
    log(f"  Insight [{insight.get('relevance_score', '?')}/3]: {title[:50]}...")
    return True

def crawl_semantic_scholar():
    """Search Semantic Scholar API for TCC/iNEST papers."""
    log("[S2] 濡偓缁?Semantic Scholar...")
    count = 0
    for query in S2_QUERIES:
        params = {
            "query": query,
            "limit": 3,
            "fields": "title,authors,year,abstract,url,externalIds,citationCount,publicationDate",
            "sort": "publicationDate:desc"
        }
        url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url)
        if S2_API_KEY:
            req.add_header("x-api-key", S2_API_KEY)
        retries = 0
        while retries <= S2_MAX_RETRIES:
            try:
                with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
                    data = json.loads(resp.read())
                    for paper in data.get("data", []):
                        if paper is None:
                            continue
                        title = paper.get("title", "") or ""
                        pub_date = paper.get("publicationDate") or ""
                        if pub_date:
                            try:
                                pd = datetime.strptime(pub_date, "%Y-%m-%d")
                                if (datetime.now() - pd).days > 90:
                                    continue
                            except:
                                pass
                        if write_insight(title,
                                        paper.get("abstract") or "(no abstract)",
                                        paper.get("url", "") or "",
                                        "S2",
                                        "TCC" if any(kw in query.lower() for kw in ["topological","chiplet","noc","network-on-chip","wafer","dark silicon"]) else "iNEST",
                                        str(paper.get("year", "") or ""),
                                        ", ".join(a.get("name", "") for a in (paper.get("authors", []) or [])[:5])):
                            count += 1
                break
            except urllib.error.HTTPError as e:
                if e.code == 429 and retries < S2_MAX_RETRIES:
                    retries += 1
                    log(f"  S2 429 ({query[:30]}...): wait {S2_RETRY_DELAY}s retry({retries}/{S2_MAX_RETRIES})")
                    time.sleep(S2_RETRY_DELAY)
                else:
                    log(f"  S2 error ({query[:30]}...): HTTP {e.code if hasattr(e,'code') else e}")
                    break
            except Exception as e:
                log(f"  S2 error ({query[:30]}...): {str(e)[:60]}")
                break
        time.sleep(S2_DELAY)

    log(f"[S2] {count} new papers")
    return count

# 閳光偓閳光偓 Source 2: arXiv 閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓
def crawl_arxiv():
    """Search arXiv with 5 sec delay between queries."""
    log("[arXiv] 濡偓缁?arXiv (娴溿倕寮堕弻銉嚄)...")
    count = 0
    for label, q in ARXIV_QUERIES:
        today = datetime.now().strftime("%Y%m%d")
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
        url = f"https://export.arxiv.org/api/query?search_query={urllib.parse.quote(q)}+AND+submittedDate:[{week_ago}+TO+{today}]&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
        req = urllib.request.Request(url, headers={"User-Agent": "iNEST-Pipeline/3.0"})
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                root = ET.fromstring(resp.read().decode("utf-8"))
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                t = entry.find("atom:title", ns)
                p_el = entry.find("atom:published", ns)
                i_el = entry.find("atom:id", ns)
                s_el = entry.find("atom:summary", ns)
                if t is None or p_el is None:
                    continue
                title = t.text.strip().replace("\n", " ") if t.text else ""
                pubdate = p_el.text[:10] if p_el.text else ""
                link = i_el.text.strip() if i_el is not None and i_el.text else ""
                abstract = s_el.text.strip().replace("\n", " ")[:500] if s_el is not None and s_el.text else ""
                try:
                    pd = datetime.strptime(pubdate, "%Y-%m-%d") if pubdate else datetime.now()
                    if (datetime.now() - pd).days > 7:
                        continue
                except:
                    pass
                track = "iNEST" if label.startswith("iNEST") else ("TCC" if label.startswith("TCC") else "General")
                if write_insight(title, abstract, link, "arXiv", track, pubdate[:4]):
                    count += 1
        except urllib.error.HTTPError as e:
            log(f"  arXiv {label}: HTTP {e.code}")
            if e.code == 429:
                time.sleep(20)
        except urllib.error.URLError as e:
            log(f"  arXiv {label}: network error, skipping")
            continue
        except Exception as e:
            log(f"  arXiv {label}: {str(e)[:60]}")
            continue
        time.sleep(3)  # Rate limit
    log(f"[arXiv] Coverage: {count} new in last 7 days across {len(ARXIV_QUERIES)} queries")
    return count

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
                    if write_insight(title, "", link, "GoogleNews", track):
                        count += 1
        except Exception as e:
            log(f"  GN error ({track}): {str(e)[:60]}")
        time.sleep(1)
    log(f"[GN] {count} new articles")
    return count

# 閳光偓閳光偓 闂冭埖顔?: 閸掑棛琚径鍕倞 Inbox (classify with LLM) 閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓
def call_deepseek(prompt, max_tokens=300, task_type="classification"):
    """Call LLM via unified router with task-aware model selection."""
    try:
        return llm_call(
            prompt,
            system="You are a research assistant. Output ONLY valid JSON.",
            task_type=task_type,
            max_tokens=max_tokens,
            temperature=0.1
        )
    except Exception as e:
        log(f"  LLM: {str(e)}")
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
        log(f"  閿?ARCHIVE {fp.name}")
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
    if summary and "## AI Summary" not in content and "## AI Summary" not in content:
        content += f"\n\n## AI 閹芥顩n\n{summary}\n"
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    
    os.rename(fp, target)
    log(f"  閿?{target.relative_to(VAULT)} [{track}]")

    log("[Process] LLM classifying inbox -> _pipeline_insights")
    return 0


def process_inbox(limit=20):
    """Classify inbox items using free LLM tier."""
    log("[Process] LLM classify (free tier, limit=" + str(limit) + ")...")
    count = 0
    inbox = VAULT / "00_Inbox"
    if not inbox.exists():
        return 0
    files = sorted(inbox.rglob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    for fp in files:
        if "_pipeline_insights" in str(fp):
            continue
        if count >= limit:
            break
        if classify_and_move(fp):
            count += 1
    log("[Process] Classified: " + str(count))
    return count

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



# -- Stage 4: Generate Genspark Research Brief ---------------------------------
def generate_genspark_snapshot():
    """Generate a useful research brief for Genspark deep analysis.
    Includes: active paper status, recent paper abstracts, inbox highlights,
    knowledge graph hotspots, and open research questions."""
    log("[Genspark] Generating research brief...")
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    brief_path = VAULT / "99_Meta" / "genspark_research_brief.md"
    brief_path.parent.mkdir(parents=True, exist_ok=True)

    active_papers = {
        "P-Paradigm": {"title": "Topology-Centric Computing Paradigm", "target": "Nature Electronics", "status": "framework", "track": "TCC"},
        "P-Mapping": {"title": "Physical Topology Mapping", "target": "IEEE TPDS", "status": "drafting", "track": "TCC"},
        "B0-Engineering": {"title": "Baseline Engineering Edition", "target": "TBD", "status": "v7 SUBMISSION", "track": "TCC"},
        "CST-Emergence": {"title": "CST Intelligent Emergence", "target": "TBD", "status": "V25 FINAL", "track": "iNEST"},
        "iNEST-Core": {"title": "iNEST Core Architecture", "target": "TBD", "status": "framework", "track": "iNEST"},
        "Liquid-Computing": {"title": "Liquid Computing Chemistry", "target": "TBD", "status": "framework", "track": "iNEST"}
    }

    recent_papers = []
    papers_dir = VAULT / "10_Library" / "Papers"
    if papers_dir.exists():
        paper_files = sorted(papers_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)[:12]
        for pf in paper_files:
            try:
                text = pf.read_text(encoding="utf-8", errors="ignore")
                if text.startswith("---"):
                    parts = text.split("---", 2)
                    body = parts[2] if len(parts) > 2 else text
                else:
                    body = text
                first_para = body.strip().split("\n\n")[0] if body.strip() else ""
                first_para = first_para.replace("\n", " ")[:300]
                recent_papers.append({
                    "title": pf.stem[:100],
                    "date": datetime.fromtimestamp(pf.stat().st_mtime).strftime("%Y-%m-%d"),
                    "excerpt": first_para
                })
            except:
                pass

    inbox_highlights = []
    inbox_dir = VAULT / "00_Inbox"
    inbox_files = sorted(
        [f for f in inbox_dir.rglob("*.md") if f.name != ".gitkeep"],
        key=lambda f: f.stat().st_mtime, reverse=True
    )[:8]
    for f in inbox_files:
        inbox_highlights.append({
            "name": f.stem[:80],
            "date": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d"),
            "folder": str(f.parent.relative_to(inbox_dir)) if f.parent != inbox_dir else "root"
        })

    graph_data = {"nodes": [], "edges": []}
    graph_path = VAULT / "knowledge_graph" / "graph_data.json"
    if graph_path.exists():
        try:
            graph_data = json.loads(open(graph_path, encoding="utf-8").read())
        except:
            pass
    nodes_sorted = sorted(
        graph_data.get("nodes", []),
        key=lambda n: n.get("out_degree", 0) + n.get("in_degree", 0),
        reverse=True
    )[:8]
    hotspots = [(n["label"], n.get("out_degree", 0) + n.get("in_degree", 0))
                for n in nodes_sorted if n.get("label")]

    total_notes = len(list(VAULT.rglob("*.md")))

    lines = []
    lines.append("---")
    lines.append(f"title: iNEST+TCC Research Brief - {today}")
    lines.append(f"date: {today}")
    lines.append("type: research-brief")
    lines.append("target: genspark")
    lines.append("---")
    lines.append("")
    lines.append(f"# iNEST + TCC Research Brief - {today}")
    lines.append("")
    lines.append("> For Genspark deep analysis. Contains actionable research context.")
    lines.append("")

    lines.append("## 1. Active Papers")
    lines.append("")
    lines.append("| Paper | Track | Target | Status |")
    lines.append("|-------|-------|--------|--------|")
    for pid, info in active_papers.items():
        lines.append(f"| {pid}: {info['title']} | {info['track']} | {info['target']} | {info['status']} |")
    lines.append("")

    lines.append("## 2. Core Research Questions (for Genspark analysis)")
    lines.append("")
    lines.append("1. **TCC**: How does network topology quantitatively determine computational capability? Route=Transform equivalence?")
    lines.append("2. **iNEST**: What is the minimal physical rule set that yields self-organized criticality in silicon?")
    lines.append("3. **Engineering**: How to implement SDI flexible interconnects at wafer scale with ns-level reconfiguration?")
    lines.append("4. **Theory**: Relationship between network connection scale and intelligence emergence? (Unproven hypothesis)")
    lines.append("")

    lines.append("## 3. Recent Papers (past week)")
    lines.append("")
    if recent_papers:
        for p in recent_papers:
            lines.append(f"### {p['title']}")
            lines.append(f"- Date: {p['date']}")
            if p['excerpt']:
                lines.append(f"- Excerpt: {p['excerpt']}")
            lines.append("")
    else:
        lines.append("(No recent papers scanned)")
        lines.append("")

    lines.append("## 4. Inbox Highlights")
    lines.append("")
    if inbox_highlights:
        for item in inbox_highlights:
            lines.append(f"- [{item['date']}] **{item['name']}** ({item['folder']})")
    else:
        lines.append("(Inbox empty)")
    lines.append("")

    lines.append("## 5. Knowledge Graph Hotspots")
    lines.append("")
    lines.append(f"Total notes: {total_notes}")
    lines.append(f"Graph nodes: {len(graph_data.get('nodes', []))} | edges: {len(graph_data.get('edges', []))}")
    lines.append("")
    if hotspots:
        lines.append("Top connected topics:")
        for label, deg in hotspots:
            lines.append(f"- **{label}** (degree={deg})")
    lines.append("")

    lines.append("## 6. Innovation Brief (latest)")
    lines.append("")
    ib_path = VAULT / "99_Meta" / f"innovation_brief_{today}.md"
    if ib_path.exists():
        try:
            ib_text = ib_path.read_text(encoding="utf-8", errors="ignore")
            lines.append(ib_text[:1000])
        except:
            lines.append("(Innovation brief not available)")
    else:
        lines.append("(Run innovation_engine.py to generate)")
    lines.append("")

    lines.append("---")
    lines.append(f"*Research brief auto-generated {now.strftime('%Y-%m-%d %H:%M')}*")
    lines.append("")

    brief_text = "\n".join(lines)
    brief_path.write_text(brief_text, encoding="utf-8")
    log(f"[Genspark] Research brief written: genspark_research_brief.md")
    return str(brief_path.relative_to(VAULT))


def main():
    print(f"\n{'='*60}")
    print(f"  iNEST + TCC Research Pipeline v3.3")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    
    start = time.time()
    
    # Stage 1: Crawl
    log("[S2] Skipped (rate limited). Using arXiv only.")
    c1 = 0
    c2 = crawl_arxiv()
    c3 = crawl_google_news()
    
    print(f"\n  Total: {c1+c2+c3} new items to inbox")
    
    # Stage 2: Process
    processed = process_inbox(limit=0)
    
    # 闂冭埖顔?: 閻儴鐦戦崶鎹愭皑
    snapshot = generate_genspark_snapshot()
    nodes, edges, missing = scan_and_build_graph()
    # Stage 5: Push insights to dashboard
    try:
        import subprocess
        dash_script = str(VAULT / '90_System' / 'scripts' / 'dashboard_data_v3.py')
        subprocess.run([sys.executable, dash_script], capture_output=True, text=True, timeout=120, cwd=str(VAULT))
        log("[Dashboard] Updating kanban...")
    except Exception as e:
        log(f"[Dashboard] Error: {e}")

    
    elapsed = time.time() - start
    print(f"\n{'='*60}")
    print(f"  Pipeline v3.3 Complete")
    print(f"  Sources: {c1}(S2) + {c2}(arXiv) + {c3}(GN) = {c1+c2+c3}")
    print(f"  Processed: {processed} | Nodes: {nodes} edges: {edges} | Missing links: {missing} | Genspark: OK")
    print(f"  Elapsed: {elapsed:.0f}s")
    print(f"{'='*60}")
    
    # Log
    log_data = {
        "date": datetime.now().isoformat(),
        "new_papers": c1+c2+c3,
        "classified": processed,
        "graph_nodes": nodes, "graph_edges": edges,
        "elapsed_s": round(elapsed, 1),
        "genspark_snapshot": snapshot
    }
    with open(LOG_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M')}.json", "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

if __name__ == "__main__":
    main()


