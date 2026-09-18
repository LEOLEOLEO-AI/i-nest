# -*- coding: utf-8 -*-
"""research_evolve.gates — 把计划的三条硬规矩变成可执行的门禁。

计划原文（research-brain）：
  * "framework/ 对 AI 只读"
  * "每次运行一次提交"
  * "结论必带出处，引用走白名单 … 没在 papers/ 登记的文献不能出现在正文里"

现状实测：这三条在 vault 里**没有任何代码在执行**——
`[实测]/[仿真]` 标签只写在 .codex 的契约文档里，没有任何脚本扫描产出；
引用白名单机制完全不存在。本模块补上这一层。

设计要点（两个已实测的教训）：
  1. **词边界铁律**。首版用 `"ns" in line` 判定单位，结果 "Tran**ns**form" 命中，
     182 个文件刷出 2975 条假违规。这与 AGENTS.md 6.3 记录的
     `interconnect` 误配 `interconnected` 是同一类错误——所有单位匹配
     必须数字化邻接 + 词边界，禁止裸子串。
  2. **门禁必须是"回归检测器"而非"债务放大器"**。
     全库既有 300+ 条未登记引用是先前的债，一次报 3281 条没人会修，
     下一轮还报同样 3281 条——那就退化成第二个"每天 18 条建议"。
     因此本模块维护 baseline：只有**基线之外的新违规**才判失败（exit 2），
     存量债单独计为 known_debt 并逐轮显示是否在减少。

退出码：0=无新增违规, 2=存在新增违规。
"""
from __future__ import annotations

import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path

from .common import (
    EVIDENCE_LABELS,
    FRAMEWORK_FILE,
    PAPERS_FILE,
    STATE_DIR,
    VAULT,
    load_config,
    load_json,
    load_yaml,
    read_text,
    save_json,
    save_yaml,
    today,
)

PAPERS_SCHEMA = "research-evolve-papers-v1"
FRAMEWORK_SCHEMA = "research-evolve-framework-v1"
BASELINE_FILE = STATE_DIR / "gate_baseline.json"

# ---------------------------------------------------------------- 引用抽取
CITE_PATTERNS = [
    re.compile(r"\\cite[a-z]*\{([^}]+)\}"),
    re.compile(r"\[@([A-Za-z][\w:.\-]+)\]"),
]
# 裸 @key2019 形式：要求含 4 位年份，避免命中邮箱/句柄
ATKEY_RE = re.compile(r"(?<![A-Za-z0-9_.@])@([A-Za-z][A-Za-z\-]{1,20}\d{4}[a-z]?)\b")
ARXIV_RE = re.compile(r"arXiv[:\s]*(\d{4}\.\d{4,5})(v\d+)?", re.I)
# DOI 在 URL 查询串里会带上 &format=json 之类的尾巴，必须在此截断，
# 否则同一个 DOI 会被计两次（一次干净、一次带查询串）。
DOI_RE = re.compile(r"(?:doi[:\s]*|doi\.org/)(10\.\d{4,9}/[^\s)\]}\"'，。&?#]+)", re.I)


def extract_citations(text: str) -> dict:
    """抽取文本中的引用标识。返回 {keys, arxiv, doi}。"""
    keys: set[str] = set()
    for pat in CITE_PATTERNS:
        for m in pat.findall(text or ""):
            for k in str(m).split(","):
                k = k.strip()
                if k:
                    keys.add(k)
    for k in ATKEY_RE.findall(text or ""):
        keys.add(k)
    return {
        "keys": sorted(keys),
        "arxiv": sorted({m[0] for m in ARXIV_RE.findall(text or "")}),
        "doi": sorted({d.rstrip(".,;") for d in DOI_RE.findall(text or "")}),
    }


# ---------------------------------------------------------------- 白名单
def load_papers() -> dict:
    data = load_yaml(PAPERS_FILE, default=None)
    if not isinstance(data, dict):
        return {"schema": PAPERS_SCHEMA, "works": []}
    data.setdefault("schema", PAPERS_SCHEMA)
    data.setdefault("works", [])
    return data


