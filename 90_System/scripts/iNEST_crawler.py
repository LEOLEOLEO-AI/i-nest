#!/usr/bin/env python3
"""iNEST 文献自动爬取脚本 v4 — 基于 V28 仿真技术栈更新关键词
================================================================
覆盖 V28 核心技术：
  STDP | FEP/自由能 | BCM/元可塑性 | 小世界网络 | 记忆巩固
  C.elegans连接组 | 稳态可塑性 | 惊讶度调控 | Lyapunov稳定性
  最小作用量 | 标度律 | 储备池计算 | 神经形态硬件
================================================================
"""

import urllib.request, urllib.error
import xml.etree.ElementTree as ET
import ssl, os
from datetime import datetime, timedelta

OBSIDIAN_WEB_CLIPS = r"D:\Obsidian\home\work\.openclaw\workspace\03_Topics\Web-Clips"
TODAY = datetime.now().strftime("%Y-%m-%d")
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
ctx = ssl.create_default_context()
all_articles = []

def add_article(source, title, url, date_str, note=""):
    key = title[:80].lower()
    for a in all_articles:
        if a["title"][:80].lower() == key:
            return
    all_articles.append({
        "source": source, "title": title.strip(),
        "url": url.strip(), "date": date_str.strip(), "note": note
    })

# ===== Google News RSS =====
print("[1/3] Searching Google News...")
gn_queries = [
    # === V28 核心技术 ===
    ("STDP plasticity", "STDP+OR+spike-timing-dependent+plasticity"),
    ("FEP active inference", "free+energy+principle+OR+active+inference+neuroscience"),
    ("BCM metaplasticity", "BCM+theory+OR+metaplasticity+OR+sliding+threshold"),
    ("small-world brain", "small-world+network+brain+OR+Watts-Strogatz+neural"),
    ("memory consolidation", "memory+consolidation+synaptic+OR+engram+OR+LTP+late-phase"),
    ("homeostatic plasticity", "homeostatic+plasticity+OR+synaptic+scaling"),
    ("neuromodulation surprise", "neuromodulation+plasticity+OR+norepinephrine+learning+OR+acetylcholine+attention"),
    ("connectome scaling", "connectome+scaling+OR+C.elegans+connectome+OR+Drosophila+connectome"),
    ("Lyapunov attractor neural", "Lyapunov+stability+neural+OR+attractor+dynamics+network"),
    ("self-organized criticality", "self-organized+criticality+brain+OR+edge+of+chaos+neural"),
    # === 硬件/工程 ===
    ("neuromorphic hardware", "neuromorphic+computing+OR+spiking+neural+network+OR+brain-inspired+chip"),
    ("memristor spintronic", "memristor+neuromorphic+OR+spintronic+neuromorphic"),
    ("reservoir computing", "reservoir+computing+OR+echo+state+network+OR+liquid+state+machine"),
    ("event camera SNN", "event+camera+spiking+neural+OR+event-driven+sensor"),
    # === 中文 ===
    ("CN neuromorphic", "%E7%A5%9E%E7%BB%8F%E5%BD%A2%E6%80%81%E8%AE%A1%E7%AE%97+OR+%E7%B1%BB%E8%84%91%E8%8A%AF%E7%89%87+OR+%E8%84%89%E5%86%B2%E7%A5%9E%E7%BB%8F"),
    ("CN FEP predictive", "%E8%87%AA%E7%94%B1%E8%83%BD%E5%8E%9F%E7%90%86+OR+%E9%A2%84%E6%B5%8B%E7%BC%96%E7%A0%81+OR+%E4%B8%BB%E5%8A%A8%E6%8E%A8%E7%90%86"),
]

for label, query in gn_queries:
    try:
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, context=ctx, timeout=30)
        root = ET.fromstring(resp.read().decode("utf-8"))
        count = 0
        for item in root.findall(".//item"):
            title_el = item.find("title")
            if title_el is None:
                continue
            title = title_el.text or ""
            pub_el = item.find("pubDate")
            pubdate = pub_el.text[:22] if pub_el is not None and pub_el.text else ""
            link_el = item.find("link")
            link = link_el.text if link_el is not None and link_el.text else ""
            try:
                pd = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M")
                if (datetime.now() - pd).days <= 7:
                    add_article("Google News", title, link, pubdate)
                    count += 1
            except:
                pass
        print(f"  {label}: {count}")
    except Exception as e:
        print(f"  {label}: err ({str(e)[:50]})")

