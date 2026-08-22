#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
meta_evolution.py — 规则层元进化引擎 (L3-L5 自进化闭环)

定位：补齐知识库自进化(self_evolve.py)之后的"规则进化"缺口。
self_evolve.py 进化"知识"(wiki/概念/假设)；本引擎进化"智能体自身的行为规则"
(AGENTS.md 条款 / 检索词 / 技能改进 / 管线参数)。

原则（防失控铁律）：
1. 只生成《规则修订提案》，绝不自动修改规则 — 审批权永远在刘勤让教授。
2. 提案必须附证据（文件+数据），无证据的修改建议不进入提案。
3. 提案按可执行性分级：P0 必须修 / P1 建议修 / P2 观察。
4. 失败案例进教训库（99_Meta/lessons_learned.md），形成可追溯的进化记忆。

执行链：
  1. 读取 self_evolve_log.json → 统计最近 N 天各步骤成功率/失败模式
  2. 读取 vault_health.md → 健康趋势（断链/孤儿/缺FM 增减）
  3. 读取 git log → 近 7 天提交模式（每日提交量、自生长是否活跃）
  4. 读取 research_task_proposals.json / hypothesis_registry.json → 研究层证据
  5. 生成《规则修订提案》→ 99_Meta/evolution_proposals/YYYY-MM-DD.md
  6. 记录本轮进化评估到 meta_evolution_log.json

用法:
    python meta_evolution.py                # 生成今日提案
    python meta_evolution.py --days 14      # 用 14 天窗口评估
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

VAULT = Path(r"D:\Obsidian\vault")
META = VAULT / "99_Meta"
SCRIPTS = VAULT / "90_System" / "scripts"
PROPOSAL_DIR = META / "evolution_proposals"
LESSONS_FILE = META / "lessons_learned.md"
LOG_FILE = META / "meta_evolution_log.json"

TODAY = datetime.now().strftime("%Y-%m-%d")


def log(msg: str) -> None:
    print(f"[meta_evolution] {msg}", flush=True)


# ── 证据源 1: self_evolve 运行日志 ──────────────────────────────

def analyze_self_evolve_log(days: int) -> dict:
    """统计自进化各步骤的成功率与失败模式。"""
    path = META / "self_evolve_log.json"
    if not path.exists():
        return {"available": False, "runs": 0}
    try:
        entries = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"available": False, "runs": 0}
    cutoff = (datetime.now() - timedelta(days=days)).date().isoformat()
    recent = [e for e in entries if e.get("date", "") >= cutoff]
    step_stats = {}
    failures = []
    for e in recent:
        steps = e.get("steps", {})
        for key, ok in steps.items():
            if isinstance(ok, bool):
                stat = step_stats.setdefault(key, {"ok": 0, "fail": 0})
                stat["ok" if ok else "fail"] += 1
        # 提取日志中的失败信号
        for line in e.get("log", []):
            low = line.lower()
            if any(t in low for t in ["timeout", "failed", "error", "退出码=124", "402"]):
                failures.append({"date": e.get("date"), "signal": line[:120]})
    return {
        "available": True,
        "runs": len(recent),
        "step_stats": step_stats,
        "failures": failures[-10:],
    }


# ── 证据源 2: 健康检查 ─────────────────────────────────────────

def analyze_health(days_back: int = 30) -> dict:
    """从历史健康数据看趋势。health 数据在 self_evolve_log 的 steps.health 中。"""
    path = META / "self_evolve_log.json"
    if not path.exists():
        return {"available": False}
    try:
        entries = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"available": False}
    cutoff = (datetime.now() - timedelta(days=days_back)).date().isoformat()
    points = []
    for e in entries:
        if e.get("date", "") < cutoff:
            continue
        h = e.get("steps", {}).get("health")
        if isinstance(h, dict):
            points.append({
                "date": e.get("date"),
                "notes": h.get("total_notes", 0),
                "broken": h.get("broken_links", 0),
                "orphans": h.get("orphan_notes", 0),
                "missing_fm": h.get("missing_frontmatter", 0),
            })
    points.sort(key=lambda p: p["date"])
    trend = {}
    if len(points) >= 2:
        first, last = points[0], points[-1]
        for key in ["notes", "broken", "orphans", "missing_fm"]:
            delta = last[key] - first[key]
            trend[key] = {"first": first[key], "last": last[key], "delta": delta}
    return {"available": True, "points": points, "trend": trend}


