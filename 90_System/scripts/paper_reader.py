#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""paper_reader.py — 基于 Zotero 本地文献库的论文阅读/问答引擎。

与高星开源项目的差异（2026-09-19 依据实测与源码核查）:
    STORM 与 GPT Researcher **都不在运行时校验引用**：
      * STORM 只做"引用序号完整性 + 重新编号"（超出参考文献数的 [n] 直接丢弃），
        没有任何 NLI/蕴含检查证明"被引片段真的支持这句话"；
      * GPT Researcher 仅在提示词里写"不要引用未出现过的来源"，且 add_references()
        会把**所有访问过的 URL** 都附上（包括从未被引用的），两个方向都没有校验。
    而 OpenScholar 的对照数据显示 **GPT-4o 的引用有 78%~90% 是编造的**。
    因此本引擎把"**引用可验证**"当作一等功能，而不是靠提示词自觉：
      1. 每个片段都带 (citationKey, 页码) 溯源；
      2. 回答必须用 [citationKey p.N] 形式引用；
      3. 生成后**逐条校验**：该 key 是否在白名单、该页是否真的在本轮检索结果里、
         该页原文是否与所支撑的句子有词面重叠 —— 不通过就明确标红，而不是默默放过。

技术选型（均为宽松许可，避开 AGPL）:
    pypdf (BSD-3) 主提取 —— 实测 10/10 可用且字符数最多；
    pdfplumber (MIT) 兜底 —— 个别版式更好；
    **不使用 PyMuPDF/fitz（AGPL）**：它会传染整个应用。
    检索用纯 Python BM25（无外部依赖，避免 chromadb/faiss/sentence-transformers 的重量级依赖链）。

用法:
    python paper_reader.py index                 # 建/更新 PDF 文本索引
    python paper_reader.py index --limit 20      # 只索引前 20 篇（试跑）
    python paper_reader.py search "问题" -k 8    # 只检索，不调 LLM
    python paper_reader.py ask "问题" -k 8       # 检索 + LLM 问答 + 引用校验
    python paper_reader.py status                # 索引状态
