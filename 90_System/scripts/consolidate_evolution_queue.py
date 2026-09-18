#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consolidate_evolution_queue.py — 一次性整理 99_Meta/evolution_queue.json 的历史堆积。

问题（2026-09-18 实测）:
    evolution_engine_v2.update_evolution_queue() 旧实现用 f"EV-{TODAY}-NNN" 作 id，
    而 id 每天不同，于是 `if item["id"] not in existing_ids` 永远成立 ——
    每天追加一条新的 "Git hygiene: N uncommitted changes"。
    实测 2026-07-19 起累积 51 条 git_hygiene + 52 条 pipeline_fix，
    再由 task_recommender 固定取最旧 10 条反复上报，形成"同一批建议永远重播"。

本脚本做一次性的**可逆**整理：
    * 按 type 分组 pending 条目；
    * 每组保留**最早一条**为唯一 open 条目，并把该组的观测合并进去
      （occurrences=组内条数、observed_values=历史观测值列表、first/last_seen）；
    * 其余条目标记为 status="superseded"，附 superseded_by 指向保留者。
    **不删除任何条目**，只改 status —— 需要时可直接改回 pending。

用法:
    python consolidate_evolution_queue.py --dry-run
    python consolidate_evolution_queue.py --apply
"""
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

VAULT = Path(r"D:\Obsidian\vault")
QUEUE = VAULT / "99_Meta" / "evolution_queue.json"
BACKUP_DIR = VAULT / "99_Meta" / "_backups"


def load():
    return json.loads(QUEUE.read_text(encoding="utf-8"))


def consolidate(queue: dict, dry: bool) -> dict:
    items = queue.get("items", [])
    groups: dict[str, list[dict]] = {}
    for it in items:
        if not isinstance(it, dict):
            continue
        if str(it.get("status", "pending")).lower() != "pending":
            continue
        groups.setdefault(str(it.get("type") or "general"), []).append(it)

    stats = {}
    for etype, group in groups.items():
        # 最早的作为唯一保留者（用 id 里的日期或 first_seen 排序）
        group.sort(key=lambda i: str(i.get("first_seen") or i.get("id") or ""))
        keeper, rest = group[0], group[1:]
        stats[etype] = {"kept": keeper.get("id"), "superseded": len(rest)}

        # 把组内观测合并进保留者
        vals = []
        for g in group:
            t = str(g.get("title", ""))
            if ":" in t:
                seg = t.split(":")[-1].strip()
                if seg:
                    vals.append(seg)
        keeper["occurrences"] = len(group)
        keeper["observed_values"] = vals
        keeper["first_seen"] = keeper.get("first_seen") or keeper.get("id", "")[:14]
        keeper["last_seen"] = datetime.now().isoformat()
        keeper["consolidated_at"] = datetime.now().isoformat()
        keeper["consolidated_note"] = (
            f"由 consolidate_evolution_queue.py 合并 {len(group)} 条同类历史堆积"
            f"（原因为旧实现每天生成新 id 导致去重失效）")

        for g in rest:
            g["status"] = "superseded"
            g["superseded_by"] = keeper.get("id")
            g["superseded_at"] = datetime.now().isoformat()

    queue["last_updated"] = datetime.now().isoformat()
    queue["consolidated"] = {
        "at": datetime.now().isoformat(),
        "by": "consolidate_evolution_queue.py",
        "groups": stats,
    }
    return queue


def main():
    dry = "--apply" not in sys.argv
    if not QUEUE.exists():
        print(f"[skip] 不存在 {QUEUE}")
        return 1

    queue = load()
    before = {s: sum(1 for i in queue.get("items", [])
                     if str(i.get("status", "pending")).lower() == s)
              for s in ("pending", "superseded", "resolved")}
    print(f"整理前: {before}  总条目 {len(queue.get('items', []))}")

    if not dry:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        bk = BACKUP_DIR / f"evolution_queue.{datetime.now():%Y%m%d_%H%M%S}.json"
        shutil.copy2(QUEUE, bk)
        print(f"已备份 -> {bk}")

    queue = consolidate(queue, dry)

    after = {s: sum(1 for i in queue.get("items", [])
                    if str(i.get("status", "pending")).lower() == s)
             for s in ("pending", "superseded", "resolved")}
    print(f"整理后: {after}  总条目 {len(queue.get('items', []))}")
    for et, st in (queue.get("consolidated", {}) or {}).get("groups", {}).items():
        print(f"   {et}: 保留 {st['kept']}，置为 superseded {st['superseded']} 条")

    if dry:
        print("\n[dry-run] 未写入。加 --apply 执行。")
    else:
        QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n已写入 {QUEUE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