# ── 证据源 3: git 提交模式 ─────────────────────────────────────

def analyze_git(days: int = 7) -> dict:
    """近 N 天提交模式：自生长是否活跃、提交频率。"""
    try:
        since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        out = subprocess.run(
            ["git", "log", f"--since={since}", "--pretty=%h %ad %s",
             "--date=format:%Y-%m-%d %H:%M"],
            cwd=str(VAULT), capture_output=True, text=True, encoding="utf-8",
            errors="ignore", timeout=30,
        ).stdout.strip()
    except Exception as e:
        return {"available": False, "error": str(e)}
    commits = [l for l in out.splitlines() if l.strip()]
    self_evolve_count = sum(1 for c in commits if "self-evolve" in c.lower())
    return {
        "available": True,
        "total_commits": len(commits),
        "self_evolve_commits": self_evolve_count,
        "sample": commits[:5],
    }


# ── 证据源 4: 研究层状态 ───────────────────────────────────────

def analyze_research() -> dict:
    hyp = META / "hypothesis_registry.json"
    tasks = META / "research_task_proposals.json"
    result = {"hypotheses": None, "pending_tasks": None}
    if hyp.exists():
        try:
            data = json.loads(hyp.read_text(encoding="utf-8"))
            result["hypotheses"] = data.get("hypotheses", [])
        except Exception:
            pass
    if tasks.exists():
        try:
            data = json.loads(tasks.read_text(encoding="utf-8"))
            proposals = data if isinstance(data, list) else data.get("proposals", [])
            result["pending_tasks"] = len(proposals)
        except Exception:
            pass
    return result


# ── 提案生成 ───────────────────────────────────────────────────

