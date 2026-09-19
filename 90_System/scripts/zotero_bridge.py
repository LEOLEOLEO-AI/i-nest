#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""zotero_bridge.py — 把 Zotero 变成科研智能体的文献真相源。

为什么用 Zotero 而不是自己维护书目:
    用户库里已有 540 条文献（421 journalArticle / 70 preprint / 42 conferencePaper）、
    323 个 PDF（实测 323/323 全部在位）、且 **Better BibTeX 已接入，540 条全都有
    稳定的 citationKey**（key 格式 auth.lower + shorttitle(3,3) + year）。
    引用的唯一真相源应该是 Zotero；vault 只做它的投影，不另存一份（避免第二正本）。

数据来源（三条都实测可用，2026-09-19）:
    1. 一致性副本 zotero.sqlite —— 拿 citationKey/DOI/作者/分类/PDF 路径
       （Zotero 运行时会锁原库，故先复制再只读查询）
    2. Better BibTeX HTTP 导出 —— 拿 BibLaTeX 全文
       GET http://127.0.0.1:23119/better-bibtex/export/library?/library.bib
    3. Zotero 本地 API（可选校验）GET http://127.0.0.1:23119/api/users/0/items

产出（全部落在 vault 内）:
    50_Output/References/zotero.bib                  实时 BibLaTeX 投影
    90_System/research_evolve/zotero/library.json    结构化书目索引
    90_System/research_evolve/zotero/reading_index.md 人读的阅读索引
    90_System/research_evolve/zotero/pdf_map.json    citationKey -> PDF 绝对路径

用法:
    python zotero_bridge.py                 # 同步（.bib + 索引 + pdf_map）
    python zotero_bridge.py --seed-papers   # 额外用 Zotero 播种引用白名单
    python zotero_bridge.py --check         # 只检查 Zotero 可达性与数量