"""
from __future__ import annotations

import json
import math
import re
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

VAULT = Path(r"D:\Obsidian\vault")
ZDIR = VAULT / "90_System" / "research_evolve" / "zotero"
PDF_MAP = ZDIR / "pdf_map.json"
LIBRARY = ZDIR / "library.json"
CACHE = ZDIR / "text_cache"
CORPUS = ZDIR / "corpus.jsonl"
SCRIPTS = VAULT / "90_System" / "scripts"

GARBLE_LIMIT = 0.18          # 乱码阈值，超过则该页标记为低质量
CHUNK_CHARS = 1200
CHUNK_OVERLAP = 200

# 参考文献页会污染检索：实测检索结果的 p.19 是 "e r a ,C .R .M i r a s s o ,a n dI .F i s c h e r ,Opt. Express 20, 32..."
# 特征：年份密度高、大量 "et al"/期刊缩写、几乎没有句子。这类页不入索引。
_REF_HINT = re.compile(
    r"(?i)\b(references|bibliography)\b|doi:|arxiv:|vol\.\s*\d+|\bpp\.\s*\d+")
_YEAR = re.compile(r"\b(19|20)\d{2}\b")


def looks_like_references(t: str) -> bool:
    """判断一页是否像参考文献列表（据此排除，避免检索命中书目而非内容）。

    实测教训: 首版只看"年份密度 + 句子终止符"，仍漏掉了形如
    '[14] Fagerholm, E.D., et al. "Cortical entropy..." 10, 8, 702, (2021). [20] Wang, S.H. et al.'
    的书目页 —— 于是它作为"高相关片段"进了检索结果。
    补充两条书目特征: 方括号编号密度、'et al.' 密度。
    """
    if len(t) < 300:
        return False
    years = len(_YEAR.findall(t))
    hints = len(_REF_HINT.findall(t))
    dens = years / (len(t) / 1000)
    stops = len(re.findall(r"[.!?]\s", t))
    bracket_nums = len(re.findall(r"\[\d{1,3}\]", t))
    etal = len(re.findall(r"(?i)\bet al\b", t))
    # 书目页: 方括号编号/et al 密集，或年份密度高且句子少
    if bracket_nums >= 6 and etal >= 3:
        return True
    if dens > 5 and etal >= 4:
        return True
    return (dens > 8 and hints > 3) or (stops / max(len(t) / 1000, 1) < 2 and dens > 5)


# ---------------------------------------------------------------- 文本提取
def garble_ratio(t: str) -> float:
    """乱码启发式：重复字符/重复三连子串占比。

    某些 PDF（旋转排版、矢量字形）会被提成 'rrraaabbbggg' 这类串。
    实测一份 185 页学位论文用 pdfplumber 提取得 0.238（乱），pypdf 得 0.015（正常）。
    """
    if len(t) < 60:
        return 1.0
    rep = len(re.findall(r"(.)\1{2,}", t))
    tri = Counter(t[i:i + 3] for i in range(len(t) - 2))
    top = tri.most_common(1)[0][1] / max(len(t) - 2, 1)
    return max(rep / max(len(t) / 100, 1), top)


def extract_pdf(path: Path) -> tuple[list[str], str]:
    """返回 (每页文本, 使用的方法)。pypdf 优先，pdfplumber 兜底。"""
    pages: list[str] = []
    method = "pypdf"
    try:
        from pypdf import PdfReader
        r = PdfReader(str(path))
        pages = [(p.extract_text() or "") for p in r.pages]
    except Exception:
        pages = []
    good = sum(1 for t in pages if len(t) > 200 and garble_ratio(t) < GARBLE_LIMIT)
    if pages and good >= max(1, len(pages) // 3):
        return pages, method
    # 兜底
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            alt = [(pg.extract_text() or "") for pg in pdf.pages]
        good2 = sum(1 for t in alt if len(t) > 200 and garble_ratio(t) < GARBLE_LIMIT)
        if good2 > good:
            return alt, "pdfplumber"
    except Exception:
        pass
    return pages, method


def chunk_pages(pages: list[str], key: str) -> list[dict]:
    """按页切块，**保留页码**以便引用可溯源。"""
    out = []
    for i, txt in enumerate(pages, 1):
        t = re.sub(r"[ \t]+", " ", txt).strip()
        if len(t) < 120:
            continue
        g = garble_ratio(t)
        if g >= GARBLE_LIMIT:
            continue                      # 低质量页直接不入索引，不污染检索
        if looks_like_references(t):
            continue                      # 参考文献页不入索引
        if len(t) <= CHUNK_CHARS:
            out.append({"key": key, "page": i, "text": t})
            continue
        start = 0
        while start < len(t):
            piece = t[start:start + CHUNK_CHARS]
            if len(piece) >= 120:
                out.append({"key": key, "page": i, "text": piece})
            start += CHUNK_CHARS - CHUNK_OVERLAP
    return out


# ---------------------------------------------------------------- 索引
def cmd_index(limit: int | None = None) -> int:
    if not PDF_MAP.exists():
        print("✗ 缺少 pdf_map.json，请先运行 zotero_bridge.py")
        return 1
    pmap = json.loads(PDF_MAP.read_text(encoding="utf-8"))["map"]
    CACHE.mkdir(parents=True, exist_ok=True)
    keys = sorted(pmap.keys())
    if limit:
        keys = keys[:limit]

    done = skip = fail = 0
    chunks_total = 0
    t0 = time.time()
    with CORPUS.open("w", encoding="utf-8") as corpus:
        # 已有缓存的重建 corpus
        for k in keys:
            cf = CACHE / f"{k}.json"
            if cf.exists():
                rec = json.loads(cf.read_text(encoding="utf-8"))
                for c in rec.get("chunks", []):
                    corpus.write(json.dumps(c, ensure_ascii=False) + "\n")
                chunks_total += len(rec.get("chunks", []))
                skip += 1
                continue
            pdf = Path(pmap[k][0])
            if not pdf.exists():
                fail += 1
                continue
            pages, method = extract_pdf(pdf)
            chunks = chunk_pages(pages, k)
            rec = {"key": k, "file": str(pdf), "method": method,
                   "pages": len(pages), "chunks": chunks,
                   "indexed": datetime.now().isoformat()}
            cf.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
            for c in chunks:
                corpus.write(json.dumps(c, ensure_ascii=False) + "\n")
            chunks_total += len(chunks)
            done += 1
            if done % 20 == 0:
                el = time.time() - t0
                print(f"  已索引 {done} 篇（{chunks_total} 块，{el:.0f}s）", flush=True)
    print(f"索引完成: 新解析 {done} · 用缓存 {skip} · 失败 {fail} · 片段 {chunks_total} · "
          f"耗时 {time.time()-t0:.0f}s")
    print(f"语料 -> {CORPUS}  ({CORPUS.stat().st_size/1024/1024:.1f} MB)")
    return 0


# ---------------------------------------------------------------- 检索
def tokenize(s: str) -> list[str]:
    """英文按词，中文按 2-gram（不引入分词依赖）。"""
    s = s.lower()
    words = re.findall(r"[a-z][a-z0-9\-]{1,}", s)
    cjk = re.findall(r"[\u4e00-\u9fff]", s)
    bigrams = ["".join(cjk[i:i + 2]) for i in range(len(cjk) - 1)]
    nums = re.findall(r"\b\d{4}\b", s)
    return words + bigrams + nums


class BM25:
    def __init__(self, chunks: list[dict], k1=1.5, b=0.75):
        self.chunks = chunks
        self.k1, self.b = k1, b
        self.docs = [tokenize(c["text"]) for c in chunks]
        self.tf = [Counter(d) for d in self.docs]
        self.len = [len(d) for d in self.docs]
        self.avg = sum(self.len) / max(len(self.len), 1)
        df = Counter()
        for d in self.docs:
            df.update(set(d))
        n = max(len(self.docs), 1)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}

    def search(self, query: str, k: int = 8) -> list[tuple[float, dict]]:
        q = tokenize(query)
        scores = []
        for i, tf in enumerate(self.tf):
            sc = 0.0
            for t in q:
                if t not in tf:
                    continue
                f = tf[t]
                sc += self.idf.get(t, 0.0) * (f * (self.k1 + 1)) / (
                    f + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg))
            if sc > 0:
                scores.append((sc, self.chunks[i]))
        scores.sort(key=lambda x: -x[0])
        return scores[:k]


def load_bm25() -> BM25 | None:
    if not CORPUS.exists():
        print("✗ 尚无索引，请先运行: python paper_reader.py index")
        return None
    chunks = []
    with CORPUS.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    if not chunks:
        print("✗ 索引为空")
        return None
    return BM25(chunks)


# ---------------------------------------------------------------- 问答 + 引用校验
PROMPT = """你是严谨的科研助手。仅依据下面提供的论文片段回答问题；不要使用片段之外的知识。

