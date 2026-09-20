# -*- coding: utf-8 -*-
"""research_evolve.tracking — 每日/每周任务跟踪（解决"看板没被用起来"）。

设计原则: **从真实执行痕迹反推**，而不是要求各处手工上报。
数据源（都已存在，实测可读）:
    * Windows 计划任务的 LastRunTime / LastTaskResult  -> 每个定时环节到底跑没跑、成没成
    * vault/logs/pipeline_*.json                       -> 论文管线的 new_papers 等指标
    * 99_Meta/self_evolve_log.json                     -> 自进化的分步结果
    * research_evolve/state/registry.json              -> 五条流的候选与闭环四数
    * research_evolve/state/triage.json                -> 今天该处理什么
    * scripts/sync_log.txt                             -> 同步成败

产出:
    70_Dashboard/daily_review.md    今天：各环节跑没跑 + 今天该做什么
    70_Dashboard/weekly_review.md   本周：推进了什么 + 卡在哪 + 下周优先级
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

from .common import VAULT, load_json, read_text, save_json
from .workstreams import WORKSTREAMS

STATE = VAULT / "90_System" / "research_evolve" / "state"
LEDGER = STATE / "run_ledger.jsonl"
DAILY = VAULT / "70_Dashboard" / "daily_review.md"
WEEKLY = VAULT / "70_Dashboard" / "weekly_review.md"
SCRIPTS = Path(r"D:\Obsidian\scripts")

# 应当按时执行的环节（名字 -> 期望周期小时）
EXPECTED = {
    "iNEST_Daily_Pipeline": 24,
    "iNEST_Daily_Sync": 24,
    "iNEST_Health_Watchdog": 2,
    "iNEST_Research_Evolve": 24,
    "iNEST_Knowledge_Evolution": 24 * 7,
    "iNEST_Weekly_Health": 24 * 7,
    "iNEST_Meta_Evolution": 24 * 7,
    "iNEST_Daily_Processing_Digest": 24,
    "iNEST_Inbox_Afternoon": 24,
}


def record(stage: str, status: str, metrics: dict | None = None,
           outputs: list[str] | None = None, note: str = "") -> None:
    """追加一条执行记录（jsonl，便于流式累积与事后分析）。"""
    STATE.mkdir(parents=True, exist_ok=True)
    rec = {"at": datetime.now().isoformat(), "stage": stage, "status": status,
           "metrics": metrics or {}, "outputs": outputs or [], "note": note}
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _tasks() -> dict:
    """读 Windows 计划任务的最近执行情况。"""
    ps = ("Get-ScheduledTask | Where-Object { $_.TaskName -like 'iNEST*' } | "
          "ForEach-Object { $i = Get-ScheduledTaskInfo -TaskName $_.TaskName; "
          "[pscustomobject]@{name=$_.TaskName; state=$_.State; "
          "last=$(if($i.LastRunTime -gt [datetime]'2000-01-01'){$i.LastRunTime.ToString('s')}else{''}); "
          "result=$i.LastTaskResult; next=$(if($i.NextRunTime){$i.NextRunTime.ToString('s')}else{''})} } | "
          "ConvertTo-Json -Depth 3 -Compress")
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="ignore", timeout=120)
        data = json.loads((r.stdout or "[]").strip() or "[]")
        if isinstance(data, dict):
            data = [data]
        return {d["name"]: d for d in data if isinstance(d, dict)}
    except Exception as e:
        return {"__error__": {"name": "任务查询失败", "state": "?", "last": "",
                              "result": 0, "next": "", "err": str(e)}}


def _age_h(iso: str) -> float | None:
    if not iso:
        return None
    try:
        return (datetime.now() - datetime.fromisoformat(iso)).total_seconds() / 3600
    except Exception:
        return None


def _pipeline_tail(n: int = 12) -> list[dict]:
    out = []
    logs = sorted((VAULT / "logs").glob("pipeline_*.json"), key=lambda p: p.stat().st_mtime)[-n:]
    for p in logs:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            d["_file"] = p.name
            out.append(d)
        except Exception:
            pass
    return out


# TaskState 枚举: 0=Unknown 1=Disabled 2=Queued 3=Ready 4=Running
# 教训: PowerShell 的 ConvertTo-Json 会把枚举序列化成**数字**，
# 首版拿它和字符串 "Ready" 比较，结果 9 个正常环节全被报成异常
# （假警报比不报更糟：会让人再也不看这一栏）。这里做显式映射。
STATE_MAP = {0: "Unknown", 1: "Disabled", 2: "Queued", 3: "Ready", 4: "Running"}
OK_STATES = {"Ready", "Running"}


def _state_name(v) -> str:
    if isinstance(v, str):
        return v
    return STATE_MAP.get(v, f"?({v})")


def _stage_table() -> list[dict]:
    """每个环节：跑没跑 / 成没成 / 是否超期。"""
    tasks = _tasks()
    rows = []
    for name, expect_h in EXPECTED.items():
        t = tasks.get(name)
        if not t:
            rows.append({"name": name, "state": "缺失", "age_h": None, "ok": False,
                         "detail": "计划任务不存在"})
            continue
        age = _age_h(t.get("last", ""))
        res = t.get("result", 0)
        state = _state_name(t.get("state", "?"))
        ok = (state in OK_STATES) and res == 0 and (age is not None and age <= expect_h * 1.5)
        detail = []
        if state not in OK_STATES:
            detail.append(f"状态 {state}")
        if res != 0:
            detail.append(f"上次结果 0x{res:X}")
        if age is None:
            detail.append("从未运行")
        elif age > expect_h * 1.5:
            detail.append(f"已 {age:.0f}h 未跑（期望 ≤{expect_h}h）")
        rows.append({"name": name, "state": state, "age_h": age, "ok": ok,
                     "detail": "；".join(detail) or "正常"})
    return rows


def _registry() -> dict:
    return load_json(STATE / "registry.json", default={}) or {}


def _triage() -> dict:
    return load_json(STATE / "triage.json", default={}) or {}


# ---------------------------------------------------------------- 日报
def daily(quiet: bool = False) -> Path:
    stages = _stage_table()
    bad = [s for s in stages if not s["ok"]]
    pipe = _pipeline_tail(5)
    reg = _registry()
    tri = _triage()
    rounds = reg.get("rounds", []) or []
    last_round = rounds[-1] if rounds else {}
    keeps = tri.get("keep", []) or []
    today_n = len(keeps)

    L = [f"# 每日跟踪 · {datetime.now():%Y-%m-%d}", "",
         f"> 生成 {datetime.now():%H:%M} · 由 `research_evolve.tracking` 从真实执行痕迹反推", "",
         "## 一、环节健康（跑没跑 / 成没成）", "",
         "| 环节 | 状态 | 上次运行 | 判断 |", "|---|---|---|---|"]
    for s in stages:
        age = f"{s['age_h']:.1f}h 前" if s["age_h"] is not None else "从未"
        L.append(f"| {s['name']} | {s['state']} | {age} | {'✅ 正常' if s['ok'] else '⚠️ ' + s['detail']} |")
    L.append("")
    if bad:
        L += [f"**有 {len(bad)} 个环节不正常**，优先看这几个。", ""]
    else:
        L += ["所有环节正常。", ""]

    L += ["## 二、论文管线（近 5 次）", "",
          "| 时间 | new_papers | api_results | 分类 | 图节点/边 | 耗时 |",
          "|---|---|---|---|---|---|"]
    for d in pipe:
        L.append(f"| {d.get('date','')[:16]} | {d.get('new_papers','?')} | "
                 f"{d.get('api_results','?')} | {d.get('classified','?')} | "
                 f"{d.get('graph_nodes','?')}/{d.get('graph_edges','?')} | "
                 f"{d.get('elapsed_s','?')}s |")
    nonzero = sum(1 for d in pipe if (d.get("new_papers") or 0) > 0)
    L += ["", f"近 {len(pipe)} 次中 **{nonzero} 次**进到了新论文。", ""]
    if pipe and nonzero == 0:
        L += ["> ⚠️ 连续 0 篇。已定位原因：`export.arxiv.org/api/query` 对本机返回 "
              "HTTP 406，需走多通道回退 —— 见 `scripts/fetch_papers.py`（已实现 "
              "arXiv 列表页 + OpenAlex 两条可用通道）。", ""]

    L += ["## 三、今天该做什么（来自分诊）", ""]
    if today_n:
        L.append(f"分诊给出 **{today_n}** 条，详情见 `70_Dashboard/inbox_triage.md`。这里只列前 5：")
        L.append("")
        for k in keeps[:5]:
            L.append(f"- [ ] **[{k.get('workstream')}]** {k.get('title','')[:70]}")
            L.append(f"  - `{k.get('path','')}`")
    else:
        L.append("分诊无待办（或尚未运行 `python -m research_evolve.triage`）。")
    L.append("")

    L += ["## 四、自进化闭环状态", "",
          f"- 轮次 **{reg.get('round','?')}** · open **{last_round.get('open_total','?')}**",
          f"- 上轮四数：opened={last_round.get('opened','?')} closed={last_round.get('closed','?')} "
          f"escalated={last_round.get('escalated','?')} gate_new={last_round.get('gate_violations','?')}",
          f"- 连续只增不关的轮数：**{reg.get('rounds') and _stagnation(rounds)}**", ""]

    L += ["## 五、按工作流的状态", "",
          "| 工作流 | 闭环定义 | open 候选 |", "|---|---|---|"]
    cands = (reg.get("candidates") or {}).values()
    for ws_id, ws in WORKSTREAMS.items():
        n = sum(1 for c in cands if c.get("verdict") == "open"
                and ws_id.lower() in str(c.get("title", "")).lower())
        L.append(f"| {ws_id} {ws.name} | {ws.closure} | {n} |")
    L += ["", "---", "",
          "**用法**：每天先看第一节有没有 ⚠️，再看第三节的待办清单。", ""]
    DAILY.parent.mkdir(parents=True, exist_ok=True)
    DAILY.write_text("\n".join(L), encoding="utf-8")
    record("daily_review", "ok", {"stages_bad": len(bad), "today_items": today_n},
           [str(DAILY.relative_to(VAULT))])
    if not quiet:
        print(f"日报 -> {DAILY}（异常环节 {len(bad)}，今日待办 {today_n}）")
    return DAILY


def _stagnation(rounds: list[dict]) -> int:
    s = 0
    for r in reversed(rounds):
        if r.get("opened", 0) > 0 and r.get("closed", 0) == 0:
            s += 1
        else:
            break
    return s


# ---------------------------------------------------------------- 周报
def weekly(quiet: bool = False) -> Path:
    since = datetime.now() - timedelta(days=7)
    pipe = [d for d in _pipeline_tail(80)
            if (d.get("date") or "")[:10] >= since.strftime("%Y-%m-%d")]
    new_total = sum((d.get("new_papers") or 0) for d in pipe)

    reg = _registry()
    rounds = [r for r in (reg.get("rounds") or [])
              if (r.get("date") or "") >= since.strftime("%Y-%m-%d")]
    opened = sum(r.get("opened", 0) for r in rounds)
    closed = sum(r.get("closed", 0) for r in rounds)
    gate = sum(r.get("gate_violations", 0) for r in rounds)

    # 台账（ledger）里的记录
    led = []
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8", errors="ignore").splitlines()[-500:]:
            try:
                r = json.loads(line)
                if (r.get("at") or "")[:10] >= since.strftime("%Y-%m-%d"):
                    led.append(r)
            except Exception:
                pass

    stages = _stage_table()
    bad = [s for s in stages if not s["ok"]]

    # 产物变化（按工作流目录的文件数与最新时间）
    ws_stats = []
    for ws_id, ws in WORKSTREAMS.items():
        files = 0
        newest = None
        for d in ws.dirs:
            p = VAULT / d
            if not p.exists():
                continue
            for f in p.rglob("*"):
                if f.is_file():
                    files += 1
                    m = f.stat().st_mtime
                    if newest is None or m > newest:
                        newest = m
        ws_stats.append({"id": ws_id, "name": ws.name, "files": files,
                         "newest": datetime.fromtimestamp(newest).strftime("%m-%d %H:%M")
                         if newest else "—", "closure": ws.closure})

    L = [f"# 每周跟踪 · 截至 {datetime.now():%Y-%m-%d}", "",
         f"> 统计窗口：{since:%Y-%m-%d} ~ {datetime.now():%Y-%m-%d} · "
         f"由 `research_evolve.tracking` 生成", "",
         "## 一、本周四个数", "",
         "| 指标 | 本周 | 说明 |", "|---|---|---|",
         f"| 入口新增论文 | **{new_total}** | 论文管线 new_papers 合计 |",
         f"| 自进化轮次 | **{len(rounds)}** | 有记录的天数 |",
         f"| 候选开启 opened | {opened} | 新进来的问题 |",
         f"| 候选关闭 closed | **{closed}** | 给出裁决并出队 |",
         f"| 门禁新增违规 | {gate} | 引用/证据标签 |",
         f"| 环节异常 | {len(bad)} | {'、'.join(s['name'] for s in bad) or '无'} |",
         ""]
    if opened > 0 and closed == 0:
        L += [f"> 🔴 **本周只增不关**（opened={opened}, closed=0）—— 这正是"
              f"「自膨胀」的信号，与旧系统失效模式相同。", ""]
    elif closed > 0:
        L += ["> ✅ 本周关闭了候选，构成真正的推进（进化 = 变异 + **选择** + 留存）。", ""]

    L += ["## 二、五条工作流的推进", "",
          "| 工作流 | 闭环定义 | 文件数 | 最近改动 |", "|---|---|---|---|"]
    for s in ws_stats:
        L.append(f"| {s['id']} {s['name']} | {s['closure']} | {s['files']} | {s['newest']} |")
    L.append("")

    if led:
        L += ["## 三、台账记录（ledger）", "",
              "| 时间 | 环节 | 状态 | 指标 |", "|---|---|---|---|"]
        for r in led[-25:]:
            L.append(f"| {r.get('at','')[:16]} | {r.get('stage')} | {r.get('status')} | "
                     f"{json.dumps(r.get('metrics') or {}, ensure_ascii=False)[:70]} |")
        L.append("")

    L += ["## 四、下周优先级（按「卡点」排序）", ""]
    prio = []
    if any((d.get("new_papers") or 0) == 0 for d in pipe[-3:]):
        prio.append("论文取数：arXiv API 已 406，确认多通道路径进入定时任务")
    if bad:
        prio.append("修复异常环节：" + "、".join(s["name"] for s in bad))
    if closed == 0:
        prio.append("处理分诊队列里 escalated 的候选（久挂未裁决）")
    prio.append("推进已 accepted 的研究方向（见 research_evolve.md）")
    for i, x in enumerate(prio, 1):
        L.append(f"{i}. {x}")
    L += ["", "---", "", "*每日跟踪见 `70_Dashboard/daily_review.md`。*", ""]

    WEEKLY.parent.mkdir(parents=True, exist_ok=True)
    WEEKLY.write_text("\n".join(L), encoding="utf-8")
    record("weekly_review", "ok",
           {"new_papers": new_total, "opened": opened, "closed": closed, "bad_stages": len(bad)},
           [str(WEEKLY.relative_to(VAULT))])
    if not quiet:
        print(f"周报 -> {WEEKLY}（论文 {new_total}，opened {opened}，closed {closed}，异常 {len(bad)}）")
    return WEEKLY


def main() -> int:
    a = sys.argv[1:]
    if "--weekly" in a:
        weekly(); return 0
    if "--both" in a:
        daily(); weekly(); return 0
    daily(); return 0


if __name__ == "__main__":
    raise SystemExit(main())
