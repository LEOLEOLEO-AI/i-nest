# -*- coding: utf-8 -*-
"""research_evolve.registry — 候选注册表 + 决策记忆（selection memory）。

这是当前系统最致命的缺失层。原 self_evolve 每天生成 18 条"建议"、78 张灵感卡、
10 条假说，但没有任何机制记住"这条提过了/这条被否决了/这条已闭环"，
结果是同一批 2026-07 的进化条目连续两个月每天重新出现在
wiki/task_recommendations.md 里，而 closed 数恒为 0。

本模块只做三件事，但每件都必须可靠：
  1. 去重      —— 用规范化标题做键，换写法也命中同一条记忆。
  2. 记账      —— 每条候选只保留一行命运：open / accepted / rejected /
                  deferred / adopted / done / superseded，且带原因与时轮。
  3. 计数      —— 每轮记录 opened / closed / escalated，使
                  "自膨胀空转"（opened>0 且 closed==0）可被程序判定而非靠人看。
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterable

from .common import (
    CLOSED_VERDICTS,
    REGISTRY_FILE,
    VERDICTS,
    days_between,
    dedup_key,
    load_json,
    norm_title,
    save_json,
    today,
)

SCHEMA = "research-evolve-registry-v1"


class Registry:
    """候选与决策的持久记忆。所有写入都走 save()，且是原子替换。"""

    def __init__(self, data: dict | None = None):
        data = data or {}
        self.schema = data.get("schema", SCHEMA)
        self.created = data.get("created", datetime.now().isoformat())
        self.round = int(data.get("round", 0))
        self.candidates: dict = data.get("candidates", {}) or {}
        self.counters = data.get("counters", {"next_id": 1}) or {"next_id": 1}
        self.rounds: list = data.get("rounds", []) or []

    # ------------------------------------------------------------ 生命周期
    @classmethod
    def load(cls) -> "Registry":
        data = load_json(REGISTRY_FILE, default=None)
        if not isinstance(data, dict):
            return cls()
        return cls(data)

    def save(self) -> None:
        save_json(REGISTRY_FILE, {
            "schema": self.schema,
            "created": self.created,
            "updated": datetime.now().isoformat(),
            "round": self.round,
            "counters": self.counters,
            "candidates": self.candidates,
            "rounds": self.rounds[-120:],
        })

    def next_round(self) -> int:
        self.round += 1
        return self.round

    def _new_id(self) -> str:
        n = int(self.counters.get("next_id", 1))
        self.counters["next_id"] = n + 1
        return f"C-{n:05d}"

    # ------------------------------------------------------------ 查询
    def by_id(self, cid: str) -> dict | None:
        for c in self.candidates.values():
            if c.get("id") == cid:
                return c
        return None

    def find_by_title(self, kind: str, title: str) -> dict | None:
        return self.candidates.get(dedup_key(kind, title))

    def open_candidates(self) -> list[dict]:
        return [c for c in self.candidates.values() if c.get("verdict") == "open"]

    def rejected_norms(self) -> set[str]:
        """已被否决/关闭的规范化标题集合——用于识别"换个说法再提一次"。"""
        out = set()
        for c in self.candidates.values():
            if c.get("verdict") in ("rejected", "superseded"):
                n = c.get("norm") or norm_title(c.get("title", ""))
                if n:
                    out.add(n)
        return out

    # ------------------------------------------------------------ 写入
    def upsert(self, cand: dict) -> tuple[str, dict]:
        """登记一条候选。返回 (状态, 记录)。

        状态取值：
          new      —— 首次出现
          recurred —— 已存在且仍 open（seen_count 递增）
          closed   —— 已存在且已关闭（不再复活，仅更新 last_seen）
        """
        kind = cand.get("kind", "idea")
        title = cand.get("title", "").strip()
        key = cand.get("key") or dedup_key(kind, title)
        now = datetime.now().isoformat()

        rec = self.candidates.get(key)
        if rec is None:
            rec = {
                "id": self._new_id(),
                "key": key,
                "kind": kind,
                "title": title,
                "norm": norm_title(title),
                "first_seen": now,
                "last_seen": now,
                "first_round": self.round,
                "last_round": self.round,
                "seen_count": 1,
                "source": cand.get("source", ""),
                "detail": cand.get("detail", ""),
                "evidence": cand.get("evidence", {}),
                "score": None,
                "score_reasons": [],
                "escalated": False,
                "verdict": "open",
                "verdict_reason": "",
                "verdict_by": "",
                "verdict_round": None,
                "verdict_at": "",
                "history": [{"round": self.round, "verdict": "open"}],
            }
            self.candidates[key] = rec
            return "new", rec

        # 已存在：刷新可变量，但**绝不覆盖已有裁决**
        rec["last_seen"] = now
        rec["last_round"] = self.round
        rec["seen_count"] = int(rec.get("seen_count", 1)) + 1
        if cand.get("source"):
            rec["source"] = cand["source"]
        if cand.get("detail"):
            rec["detail"] = cand["detail"]
        if cand.get("evidence"):
            rec["evidence"] = cand["evidence"]
        state = "recurred" if rec.get("verdict") == "open" else "closed"
        return state, rec

    def set_verdict(self, rec: dict, verdict: str, reason: str,
                    by: str = "auto") -> None:
        if verdict not in VERDICTS:
            raise ValueError(f"未知裁决: {verdict}")
        prev = rec.get("verdict")
        if prev == verdict:
            return
        rec["verdict"] = verdict
        rec["verdict_reason"] = reason
        rec["verdict_by"] = by
        rec["verdict_round"] = self.round
        rec["verdict_at"] = datetime.now().isoformat()
        rec.setdefault("history", []).append(
            {"round": self.round, "verdict": verdict, "reason": reason, "by": by})

    # ------------------------------------------------------------ 轮次记账
    def close_round(self, gate_violations: int, note: str = "") -> dict:
        """写入本轮四数。这是"进化"与"空转"的判据来源。"""
        opened = [c for c in self.candidates.values() if c.get("first_round") == self.round]
        closed = [c for c in self.candidates.values()
                  if c.get("verdict_round") == self.round and c.get("verdict") in CLOSED_VERDICTS]
        escalated = [c for c in self.candidates.values()
                     if c.get("verdict") == "open" and c.get("escalated")]
        entry = {
            "round": self.round,
            "date": today(),
            "at": datetime.now().isoformat(),
            "opened": len(opened),
            "closed": len(closed),
            "escalated": len(escalated),
            "open_total": len(self.open_candidates()),
            "gate_violations": int(gate_violations),
            "note": note,
        }
        self.rounds.append(entry)
        return entry

    def stagnation_streak(self) -> int:
        """连续多少轮 opened>0 且 closed==0 —— 即"自膨胀空转"轮数。"""
        streak = 0
        for r in reversed(self.rounds):
            if r.get("opened", 0) > 0 and r.get("closed", 0) == 0:
                streak += 1
            else:
                break
        return streak

    def last_round(self) -> dict | None:
        return self.rounds[-1] if self.rounds else None

    def stats(self) -> dict:
        by_verdict: dict[str, int] = {}
        by_kind: dict[str, int] = {}
        for c in self.candidates.values():
            by_verdict[c.get("verdict", "?")] = by_verdict.get(c.get("verdict", "?"), 0) + 1
            by_kind[c.get("kind", "?")] = by_kind.get(c.get("kind", "?"), 0) + 1
        return {
            "total": len(self.candidates),
            "by_verdict": by_verdict,
            "by_kind": by_kind,
            "open": len(self.open_candidates()),
            "round": self.round,
            "stagnation_streak": self.stagnation_streak(),
        }

    # ------------------------------------------------------------ 年龄升级
    def mark_escalations(self, max_open_days: float) -> list[dict]:
        """把长期未裁决的 open 候选标记为 escalated（升级，不是重新生成）。"""
        out = []
        for c in self.open_candidates():
            age = days_between(c.get("first_seen", ""))
            if age >= max_open_days:
                if not c.get("escalated"):
                    c["escalated"] = True
                    c.setdefault("history", []).append(
                        {"round": self.round, "verdict": "escalate",
                         "reason": f"已挂起 {age:.0f} 天未裁决", "by": "auto"})
                c["age_days"] = round(age, 1)
                out.append(c)
        return out

    def human_queue(self, limit: int) -> list[dict]:
        """呈交用户裁决的队列：升级的优先，其次高分，年龄作次序。"""
        cands = [c for c in self.open_candidates() if c.get("score") is not None]
        cands.sort(key=lambda c: (
            0 if c.get("escalated") else 1,
            -(c.get("score") or 0.0),
            -days_between(c.get("first_seen", "")),
        ))
        return cands[:limit]


def bootstrap_from(data: dict | None) -> Registry:
    """从旧状态迁移（可选）：把已有的 evolution_queue 摘要并入记忆。"""
    reg = Registry.load()
    if not data:
        return reg
    return reg


def summarize_counts(items: Iterable[dict]) -> dict:
    out: dict[str, int] = {}
    for it in items:
        k = it.get("verdict", "?")
        out[k] = out.get(k, 0) + 1
    return out