要求：
1. 每个论断后面用 [citationKey p.页码] 标注来源，例如 [smith2024 p.3]。
2. 只能引用下面出现过的 citationKey 与页码。**不得编造引用**。
3. 若片段不足以回答，直接说"所给片段无法回答"，不要猜测。
4. 用中文回答，简洁，最后附"依据"清单。

问题：{q}

论文片段：
{ctx}
"""


CITE_RE = re.compile(r"\[([A-Za-z0-9_\-\.]+)\s+p\.?\s*(\d+)\]")


def strip_hallucinated_citations(answer: str, hits: list[tuple[float, dict]]) -> tuple[str, list[str], list[str]]:
    """**程序化删除**不在检索结果里的引用 —— 本引擎最关键的防编造机制。

    依据（2026-09-19 源码核查）:
      * GPT-4o 的引用有 78%~90% 是编造的（OpenScholar 论文 Table 3）；OpenScholar-8B 为 0.0%。
        说明"在提示词里要求不要编造"**不生效**，必须结构性解决。
      * PaperQA2 的做法: 有效 key 是**闭集**，生成后计算 set(emit) - set(valid)，
        对差集里的 key 直接 .replace(key, "") 抹掉；参考文献表**只由幸存者**构建。
        本函数照此实现。
      * STORM 只做序号完整性、GPT Researcher 完全不做，两者都不删。

    返回 (清洗后的回答, 被抹掉的引用列表, 保留的引用列表)
    """
    valid_keys = {h[1]["key"] for h in hits}
    valid_pairs = {(h[1]["key"], h[1]["page"]) for h in hits}
    stripped, kept = [], []
    for ck, pg in CITE_RE.findall(answer):
        if ck not in valid_keys or (ck, int(pg)) not in valid_pairs:
            stripped.append(f"{ck} p.{pg}")
    clean = answer
    for token in stripped:
        ck, _, pg = token.rpartition(" p.")
        # 抹掉形如 [ck p.N] 的整段；同时容忍空格差异
        clean = re.sub(r"\[\s*" + re.escape(ck) + r"\s+p\.?\s*" + re.escape(pg) + r"\s*\]",
                       "", clean)
    kept = [f"{ck} p.{pg}" for ck, pg in CITE_RE.findall(clean)]
    return clean, stripped, kept


def verify_citations(answer: str, hits: list[tuple[float, dict]]) -> dict:
    """逐条校验回答里的引用，并按语种决定是否做词面支撑检查。

    首版缺陷（实测）: 用"引用所在句子的词元"与"英文原文"做重叠，中文回答永远是 0.00，
    全部被判"支撑较弱" —— 那是**跨语言伪失败**，不是真的没支撑。
    现修正: 只在回答与原文**同文字系统**时才做词面校验；跨语言时明确标注"未做词面校验"，
    不把它算作失败（结构性校验——key 与页码是否真的在检索结果里——仍然照做）。
    """
    allowed_keys = {h[1]["key"] for h in hits}
    allowed_pairs = {(h[1]["key"], h[1]["page"]) for h in hits}
    page_text = {(h[1]["key"], h[1]["page"]): h[1]["text"] for h in hits}

    has_cjk = bool(re.search(r"[\u4e00-\u9fff]", answer))
    cites = CITE_RE.findall(answer)
    ok, unknown_key, unknown_page, weak, skipped = [], [], [], [], []
    lines = answer.splitlines()
    for ck, pg in cites:
        p = int(pg)
        if ck not in allowed_keys:
            unknown_key.append(f"{ck} p.{p}")
            continue
        if (ck, p) not in allowed_pairs:
            unknown_page.append(f"{ck} p.{p}")
            continue
        src_raw = page_text[(ck, p)]
        src_cjk = bool(re.search(r"[\u4e00-\u9fff]", src_raw))
        if src_cjk != has_cjk:
            skipped.append(f"{ck} p.{p}")
            ok.append(f"{ck} p.{p}")
            continue
        sent = next((l for l in lines if ck in l and f"p.{p}" in l), "")
        toks = set(tokenize(sent))
        src = set(tokenize(src_raw))
        overlap = len(toks & src) / max(len(toks), 1)
        if overlap < 0.12:
            weak.append(f"{ck} p.{p} (重叠 {overlap:.2f})")
        else:
            ok.append(f"{ck} p.{p}")
    return {"ok": ok, "unknown_key": unknown_key, "unknown_page": unknown_page,
            "weak_support": weak, "cross_lingual_skipped": skipped, "total": len(cites)}


def expand_query(q: str) -> str:
    """中文提问 -> 英文检索词。

    问题（实测）: 库里 268 篇 PDF 基本是英文，而用户会用中文提问。
    中文经 CJK 2-gram 切词后与英文正文零重叠，BM25 直接返回"未检索到相关片段"。
    最省的办法是用一次小 LLM 调用把问题转成英文检索词（比引入多语种 embedding 轻得多）。
    """
    if not re.search(r"[\u4e00-\u9fff]", q):
        return q
    try:
        sys.path.insert(0, str(SCRIPTS))
        import llm_client  # noqa: PLC0415
        en = llm_client.call(
            "Translate the following research question into a short English search query. "
            "Output ONLY the query terms, no explanation, no quotes.\n\n" + q,
            max_tokens=120, timeout=45, retries=1)
        if en:
            en = en.strip().splitlines()[0]
            print(f"  [查询翻译] {en}")
            return f"{q} {en}"
    except Exception as e:
        print(f"  [查询翻译失败] {type(e).__name__}: {e}")
    return q


ABSTAIN_SCORE = 6.0      # 检索最高分低于此值 -> 直接弃答，不调 LLM（PaperQA2 模式 2）
NOTE_DIR = VAULT / "20_Processing" / "22_Audit" / "paper_notes"


def write_note(q: str, answer: str, hits: list[tuple[float, dict]],
               v: dict, certain: bool) -> Path:
    """把问答落成 Obsidian 笔记（模式 8：markdown + YAML frontmatter + Pandoc [@citekey]）。

    依据 llm-for-zotero（3.1k★，最贴近本场景的项目）：笔记用 YAML frontmatter +
    Pandoc 的 [@citekey] 语法，Obsidian 的 Zotero Integration 才能直接消费。
    """
    NOTE_DIR.mkdir(parents=True, exist_ok=True)
    import hashlib
    slug = re.sub(r"[^\w\u4e00-\u9fff]+", "-", q)[:40].strip("-")
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = NOTE_DIR / f"{ts}_{slug}.md"

    cites = sorted({f"{c['key']}" for _, c in hits})
    fm = [
        "---",
        f"title: \"{q[:80].replace(chr(34), chr(39))}\"",
        f"created: {datetime.now():%Y-%m-%d %H:%M}",
        "type: paper-qa",
        f"certain: {str(certain).lower()}",
        f"citations_verified: {len(v['ok'])}",
        f"citations_stripped: {len(v.get('stripped', []))}",
        "sources:",
    ]
    for c in cites:
        fm.append(f"  - \"[[{c}]]\"")
    fm += ["citekeys:", *[f"  - \"@{c}\"" for c in cites], "---", ""]

    body = [f"# {q}", "", answer.strip(), "", "## 依据（页面级）", ""]
    for sc, c in hits:
        body.append(f"- `{c['key']}` p.{c['page']} (BM25 {sc:.2f})")
    if v.get("stripped"):
        body += ["", "## 已剔除的无效引用（程序化删除）", "",
                 "> 这些引用不在本轮检索结果里，按 PaperQA2 的做法直接抹除，"
                 "而不是留在文中误导读者。", ""]
        for s in v["stripped"]:
            body.append(f"- ~~{s}~~")
    body += ["", f"*由 `paper_reader.py` 生成 · {datetime.now():%Y-%m-%d %H:%M}*"]
    path.write_text("\n".join(fm + body), encoding="utf-8")
    return path


def cmd_ask(q: str, k: int, no_llm: bool = False, note: bool = False) -> int:
    bm = load_bm25()
    if bm is None:
        return 1
    hits = bm.search(expand_query(q), k)

    # --- 模式 2: 确定性弃答（不调 LLM）---
    # PaperQA2 在证据为空/不足时**不调用模型**，直接返回"I cannot answer"。
    # 依据: 好的系统在无证据时约 98% 的时间会弃答（ContraCrow 实测）。
    if not hits or hits[0][0] < ABSTAIN_SCORE:
        print(f"检索证据不足（最高分 {hits[0][0] if hits else 0:.2f} < 阈值 {ABSTAIN_SCORE}）。")
        print("I cannot answer：所给材料不足以支撑回答。（未调用 LLM）")
        return 4

    print(f"=== 检索到 {len(hits)} 个片段 ===")
    for sc, c in hits:
        print(f"  [{sc:6.2f}] {c['key']} p.{c['page']}  {c['text'][:70].replace(chr(10),' ')}...")

    if no_llm:
        return 0

    ctx = "\n\n".join(
        f"--- [{c['key']} p.{c['page']}] ---\n{c['text'][:1600]}" for _, c in hits)
    prompt = PROMPT.format(q=q, ctx=ctx)

    sys.path.insert(0, str(SCRIPTS))
    import llm_client  # noqa: PLC0415
    print("\n=== LLM 生成中 ===")
    ans = llm_client.call(prompt, max_tokens=1800, timeout=120)
    if not ans:
        print("✗ LLM 调用失败")
        return 2

    # --- 模式 1: 程序化抹除无效引用（本引擎最关键的防编造机制）---
    clean, stripped, kept = strip_hallucinated_citations(ans, hits)

    print("\n" + "=" * 70)
    print(clean)
    print("=" * 70)

    v = verify_citations(clean, hits)
    v["stripped"] = stripped

    certain = bool(v["ok"]) and not v["unknown_key"] and not v["unknown_page"] \
        and not v["weak_support"] and not stripped

    print(f"\n=== 引用校验（生成 {len(CITE_RE.findall(ans))} 条 → 保留 {len(kept)} 条）===")
    print(f"  确定性(certain)        : {'是' if certain else '否'}")
    print(f"  ✓ 通过                 : {len(v['ok'])}")
    if stripped:
        print(f"  ✗ 编造/越界已**抹除**   : {stripped}")
    if v["cross_lingual_skipped"]:
        print(f"  – 跨语言未做词面校验   : {v['cross_lingual_skipped']}")
    if v["weak_support"]:
        print(f"  ⚠ 词面支撑较弱         : {v['weak_support']}")
    if not v["total"]:
        print("  ⚠ 回答里没有任何引用 —— 无法溯源，按不可采信处理")

    if note:
        p = write_note(q, clean, hits, v, certain)
        print(f"\n笔记 -> {p}")
    return 0 if certain else 3


def cmd_status() -> int:
    idx = sorted(CACHE.glob("*.json")) if CACHE.exists() else []
    print(f"已索引论文: {len(idx)}")
    if CORPUS.exists():
        print(f"语料文件: {CORPUS.stat().st_size/1024/1024:.1f} MB")
    if LIBRARY.exists():
        s = json.loads(LIBRARY.read_text(encoding="utf-8"))["stats"]
        print(f"Zotero 可引用 {s['total_citable']} · 有 PDF {s['with_pdf']}")
    lowq = 0
    for f in idx[:400]:
        r = json.loads(f.read_text(encoding="utf-8"))
        if r.get("chunks") and r.get("pages") and len(r["chunks"]) < r["pages"] * 0.3:
            lowq += 1
    print(f"提取质量偏低(片段数 < 页数*0.3)的论文: {lowq}")
    return 0


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    cmd = a[0]
    kw = {}
    for i, x in enumerate(a):
        if x == "-k" and i + 1 < len(a):
            kw["k"] = int(a[i + 1])
    if cmd == "index":
        lim = None
        if "--limit" in a:
            lim = int(a[a.index("--limit") + 1])
        return cmd_index(lim)
    if cmd == "search":
        q = next((x for x in a[1:] if not x.startswith("-") and not x.isdigit()), "")
        return cmd_ask(q, kw.get("k", 8), no_llm=True)
    if cmd == "ask":
        q = next((x for x in a[1:] if not x.startswith("-") and not x.isdigit()), "")
        return cmd_ask(q, kw.get("k", 8), note="--note" in a)
    if cmd == "status":
        return cmd_status()
    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
