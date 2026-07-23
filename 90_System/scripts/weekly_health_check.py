"""
Weekly Health Check — runs every Sunday 03:00
Checks: pipeline health, vault integrity, graph stats, broken links, disk usage, git status
"""
import json, os, sys, subprocess
from pathlib import Path
from datetime import datetime, timedelta

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
MOC = VAULT / "60_MOC"
LOGS = VAULT / "logs"
SCRIPTS = VAULT / "90_System" / "scripts"
META = VAULT / "99_Meta"
PROPOSALS = META / "research_task_proposals.json"
ANALYSIS_CACHE = META / "daily_analysis_cache.json"
SYNC_STATE = Path(r"D:\Obsidian\scripts\gitee_sync_state.json")
PIPELINE_GUARD_STATUS = VAULT / "state" / "pipeline_guard_status.json"

TODAY = datetime.now()
WEEK_AGO = TODAY - timedelta(days=7)

def check_file(path):
    return path.exists()

def count_files(directory, pattern="*.md"):
    return len(list(Path(directory).rglob(pattern))) if Path(directory).exists() else 0

def check_port(port):
    import socket
    try:
        s = socket.create_connection(("127.0.0.1", port), timeout=3)
        s.close()
        return True
    except:
        return False

def run(cmd, timeout=30, limit=200):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=True)
        output = r.stdout.strip()
        return r.returncode == 0, output if limit is None else output[:limit]
    except:
        return False, "TIMEOUT"

def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as error:
        return None, str(error)

def git_remotes():
    ok, out = run("git remote", timeout=15)
    return set(out.splitlines()) if ok else set()

def cache_summary():
    data, error = load_json(ANALYSIS_CACHE)
    if error:
        return 0, error
    return len(data.get("items", {})), None

def get_pipeline_stats():
    """Get pipeline runs from past week."""
    runs = []
    if LOGS.exists():
        for f in sorted(LOGS.glob("pipeline_*.json"), reverse=True):
            ts = f.stem.replace("pipeline_", "")
            try:
                dt = datetime.strptime(ts, "%Y%m%d_%H%M")
                if dt >= WEEK_AGO:
                    d = json.loads(f.read_text(encoding="utf-8"))
                    runs.append({"date": dt.strftime("%Y-%m-%d %H:%M"), "papers": d.get("new_papers", 0),
                                 "nodes": d.get("graph_nodes", 0), "edges": d.get("graph_edges", 0),
                                 "elapsed": d.get("elapsed_s", 0)})
            except:
                pass
    return runs