# ===== arXiv API =====
print("[2/3] Searching arXiv...")
arxiv_queries = [
    # === V28 核心理论 ===
    ("STDP", "all:STDP+OR+all:spike-timing-dependent+plasticity"),
    ("FEP/active inference", "all:free+energy+principle+OR+all:active+inference"),
    ("BCM/metaplasticity", "all:BCM+OR+all:metaplasticity"),
    ("small-world neural", "all:small-world+AND+all:neural+network"),
    ("memory consolidation", "all:memory+consolidation+AND+all:synaptic"),
    ("homeostatic plasticity", "all:homeostatic+plasticity+OR+all:synaptic+scaling"),
    ("connectome", "all:connectome+AND+all:scaling"),
    ("attractor dynamics", "all:attractor+dynamics+AND+all:neural"),
    ("self-organized criticality", "all:self-organized+AND+all:criticality+AND+all:neural"),
    # === 硬件 ===
    ("SNN neuromorphic", "all:neuromorphic+AND+all:spiking+neural+network"),
    ("memristor neuro", "all:memristor+AND+all:neuromorphic"),
    ("reservoir computing", "all:reservoir+computing+OR+all:echo+state+network"),
    ("event-driven SNN", "all:event-driven+AND+all:spiking+neural"),
    ("spintronic neuro", "all:spintronic+AND+all:neuromorphic"),
    ("predictive coding", "all:predictive+coding+AND+all:brain"),
]

for label, query in arxiv_queries:
    try:
        url = f"https://export.arxiv.org/api/query?search_query={query}&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
        req = urllib.request.Request(url, headers={"User-Agent": "iNEST/4.0"})
        resp = urllib.request.urlopen(req, context=ctx, timeout=30)
        root = ET.fromstring(resp.read().decode("utf-8"))
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        count = 0
        for entry in root.findall("atom:entry", ns):
            t = entry.find("atom:title", ns)
            p = entry.find("atom:published", ns)
            i = entry.find("atom:id", ns)
            if t is None or p is None:
                continue
            title = t.text.strip().replace("\n"," ")
            pubdate = p.text[:10]
            link = i.text if i is not None else ""
            try:
                pd = datetime.strptime(pubdate, "%Y-%m-%d")
                if (datetime.now() - pd).days <= 7:
                    s = entry.find("atom:summary", ns)
                    note = s.text.strip()[:200].replace("\n"," ") if s is not None else ""
                    add_article("arXiv", title, link, pubdate, note)
                    count += 1
            except:
                pass
        print(f"  {label}: {count}")
    except urllib.error.HTTPError as e:
        print(f"  {label}: HTTP {e.code}")
    except Exception as e:
        print(f"  {label}: err ({str(e)[:50]})")

# ===== Save =====
print(f"[3/3] Saving... {len(all_articles)} total")

new_articles = []
week_articles = []
for a in all_articles:
    try:
        if " " in a["date"]:
            pd = datetime.strptime(a["date"], "%a, %d %b %Y %H:%M")
        else:
            pd = datetime.strptime(a["date"], "%Y-%m-%d")
        date_str = pd.strftime("%Y-%m-%d")
        if date_str in (TODAY, YESTERDAY):
            new_articles.append(a)
        else:
            week_articles.append(a)
    except:
        week_articles.append(a)

md = f"""---
date: {TODAY}
tags: [iNEST, literature-tracking, web-clip, auto-crawl]
source: Google News RSS + arXiv API (auto)
topics: [STDP, FEP, BCM, small-world, consolidation, homeostasis, connectome, neuromorphic]
---

# {TODAY} iNEST Daily Literature Crawl

> Crawl time: {datetime.now().strftime("%Y-%m-%d %H:%M")}
> Keywords: STDP · FEP/自由能 · BCM/元可塑性 · 小世界网络 · 记忆巩固 · 稳态可塑性 · 连接组 · 神经形态硬件
> New: {len(new_articles)} | Week: {len(week_articles)}

"""

if new_articles:
    md += "## New (Yesterday & Today)\n\n"
    for a in sorted(new_articles, key=lambda x: x["date"], reverse=True):
        md += f'- **[{a["title"]}]({a["url"]})**\n'
        md += f'  - {a["source"]} | {a["date"]}\n'
        if a["note"]:
            md += f'  - {a["note"][:150]}\n'
        md += "\n"
elif not week_articles:
    md += "No new articles found today.\n"

if week_articles:
    md += "## This Week\n\n"
    for a in sorted(week_articles, key=lambda x: x["date"], reverse=True):
        md += f'- **[{a["title"]}]({a["url"]})**\n'
        md += f'  - {a["source"]} | {a["date"]}\n'
        if a["note"]:
            md += f'  - {a["note"][:150]}\n'
        md += "\n"

os.makedirs(OBSIDIAN_WEB_CLIPS, exist_ok=True)
filepath = os.path.join(OBSIDIAN_WEB_CLIPS, f"{TODAY} iNEST Daily Crawl.md")
with open(filepath, "w", encoding="utf-8") as f:
    f.write(md)
print(f"  Saved: {filepath}")
print("Done!")
