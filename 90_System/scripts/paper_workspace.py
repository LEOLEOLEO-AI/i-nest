#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""paper_workspace.py — 论文工作区：新建脚手架 + 版本体检 + 引用闸门。

回答"写论文的流程配置上了吗":
    已配置的部分:
      * Zotero 作为引用唯一真相源（540 条 / 100% Better BibTeX citationKey）
      * 50_Output/References/zotero.bib（BBT 实时导出，501 KB）—— LaTeX 直接 \\cite{}
      * 引用白名单 papers.yaml（544 条）—— 门禁会拦下未登记引用
      * 门禁扫描 50_Output/51_Papers/**（含 \\cite{}、DOI、arXiv id 与数字证据标签）
    缺的部分（本脚本补上）:
      * 新建论文没有统一脚手架 —— 每次靠手工拼目录与 .tex
      * 论文的版本蔓延没人管（实测 A1_CST 一篇就有 9 个 .tex 变体:
        A1_CST / _ASCII / _BASELINE_FIX / _BUILD / _clean / _clean_FIXED /
        _clean_FIXED2 / _clean_NOFONTSPEC / _CLEAN_v1）
      * 新建后没有自动接上 zotero.bib 与门禁

用法:
    python paper_workspace.py new --id P3_MyTopic --title "题目" [--venue "目标期刊"]
    python paper_workspace.py lint            # 论文版本蔓延体检
    python paper_workspace.py check --id X    # 对某篇跑门禁与结构检查
    python paper_workspace.py list            # 已登记论文
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

VAULT = Path(r"D:\Obsidian\vault")
PAPERS = VAULT / "50_Output" / "51_Papers"
REGISTRY = VAULT / "90_System" / "research_evolve" / "state" / "paper_registry.json"
ZOTERO_BIB = VAULT / "50_Output" / "References" / "zotero.bib"
PLATFORM = VAULT / "90_System"

SECTIONS = ["Abstract", "Introduction", "Related Work", "Method",
            "Experiments", "Results", "Discussion", "Conclusion", "Limitations"]

TEX_MAIN = r"""% !TEX program = xelatex
% ============================================================
% {title}
% 工作区 {pid} · 建立于 {date}
% 引用源: ../References/zotero.bib（由 zotero_bridge.py 从 Zotero 导出，勿手改）
%
% 铁律（AGENTS.md §0.1 / 门禁会检查）:
%   1. 正文引用只能来自 papers.yaml 白名单里的文献（未登记会被门禁拦下）
%   2. 任何性能数字必须带 [实测]/[仿真]/[引用]/[推导]/[假设]/[待测] 标签
%   3. 含公式的理论主张须经 manuscript-math-verify 或显式标 [待测]
% ============================================================
\documentclass[11pt]{{article}}
\usepackage{{amsmath,amssymb,graphicx,booktabs,hyperref}}
\usepackage[numbers]{{natbib}}

\title{{{title}}}
\author{{}}
\date{{\today}}

\begin{{document}}
\maketitle

\begin{{abstract}}
% 一句话：问题 / 方法 / 关键结果（数字必须带证据标签）/ 意义
\end{{abstract}}

\section{{Introduction}}
\section{{Related Work}}
\section{{Method}}
\section{{Experiments}}
% 实验配置必须可复现：数据来源、参数、随机种子、基线
\section{{Results}}
% 每个数字后标 [实测]/[仿真]/[引用]/[推导]/[待测]
\section{{Discussion}}
\section{{Conclusion}}
\section{{Limitations}}

\bibliographystyle{{plainnat}}
\bibliography{{../References/zotero}}

\end{{document}}
"""

README = """# {title}

- 工作区 ID: `{pid}`
- 建立: {date}
- 目标期刊/会议: {venue}

## 目录

```
{pid}/
├── main.tex            正文（唯一规范稿；历史版本交给 git，不要再建 _v2/_FIXED）
├── notes.md            论证笔记与待办
├── figures/            图（源文件 + 导出）
├── data/               结果数据（大文件走 .gitignore，不入库）
└── REVIEW.md           自审清单（提交前逐条过）
```

## 引用怎么走

1. Zotero 里确认条目（citationKey 由 Better BibTeX 生成）
2. 跑 `python 90_System/scripts/zotero_bridge.py --seed-papers` 同步书目与白名单
3. 正文用 `\\cite{{citationKey}}`；未在白名单的引用会被门禁拦下

## 三个拍板点（AI 不做）

框架定稿 / 结果判读 / 最终定稿 —— 见 AGENTS.md。

## 提交前

```bash
python 90_System/scripts/paper_workspace.py check --id {pid}
```
"""

REVIEW = """# 自审清单 · {title}

## 证据与数字
- [ ] 每个性能数字都带 `[实测]/[仿真]/[引用]/[推导]/[假设]/[待测]`
- [ ] 仿真数字没有被写成实测
- [ ] 引用全部来自 papers.yaml 白名单（门禁已自动检查）
- [ ] 关键结论配了 `V-*` 验证任务与验收标准

## 可复现
- [ ] 数据来源、参数、随机种子、基线都写清
- [ ] 代码留了 run_manifest（种子/配置哈希/依赖版本）
- [ ] 大文件不入库（走 .gitignore）

## 结构
- [ ] Abstract/Intro/Related/Method/Exp/Results/Discussion/Conclusion/Limitations 齐全
- [ ] 只有一份规范稿（没有 _v2/_FIXED/_clean 之类并行变体）

## 数学（若有）
- [ ] 符号定义完整、假设与边界条件写明
- [ ] 经 `manuscript-math-verify` 或标 `[待测]`
"""


def load_reg() -> dict:
    if REGISTRY.exists():
        try:
            return json.loads(REGISTRY.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"schema": "paper-registry-v1", "papers": {}}


def save_reg(r: dict) -> None:
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    r["updated"] = datetime.now().isoformat()
    REGISTRY.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_new(pid: str, title: str, venue: str = "待定") -> int:
    d = PAPERS / pid
    if d.exists():
        print(f"✗ 已存在 {d}，不覆盖")
        return 1
    (d / "figures").mkdir(parents=True, exist_ok=True)
    (d / "data").mkdir(parents=True, exist_ok=True)
    (d / "main.tex").write_text(
        TEX_MAIN.format(title=title, pid=pid, date=f"{datetime.now():%Y-%m-%d}"),
        encoding="utf-8")
    (d / "README.md").write_text(
        README.format(title=title, pid=pid, date=f"{datetime.now():%Y-%m-%d}", venue=venue),
        encoding="utf-8")
    (d / "REVIEW.md").write_text(REVIEW.format(title=title), encoding="utf-8")
    (d / "notes.md").write_text(f"# {title} · 论证笔记\n\n## 待办\n- [ ] \n", encoding="utf-8")

    reg = load_reg()
    reg["papers"][pid] = {"id": pid, "title": title, "venue": venue,
                          "dir": f"50_Output/51_Papers/{pid}",
                          "created": datetime.now().isoformat(),
                          "canonical": f"50_Output/51_Papers/{pid}/main.tex",
                          "bib": "50_Output/References/zotero.bib",
                          "history": [{"at": datetime.now().isoformat(), "note": "新建工作区"}]}
    save_reg(reg)

    print(f"✓ 已建论文工作区 {d}")
    print(f"  正文   : {d/'main.tex'}（唯一规范稿）")
    print(f"  引用   : main.tex 已指向 ../References/zotero（zotero_bridge.py 产出）")
    print(f"  自审   : {d/'REVIEW.md'}")
    print(f"  登记   : {REGISTRY}")
    print(f"  下一步 : 跑 zotero_bridge.py --seed-papers 同步书目与白名单")
    if not ZOTERO_BIB.exists():
        print("  ⚠ 尚未生成 zotero.bib，请先运行 scripts/zotero_bridge.py")
    return 0


VARIANT_RE = re.compile(
    r"(_clean|_FIXED|_fixed|_ASCII|_BUILD|_build|_NOFONTSPEC|_v\d+|-v\d+|_\d+|_bak|_old|_new|_final)+$")


def cmd_lint() -> int:
    """论文版本蔓延体检 —— 对应实测 A1_CST 一篇 9 个变体。"""
    groups: dict[str, list[str]] = {}
    for p in PAPERS.rglob("*.tex"):
        base = VARIANT_RE.sub("", p.stem)
        if base != p.stem:
            groups.setdefault(f"{p.parent.name}/{base}", []).append(p.name)
    print("=== 论文 LaTeX 版本蔓延体检 ===")
    if not groups:
        print("  未发现并行变体")
        return 0
    tot = sum(len(v) for v in groups.values())
    print(f"  发现 {len(groups)} 组、共 {tot} 个变体文件：")
    for k, v in sorted(groups.items(), key=lambda x: -len(x[1])):
        print(f"    [{len(v):>2} 个] {k}")
        for f in sorted(v)[:5]:
            print(f"             {f}")
        if len(v) > 5:
            print(f"             … 其余 {len(v)-5} 个")
    print("\n  建议：只保留一份规范稿（如 main.tex），其余交给 git 历史。")
    print("        新稿用 `paper_workspace.py new` 建工作区，不要再手工复制 _v2/_FIXED。")
    return 0


def cmd_check(pid: str) -> int:
    reg = load_reg()
    rec = reg["papers"].get(pid)
    d = PAPERS / pid
    print(f"=== 检查 {pid} ===")
    if not d.exists():
        print(f"✗ 目录不存在 {d}")
        return 1
    texs = sorted(d.rglob("*.tex"))
    print(f"  .tex 文件: {len(texs)} 个 {[t.name for t in texs][:5]}")
    if len(texs) > 2:
        print(f"  ⚠ 变体偏多（>2），建议收敛到 main.tex")
    # 结构检查
    main = d / "main.tex"
    if main.exists():
        t = main.read_text(encoding="utf-8", errors="ignore")
        missing = [s for s in SECTIONS if f"\\section{{{s}}}" not in t
                   and f"\\begin{{abstract}}" not in t[:2000] or
                   (s != "Abstract" and f"\\section{{{s}}}" not in t)]
        if missing:
            print(f"  ⚠ 缺章节: {missing}")
        else:
            print("  ✓ 章节齐全")
        print(f"  ✓ 引用源指向 zotero: {'zotero' in t}")
    # 门禁
    sys.path.insert(0, str(PLATFORM))
    from research_evolve import gates  # noqa: PLC0415
    papers = gates.load_papers()
    viol = []
    for t in texs:
        txt = t.read_text(encoding="utf-8", errors="ignore")
        for v in gates.check_citations(txt, papers):
            v["file"] = t.relative_to(VAULT).as_posix(); viol.append(v)
        for v in gates.check_evidence_labels(txt):
            v["file"] = t.relative_to(VAULT).as_posix(); viol.append(v)
    print(f"  门禁: {len(viol)} 项")
    for v in viol[:8]:
        print(f"    [{v['type']}] {v.get('value') or v.get('excerpt','')[:60]}")
    if rec:
        print(f"  登记: {rec.get('title')} · 目标 {rec.get('venue')}")
    else:
        print(f"  ⚠ 未登记进 paper_registry.json")
    return 0 if not viol else 2


def cmd_list() -> int:
    reg = load_reg()
    ps = reg.get("papers", {})
    print(f"=== 已登记论文 {len(ps)} 篇 ===")
    for k, v in ps.items():
        print(f"  {k}  {v.get('title','')[:52]}")
        print(f"      规范稿: {v.get('canonical')}")
        print(f"      目标: {v.get('venue')}  建立: {str(v.get('created'))[:10]}")
    return 0


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__); return 1
    cmd = a[0]
    if cmd == "new":
        pid = a[a.index("--id") + 1] if "--id" in a else ""
        title = a[a.index("--title") + 1] if "--title" in a else ""
        venue = a[a.index("--venue") + 1] if "--venue" in a else "待定"
        if not pid or not title:
            print("用法: new --id <ID> --title <标题> [--venue <目标>]")
            return 1
        return cmd_new(pid, title, venue)
    if cmd == "lint":
        return cmd_lint()
    if cmd == "check":
        return cmd_check(a[a.index("--id") + 1] if "--id" in a else "")
    if cmd == "list":
        return cmd_list()
    print(__doc__); return 1


if __name__ == "__main__":
    raise SystemExit(main())