def build_proposal(evidence: dict, days: int) -> str:
    """基于证据生成规则修订提案（只建议，不执行）。"""
    lines = []
    lines.append(f"# 规则修订提案（元进化评估 #{TODAY}）")
    lines.append("")
    lines.append(f"> 生成时间: {TODAY} ｜ 评估窗口: 近 {days} 天 ｜ 引擎: meta_evolution.py")
    lines.append("> 审批人: 刘勤让教授 ｜ 原则: 只提案不自动执行，无证据不进提案")
    lines.append("")
    lines.append("## 一、证据摘要")
    lines.append("")
    ev = evidence["self_evolve"]
    if ev.get("available"):
        lines.append(f"- **自进化运行**: 窗口内 {ev['runs']} 次运行")
        for step, stat in ev.get("step_stats", {}).items():
            lines.append(f"  - {step}: 成功 {stat['ok']} / 失败 {stat['fail']}")
        if ev.get("failures"):
            lines.append(f"  - ⚠️ 失败信号 {len(ev['failures'])} 条（最近）:")
            for f in ev["failures"][-5:]:
                lines.append(f"    - [{f['date']}] {f['signal'][:100]}")
    else:
        lines.append("- 自进化日志不可用")
    lines.append("")
    h = evidence["health"]
    if h.get("available") and h.get("trend"):
        lines.append("- **健康趋势**（窗口首末对比）:")
        for key, t in h["trend"].items():
            arrow = "↑" if t["delta"] > 0 else ("↓" if t["delta"] < 0 else "→")
            lines.append(f"  - {key}: {t['first']} → {t['last']} ({arrow}{abs(t['delta'])})")
    lines.append("")
    g = evidence["git"]
    if g.get("available"):
        lines.append(f"- **Git 提交**: 近 {days} 天共 {g['total_commits']} 次，其中自生长提交 {g['self_evolve_commits']} 次")
    lines.append("")
    r = evidence["research"]
    if r.get("hypotheses"):
        active = [x for x in r["hypotheses"] if x.get("status") in ("proposed", "under_investigation")]
        lines.append(f"- **研究假设**: 共 {len(r['hypotheses'])} 条，进行中 {len(active)} 条")
    if r.get("pending_tasks") is not None:
        lines.append(f"- **研究任务建议**: {r['pending_tasks']} 条待审")
    lines.append("")
    lines.append("## 二、规则修订建议")
    lines.append("")
    lines.append("### P0 — 必须修（有明确失败证据）")
    lines.append("")
    p0 = []
    if ev.get("available"):
        for step, stat in ev.get("step_stats", {}).items():
            if stat["fail"] > 0:
                p0.append(f"- **{step} 步骤近期失败 {stat['fail']} 次** — 建议：检查超时参数/依赖，或降级为可跳过步骤（证据: self_evolve_log.json）")
    if not p0:
        lines.append("- （无 — 近期自进化步骤全部成功）")
    else:
        lines.extend(p0)
    lines.append("")
    lines.append("### P1 — 建议修（有趋势证据）")
    lines.append("")
    p1 = []
    if h.get("available") and h.get("trend"):
        for key, t in h["trend"].items():
            if key != "notes" and t["delta"] > 20:
                p1.append(f"- **{key} 上升 {t['delta']}**（{t['first']}→{t['last']}）— 建议：安排一次专项清理（证据: vault_health）")
    if not p1:
        lines.append("- （无 — 健康指标稳定或改善）")
    else:
        lines.extend(p1)
    lines.append("")
    lines.append("### P2 — 观察项")
    lines.append("")
    p2 = []
    if g.get("available"):
        if g["total_commits"] < 3:
            p2.append("- **提交频率偏低** — 检查定时任务是否被禁用或机器休眠")
    if r.get("pending_tasks") and r["pending_tasks"] > 10:
        p2.append(f"- **研究任务积压 {r['pending_tasks']} 条** — 建议安排审阅批次")
    if not p2:
        lines.append("- （无）")
    else:
        lines.extend(p2)
    lines.append("")
    lines.append("## 三、审批")
    lines.append("")
    lines.append("- [ ] 批准 P0 项（在对应行后加 ✅ 表示同意执行）")
    lines.append("- [ ] 批准 P1 项")
    lines.append("- [ ] 批准 P2 项")
    lines.append("- [ ] 其他意见（写入下方）")
    lines.append("")
    lines.append("---")
    lines.append("*本提案由 meta_evolution.py 自动生成，不包含任何自动修改。审批通过后由科研智能体执行修订并提交。*")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="规则层元进化引擎")
    parser.add_argument("--days", type=int, default=7, help="评估窗口天数")
    args = parser.parse_args()

    log(f"开始元进化评估（窗口 {args.days} 天）")
    evidence = {
        "self_evolve": analyze_self_evolve_log(args.days),
        "health": analyze_health(30),
        "git": analyze_git(args.days),
        "research": analyze_research(),
    }
    proposal = build_proposal(evidence, args.days)

    PROPOSAL_DIR.mkdir(parents=True, exist_ok=True)
    proposal_path = PROPOSAL_DIR / f"{TODAY}.md"
    proposal_path.write_text(proposal, encoding="utf-8")
    log(f"提案已生成: {proposal_path}")

    # 记录评估日志
    record = {
        "date": TODAY,
        "window_days": args.days,
        "evidence": {
            "self_evolve_runs": evidence["self_evolve"].get("runs"),
            "git_commits": evidence["git"].get("total_commits"),
            "health_trend": evidence["health"].get("trend"),
        },
        "proposal": str(proposal_path),
    }
    history = []
    if LOG_FILE.exists():
        try:
            history = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except Exception:
            history = []
    history.append(record)
    LOG_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"评估日志已记录: {LOG_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
