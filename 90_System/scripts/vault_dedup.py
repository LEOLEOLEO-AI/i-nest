#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vault_dedup.py — 清理 vault 内**内容完全相同**的 .md 冗余副本。

范围严格限定: 只处理 size+sha1 完全一致的 .md 文件组。
内容不同的一律不动（哪怕同名）——"同名不同内容"往往是不同稿次，删错代价高。

保留规则（按 AGENTS.md 1.4 的知识单向流动方向定优先级，序号小者优先保留）:
    30_TCC/ 40_iNEST/ 50_Output/   研究实体，最高优先
    20_Processing/                 加工层（arxiv-auto 等管线的产出地）
    10_Knowledge/ 60_MOC/          知识层 / 索引层
    00_Inbox/                      入口层，**副本优先删这里**（消费完即冗余）
    70_Dashboard/ 90_System/ 99_Meta/ state/ logs/
    raw/ wiki/ 80_Archive/         其它

已知典型情形: 21:00 同步把 20_Processing/20_KnowledgeBase/arxiv-auto/ 的日报
"提取到" 00_Inbox/03_Genspark/ —— 这是设计使然（便于人看），但产生逐字节相同的副本。

用法:
    python vault_dedup.py              # dry-run，只报告
    python vault_dedup.py --apply      # 删除冗余副本（保留优先目录中的那份）
"""
import hashlib
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

VAULT = Path(r"D:\Obsidian\vault")
MANIFEST_DIR = Path(r"D:\Obsidian\_backups\vault_dedup_20260919")

PRIORITY = [
    "30_TCC/", "40_iNEST/", "50_Output/",
    "20_Processing/",
    "10_Knowledge/", "60_MOC/",
    "00_Inbox/",
    "70_Dashboard/", "90_System/", "99_Meta/", "state/", "logs/",
    "raw/", "wiki/", "80_Archive/",
]
SKIP_PREFIX = (".git/", ".obsidian/", ".smart-env/", ".claudian", ".workbuddy/",
               ".neural_", ".openclaw/", ".tasks/", "_external/")


def rank(rel: str) -> int:
    for i, p in enumerate(PRIORITY):
        if rel.startswith(p):
            return i
    return len(PRIORITY)


def main() -> int:
    apply = "--apply" in sys.argv

    by_hash: dict[str, list[str]] = defaultdict(list)
    n = 0
    for p in VAULT.rglob("*.md"):
        rel = p.relative_to(VAULT).as_posix()
        if rel.startswith(SKIP_PREFIX):
            continue
        try:
            h = hashlib.sha1(p.read_bytes()).hexdigest()
        except Exception:
            continue
        by_hash[h].append(rel)
        n += 1

    groups = {h: v for h, v in by_hash.items() if len(v) > 1}
    to_delete: list[dict] = []
    deferred: list[dict] = []
    for h, files in groups.items():
        ordered = sorted(files, key=lambda r: (rank(r), len(r), r))
        keep, drop = ordered[0], ordered[1:]
        for d in drop:
            try:
                sz = (VAULT / d).stat().st_size
            except Exception:
                sz = 0
            item = {"path": d, "kept": keep, "sha1": h, "bytes": sz}

            # 判据收紧（实跑后修正）：
            #  1) 只删 **00_Inbox 里的副本**（入口层，消费完即冗余；保留者不在 Inbox）
            #  2) 以及 0 字节的空文件（多余的空壳，无内容价值）
            # 其余一律**只报告不删**。原因: 实测发现有两类"相同但不是冗余"——
            #   * 60_MOC/02_DeepSeek_Insights.md 与 _2026-09-18.md 是"当前 + 按日归档"，
            #     内容此刻相同，但**删掉带日期的会丢历史**，下一轮 canonical 就变了；
            #   * 同名不同内容的多是不同稿次。
            # 精确率优先于覆盖率：宁可少删，不可误删。
            is_inbox_copy = d.startswith("00_Inbox/") and not keep.startswith("00_Inbox/")
            is_empty = sz == 0
            if is_inbox_copy or is_empty:
                to_delete.append(item)
            else:
                item["why_deferred"] = ("按日归档 vs 当前版本，删了会丢历史"
                                        if not is_empty else "")
                deferred.append(item)

    waste = sum(d["bytes"] for d in to_delete)
    print(f"扫描 .md 文件 {n} 个")
    print(f"内容完全相同组: {len(groups)} 组")
    print(f"  → 判定为冗余、可删: {len(to_delete)} 个（{waste/1024:.0f} KB）")
    print(f"  → 判定为**非冗余、保留**: {len(deferred)} 个（按日归档/不同稿次等）")
    if deferred:
        print("\n  保留样例（不删，理由）:")
        for d in deferred[:6]:
            print(f"    KEEP {d['path'][:64]}")
            print(f"         （与 {d['kept'][:52]} 相同，但 {d.get('why_deferred','')}）")

    by_dir: dict[str, int] = defaultdict(int)
    for d in to_delete:
        by_dir[d["path"].split("/")[0] + "/" + (d["path"].split("/")[1] if "/" in d["path"] else "")] += 1
    print("\n冗余副本所在目录（前 10）:")
    for k, v in sorted(by_dir.items(), key=lambda x: -x[1])[:10]:
        print(f"  {k:<52} {v}")

    print("\n样例（删 <- 保留）:")
    for d in to_delete[:8]:
        print(f"  DEL {d['path'][:66]}")
        print(f"      KEEP {d['kept'][:62]}")

    if not apply:
        print("\n[dry-run] 未删除。加 --apply 执行（会写清单）。")
        return 0

    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    deleted = failed = 0
    for d in to_delete:
        try:
            (VAULT / d["path"]).unlink()
            deleted += 1
        except Exception as e:
            failed += 1
            print(f"  删除失败 {d['path']}: {e}")
    man = {"generated": datetime.now().isoformat(),
           "rule": "delete only (a) copies under 00_Inbox/ whose kept twin is elsewhere, "
                   "or (b) extra 0-byte files; byte-identical (sha1) .md only",
           "scanned": n, "groups": len(groups), "deleted": deleted,
           "failed": failed, "bytes_freed": waste,
           "deferred_not_deleted": len(deferred), "items": to_delete}
    (MANIFEST_DIR / "MANIFEST.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n已删除 {deleted} 个冗余副本（失败 {failed}）")
    print(f"清单 -> {MANIFEST_DIR/'MANIFEST.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
