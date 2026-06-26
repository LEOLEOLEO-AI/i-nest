#!/usr/bin/env python3
"""
iNEST+TCC Research Pipeline v3.0 �?Unified Daily Crawl �?Classify �?Graph
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

# ── Config ──────────────────────────────────────────────
VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
INBOX = VAULT / "00_Inbox" / "_pipeline_insights"
LOG_DIR = VAULT / "logs"
LOG_DIR.mkdir(exist_ok=True)

S2_API_KEY = os.environ.get("S2_API_KEY", "s2k-hUuwuX3sqJjRFbkjC6OZg4aR6yyJxkRzxcHKNJZx")

TODAY = datetime.now().strftime("%Y-%m-%d")
ctx = ssl.create_default_context()

# ── Search Queries (TCC + iNEST) ───────────────────────
S2_QUERIES = [
    # === TCC: Small-world topology for wafer-scale computing ===
    "network-on-chip topology small-world complex network",
    "chiplet interconnect wafer-scale routing topology optimization",
    # === iNEST: Criticality & emergence in neural systems ===
    "self-organized criticality neuronal avalanche information capacity",
    "edge of chaos neuromorphic computing reservoir dynamics",
    "neuromorphic memristor spiking neural network critical",
    # === Bridge: Complex network theory → computation ===
    "complex network phase transition information processing emergence",
    "free energy principle self-organization neural computation",
    "integrated information causal emergence neural network",
    # === Benchmarks: Known systems ===
    "C. elegans connectome small-world network computation",
]

# iNEST-style cross-domain arXiv queries
ARXIV_QUERIES = [
    ("criticality-information", 'abs:criticality AND abs:"information capacity" AND (abs:neural OR abs:network)'),
    ("neuromorphic-critical", 'abs:neuromorphic AND abs:critical AND (abs:chip OR abs:hardware)'),
    ("emergence-complex", 'abs:emergence AND abs:"complex network" AND (abs:intelligence OR abs:computation)'),
    ("smallworld-computing", 'abs:"small-world" AND (abs:computing OR abs:chip OR abs:interconnect)'),
    ("free-energy-neural", 'abs:"free energy" AND abs:neural AND (abs:self-organization OR abs:emergence)'),
    ("NoC-topology", 'abs:"network-on-chip" AND abs:topology AND (abs:optimization OR abs:critical)'),
    ("wafer-integration", 'abs:"wafer-scale" AND (abs:integration OR abs:interconnect OR abs:architecture)'),
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

def generate_deep_insight(title, text, detail):
    """生成深度TCC/iNEST洞察。返回dict: tcc, inest, actionable, relevance_score(0-3)"""
    tcc_kw = [
        'network-on-chip', 'noc', 'chiplet', 'wafer-scale', 'interconnect',
        'topology', 'routing', 'placement', 'small-world', 'scale-free',
        'dark silicon', 'manycore', '3d stacking', 'heterogeneous integration',
        'crossbar', 'switching fabric', 'mesh', 'torus', 'signal integrity'
    ]
    inest_kw = [
        'neuromorphic', 'spiking neural', 'snn', 'memristor', 'criticality',
        'self-organized critical', 'neuronal avalanche', 'edge of chaos',
        'emergence', 'free energy', 'active inference', 'integrated information',
        'reservoir computing', 'liquid state', 'echo state',
        'stdp', 'surrogate gradient', 'phase transition', 'power law',
        'complex network', 'brain-inspired', 'predictive coding',
        'e/i balance', 'excitatory inhibitory', 'c. elegans', 'connectome'
    ]
    
    tcc_matches = [kw for kw in tcc_kw if kw in text]
    inest_matches = [kw for kw in inest_kw if kw in text]
    
    tcc_score = min(len(tcc_matches), 3)
    inest_score = min(len(inest_matches), 3)
    relevance = min(tcc_score + inest_score, 3)
    
    if relevance == 0:
        return None
    
    result = {'relevance_score': relevance}
    
    # TCC洞察
    if tcc_matches:
        lines = []
        lines.append(f'**关键词匹配**: {", ".join(tcc_matches[:5])}')
        
        if any(kw in text for kw in ['network-on-chip', 'noc', 'chiplet', 'interconnect']):
            lines.append('')
            lines.append('**借鉴**: 该研究的互连/拓扑优化方法可直接借鉴到TCC芯粒网络中。重点关注其拓扑生成算法、路由策略或布局优化思路。')
        if any(kw in text for kw in ['small-world', 'scale-free', 'topology', 'complex network']):
            lines.append('')
            lines.append('**理论贡献**: 复杂网络拓扑性质对TCC的元拓扑设计有直接指导意义。若揭示新的"拓扑-功能"映射关系，应纳入TCC拓扑设计空间。')
        if any(kw in text for kw in ['wafer-scale', 'dark silicon', 'manycore']):
            lines.append('')
            lines.append('**工程价值**: 晶圆级/众核架构研究为TCC的SDI物理网络提供工程参考基线。关注其功耗管理、热约束和扩展性策略。')
        if any(kw in text for kw in ['crossbar', 'mesh', 'torus', 'switching']):
            lines.append('')
            lines.append('**拓扑结构**: 该文的交换/互连结构可作为TCC网络候选拓扑模板，与σ≥4.0目标进行对比分析。')
        
        result['tcc'] = '\n'.join(lines)
    
    # iNEST洞察
    if inest_matches:
        lines = []
        lines.append(f'**关键词匹配**: {", ".join(inest_matches[:5])}')
        
        if any(kw in text for kw in ['criticality', 'neuronal avalanche', 'edge of chaos', 'self-organized critical']):
            lines.append('')
            lines.append('**核心理论**: 临界态/自组织临界性是iNEST的理论基石。该文可能提供新的临界性度量方法、相变机制或实验证据，直接强化"临界拓扑产生超线性信息处理能力"的核心命题。')
            if any(kw in text for kw in ['information capacity', 'dynamic range', 'mutual information']):
                lines.append('**定量证据**: 该文可能提供临界态 vs 非临界态的信息处理能力定量对比数据，这是iNEST论文最重要的引用来源。')
        
        if any(kw in text for kw in ['emergence', 'integrated information', 'causal emergence']):
            lines.append('')
            lines.append('**涌现机制**: 关于涌现/因果涌现的研究为iNEST"复杂网络→智能涌现"核心命题提供理论支撑。关注其如何定义和量化涌现现象。')
        
        if any(kw in text for kw in ['free energy', 'active inference', 'predictive coding']):
            lines.append('')
            lines.append('**自组织理论**: 自由能原理/主动推理框架为iNEST自组织机制提供数学基础。可用于形式化描述"网络如何自发趋向临界态"。')
        
        if any(kw in text for kw in ['neuromorphic', 'memristor', 'spiking neural', 'snn']):
            lines.append('')
            lines.append('**硬件实现**: 神经形态硬件方案为iNEST物理实现提供技术路线参考。关注其如何将临界动力学映射到电路层面。')
        
        if any(kw in text for kw in ['reservoir computing', 'liquid state', 'echo state']):
            lines.append('')
            lines.append('**计算范式**: 储备池计算天然处于"临界边缘"，其不需要训练内部权重的特性，与iNEST"拓扑即计算"高度一致。')
        
        if any(kw in text for kw in ['c. elegans', 'connectome']):
            lines.append('')
            lines.append('**基准系统**: C. elegans connectome是iNEST验证小世界拓扑→计算涌现的最小完整模型系统。新连接组数据可直接更新仿真基准。')
        
        result['inest'] = '\n'.join(lines)
    
    # 可执行行动
    actions = []
    citations = detail.get('citations', 0)
    if citations > 50:
        actions.append(f'⭐ 高影响力论文（{citations}引用），建议全文精读并在下周组会讨论。')
    elif citations > 10:
        actions.append(f'📖 中等影响力（{citations}引用），建议浏览引言和结论部分。')
    else:
        actions.append(f'📄 较新/冷门论文（{citations}引用），关注其创新点，选择性阅读。')
    
    if any(kw in text for kw in ['algorithm', 'method', 'framework', 'architecture']):
        actions.append('🔬 包含具体方法/框架，可在CST仿真中复现验证。')
    if any(kw in text for kw in ['benchmark', 'dataset', 'connectome', 'open source']):
        actions.append('📦 含公开数据/代码，可直接下载集成到工具链。')
    if any(kw in text for kw in ['review', 'survey', 'comprehensive']):
        actions.append('📚 综述性论文，可作为该方向文献调研的入口。')
    
    result['actionable'] = '\n'.join(actions)
    
    return result



def safe_filename(s):
    return re.sub(r'[<>:"/\\|?*]', "", s)[:60]

def write_insight(title, abstract, url, source, track="General", year="", authors="", s2_detail=None):
    """深度洞察提炼。只保存有意义的TCC/iNEST启示。"""
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
        log(f"  跳过(重复): {title[:50]}... [{reason}]")
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
        log(f"  跳过(弱相关): {title[:50]}...")
        return False
    
    tcc_block = ""
    if insight.get('tcc'):
        tcc_block = f"## TCC 启示\n\n{insight['tcc']}\n"
    inest_block = ""
    if insight.get('inest'):
        inest_block = f"## iNEST 启示\n\n{insight['inest']}\n"
    actionable = ""
    if insight.get('actionable'):
        actionable = f"## 可执行行动\n\n{insight['actionable']}\n"
    
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
    parts.append(f"tags: [洞察, {track.lower()}, 来自{source.lower()}]")
    parts.append(f"citations: {citations}")
    parts.append(f"relevance: {insight.get('relevance_score', 1)}")
    parts.append("status: 洞察")
    parts.append("---")
    parts.append("")
    parts.append(f"# {title}")
    parts.append("")
    parts.append(f"**{authors}** ({detail.get('year', year)}) | *{journal or '未知期刊'}*")
    parts.append(f"**引用数**: {citations} | **参考文献数**: {refs}")
    if fields:
        parts.append(f"**领域**: {fields}")
    if doi:
        parts.append(f"**DOI**: {doi}")
    parts.append(f"**链接**: [{url}]({url})")
    parts.append("")
    if tldr:
        parts.append(f"## 一句话总结")
        parts.append("")
        parts.append(tldr)
        parts.append("")
    if detail.get('abstract') or abstract:
        parts.append(f"## 摘要")
        parts.append("")
        txt = detail.get('abstract', abstract or "")
        parts.append(txt[:1200])
        parts.append("")
    if tcc_block:
        parts.append("## TCC 启示")
        parts.append("")
        parts.append(insight['tcc'])
        parts.append("")
    if inest_block:
        parts.append("## iNEST 启示")
        parts.append("")
        parts.append(insight['inest'])
        parts.append("")
    if actionable:
        parts.append("## 可执行行动")
        parts.append("")
        parts.append(insight['actionable'])
        parts.append("")
    parts.append("---")
    parts.append(f"*{TODAY} 科研管线v3.1自动提炼 | 相关度: {insight.get('relevance_score', 1)}/3*")
    
    content = "\n".join(parts)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    new_count += 1
    mark_as_seen(title, s2_id=s2_id, filepath=str(fp))
    log(f"  洞察 [{insight.get('relevance_score', '?')}/3]: {title[:50]}...")
    return True

def crawl_semantic_scholar():
    """Search Semantic Scholar API for TCC/iNEST papers."""
    log("[S2] 检索 Semantic Scholar...")
    count = 0
    for query in S2_QUERIES:
        params = {
            "query": query,
            "limit": 2,
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
                        continue  # �?FIX: skip None items
                    title = paper.get("title", "") or ""
                    abstract = paper.get("abstract") or "(no abstract)"
                    paper_url = paper.get("url", "") or ""
                    authors_list = paper.get("authors", []) or []
                    author_str = ", ".join(a.get("name", "") for a in authors_list[:5])
                    year = paper.get("year", "") or ""
                    track = "TCC" if any(kw in query.lower() for kw in ["topological","chiplet","noc","network-on-chip","wafer","dark silicon"]) else "iNEST"
                    if write_insight(title, abstract, paper_url, "S2", track, str(year), author_str):
                        count += 1
        except Exception as e:
            log(f"  S2 error ({query[:30]}...): {str(e)[:60]}")
        time.sleep(1.2)
    log(f"[S2] {count} new papers")
    return count

# ── Source 2: arXiv ────────────────────────────────────
def crawl_arxiv():
    """Search arXiv with 5s delay between queries."""
    log("[arXiv] 检索 arXiv (交叉查询)...")
    count = 0
    for label, q in ARXIV_QUERIES:
        url = f"https://export.arxiv.org/api/query?search_query={urllib.parse.quote(q)}&start=0&max_results=3&sortBy=submittedDate&sortOrder=descending"
        req = urllib.request.Request(url, headers={"User-Agent": "iNEST-Pipeline/3.0"})
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
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
                    if (datetime.now() - pd).days > 14:
                        continue
                except:
                    pass
                track = "iNEST" if any(kw in q.lower() for kw in ["neural","brain","emergence","free energy","critical","spiking","reservoir","stdp"]) else "TCC"
                if write_insight(title, abstract, link, "arXiv", track, pubdate[:4]):
                    count += 1
        except urllib.error.HTTPError as e:
            log(f"  arXiv {label}: HTTP {e.code}")
            if e.code == 429:
                time.sleep(20)
        except Exception as e:
            log(f"  arXiv {label}: {str(e)[:60]}")
        time.sleep(5)  # Rate limit
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

# ── 阶段2: 分类处理 Inbox (classify with LLM) ─────────
def call_deepseek(prompt, max_tokens=300):
    """Call LLM via unified router (auto-fallback)."""
    try:
        return llm_call(
            prompt,
            system="You are a research assistant. Output ONLY valid JSON.",
            model_tier="default",
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
        log(f"  �?ARCHIVE {fp.name}")
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
    log(f"  �?{target.relative_to(VAULT)} [{track}]")

    log("[Process] LLM分类已禁用，论文在 _pipeline_insights 中。")
    return 0


def process_inbox(limit=20):
    """Classify inbox items. Disabled due to LLM balance."""
    log("[Process] LLM分类已禁用，论文在 _pipeline_insights 中。")
    return 0

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



# -- Stage 4: Generate Genspark Snapshot ---------------------------------
def generate_genspark_snapshot():
    """Generate project snapshot for Genspark top-tier model consumption."""
    log("[Genspark] Generating project snapshot...")
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    snapshot_path = VAULT / "99_Meta" / f"genspark_snapshot_{today}.md"
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)

    lib_papers = len(list((VAULT / "10_Library" / "Papers").glob("*.md")))
    lib_articles = len(list((VAULT / "10_Library" / "Articles").glob("*.md")))
    inbox_count = len([f for f in (VAULT / "00_Inbox").glob("*.md") if f.name != ".gitkeep"])
    genspark_inbox = len(list((VAULT / "00_Inbox" / "_from_genspark").glob("*.md")))
    papers_out = len(list((VAULT / "50_Output" / "51_Papers").glob("*.md")))
    patents_out = len(list((VAULT / "50_Output" / "52_Patents").glob("*.md")))

    graph_data = {"nodes": [], "edges": []}
    graph_path = VAULT / "knowledge_graph" / "graph_data.json"
    if graph_path.exists():
        try:
            with open(graph_path, encoding="utf-8") as f:
                graph_data = json.load(f)
        except:
            pass

    nodes_sorted = sorted(graph_data.get("nodes", []), key=lambda n: n.get("out_degree", 0) + n.get("in_degree", 0), reverse=True)[:10]
    top_nodes = "\n".join(f"- [[{n['label']}]] (out={n['out_degree']}, in={n['in_degree']})" for n in nodes_sorted if n.get('label'))

    inbox_files = sorted([f for f in (VAULT / "00_Inbox").glob("*.md") if f.name != ".gitkeep"], key=lambda f: f.stat().st_mtime, reverse=True)[:10]
    recent_inbox = "\n".join(f"- {f.name} [{datetime.fromtimestamp(f.stat().st_mtime).strftime('%m-%d %H:%M')}]" for f in inbox_files) if inbox_files else "(empty)"

    log_files = sorted(LOG_DIR.glob("pipeline_*.json"), reverse=True)[:3]
    recent_logs = ""
    for lf in log_files:
        try:
            ld = json.loads(open(lf, encoding="utf-8").read())
            recent_logs += f"- {ld.get('date','')[:10]}: {ld.get('new_papers',0)} papers, {ld.get('classified',0)} classified\n"
        except:
            pass

    with open(snapshot_path, "w", encoding="utf-8") as f:
        f.write(f"---\ntitle: Genspark Project Snapshot - {today}\ndate: {today}\ntype: snapshot\ntarget: genspark\ntags: [genspark, snapshot, project-status]\n---\n\n")
        f.write(f"# Genspark Project Snapshot - {today}\n\n")
        f.write("## 1. Vault Overview\n\n| Metric | Count |\n|--------|-------|\n")
        f.write(f"| Library Papers | {lib_papers} |\n| Library Articles | {lib_articles} |\n| Output Papers | {papers_out} |\n| Output Patents | {patents_out} |\n| Inbox (unprocessed) | {inbox_count} |\n| Genspark Inbox (pending) | {genspark_inbox} |\n| Knowledge Graph Nodes | {len(graph_data.get('nodes', []))} |\n| Knowledge Graph Edges | {len(graph_data.get('edges', []))} |\n\n")
        f.write(f"## 2. Recent Pipeline Runs\n\n{recent_logs}\n\n")
        f.write(f"## 3. Recent Inbox Items\n\n{recent_inbox}\n\n")
        f.write(f"## 4. Top Connected Topics\n\n{top_nodes if top_nodes else '(empty)'}\n\n")
        f.write("## 5. Current Focus Areas\n\n- **TCC**: Topological Computing - wafer-scale integration, network-on-chip\n- **iNEST**: Intelligent Neural Emergent System Theory - neuromorphic, self-organized criticality, emergence\n\n")
        f.write(f"## 6. Open Questions\n\n(Review via Genspark)\n---\n*Auto-generated {now.strftime('%Y-%m-%d %H:%M')}*\n")

    latest_path = VAULT / "99_Meta" / "genspark_latest_snapshot.md"
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(open(snapshot_path, encoding="utf-8").read())

    log(f"[Genspark] Snapshot written: {snapshot_path.name}")
    return str(snapshot_path.relative_to(VAULT))
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
    
    print(f"\n  阶段1 完成: {c1+c2+c3} new items to inbox")
    
    # Stage 2: Process
    processed = process_inbox(limit=20)
    
    # 阶段3: 知识图谱
    snapshot = generate_genspark_snapshot()
    nodes, edges, missing = scan_and_build_graph()
    # Stage 5: Push insights to dashboard
    try:
        import subprocess
        dash_script = str(VAULT / '90_System' / 'scripts' / 'dashboard_data_v3.py')
        subprocess.run([sys.executable, dash_script], capture_output=True, text=True, timeout=120, cwd=str(VAULT))
        log("[Dashboard] 看板已更新")
    except Exception as e:
        log(f"[Dashboard] 跳过: {e}")

    
    elapsed = time.time() - start
    print(f"\n{'='*60}")
    print(f"  管线 v3.1 完成")
    print(f"  新增: {c1}(S2) + {c2}(arXiv) + {c3}(GN) = {c1+c2+c3}")
    print(f"  已分类: {processed} | 图谱: {nodes}节点{edges}边 | 缺失反向链接: {missing} | Genspark快照: OK")
    print(f"  耗时: {elapsed:.0f}秒")
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
    with open(LOG_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M')}.json", "w") as f:
        json.dump(log_data, f, indent=2)

if __name__ == "__main__":
    main()