def paper_index(papers: dict) -> tuple[set[str], set[str], set[str], set[str]]:
    """返回 (允许keys, 允许arXiv, 允许DOI, 禁止标识)。"""
    keys, arxiv, doi, blocked = set(), set(), set(), set()
    for w in papers.get("works", []) or []:
        if not isinstance(w, dict):
            continue
        status = str(w.get("status", "pending")).lower()
        ident = str(w.get("identifier", "") or "")
        targets = [ident]
        if w.get("key"):
            targets.append(str(w["key"]))
        if status == "rejected":
            for t in targets:
                if t.strip():
                    blocked.add(t.strip())
            continue
        if w.get("key"):
            keys.add(str(w["key"]).strip())
        m = ARXIV_RE.search(ident)
        if m:
            arxiv.add(m.group(1))
        m = DOI_RE.search(ident)
        if m:
            doi.add(m.group(1).rstrip(".,;").lower())
    return keys, arxiv, doi, blocked


def register_paper(key: str, title: str, identifier: str,
                   status: str = "pending", source: str = "") -> dict:
    papers = load_papers()
    works = papers.setdefault("works", [])
    for w in works:
        if isinstance(w, dict) and str(w.get("key")) == key:
            w.update({"title": title, "identifier": identifier,
                      "status": status, "source": source, "updated": today()})
            save_yaml(PAPERS_FILE, papers)
            return w
    w = {"key": key, "title": title, "identifier": identifier,
         "status": status, "added": today(), "source": source}
    works.append(w)
    save_yaml(PAPERS_FILE, papers)
    return w


def check_citations(text: str, papers: dict) -> list[dict]:
    cites = extract_citations(text)
    keys, arxiv, doi, blocked = paper_index(papers)
    out = []
    for k in cites["keys"]:
        if k in blocked:
            out.append({"type": "citation-blocked", "value": k,
                        "why": "该文献核验未通过，禁止引用"})
        elif k not in keys:
            out.append({"type": "citation-unregistered", "value": k,
                        "why": "引用键未在 papers.yaml 登记（防编造）"})
    for a in cites["arxiv"]:
        if a not in arxiv:
            out.append({"type": "citation-unregistered", "value": f"arXiv:{a}",
                        "why": "arXiv 标识未在白名单登记"})
    for d in cites["doi"]:
        if d.lower() not in doi:
            out.append({"type": "citation-unregistered", "value": f"doi:{d}",
                        "why": "DOI 未在白名单登记"})
    return out