"""
from __future__ import annotations

import json
import shutil
import sqlite3
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ZOTERO_DIR = Path(r"C:\Users\LEO\Zotero")
ZOTERO_DB = ZOTERO_DIR / "zotero.sqlite"
STORAGE = ZOTERO_DIR / "storage"
API_BASE = "http://127.0.0.1:23119"
BBT_LIBRARY = f"{API_BASE}/better-bibtex/export/library?/library.bib"

VAULT = Path(r"D:\Obsidian\vault")
OUT_DIR = VAULT / "90_System" / "research_evolve" / "zotero"
BIB_OUT = VAULT / "50_Output" / "References" / "zotero.bib"
TMP_DB = Path(r"D:\Temp\zotero_ro.sqlite")

# 只把这些条目类型当作"可引用文献"（附件/笔记/批注不算）
CITABLE = {"journalArticle", "preprint", "conferencePaper", "book", "bookSection",
           "report", "thesis", "manuscript", "document", "webpage", "patent"}


def log(m: str) -> None:
    print(m, flush=True)


def snapshot_db() -> Path:
    """复制 Zotero 库以避开运行中的写锁（含 WAL/SHM 以保证一致）。"""
    TMP_DB.parent.mkdir(parents=True, exist_ok=True)
    if not ZOTERO_DB.exists():
        raise FileNotFoundError(f"找不到 {ZOTERO_DB}")
    shutil.copy2(ZOTERO_DB, TMP_DB)
    for suf in ("-wal", "-shm"):
        src = Path(str(ZOTERO_DB) + suf)
        if src.exists():
            shutil.copy2(src, Path(str(TMP_DB) + suf))
    return TMP_DB


def fetch_bib(timeout: int = 60) -> str | None:
    """从 Better BibTeX 的 HTTP 端点取 BibLaTeX。"""
    try:
        with urllib.request.urlopen(BBT_LIBRARY, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        log(f"⚠️ BBT 导出失败（Zotero 未运行或 BBT 未装）: {type(e).__name__}: {e}")
        return None


def read_library(db: Path) -> tuple[list[dict], dict]:
    """从库副本读出可引用条目 + citationKey + PDF 路径 + 分类。"""
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    cur = con.cursor()

    # itemID -> {fieldName: value}
    fields = {}
    cur.execute("""SELECT id.itemID, f.fieldName, v.value
                   FROM itemData id
                   JOIN fields f ON f.fieldID = id.fieldID
                   JOIN itemDataValues v ON v.valueID = id.valueID""")
    for item_id, fname, val in cur.fetchall():
        fields.setdefault(item_id, {})[fname] = val

    # itemID -> creators
    creators = {}
    cur.execute("""SELECT ic.itemID, c.firstName, c.lastName, c.fieldMode, ic.orderIndex
                   FROM itemCreators ic JOIN creators c ON c.creatorID = ic.creatorID
                   ORDER BY ic.itemID, ic.orderIndex""")
    for item_id, first, last, mode, _ in cur.fetchall():
        name = (last or "") if mode == 1 else f"{last or ''}, {first or ''}".strip(", ")
        creators.setdefault(item_id, []).append(name)

    # itemID -> collections
    colls = {}
    cur.execute("""SELECT ci.itemID, c.collectionName FROM collectionItems ci
                   JOIN collections c ON c.collectionID = ci.collectionID""")
    for item_id, cname in cur.fetchall():
        colls.setdefault(item_id, []).append(cname)

    # PDF 附件: parentItemID -> [(key, filename)]
    pdfs = {}
    cur.execute("""SELECT ia.parentItemID, i.key, ia.path
                   FROM itemAttachments ia JOIN items i ON i.itemID = ia.itemID
                   WHERE ia.contentType = 'application/pdf' AND ia.parentItemID IS NOT NULL""")
    for parent, akey, path in cur.fetchall():
        if not path:
            continue
        fname = Path(path.replace("storage:", "")).name
        pdfs.setdefault(parent, []).append((akey, fname))

    # 条目主表
    cur.execute("""SELECT i.itemID, i.key, it.typeName FROM items i
                   JOIN itemTypes it ON it.itemTypeID = i.itemTypeID
                   WHERE i.itemID NOT IN (SELECT itemID FROM deletedItems)""")
    rows = cur.fetchall()
    con.close()

    lib = []
    for item_id, key, type_name in rows:
        if type_name not in CITABLE:
            continue
        f = fields.get(item_id, {})
        entry = {
            "itemKey": key,
            "citationKey": f.get("citationKey", ""),
            "itemType": type_name,
            "title": (f.get("title") or "").strip(),
            "date": (f.get("date") or "").strip(),
            "DOI": (f.get("DOI") or "").strip(),
            "url": (f.get("url") or "").strip(),
            "publication": (f.get("publicationTitle") or f.get("bookTitle")
                            or f.get("proceedingsTitle") or "").strip(),
            "abstract": (f.get("abstractNote") or "")[:1200],
            "creators": creators.get(item_id, []),
            "collections": colls.get(item_id, []),
            "pdfs": [{"attachmentKey": k, "filename": n,
                      "path": str(STORAGE / k / n)} for k, n in pdfs.get(item_id, [])],
        }
        if not entry["citationKey"]:
            # BBT 未覆盖时用 itemKey 兜底，保证每条都有可引用的键
            entry["citationKey"] = f"zotero-{key.lower()}"
            entry["citationKeySource"] = "fallback-itemKey"
        lib.append(entry)

    stats = {
        "total_citable": len(lib),
        "with_doi": sum(1 for e in lib if e["DOI"]),
        "with_pdf": sum(1 for e in lib if e["pdfs"]),
        "with_citation_key": sum(1 for e in lib if not e.get("citationKeySource")),
        "by_type": {},
    }
    for e in lib:
        stats["by_type"][e["itemType"]] = stats["by_type"].get(e["itemType"], 0) + 1
    return lib, stats


def year_of(date: str) -> str:
    import re
    m = re.search(r"(19|20)\d{2}", date or "")
    return m.group(0) if m else ""


def write_outputs(lib: list[dict], stats: dict, bib: str | None) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (VAULT / "50_Output" / "References").mkdir(parents=True, exist_ok=True)

    if bib:
        BIB_OUT.write_text(bib, encoding="utf-8")
        log(f"  BibLaTeX -> {BIB_OUT}  ({len(bib.splitlines())} 行)")

    (OUT_DIR / "library.json").write_text(json.dumps(
        {"generated": datetime.now().isoformat(),
         "source": "Zotero + Better BibTeX (local)",
         "stats": stats, "items": lib}, ensure_ascii=False, indent=2), encoding="utf-8")

    pdf_map = {e["citationKey"]: [p["path"] for p in e["pdfs"]]
               for e in lib if e["pdfs"]}
    (OUT_DIR / "pdf_map.json").write_text(json.dumps(
        {"generated": datetime.now().isoformat(), "count": len(pdf_map),
         "map": pdf_map}, ensure_ascii=False, indent=2), encoding="utf-8")

    L = ["# Zotero 阅读索引", "",
         f"**同步**: {datetime.now():%Y-%m-%d %H:%M} · 来源 Zotero + Better BibTeX（本机）", "",
         "## 统计", "",
         f"- 可引用条目 **{stats['total_citable']}**",
         f"- 有 DOI **{stats['with_doi']}** · 有 PDF **{stats['with_pdf']}** · 有 BBT citationKey **{stats['with_citation_key']}**",
         "", "| 类型 | 数量 |", "|---|---|"]
    for k, v in sorted(stats["by_type"].items(), key=lambda x: -x[1]):
        L.append(f"| {k} | {v} |")
    L += ["", "## 条目（按年份倒序）", "",
          "| citationKey | 年份 | 标题 | 类型 | PDF |", "|---|---|---|---|---|"]
    for e in sorted(lib, key=lambda x: (year_of(x["date"]) or "0000"), reverse=True):
        t = e["title"].replace("|", "\\|")[:110]
        pdf = "✓" if e["pdfs"] else "—"
        L.append(f"| `{e['citationKey']}` | {year_of(e['date'])} | {t} | {e['itemType']} | {pdf} |")
    L += ["", "> 引用时用 `citationKey`；PDF 绝对路径见 `pdf_map.json`。",
          "> 本文件由 `zotero_bridge.py` 生成，**不要手工编辑**（下次同步会覆盖）。"]
    (OUT_DIR / "reading_index.md").write_text("\n".join(L), encoding="utf-8")
    log(f"  索引 -> {OUT_DIR/'library.json'}")
    log(f"  阅读索引 -> {OUT_DIR/'reading_index.md'}")
    log(f"  PDF 映射 -> {OUT_DIR/'pdf_map.json'}  ({len(pdf_map)} 条)")


def seed_papers(lib: list[dict]) -> None:
    """把 Zotero 播种进引用白名单（papers.yaml）。

    状态语义（不擅自升级）:
        Zotero 条目 = 用户已收录的真实文献 -> status="pending"
        （"已登记、题录待核验"。只有人工核对题名/作者/年份后才升为 verified。）

    用批量接口: 540 条若走单条 register_paper() 是 O(n²)，实测 >120s 未完成。
    """
    sys.path.insert(0, str(VAULT / "90_System"))
    from research_evolve.gates import load_papers, register_papers_bulk  # noqa: PLC0415
    before = len(load_papers().get("works", []))
    records = []
    for e in lib:
        ident = f"doi:{e['DOI']}" if e["DOI"] else (
            f"zotero:{e['itemKey']}" if e["itemKey"] else f"url:{e['url']}")
        records.append({
            "key": e["citationKey"], "title": e["title"], "identifier": ident,
            "status": "pending",
            "source": f"zotero:{e['itemType']}" + (f" ({e['publication']})" if e["publication"] else ""),
        })
    res = register_papers_bulk(records)
    after = len(load_papers().get("works", []))
    log(f"  引用白名单: {before} -> {after} 条（新增 {res['added']}，更新 {res['updated']}）")


def check() -> int:
    ok = True
    try:
        with urllib.request.urlopen(f"{API_BASE}/connector/ping", timeout=8) as r:
            log(f"Zotero 本地 API: OK ({r.read().decode('utf-8','ignore').strip()[:60]})")
    except Exception as e:
        log(f"Zotero 本地 API: 不可达 ({type(e).__name__})"); ok = False
    db = snapshot_db()
    lib, stats = read_library(db)
    log(f"可引用条目 {stats['total_citable']} | 有DOI {stats['with_doi']} | "
        f"有PDF {stats['with_pdf']} | 有BBT key {stats['with_citation_key']}")
    log(f"按类型: {stats['by_type']}")
    bib = fetch_bib()
    log(f"BBT 导出: {'OK' if bib else '失败'} ({len(bib) if bib else 0} 字符)")
    return 0 if ok else 1


def main() -> int:
    args = sys.argv[1:]
    if "--check" in args:
        return check()

    log("=== Zotero -> vault 同步 ===")
    db = snapshot_db()
    lib, stats = read_library(db)
    log(f"读到可引用条目 {stats['total_citable']}（有PDF {stats['with_pdf']}，"
        f"有BBT citationKey {stats['with_citation_key']}）")
    bib = fetch_bib()
    write_outputs(lib, stats, bib)
    if "--seed-papers" in args:
        seed_papers(lib)
    log("=== 完成 ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