def generate_report():
    lines = []
    lines.append(f"# 系统健康周报 — {TODAY.strftime('%Y-%m-%d')}")
    lines.append(f"> 自动生成 | 检查范围: {WEEK_AGO.strftime('%m-%d')} ~ {TODAY.strftime('%m-%d')}")
    lines.append("")

    # 1. Core Services
    lines.append("## 1. 核心服务")
    lines.append("")
    lines.append(f"| 服务 | 状态 |")
    lines.append(f"|------|------|")
    preview = "OK" if check_port(8899) else "DOWN"
    jojo = "OK" if check_port(57321) else "DOWN"
    lines.append(f"| 预览服务器 (:8899) | {preview} |")
    lines.append(f"| JOJO LLM (:57321) | {jojo} |")
    lines.append("")

    # 2. Pipeline Runs
    runs = get_pipeline_stats()
    lines.append("## 2. 本周管线运行")
    lines.append("")
    if runs:
        lines.append(f"| 时间 | 论文 | 节点 | 边 | 耗时 |")
        lines.append(f"|------|------|------|------|------|")
        for r in runs[:14]:
            elapsed_m = r["elapsed"] / 60
            lines.append(f"| {r['date']} | {r['papers']} | {r['nodes']} | {r['edges']} | {elapsed_m:.0f}min |")
        total_papers = sum(r["papers"] for r in runs)
        lines.append(f"| **合计** | **{total_papers}** | — | — | — |")
    else:
        lines.append("(本周无管线运行记录)")
    lines.append("")

    # 3. Vault Stats
    total_md = count_files(VAULT, "*.md")
    inbox_count = len(list((VAULT / "00_Inbox" / "_pipeline_insights").glob("*.md"))) if (VAULT / "00_Inbox" / "_pipeline_insights").exists() else 0
    papers_count = len([d for d in (VAULT / "50_Output" / "51_Papers").iterdir() if d.is_dir() and not d.name.startswith(".")]) if (VAULT / "50_Output" / "51_Papers").exists() else 0
    
    lines.append("## 3. 知识库统计")
    lines.append("")
    lines.append(f"- 总笔记: {total_md}")
    lines.append(f"- 待处理收件箱: {inbox_count}")
    lines.append(f"- 活跃论文项目: {papers_count}")
    lines.append("")

    # 4. Git Status
    ok, out = run("git status --short", timeout=15, limit=None)
    lines.append("## 4. Git 状态")
    lines.append("")
    if ok:
        changes = [l for l in out.split("\n") if l.strip()]
        lines.append(f"- 未提交变更: {len(changes)} 个文件")
    else:
        lines.append(f"- Git 检查失败: {out[:100]}")
    remotes = git_remotes()
    lines.append(f"- GitHub 远端: {'OK' if 'github' in remotes else 'MISSING'}")
    lines.append(f"- Gitee 远端: {'OK' if 'gitee' in remotes else 'MISSING'}")
    lines.append("")

    # 5. Daily Generator
    daily_action = MOC / "03_Daily_Action.md"
    if daily_action.exists():
        age = TODAY - datetime.fromtimestamp(daily_action.stat().st_mtime)
        lines.append(f"## 5. 每日洞察更新")
        lines.append(f"- 最后更新: {age.days} 天前")
    lines.append("")

    # 6. Data contracts
    lines.append("## 6. 数据契约")
    lines.append("")
    proposals, proposal_error = load_json(PROPOSALS)
    if proposal_error:
        lines.append(f"- 任务提案 JSON: INVALID ({proposal_error[:120]})")
    else:
        pending = sum(item.get("status") == "pending_review" for item in proposals.get("items", []))
        lines.append(f"- 任务提案 JSON: OK ({pending} 待审核)")
    cache_count, cache_error = cache_summary()
    lines.append(f"- 每日分析缓存: {'INVALID' if cache_error else f'OK ({cache_count} 项)'}")
    if SYNC_STATE.exists():
        sync_age = TODAY - datetime.fromtimestamp(SYNC_STATE.stat().st_mtime)
        lines.append(f"- 最近同步状态: {sync_age.days} 天前")
    else:
        lines.append("- 最近同步状态: 尚无成功记录")
    guard, guard_error = load_json(PIPELINE_GUARD_STATUS)
    if guard_error:
        lines.append("- 管线超时守卫: 尚无运行记录")
    else:
        lines.append(f"- 管线超时守卫: {guard.get('status', 'unknown')}")
    lines.append("")

    # 7. Issues
    issues = []
    if not check_port(8899):
        issues.append("预览服务器 :8899 未运行")
    if len(runs) < 5:
        issues.append(f"本周仅 {len(runs)} 次管线运行（预期 >=5）")
    if proposal_error:
        issues.append("任务提案 JSON 无效")
    if 'github' not in remotes or 'gitee' not in remotes:
        issues.append("Git 双远端配置不完整")
    if not SYNC_STATE.exists() or (TODAY - datetime.fromtimestamp(SYNC_STATE.stat().st_mtime)).total_seconds() > 36 * 3600:
        issues.append("Git 同步状态超过 36 小时未成功更新")
    if not guard_error and guard.get("status") in {"timeout", "paused"}:
        issues.append("科研管线因超时等待人工确认")
    
    if issues:
        lines.append("## 7. 需处理问题")
        lines.append("")
        for issue in issues:
            lines.append(f"- **{issue}**")
    else:
        lines.append("## 7. 状态")
        lines.append("")
        lines.append("全部正常。")
    
    lines.append("")
    lines.append(f"*报告生成于 {TODAY.strftime('%Y-%m-%d %H:%M')}*")
    
    report_path = MOC / f"weekly_health_{TODAY.strftime('%Y%m%d')}.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path

if __name__ == "__main__":
    import os
    os.chdir(str(VAULT))
    path = generate_report()
    print(f"Weekly health report: {path.name}")
    print("Done")
