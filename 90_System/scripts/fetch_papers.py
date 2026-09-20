#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_papers.py — 多通道论文取数（修复 arXiv API 被 406 拦截导致的断流）。

诊断（2026-09-20 实测）:
    管线 `new_papers=0` 连续 4 天、`api_results=0`。逐项测试发现:
      * `export.arxiv.org/api/query` 对**所有** User-Agent 都返回 **HTTP 406 Not Acceptable**
        （浏览器 UA、规范 UA、无 UA 全试过）—— 是该子域被拦，不是 UA 问题；
      * 但 `arxiv.org/list/<cat>/recent`（官网列表页）**HTTP 200**，一次可取 46 个 arXiv ID；
      * `rss.arxiv.org/rss/<cat>` **HTTP 200**，是合法 RSS（当时 channel 内无 item）；
      * `api.openalex.org` 可用（需 polite pool + 限速，否则 429）；
      * Semantic Scholar 可用（会 429，需退避）。
    结论: 不能只依赖 arXiv API。改为**多通道依次回退**，任一通道可用即不空跑。

用法:
    python fetch_papers.py --days 7                 # 取近 N 天，多通道
    python fetch_papers.py --days 7 --limit 40      # 限制条数
    python fetch_papers.py --probe                  # 只探测各通道可用性
    python fetch_papers.py --days 7 --json out.json # 落盘
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

VAULT = Path(r"D:\Obsidian\vault")
sys.path.insert(0, str(VAULT / "90_System"))     # 让 research_evolve 可导入
STATE = VAULT / "90_System" / "research_evolve" / "state"
SEEN_FILE = STATE / "seen_papers.json"
UA = {"User-Agent": "Mozilla/5.0 (compatible; iNEST-Pipeline/3.5; +mailto:research@local)"}
MAILTO = "research@local"        # OpenAlex polite pool

CATEGORIES = ["cs.NE", "cs.AI", "cs.SI", "cs.NI", "cs.DC", "cs.MA",
              "physics.soc-ph", "cond-mat.mes-hall", "nlin.AO", "q-bio.NC"]


