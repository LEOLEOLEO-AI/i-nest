# -*- coding: utf-8 -*-
"""
溯源分类 + 原位打标签脚本
原则：
  - 含「刘勤让 / inest研究组 / 刘主任」等署名标记  -> provenance: own   (我们研究过程中产生的内容)
  - 含文献名/第三方平台名(Genspark/得到/Codex/arXiv/DOI/S2...) -> provenance: external (网上爬取)
  - 无标记 -> 位置启发式：30_TCC/40_iNEST/50_Output 等视为 own 候选；Papers/arxiv/文献/imports/00_Inbox 视为 external；其余 pending
仅对 own/external 注入 frontmatter；pending 不打标签(留待人工审查)，仅记入 classification.json。
"""
import os, re, json, sys
from collections import Counter
from pathlib import Path

VAULT = Path(r"D:\obsidian\vault")
OUT = VAULT / "99_Meta" / "classification.json"
EXCLUDE_DIRS = {".git", ".obsidian", "node_modules", "__pycache__", ".trash"}

OWN_MARKERS = ["刘勤让", "inest研究组", "inest 研究组", "iNEST研究组", "INEST研究组", "刘主任"]
# 第三方平台 / 文献来源标记（爬取内容特征）。注意避免过于通用的词(如裸"得到")造成误判。
CRAWL_MARKERS = ["Genspark", "gespark", "得到大脑", "getnote", "GetNote", "GetNote_",
    "Codex", "semantic scholar", "arXiv", "arxiv", "doi.org", "doi:", "10.",
    "pubmed", "ieee xplore", "google scholar", "web of science", "arxiv.org",
    "sci-hub", "researchgate", "acm.org", "springer", "semanticscholar",
    "nature.com", "science.org", "ieee.org", "知乎", "公众号", "机器之心",
    "量子位", "新智元", "引用格式", "参考文献"]
# 外部子目录信号：即使顶层是 TCC/iNEST 也判为 external
EXTERNAL_SUBFOLDER = ["papers", "arxiv", "文献", "imports", "crawl",
    "reference", "references", "_pipeline_insights", "daily", "getnote"]


def has_any(text, markers):
    tl = text.lower()
    return [m for m in markers if m.lower() in tl]


def classify(rel, text):
    parts = Path(rel).parts
    top = parts[0].lower() if parts else ""
    own_hits = has_any(text, OWN_MARKERS)
    crawl_hits = has_any(text, CRAWL_MARKERS)
    in_external_sub = any(s in rel.lower() for s in EXTERNAL_SUBFOLDER)
    if own_hits:
        return "own", "high", "含署名标记: " + ", ".join(own_hits[:3])
    if crawl_hits or in_external_sub or top in ("00_inbox", "raw"):
        reason = ("含平台/文献标记: " + ", ".join(crawl_hits[:3])) if crawl_hits else ("外部子目录: " + rel)
        return "external", "high", reason
    # 位置启发式（无标记文件）
    if top in ("30_tcc", "40_inest", "50_output", "20_processing"):
        return "own", "location", "位置启发式: 位于 " + top + " (自有研究候选,需复核)"
    if top in ("10_knowledge", "60_moc", "70_dashboard", "80_archive", "90_system", "99_meta", "wiki"):
        return "pending", "none", "位置启发式: 位于 " + top + " (待审)"
    return "pending", "none", "位置启发式: 无法判定 (待审)"


def theme_of(rel):
    parts = [seg.lower() for seg in Path(rel).parts]
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}"
    return parts[0] if parts else "?"


def status_of(rel, text):
    r = rel.lower(); t = text.lower()
    if "legacy" in r or "39_legacy" in r:
        return "legacy(遗留)"
    if "80_archive" in r or "_archive" in r:
        return "archived(已归档)"
    if any(k in r for k in ["项目", "projects", "申报书", "专项", "立项"]) or "申报" in t:
        return "project(项目)"
    if "专利" in r or "交底" in r:
        return "patent(专利)"
    if "论文" in r or "paper" in r or re.search(r"\d{4}\.\d{4,5}", rel):
        return "paper(论文)"
    if "纪要" in r or "组会" in r or "会议" in r:
        return "meeting(纪要)"
    if "理论" in r or "theory" in r or "战略" in r or "报告" in r:
        return "theory(理论/战略)"
    return "active(常规)"


def title_of(text):
    m = re.search(r'^#\s+(.+)$', text, re.M)
    if m:
        return m.group(1).strip()[:80]
    m2 = re.search(r'title:\s*["\']?(.+?)["\']?\s*$', text, re.M)
    if m2:
        return m2.group(1).strip()[:80]
    return ""


def add_provenance(text, value):
    if text.startswith('---'):
        lines = text.split('\n')
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                end = i
                break
        if end is None:
            return f'---\nprovenance: {value}\n---\n\n' + text
        for i in range(1, end):
            if lines[i].startswith('provenance:'):
                lines[i] = f'provenance: {value}'
                return '\n'.join(lines)
        lines.insert(end, f'provenance: {value}')
        return '\n'.join(lines)
    return f'---\nprovenance: {value}\n---\n\n' + text


def main(apply=False):
    records = []
    changed = 0
    tagged = 0
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            if not f.endswith('.md'):
                continue
            fp = Path(root) / f
            try:
                text = fp.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            rel = str(fp.relative_to(VAULT))
            prov, conf, reason = classify(rel, text)
            records.append({
                "path": rel,
                "provenance": prov,
                "confidence": conf,
                "reason": reason,
                "theme": theme_of(rel),
                "status": status_of(rel, text),
                "title": title_of(text),
                "has_citations": bool(has_any(text, CRAWL_MARKERS)),
            })
            if apply and prov in ("own", "external"):
                newtext = add_provenance(text, prov)
                if newtext != text:
                    fp.write_text(newtext, encoding='utf-8')
                    changed += 1
                tagged += 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding='utf-8')
    pc = Counter(r['provenance'] for r in records)
    cc = Counter((r['provenance'], r['confidence']) for r in records)
    tc = Counter(r['theme'] for r in records if r['provenance'] == 'own')
    print(f"总文件: {len(records)}")
    print(f"provenance 分布: {dict(pc)}")
    print("provenance/confidence 分布:")
    for k, v in sorted(cc.items()):
        print(f"    {k[0]:10s} {k[1]:10s} {v}")
    print("own 主题分布:")
    for k, v in tc.most_common():
        print(f"    {k:34s} {v}")
    print(f"classification.json -> {OUT}")
    if apply:
        print(f"应打标签: {tagged}, 实际改写: {changed}")


if __name__ == '__main__':
    main(apply=('--apply' in sys.argv))