# ---------------------------------------------------------------- 数字证据标签
# 判定规则（三轮收窄后的最终口径，追求精确率而非召回率）：
#   一行构成"性能论断"当且仅当：**性能指标名词**与一个数字在 30 字符内共现，
#   且该行没有任何证据标签。
#
# 为什么不再用"数字 + 单位"判定（两次实测的返工教训）：
#   v1 用 `"ns" in line`       -> "Tran**ns**form" 命中，刷出 2975 条假违规；
#   v2 用"数字 + 单位"          -> "21**KB**" 文件体积、"64**×**64" 阵列尺寸
#                                又成了"性能论断"，仍有 1192 条假违规。
#   体积、行数、阵列维度都是**文档/结构元数据**，不是性能指标。
#   AGENTS.md 0.1 管的是"延迟、吞吐、能耗、面积、成本"这类指标，
#   所以必须锚定**指标名词**，而不是单位符号。
METRIC_NOUNS = [
    "延迟", "时延", "吞吐", "能耗", "功耗", "能效", "面积", "成本", "带宽",
    "频率", "算力", "精度", "加速比", "速度", "容量", "错误率", "准确率",
    "latency", "throughput", "energy", "power", "efficiency", "area",
    "bandwidth", "frequency", "accuracy", "speedup", "cost", "precision",
]
METRIC_NOUNS_L = [m.lower() for m in METRIC_NOUNS]
# 独立数字 token：左右不得紧邻拉丁字母数字，避免 "R1"、"C2C"、"5plus4"
# 里的数字被当成量值；允许科学计数法 "1.4E3"。
NUM_RE = re.compile(r"(?<![A-Za-z0-9])\d[\d,]*(?:\.\d+)?(?:\s*[Ee][+-]?\d+)?(?![A-Za-z0-9])")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
FILEEXT_RE = re.compile(r"\.(md|py|json|pdf|tex|bib|html|csv|yaml|yml|js|txt|pptx)\b", re.I)
# 文档元数据特征：体积/行数/字数——出现这些基本可判为清单行而非论断
DOCMETA_RE = re.compile(r"\d[\d.,]*\s*(?:KB|MB|GB|TB|行|字|字符|页)\b", re.I)
PROXIMITY = 30
# 行首有序/无序列表标记：扫描前剥掉，避免 "1. Accuracy ..." 的序号被当成量值
LISTMARK_RE = re.compile(r"^\s*(?:[-*+•]\s+|\d{1,3}[.、)]\s+)")
# 数学公式片段：$...$ / $$...$$ 内部的数字是符号量，不是性能指标
MATH_SPAN_RE = re.compile(r"\$\$.+?\$\$|\$.+?\$", re.S)
# 交叉引用（式(16) / 表 3 / 图 2 / [R01] / Eq.(4) / Section 5）：
# 其中数字是编号而非量值。实测误报来源之一正是 "按正文式（16）…结合成本项"。
XREF_RE = re.compile(
    r"(?:式|公式|表|图|附录|第)\s*[（(]?\s*\d{1,4}[A-Za-z]?\s*[）)]?\s*[章节]?"
    r"|\[\s*[A-Za-z]?\d{1,3}\s*\]"
    r"|\b(?:Eq|Eqs|Fig|Figs|Table|Section|Sec|Ref|Refs)\.?\s*\(?\d{1,3}\)?"
    # 定理类环境编号（Remark 3 / Theorem 2.1 / 引理 4）：数字是编号，不是量值
    r"|\b(?:Remark|Theorem|Thm|Lemma|Proposition|Corollary|Definition|Def|"
    r"Assumption|Claim|Note|Step|Algorithm|Alg|Appendix|Equation)\s*\.?\s*\d{1,3}(?:\.\d{1,3})*"
    r"|(?:定理|引理|推论|定义|假设|命题|性质|注|步骤|算法|附录)\s*\d{1,3}",
    re.I,
)


def _metric_near_number(s: str) -> tuple[bool, str]:
    """数字与指标名词在 PROXIMITY 字符窗口内共现则算论断，并返回命中的名词。

    扫描前先剔除三类"数字但不是量值"的内容：行首列表标记、数学公式、交叉引用编号。
    """
    scan = MATH_SPAN_RE.sub(" ", s)
    scan = XREF_RE.sub(" ", scan)
    scan = LISTMARK_RE.sub("", scan).lower()
    for m in NUM_RE.finditer(scan):
        lo = max(0, m.start() - PROXIMITY)
        hi = min(len(scan), m.end() + PROXIMITY)
        window = scan[lo:hi]
        for noun in METRIC_NOUNS_L:
            if noun in window:
                return True, noun
    return False, ""