def _get(url: str, timeout: int = 45, headers: dict | None = None) -> tuple[int, str]:
    req = urllib.request.Request(url, headers=headers or UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return -1, ""


# ---------------------------------------------------------------- 通道 1: arXiv API
def ch_arxiv_api(cat: str, max_results: int = 50) -> list[dict]:
    q = urllib.parse.urlencode({"search_query": f"cat:{cat}", "start": 0,
                                "max_results": max_results,
                                "sortBy": "submittedDate", "sortOrder": "descending"})
    st, body = _get(f"https://export.arxiv.org/api/query?{q}")
    if st != 200 or "<entry>" not in body:
        return []
    out = []
    for e in re.findall(r"<entry>(.*?)</entry>", body, re.S):
        t = re.search(r"<title>(.*?)</title>", e, re.S)
        i = re.search(r"<id>(.*?)</id>", e)
        p = re.search(r"<published>(.*?)</published>", e)
        s = re.search(r"<summary>(.*?)</summary>", e, re.S)
        out.append({"title": re.sub(r"\s+", " ", t.group(1)).strip() if t else "",
                    "id": (i.group(1).split("/abs/")[-1] if i else ""),
                    "published": p.group(1)[:10] if p else "",
                    "abstract": re.sub(r"\s+", " ", s.group(1)).strip()[:1200] if s else "",
                    "channel": "arxiv_api", "categories": [cat]})
    return out


# ---------------------------------------------------------------- 通道 2: arXiv 列表页（实测可用）
def ch_arxiv_listing(cat: str) -> list[dict]:
    st, html = _get(f"https://arxiv.org/list/{cat}/recent")
    if st != 200 or not html:
        return []
    ids = re.findall(r'arXiv:(\d{4}\.\d{4,5})', html)
    # 标题在 <div class="list-title"> 内，结构随版本变，做宽松提取
    titles = re.findall(r'list-title[^>]*>\s*(?:<span[^>]*>)?\s*Title:\s*</span>\s*(.*?)</div>',
                        html, re.S)
    titles = [re.sub(r"<[^>]+>", "", t).strip() for t in titles]
    out = []
    for n, aid in enumerate(dict.fromkeys(ids)):
        t = titles[n] if n < len(titles) else ""
        out.append({"title": t, "id": aid, "published": "", "abstract": "",
                    "channel": "arxiv_listing", "categories": [cat]})
    return out


# ---------------------------------------------------------------- 通道 3: arXiv RSS
def ch_arxiv_rss(cat: str) -> list[dict]:
    st, xml = _get(f"https://rss.arxiv.org/rss/{cat}")
    if st != 200:
        return []
    out = []
    for it in re.findall(r"<item>(.*?)</item>", xml, re.S):
        t = re.search(r"<title>(.*?)</title>", it, re.S)
        l = re.search(r"<link>(.*?)</link>", it, re.S)
        d = re.search(r"<description>(.*?)</description>", it, re.S)
        dc = re.search(r"<dc:date>(.*?)</dc:date>", it, re.S)
        out.append({"title": re.sub(r"\s+", " ", t.group(1)).strip() if t else "",
                    "id": (l.group(1).split("/abs/")[-1] if l else ""),
                    "published": dc.group(1)[:10] if dc else "",
                    "abstract": re.sub(r"<[^>]+>", " ", d.group(1))[:1200] if d else "",
                    "channel": "arxiv_rss", "categories": [cat]})
    return out


# ---------------------------------------------------------------- 通道 4: OpenAlex
def ch_openalex(query: str, days: int = 7, per_page: int = 50) -> list[dict]:
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    url = ("https://api.openalex.org/works?" + urllib.parse.urlencode({
        "search": query, "filter": f"from_publication_date:{since}",
        "per-page": per_page, "sort": "publication_date:desc",
        "mailto": MAILTO}))                      # polite pool，避免 429
    st, body = _get(url, timeout=60)
    if st != 200:
        return []
    try:
        d = json.loads(body)
    except Exception:
        return []
    out = []
    for w in d.get("results", []):
        out.append({"title": (w.get("title") or "").strip(),
                    "id": (w.get("doi") or w.get("id") or "").split("/")[-1],
                    "published": (w.get("publication_date") or "")[:10],
                    "abstract": "", "channel": "openalex",
                    "doi": w.get("doi") or "", "categories": [w.get("type", "")]})
    return out


# ---------------------------------------------------------------- 去重/相关性
def scope_ok(text: str) -> tuple[bool, list[str]]:
    sys.path.insert(0, str(VAULT / "90_System"))
    from research_evolve.score import scope_check  # noqa: PLC0415
    sc = scope_check(text)
    hits = sc["tcc_hits"] + sc["inest_hits"]
    return (bool(hits) and not sc["excluded"]), hits


def load_seen() -> set:
    if SEEN_FILE.exists():
        try:
            return set(json.loads(SEEN_FILE.read_text(encoding="utf-8")).get("ids", []))
        except Exception:
            pass
    return set()


def save_seen(ids: set) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    SEEN_FILE.write_text(json.dumps(
        {"updated": datetime.now().isoformat(), "count": len(ids),
         "ids": sorted(ids)[-20000:]}, ensure_ascii=False), encoding="utf-8")


CHANNELS = [("arxiv_api", ch_arxiv_api), ("arxiv_rss", ch_arxiv_rss),
            ("arxiv_listing", ch_arxiv_listing)]


def probe() -> None:
    print("=== 各通道可用性探测 ===")
    for name, fn in CHANNELS:
        t = time.time()
        try:
            r = fn("cs.NE")
            print(f"  {name:<16} {('OK ' if r else 'EMPTY')}  {len(r):>3} 条  {time.time()-t:.1f}s")
        except Exception as e:
            print(f"  {name:<16} FAIL {type(e).__name__}: {str(e)[:60]}")
    for q in ("reservoir computing", "criticality brain"):
        t = time.time()
        r = ch_openalex(q, days=30, per_page=5)
        print(f"  {'openalex':<16} {('OK ' if r else 'EMPTY')}  {len(r):>3} 条  {time.time()-t:.1f}s  ({q})")


def fetch(days: int = 7, limit: int = 120) -> dict:
    seen = load_seen()
    found: dict[str, dict] = {}
    stats: dict[str, int] = {}
    for cat in CATEGORIES:
        for name, fn in CHANNELS:
            try:
                items = fn(cat)
            except Exception:
                items = []
            stats[name] = stats.get(name, 0) + len(items)
            for it in items:
                if not it.get("title") and not it.get("id"):
                    continue
                key = it.get("id") or it["title"][:80]
                if key in found:
                    continue
                found[key] = it
            if items:                      # 该分类已拿到就不必再试后续通道
                break
    # OpenAlex 补一轮（按主题词，覆盖 arXiv 分类之外）
    for q in ("reservoir computing", "criticality brain network",
              "emergence complex network", "neuromorphic interconnect"):
        for it in ch_openalex(q, days=days, per_page=25):
            key = it.get("doi") or it.get("id") or it["title"][:80]
            if key and key not in found:
                found[key] = it
        time.sleep(1.0)                        # 礼貌限速

    # 领域过滤 + 去重
    keep, rejected = [], []
    for it in found.values():
        text = (it.get("title", "") + " " + it.get("abstract", ""))
        ok, hits = scope_ok(text)
        k = it.get("id") or it["title"][:80]
        if k in seen:
            continue
        it["domain_hits"] = hits[:6]
        (keep if ok else rejected).append(it)

    keep.sort(key=lambda x: -len(x.get("domain_hits", [])))
    keep = keep[:limit]
    return {"fetched_at": datetime.now().isoformat(), "window_days": days,
            "channel_counts": stats, "total_found": len(found),
            "kept": len(keep), "rejected_out_of_scope": len(rejected),
            "papers": keep}


def main() -> int:
    a = sys.argv[1:]
    if "--probe" in a:
        probe(); return 0
    days = int(a[a.index("--days") + 1]) if "--days" in a else 7
    limit = int(a[a.index("--limit") + 1]) if "--limit" in a else 120
    r = fetch(days, limit)
    print(f"通道命中: {r['channel_counts']}")
    print(f"候选 {r['total_found']} -> 领域内 {r['kept']}（越界 {r['rejected_out_of_scope']}）")
    for p in r["papers"][:12]:
        print(f"  [{len(p['domain_hits'])}] ({p['channel']}) {p['title'][:78]}")
        if p["domain_hits"]:
            print(f"        命中: {p['domain_hits']}")
    if "--json" in a:
        out = Path(a[a.index("--json") + 1])
        out.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"-> {out}")
    if "--mark-seen" in a:
        seen = load_seen() | {(p.get("id") or p["title"][:80]) for p in r["papers"]}
        save_seen(seen)
        print(f"已记入 seen: {len(seen)}")
    return 0 if r["kept"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
