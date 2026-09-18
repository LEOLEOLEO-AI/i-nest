# -*- coding: utf-8 -*-
"""research_evolve.seed_papers — 从文稿参考文献表播种引用白名单。

为什么需要它：引用白名单（papers.yaml）是防编造的第一机制，但从零手填
几百条不现实。而项目里的理论专著（如 18_iNEST_Final_Theory_20260917/
01_Final_Theory.md）本身就有结构化参考文献表，**并且逐条声明了核验层级**
（"题录已核" / "摘要已核" / "相关正文已核"）。

于是最诚实的播种方式：把文稿自己的声明搬进白名单，而不是让 AI 替它
"认定已核验"。本工具只搬运，不判断。

status 映射（严格照搬文稿声明，不升级）：
    题录已核 / 题录与相关内容已核 / 相关正文已核  -> verified
    摘要已核 / 其他/未声明                        -> pending

用法:
    cd D:\\Obsidian\\vault\\90_System
    python -m research_evolve.seed_papers "50_Output/53_Monographs/18_iNEST_Final_Theory_20260917/01_Final_Theory.md"
    python -m research_evolve.seed_papers <file> --dry-run
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from .gates import load_papers, register_paper
from .common import VAULT

# 参考文献行有两种实际存在的写法（同一份文稿里混用）：
#   A) 作者在前: "- [R01] Dambre et al. (2012). Information Processing Capacity ... [doi](...)"
#   B) 标题在前: "- [R34] Online dynamical learning and sequence memory ... (2023). Nature Communications. [doi](...)"
# 首版正则把作者段限死在 80 字符并要求括号前就是作者，于是 B 类（标题长于 80）全部漏掉
# （实测漏了 R34/R35/R37）。改为先宽松地抓 [id]...[doi] 主体，再判断哪一段是标题。
REF_LINE_RE = re.compile(
    r"^\s*[-*]\s*\[(?P<rid>[A-Za-z]?\d{1,3})\]\s*"
    r"(?P<body>.{0,400}?)"
    r"\[(?P<doi>10\.\d{4,9}/[^\]]+)\]",
    re.M | re.S,
)
YEAR_RE = re.compile(r"\((\d{4})\)")
# 作者段特征：含 et al / 字符数短且词数少
_AUTHORY_RE = re.compile(r"\bet al\b|&|,\s*[A-Z][a-z]+$", re.I)
# 11_Additional_Source_Records.md 的 API 结果行: ## R39 Source: <url> HTTP: 200 Title: X. DOI: 10....
API_TITLE_RE = re.compile(
    r"DOI:\s*(?P<doi>10\.\d{4,9}/[^\s]+)\s*(?:\r?\n)?(?P<rest>.{0,400}?)Title:\s*(?P<title>[^\n]{5,300})",
    re.S,
)
API_TITLE_RE2 = re.compile(
    r"Title:\s*(?P<title>[^\n]{5,300}?)\s*DOI:\s*(?P<doi>10\.\d{4,9}/[^\s]+)",
    re.S,
)


def _split_authors_title(body: str) -> tuple[str, str, str]:
    """从参考文献主体里分出 (authors, title, year)。"""
    body = re.sub(r"\s+", " ", body).strip()
    m = YEAR_RE.search(body)
    year = m.group(1) if m else ""
    if not m:
        return "", body.rstrip("."), year
    prefix = body[:m.start()].strip()
    rest = body[m.end():].strip().lstrip(".").strip()
    rest = re.sub(r"\.\s*$", "", rest).strip()
    # 判断 prefix 是作者还是标题
    is_author = bool(_AUTHORY_RE.search(prefix)) or (
        len(prefix) <= 45 and len(prefix.split()) <= 5)
    if is_author:
        return prefix, rest, year
    # 标题在前：prefix 是标题，rest 是期刊/其余
    return "", prefix.rstrip("."), year

VERIFIED_MARKERS = ("题录已核", "题录与相关内容已核", "相关正文已核", "题录已核；",
                    "相关正文及定理已核")


def _status_from_note(note: str) -> tuple[str, str]:
    """按文稿自己的声明决定 status，不擅自升级。"""
    if any(m in note for m in VERIFIED_MARKERS):
        return "verified", "文稿声明题录/正文已核"
    if "摘要已核" in note:
        return "pending", "文稿声明仅摘要已核"
    if note.strip():
        return "pending", "文稿有核验说明但未声明题录已核"
    return "pending", "文稿未声明核验层级"


def seed_from_reference_list(text: str, source: str, dry: bool = False) -> list[dict]:
    out = []
    seen = set()
    for m in REF_LINE_RE.finditer(text):
        rid = m.group("rid")
        # "[R01]" 的捕获组已含前导 R（可选字母），不要重复加前缀
        key = rid if rid[:1].isalpha() else f"R{rid}"
        doi = m.group("doi").strip().rstrip(".,;").split("&")[0].split("?")[0]
        if doi in seen:
            continue
        seen.add(doi)
        authors, title, year = _split_authors_title(m.group("body"))
        # 核验说明 = 该行 DOI 链接之后到行尾
        nl = text.find("\n", m.end())
        tail = text[m.end(): nl if nl > 0 else len(text)]
        status, why = _status_from_note(tail)
        rec = {"key": key, "title": title or f"(题名待补) {doi}",
               "identifier": f"doi:{doi}", "status": status,
               "source": f"{source} ({why})",
               "authors": authors, "year": year}
        out.append(rec)
        if not dry:
            register_paper(rec["key"], rec["title"], rec["identifier"],
                           rec["status"], rec["source"])
    return out


def seed_from_api_records(text: str, source: str, dry: bool = False) -> list[dict]:
    out = []
    seen = set()
    for rx in (API_TITLE_RE, API_TITLE_RE2):
        for m in rx.finditer(text):
            # URL 查询串必须截断，否则同一 DOI 会以 "doi&format=json" 形式重复登记
            doi = m.group("doi").strip().rstrip(".,;").split("&")[0].split("?")[0]
            title = re.sub(r"\s+", " ", m.group("title")).strip()
            title = title.split(" DOI:")[0].strip().rstrip(".")
            if doi in seen or len(title) < 5:
                continue
            seen.add(doi)
            rec = {"key": f"API-{doi.split('/')[-1][:24]}", "title": title,
                   "identifier": f"doi:{doi}", "status": "pending",
                   "source": f"{source} (题录取自 Crossref/EuropePMC 返回)"}
            out.append(rec)
            if not dry:
                register_paper(rec["key"], rec["title"], rec["identifier"],
                               rec["status"], rec["source"])
    return out


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 1

    total = 0
    for rel in args:
        p = (VAULT / rel) if not Path(rel).is_absolute() else Path(rel)
        if not p.exists():
            print(f"[skip] 不存在: {p}")
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        src = p.relative_to(VAULT).as_posix() if p.is_relative_to(VAULT) else str(p)
        recs = seed_from_reference_list(text, src, dry)
        mode = "参考文献表" if recs else "API 记录"
        if not recs:
            recs = seed_from_api_records(text, src, dry)
        print(f"[{ 'DRY ' if dry else ''}{mode}] {src} -> {len(recs)} 条")
        for r in recs[:5]:
            print(f"    {r['key']:>10}  {r['status']:<8} {r['title'][:62]}")
        if len(recs) > 5:
            print(f"    ... 其余 {len(recs)-5} 条")
        total += len(recs)

    print(f"\n合计登记 {total} 条 -> {load_papers() and 'papers.yaml'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
