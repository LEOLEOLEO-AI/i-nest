# -*- coding: utf-8 -*-
"""research_evolve.evolve — 闭环编排器（一次运行 = 一轮进化）。

与现有 self_evolve.py 的根本区别：
    self_evolve 的顺序是"编译→生长→链接→生成建议→提交"，
    每一步都只**新增**文件，从不关闭任何东西；因此
    wiki/evolution_report.md 连续多轮都是
    "Hypothesis Validation (0 updates) / Research Direction Recommendations (0)"，
    而 wiki/task_recommendations.md 每天重新列出同一批 2026-07 的条目。

    本编排器的顺序是"收集→去重记账→评分→**关闭**→门禁→报告→提交"，
    并把 closed 作为一等指标：opened>0 且 closed==0 连续两轮即判定
    "自膨胀空转"，写入报告与状态，供看门狗告警。

用法：
    python -m research_evolve.evolve                # 跑一轮
    python -m research_evolve.evolve --status       # 只看状态
    python -m research_evolve.evolve --list         # 列出待裁决队列
    python -m research_evolve.evolve --decide C-00012 accepted "理由"
    python -m research_evolve.evolve --no-git       # 不提交
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from . import gates, harvest, score
from .common import (
    CLOSED_VERDICTS,
    PKG,
    REPORT_FILE,
    STATE_DIR,
    VAULT,
    RunLog,
    append_run_log,
    days_between,
    load_config,
    read_text,
    today,
)
from .registry import Registry
from .score import auto_verdict, score_candidate

LOCK_FILE = STATE_DIR / "evolve.lock"
FREEZE_FILE = STATE_DIR / "freeze.json"
LOCK_MAX_AGE_H = 6

# 本工具拥有写权限的路径（白名单提交，绝不用 git add -A）
OWNED_PATHS = [
    "90_System/research_evolve/",
    "70_Dashboard/research_evolve.md",
    "99_Meta/research_evolve_log.json",
]


# ---------------------------------------------------------------- 单例锁
def _pid_alive(pid: int) -> bool:
    """Windows 下判断 PID 存活。必须用 tasklist——os.kill(pid,0) 会真的杀进程。"""
    try:
        r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="ignore", timeout=20)
        return str(pid) in (r.stdout or "")
    except Exception:
        return False


def acquire_lock(log) -> bool:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if LOCK_FILE.exists():
        try:
            info = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
            pid = int(info.get("pid", -1))
            age_h = days_between(info.get("started", "")) * 24
            if pid != os.getpid() and _pid_alive(pid) and age_h < LOCK_MAX_AGE_H:
                log(f"⚠️ 已有实例在运行 (PID={pid}, {age_h:.2f}h)，本轮跳过。")
                return False
            log(f"接管僵死锁 (PID={pid}, {age_h:.2f}h)。")
        except Exception as e:
            log(f"锁文件损坏({type(e).__name__})，接管。")
    LOCK_FILE.write_text(json.dumps(
        {"pid": os.getpid(), "started": datetime.now().isoformat()}),
        encoding="utf-8")
    return True


def release_lock() -> None:
    try:
        if LOCK_FILE.exists():
            info = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
            if int(info.get("pid", -1)) == os.getpid():
                LOCK_FILE.unlink()
    except Exception:
        pass


# ---------------------------------------------------------------- 收集
def collect(log) -> list[dict]:
    """收集所有候选。失败隔离：单个来源异常不影响其余。"""
    sources = [
        ("假说注册表", harvest.harvest_hypotheses),
        ("进化队列", harvest.harvest_evolution_queue),
        ("灵感卡片", harvest.harvest_ideas),
        ("跨域桥", harvest.harvest_bridges),
    ]
    out: list[dict] = []
    for name, fn in sources:
        try:
            got = fn()
            log(f"收集 {name}: {len(got)} 条")
            out.extend(got)
        except Exception as e:
            log(f"⚠️ 收集 {name} 失败(已隔离): {type(e).__name__}: {e}")
    return out


# ---------------------------------------------------------------- 冻结守卫
def freeze_guard(log, cfg: dict) -> dict:
    """无新来源则冻结"新增概念"。这是 08-27 诊断已提但至今未落地的闸门。

    实测：wiki/concepts 6123 个文件中 5940 个带 auto:true，且 2026-09-15/09-17
    两次自进化各提交 6193/6196 个文件，而当日管线 new_papers=0。
    即"没有新论文，概念却在长"。
    """
    act = harvest.new_source_activity(days=cfg.get("freeze_window_days", 2))
    frozen = bool(cfg.get("freeze_requires_new_source", True)) and act["total"] == 0
    state = {
        "evaluated": datetime.now().isoformat(),
        "new_source_total": act["total"],
        "new_source_counts": act["counts"],
        "window_days": act["window_days"],
        "freeze_new_concepts": frozen,
        "reason": ("近窗口内无新来源材料，冻结新增概念（仅允许链接/去重/回收）"
                   if frozen else f"有新来源 {act['total']} 篇，允许增量编译"),
    }
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    FREEZE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    log(f"冻结守卫: {state['reason']}")
    return state


# ---------------------------------------------------------------- 一轮
def run_round(log) -> dict:
    cfg = load_config()
    reg = Registry.load()

    # 历史新来源窗口（用于冻结守卫）
    cfg.setdefault("freeze_window_days", 2)

    reg.next_round()
    log(f"=== 第 {reg.round} 轮开始 ===")

    # 1) 收集
    raw = collect(log)
    log(f"候选合计: {len(raw)} 条")

    # 2) 去重记账
    new_n = recur_n = closed_seen_n = 0
    for cand in raw:
        try:
            state, rec = reg.upsert(cand)
        except Exception as e:
            log(f"⚠️ 登记失败(已跳过) {cand.get('title','')[:40]}: {e}")
            continue
        if state == "new":
            new_n += 1
            # 用来源自带的创建日期回填 first_seen，使"年龄"真实
            created = (cand.get("evidence") or {}).get("created") or \
                      (cand.get("evidence") or {}).get("card_date") or ""
            if created:
                try:
                    iso = datetime.fromisoformat(str(created).replace("/", "-"))
                    rec["first_seen"] = iso.isoformat()
                except Exception:
                    pass
        elif state == "recurred":
            recur_n += 1
        else:
            closed_seen_n += 1
    log(f"登记: 新增 {new_n} | 复现(仍开放) {recur_n} | 已关闭不再复活 {closed_seen_n}")

    # 3) 评分（对所有 open）
    rejected_norms = reg.rejected_norms()
    scored_n = 0
    for rec in reg.open_candidates():
        try:
            scored = score_candidate({"record": rec}, cfg)
        except Exception as e:
            log(f"⚠️ 评分失败(已跳过) {rec.get('id')}: {e}")
            continue
        rec["score"] = scored["score"]
        rec["score_reasons"] = scored["reasons"]
        rec["flags"] = scored["flags"]
        scored_n += 1

        dup = (rec.get("norm") or "") in rejected_norms and rec.get("verdict") == "open"
        verdict = auto_verdict(rec, scored, cfg, dup_of_rejected=dup)
        if verdict:
            reg.set_verdict(rec, verdict[0], verdict[1], by="auto")
    log(f"评分: {scored_n} 条 open 候选已打分")

    # 4) 年龄升级
    esc = reg.mark_escalations(float(cfg.get("max_open_days", 14)))
    log(f"升级(久挂未裁决): {len(esc)} 条")

    # 5) 门禁（棘轮：只有基线之外的新违规才算"本轮违规"）
    gate_res = gates.gate_result(cfg)
    log(f"门禁: 扫描 {gate_res['scanned_files']} 文件, 新增违规 {len(gate_res['new'])} 项, "
        f"存量债 {len(gate_res['known'])} 项, 本轮消除 {len(gate_res['fixed'])} 项")

    # 6) 冻结守卫
    fz = freeze_guard(log, cfg)

    # 7) 轮次记账（gate_violations 记"新增违规"，存量债单列不触发告警）
    entry = reg.close_round(len(gate_res["new"]))
    log(f"本轮四数: opened={entry['opened']} closed={entry['closed']} "
        f"escalated={entry['escalated']} gate_new={entry['gate_violations']}")

    streak = reg.stagnation_streak()
    if streak >= 2:
        log(f"🔴 自膨胀告警: 连续 {streak} 轮只新增不关闭")

    reg.save()

    # 8) 状态汇总给看门狗
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / "status.json").write_text(json.dumps({
        "updated": datetime.now().isoformat(),
        "round": reg.round,
        "rounds": entry,
        "stagnation_streak": streak,
        "gate_new_violations": len(gate_res["new"]),
        "gate_known_debt": len(gate_res["known"]),
        "gate_fixed_this_round": len(gate_res["fixed"]),
        "gate_total": gate_res["count"],
        "freeze_new_concepts": fz["freeze_new_concepts"],
        "new_source_total": fz["new_source_total"],
        "open_total": entry["open_total"],
        "stats": reg.stats(),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    # 9) 报告
    write_report(reg, entry, gate_res, fz, cfg, streak, log)

    return {"entry": entry, "gate": gate_res, "freeze": fz,
            "streak": streak, "stats": reg.stats()}


# ---------------------------------------------------------------- 报告
def write_report(reg: Registry, entry: dict, gate_res: dict, fz: dict,
                 cfg: dict, streak: int, log) -> None:
    prev = reg.rounds[-2] if len(reg.rounds) >= 2 else None

    def delta(key: str) -> str:
        if not prev:
            return "—"
        d = entry.get(key, 0) - prev.get(key, 0)
        return f"{d:+d}" if d else "0"

    L: list[str] = []
    L.append("# 科研自进化闭环报告")
    L.append("")
    L.append(f"> 第 **{entry['round']}** 轮 · {datetime.now():%Y-%m-%d %H:%M} · "
             f"由 `research_evolve.evolve` 生成（每次运行一轮，一轮一次提交）")
    L.append("")
    L.append("## 一、闭环四数（判定\"进化\"还是\"空转\"的唯一依据）")
    L.append("")
    L.append("| 指标 | 本轮 | 上轮 | Δ | 含义 |")
    L.append("|---|---|---|---|---|")
    L.append(f"| 新增候选 opened | {entry['opened']} | "
             f"{prev['opened'] if prev else '—'} | {delta('opened')} | 本轮新进来的问题 |")
    L.append(f"| 关闭候选 closed | {entry['closed']} | "
             f"{prev['closed'] if prev else '—'} | {delta('closed')} | **已给出裁决并出队** |")
    L.append(f"| 升级 escalated | {entry['escalated']} | "
             f"{prev['escalated'] if prev else '—'} | {delta('escalated')} | 久挂未裁决，需拍板 |")
    L.append(f"| 门禁违规 | {entry['gate_violations']} | "
             f"{prev['gate_violations'] if prev else '—'} | {delta('gate_violations')} | 引用/证据标签/正本改动 |")
    L.append(f"| 当前 open 总数 | {entry['open_total']} | — | — | 待办池水位 |")
    L.append("")
    if streak >= 2:
        L.append(f"> 🔴 **自膨胀告警**：连续 **{streak}** 轮 `opened > 0` 且 `closed == 0`。"
                 f"这正是旧 self_evolve 的失效模式（每天生成 18 条建议、"
                 f"连续两月关闭 0 条）。请优先处理下面的裁决队列。")
    elif entry["closed"] > 0:
        L.append(f"> ✅ 本轮关闭 **{entry['closed']}** 条，构成一次真正的进化轮"
                 f"（进化 = 变异 + **选择** + 留存；旧系统只有变异与留存）。")
    L.append("")

    # 冻结守卫
    L.append("## 二、冻结守卫（无新论文则不许长概念）")
    L.append("")
    L.append(f"- 近 **{fz['window_days']}** 天新来源材料：**{fz['new_source_total']}** 篇 "
             f"（{', '.join(f'{k}={v}' for k, v in fz['new_source_counts'].items())}）")
    L.append(f"- 判定：**{'冻结新增概念' if fz['freeze_new_concepts'] else '允许增量编译'}**")
    L.append(f"- 依据：{fz['reason']}")
    L.append(f"- 状态文件：`90_System/research_evolve/state/freeze.json`")
    L.append("")

    # 人的裁决队列
    q = reg.human_queue(int(cfg.get("max_human_decisions", 7)))
    L.append(f"## 三、待您裁决（{len(q)} 条，最高优先在前）")
    L.append("")
    if not q:
        L.append("_队列为空。_")
    for c in q:
        flag = "🔺升级 " if c.get("escalated") else ""
        age = days_between(c.get("first_seen", ""))
        L.append(f"### {c['id']} · {flag}score={c.get('score')} · "
                 f"{c.get('kind')} · 挂起 {age:.0f} 天 · 见 {c.get('seen_count')} 次")
        L.append("")
        L.append(f"**{c.get('title','')}**")
        L.append("")
        if c.get("detail"):
            L.append(f"- 详情：{c['detail'][:300]}")
        if c.get("source"):
            L.append(f"- 来源：`{c['source']}`")
        for r in (c.get("score_reasons") or [])[:4]:
            L.append(f"- {r}")
        if c.get("flags"):
            L.append(f"- 标记：{', '.join(c['flags'])}")
        L.append(f"- 裁决：`python -m research_evolve.evolve --decide {c['id']} "
                 f"accepted|rejected|deferred \"理由\"`")
        L.append("")

    # 本轮关闭
    closed = [c for c in reg.candidates.values()
              if c.get("verdict_round") == entry["round"] and c.get("verdict") in CLOSED_VERDICTS]
    L.append(f"## 四、本轮关闭 {len(closed)} 条（含原因，永不复活）")
    L.append("")
    if not closed:
        L.append("_无。_")
    for c in closed[:40]:
        L.append(f"- `{c['id']}` **{c.get('title','')[:80]}** → "
                 f"**{c.get('verdict')}**（{c.get('verdict_reason','')}）")
    if len(closed) > 40:
        L.append(f"- … 其余 {len(closed)-40} 条见 `state/registry.json`")
    L.append("")

    # 门禁
    new_v = gate_res.get("new", [])
    known_v = gate_res.get("known", [])
    L.append(f"## 五、门禁（新增违规 {len(new_v)} · 存量债 {len(known_v)} · "
             f"本轮消除 {len(gate_res.get('fixed', []))}）")
    L.append("")
    L.append(f"扫描 {gate_res['scanned_files']} 个交付草稿文件。"
             f"**只有基线之外的新违规才判失败**——门禁是回归检测器，"
             f"不是把存量债每天重报一遍（那会退化成第二个\"每天 18 条建议\"）。")
    L.append("")
    if not gate_res["violations"]:
        L.append("_无违规。_")
    else:
        by_type: dict[str, int] = {}
        for v in gate_res["violations"]:
            by_type[v["type"]] = by_type.get(v["type"], 0) + 1
        L.append("| 类型 | 总数 | 其中新增 |")
        L.append("|---|---|---|")
        new_by_type: dict[str, int] = {}
        for v in new_v:
            new_by_type[v["type"]] = new_by_type.get(v["type"], 0) + 1
        for k, n in sorted(by_type.items(), key=lambda x: -x[1]):
            L.append(f"| {k} | {n} | {new_by_type.get(k, 0)} |")
        L.append("")
    if new_v:
        L.append("**新增违规（须处理）**")
        L.append("")
        for v in new_v[:15]:
            loc = v.get("file") or v.get("value") or ""
            ln = f":{v['line']}" if v.get("line") else ""
            L.append(f"- `{loc}{ln}` **{v['type']}** — {v.get('why','')}")
    L.append("")
    L.append("> 收敛方式：人工复核后运行 "
             "`python -m research_evolve.gates --update-baseline` 接受当前存量为债。")
    L.append("")

    # 概念债
    try:
        debt = harvest.concept_debt()
    except Exception:
        debt = {}
    if debt:
        L.append("## 六、概念层负债（实测口径）")
        L.append("")
        L.append(f"- 概念文件总数：**{debt['total']}**")
        L.append(f"- 带 `auto: true` 自动占位：**{debt['auto_stub']}** "
                 f"（{100*debt['auto_stub']/max(debt['total'],1):.1f}%）")
        L.append(f"- 文件名近似文章标题：**{debt['title_like']}** "
                 f"（{100*debt['title_like']/max(debt['total'],1):.1f}%）")
        L.append(f"- 孤儿概念（自报）：**{debt['orphan_reported']}** "
                 f"— 来源 `{debt['orphan_source']}`")
        L.append("")
        L.append("> 说明：孤儿数取自生成器自报，未在本轮重算（重算 6000+ 文件全库链接成本高，"
                 "且 `wiki_grow.py` 的 `Knowledge Graph Density` 是按概念**数量**分档的伪造指标，"
                 "不可用于判断图质量）。")
        L.append("")

    L.append("---")
    L.append("")
    L.append("*本报告由 `research_evolve` 生成：每轮一次运行、一次提交，"
             "所有计数均来自本轮实际扫描，扫描口径与阈值见 "
             "`90_System/research_evolve/config.yaml`，"
             "候选与裁决的完整记忆见 `90_System/research_evolve/state/registry.json`。*")

    text = "\n".join(L)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(text, encoding="utf-8")
    log(f"报告已写入 {REPORT_FILE}")


# ---------------------------------------------------------------- git
def git_commit(log, do_commit: bool = True) -> dict:
    """白名单提交（只提交本工具拥有的路径），**不推送**。

    不推送是刻意的：本地 main 与 github/main 的 merge-base 为空
    （本地 90 提交 / 远端 721 提交，无共同祖先），任何 push 都会被拒。
    自动重试 push 会让失败被埋在日志里（旧 self_evolve 正是如此，
    连续 8 天 push 失败仍报 exit 0）。把是否合并交给用户裁决。
    """
    def run(args):
        return subprocess.run(args, cwd=str(VAULT), capture_output=True,
                              text=True, encoding="utf-8", errors="ignore")

    st = run(["git", "status", "--porcelain", "--"] + OWNED_PATHS)
    if not st.stdout.strip():
        log("git: 本工具路径无改动，跳过提交。")
        return {"committed": False, "reason": "no-change"}

    if not do_commit:
        log("git: --no-git 指定，跳过提交。")
        return {"committed": False, "reason": "disabled"}

    run(["git", "add", "--"] + OWNED_PATHS)
    msg = f"feat(research-evolve): 自进化闭环第 {Registry.load().round} 轮 — 收集/评分/关闭/门禁"
    c = run(["git", "commit", "-q", "-m", msg])
    if c.returncode != 0:
        log(f"⚠️ git commit 失败: {(c.stderr or c.stdout)[:200]}")
        return {"committed": False, "reason": "commit-failed"}

    # 只报告同步状态，不做任何 push/pull
    local_only = run(["git", "rev-list", "--count", "github/main..HEAD"])
    remote_only = run(["git", "rev-list", "--count", "HEAD..github/main"])
    base = run(["git", "merge-base", "HEAD", "github/main"])
    diverged = not (base.stdout or "").strip()
    log(f"已本地提交。同步状态: 本地独有 {local_only.stdout.strip()} / "
        f"远端独有 {remote_only.stdout.strip()} / 共同祖先 "
        f"{'无(历史已分叉)' if diverged else '有'}")
    return {"committed": True, "diverged": diverged,
            "local_only": local_only.stdout.strip(),
            "remote_only": remote_only.stdout.strip()}


# ---------------------------------------------------------------- CLI
def cmd_status() -> int:
    reg = Registry.load()
    st = reg.stats()
    print(f"轮次: {st['round']}")
    print(f"候选总数: {st['total']} | open: {st['open']}")
    print(f"按裁决: {st['by_verdict']}")
    print(f"按种类: {st['by_kind']}")
    print(f"自膨胀连续轮数: {st['stagnation_streak']}")
    for r in reg.rounds[-5:]:
        print(f"  R{r['round']:>3} {r['date']} opened={r['opened']:>3} "
              f"closed={r['closed']:>3} escalated={r['escalated']:>3} "
              f"gate={r['gate_violations']:>3}")
    return 0


def cmd_list(limit: int = 20) -> int:
    reg = Registry.load()
    for c in reg.human_queue(limit):
        age = days_between(c.get("first_seen", ""))
        flag = "ESCALATED " if c.get("escalated") else ""
        print(f"{c['id']} score={c.get('score')} {flag}age={age:.0f}d "
              f"seen={c.get('seen_count')} [{c.get('kind')}] {c.get('title','')[:70]}")
    return 0


def cmd_decide(cid: str, verdict: str, reason: str) -> int:
    reg = Registry.load()
    rec = reg.by_id(cid)
    if rec is None:
        print(f"未找到候选 {cid}")
        return 1
    try:
        reg.set_verdict(rec, verdict, reason, by="human")
    except ValueError as e:
        print(e)
        return 1
    reg.save()
    print(f"{cid} -> {verdict}（{reason}）")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "--status":
        return cmd_status()
    if argv and argv[0] == "--list":
        n = int(argv[1]) if len(argv) > 1 else 20
        return cmd_list(n)
    if argv and argv[0] == "--decide":
        if len(argv) < 4:
            print('用法: --decide <id> <accepted|rejected|deferred|adopted|done> "理由"')
            return 1
        return cmd_decide(argv[1], argv[2], argv[3])

    do_git = "--no-git" not in argv
    log = RunLog("research_evolve")
    if not acquire_lock(log):
        return 0
    try:
        res = run_round(log)
        git_res = git_commit(log, do_commit=do_git)
        append_run_log([log.as_dict(), {"step": "git", "result": git_res}])
        print()
        print(f"轮次 {res['entry']['round']} 完成 | opened={res['entry']['opened']} "
              f"closed={res['entry']['closed']} escalated={res['entry']['escalated']} "
              f"gate={res['entry']['gate_violations']} open={res['entry']['open_total']}")
        print(f"报告: {REPORT_FILE}")
        return 0
    finally:
        release_lock()


if __name__ == "__main__":
    raise SystemExit(main())