def check_evidence_labels(text: str) -> list[dict]:
    """扫描缺证据标签的性能论断行。锚定指标名词，避开单位与元数据噪声。"""
    out = []
    in_fence = False
    for i, line in enumerate((text or "").splitlines(), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("---"):
            continue
        if s.startswith("|"):           # 表格另行人工核对
            continue
        if not NUM_RE.search(s):
            continue
        if any(lbl in s for lbl in EVIDENCE_LABELS):
            continue
        # 文档/结构元数据行（体积、行数、字数、页数）不是性能指标，一律不计
        if DOCMETA_RE.search(s):
            continue
        hit, noun = _metric_near_number(s)
        if not hit:
            continue
        out.append({"type": "unlabeled-number", "line": i,
                    "why": f"性能论断（指标词：{noun}）未带证据标签（AGENTS.md 0.1）",
                    "excerpt": s[:160], "metric_noun": noun})
    return out


# ---------------------------------------------------------------- framework 只读
def _sha1_file(p: Path) -> str:
    try:
        return hashlib.sha1(p.read_bytes()).hexdigest()
    except Exception:
        return ""


def load_framework() -> dict:
    data = load_yaml(FRAMEWORK_FILE, default=None)
    if not isinstance(data, dict):
        return {"schema": FRAMEWORK_SCHEMA, "files": []}
    data.setdefault("schema", FRAMEWORK_SCHEMA)
    data.setdefault("files", [])
    return data


def _discover_framework_paths() -> list[str]:
    """默认纳入的 framework 正本：SSOT 裁定 + 理论层（用户写、AI 只读）。"""
    cands: list[str] = []
    for rel in ("60_MOC/00_治理/SSOT_公式与术语裁定_20260826.md",
                "60_MOC/00_治理/00_科研智能体使用手册_20260821.md"):
        if (VAULT / rel).exists():
            cands.append(rel)
    for d in ("30_TCC/31_Theory", "40_iNEST/41_Theory"):
        root = VAULT / d
        if root.exists():
            for f in sorted(root.rglob("*.md"))[:60]:
                cands.append(f.relative_to(VAULT).as_posix())
    return cands


def seal_framework(paths: list[str] | None = None) -> dict:
    """把 framework 正本文件的当前哈希写入清单（封印）。"""
    if paths is None:
        paths = _discover_framework_paths()
    files = []
    for rel in paths:
        p = VAULT / rel
        if p.exists() and p.is_file():
            files.append({"path": rel, "sha1": _sha1_file(p),
                          "bytes": p.stat().st_size})
    data = {"schema": FRAMEWORK_SCHEMA, "sealed": today(), "files": files}
    save_yaml(FRAMEWORK_FILE, data)
    return data


def check_framework() -> list[dict]:
    out = []
    for entry in load_framework().get("files", []) or []:
        rel = entry.get("path")
        if not rel:
            continue
        p = VAULT / rel
        if not p.exists():
            out.append({"type": "framework-missing", "value": rel,
                        "why": "framework 正本文件缺失"})
            continue
        if entry.get("sha1") and _sha1_file(p) != entry["sha1"]:
            out.append({"type": "framework-modified", "value": rel,
                        "why": "framework 只读文件内容已变更（须由用户本人确认）"})
    return out


# ---------------------------------------------------------------- 基线（棘轮）
def _fingerprint(v: dict) -> str:
    """违规指纹：用于基线比对。

    刻意**不使用行号**——行号会随文件任何编辑而漂移，那会让所有存量违规
    瞬间变成"新增"、旧指纹又变成"已修复"，基线变成噪声源。
    改用 (类型, 文件, 值/正文归一) 作为身份，对行漂移免疫。
    """
    ident = v.get("value") or ""
    if not ident and v.get("excerpt"):
        ident = re.sub(r"\s+", " ", str(v["excerpt"])).strip()[:120]
    raw = f"{v.get('type')}|{v.get('file','')}|{ident}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def load_baseline() -> dict:
    return load_json(BASELINE_FILE, default={"entries": {}}) or {"entries": {}}


def save_baseline(violations: list[dict]) -> dict:
    entries = {}
    for v in violations:
        entries[_fingerprint(v)] = {
            "type": v.get("type"), "file": v.get("file"), "value": v.get("value"),
            "line": v.get("line"), "why": v.get("why"),
            "accepted": datetime.now().isoformat(),
        }
    data = {"generated": datetime.now().isoformat(),
            "note": "存量债基线。只有基线之外的新违规才判门禁失败。人工复核后可用 --update-baseline 收敛。",
            "entries": entries}
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    save_json(BASELINE_FILE, data)
    return data


def diff_baseline(violations: list[dict]) -> dict:
    """把本轮违规分成 新增 / 存量。新增才判失败。"""
    base = load_baseline().get("entries", {}) or {}
    new, known = [], []
    seen = set()
    for v in violations:
        fp = _fingerprint(v)
        seen.add(fp)
        if fp in base:
            known.append(v)
        else:
            v["fingerprint"] = fp
            new.append(v)
    fixed = [k for k in base if k not in seen]
    return {"new": new, "known": known, "fixed": fixed,
            "baseline_size": len(base)}


# ---------------------------------------------------------------- 产出扫描
def scan_outputs(cfg: dict | None = None) -> dict:
    cfg = cfg or load_config()
    papers = load_papers()
    limit = int(cfg.get("gate_scan_limit", 400))
    violations: list[dict] = []
    scanned = 0
    for rel in cfg.get("gate_paths", []):
        root = VAULT / rel
        if not root.exists():
            continue
        for f in sorted(root.rglob("*.md")):
            if scanned >= limit:
                break
            scanned += 1
            txt = read_text(f)
            if not txt.strip():
                continue
            frel = f.relative_to(VAULT).as_posix()
            for v in check_citations(txt, papers):
                v["file"] = frel
                violations.append(v)
            for v in check_evidence_labels(txt):
                v["file"] = frel
                violations.append(v)
    for v in check_framework():
        violations.append(v)
    return {"scanned_files": scanned, "violations": violations,
            "count": len(violations)}


def gate_result(cfg: dict | None = None) -> dict:
    """门禁总判定：新增违规 -> 失败；存量债 -> 报告但不失败。"""
    res = scan_outputs(cfg)
    d = diff_baseline(res["violations"])
    res.update(d)
    res["failed"] = len(d["new"]) > 0
    return res


# ---------------------------------------------------------------- CLI
def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "--check"

    if cmd == "--seal-framework":
        data = seal_framework()
        print(f"已封印 {len(data['files'])} 个 framework 正本文件 -> {FRAMEWORK_FILE}")
        return 0

    if cmd == "--update-baseline":
        res = scan_outputs()
        save_baseline(res["violations"])
        print(f"基线已更新：接受 {res['count']} 条存量债（扫描 {res['scanned_files']} 文件）")
        print(f"-> {BASELINE_FILE}")
        return 0

    if cmd == "--register":
        if len(argv) < 4:
            print("用法: --register <key> <title> <identifier> [status] [source]")
            return 1
        key, title, ident = argv[1], argv[2], argv[3]
        status = argv[4] if len(argv) > 4 else "pending"
        src = argv[5] if len(argv) > 5 else "manual"
        print(f"已登记: {register_paper(key, title, ident, status, src)}")
        return 0

    if cmd == "--check":
        r = gate_result()
        print(f"扫描 {r['scanned_files']} 文件 | 违规合计 {r['count']} | "
              f"新增 {len(r['new'])} | 存量债 {len(r['known'])} | "
              f"本轮已修复 {len(r['fixed'])}")
        for v in r["new"][:30]:
            loc = v.get("file") or v.get("value") or ""
            ln = f":{v['line']}" if v.get("line") else ""
            print(f"  [NEW] [{v['type']}] {loc}{ln} — {v.get('why','')}")
            if v.get("excerpt"):
                print(f"        {v['excerpt'][:120]}")
        if r["failed"]:
            print(f"\n结论: 门禁未通过（{len(r['new'])} 项新增违规）")
            return 2
        print("\n结论: 门禁通过（无新增违规）")
        return 0

    print("用法: gates.py [--check | --seal-framework | --update-baseline | --register ...]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
