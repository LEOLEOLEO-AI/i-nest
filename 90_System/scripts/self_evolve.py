# -*- coding: utf-8 -*-
"""
self_evolve.py — 知识库自进化 / 自生长 编排器 (Karpathy LLM-Wiki 风格)

设计目标: 可无人值守、可每日定时运行、不失控、幂等、失败不破坏数据。

执行链:
  1. 增量编译 raw/新来源 -> wiki (仅当存在未处理文件时调用 LLM, 带超时与失败隔离)
  2. wiki_grow: 概念图谱交叉链接 + 去重 + 刷新 index/backlinks/health (纯本地)
  3. 全库轻量健康自检 (断链/孤儿/缺 frontmatter, 纯本地无 LLM) -> 99_Meta/vault_health.md
  4. 刷新 Home.md (实时 git 状态)
  5. git add + commit + push github (仅当有改动)

所有 LLM 调用都带超时与异常隔离, 单步失败不影响其余步骤, 全程记录日志到
99_Meta/self_evolve_log.json。
"""
import json
import subprocess
import sys
import re
import datetime
from pathlib import Path
from collections import defaultdict

VAULT = Path(r"D:/obsidian/vault")
SCRIPTS = VAULT / "90_System" / "scripts"
LOG_FILE = VAULT / "99_Meta" / "self_evolve_log.json"
PY = sys.executable
NOW = datetime.datetime.now()
TODAY = NOW.strftime("%Y-%m-%d")

log_entries = []


def log(msg):
    line = f"[{NOW:%H:%M:%S}] {msg}"
    log_entries.append((NOW.isoformat(), msg))
    print("[self_evolve]", msg, flush=True)


def run_script(rel, *args, timeout=600):
    """运行一个脚本, 返回 (rc, out). 失败隔离, 不抛异常。"""
    cmd = [PY, str(SCRIPTS / rel), *args]
    try:
        r = subprocess.run(cmd, cwd=str(VAULT), capture_output=True,
                           text=True, encoding="utf-8", errors="ignore", timeout=timeout)
        out = (r.stdout + r.stderr)[-1500:]
        return r.returncode, out
    except subprocess.TimeoutExpired:
        return 124, f"TIMEOUT after {timeout}s"
    except Exception as e:
        return 1, f"ERR {type(e).__name__}: {e}"


def step_compile_if_new():
    """仅当存在未编译来源时运行 wiki_compiler (状态化, 增量)。"""
    state_file = VAULT / "state" / "wiki_compiler_state.json"
    state = {}
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception:
            state = {}
    processed = state.get("processed_files", {})
    # 探测主要来源目录是否有新/修改文件 (mtime > 记录)
    sources = []
    for d in ("raw", "imports", "tcc/papers", "inest/papers", "30_TCC", "40_iNEST"):
        p = VAULT / d
        if p.exists():
            sources.append(p)
    new_count = 0
    try:
        for base in sources:
            for f in base.rglob("*.md"):
                key = str(f.relative_to(VAULT))
                mtime = f.stat().st_mtime
                last = processed.get(key)
                if last is None or mtime > last:
                    new_count += 1
    except Exception:
        new_count = -1
    if new_count > 0:
        log(f"检测到 {new_count} 个新/修改来源, 运行 wiki_compiler (LLM, 限 300s)...")
        rc, out = run_script("wiki_compiler.py", timeout=300)
        log(f"wiki_compiler 退出码={rc} | {out[-300:]}")
        return rc == 0
    else:
        log("无新来源, 跳过 wiki_compiler 编译 (增量保护)。")
        return True


def step_grow():
    log("运行 wiki_grow 交叉链接/去重...")
    rc, out = run_script("wiki_grow.py", timeout=300)
    log(f"wiki_grow 退出码={rc} | {out[-300:]}")
    return rc == 0


def step_vault_health():
    """纯本地全库健康自检: 断链 / 孤儿 / 缺 frontmatter。无 LLM。"""
    log("运行全库健康自检 (纯本地)...")
    notes = list(VAULT.rglob("*.md"))
    # 排除 .git / 排除 wiki 概念自身重叠 (仍纳入, 因概念也是链接目标)
    all_names = set()
    for f in notes:
        rel = f.relative_to(VAULT)
        if str(rel).startswith(".git"):
            continue
        all_names.add(f.stem)
    outgoing = defaultdict(set)  # name -> {target basenames}
    missing_fm = 0
    link_re = re.compile(r"\[\[([^\]]+)\]]")
    for f in notes:
        rel = f.relative_to(VAULT)
        if str(rel).startswith(".git"):
            continue
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if not txt.lstrip().startswith("---"):
            missing_fm += 1
        targets = set()
        for m in link_re.findall(txt):
            tgt = m.split("|")[0].split("#")[0].strip()
            if tgt:
                targets.add(tgt)
        outgoing[f.stem] |= targets
    # 断链 + 孤儿
    broken = 0
    broken_samples = []
    incoming = defaultdict(set)
    for name, tgts in outgoing.items():
        for t in tgts:
            if t not in all_names:
                broken += 1
                if len(broken_samples) < 20:
                    broken_samples.append((name, t))
            else:
                incoming[t].add(name)
    orphans = [n for n in all_names if n not in incoming and n in outgoing]
    report = {
        "date": TODAY,
        "total_notes": len(all_names),
        "missing_frontmatter": missing_fm,
        "broken_links": broken,
        "broken_samples": broken_samples[:20],
        "orphan_notes": len(orphans),
    }
    out_path = VAULT / "99_Meta" / "vault_health.md"
    lines = [f"# 全库健康自检\n", f"> 生成: {TODAY}\n"]
    lines.append(f"- 笔记总数(可链接目标): **{report['total_notes']}**")
    lines.append(f"- 缺 frontmatter 笔记: **{report['missing_frontmatter']}**")
    lines.append(f"- 断链(指向不存在笔记的 [[...]]): **{report['broken_links']}**")
    if broken_samples:
        lines.append("\n## 断链样本\n")
        for src, tgt in broken_samples:
            lines.append(f"- `[[{src}]]` -> `[[{tgt}]]` (不存在)")
    lines.append(f"\n- 孤儿笔记(无入链, 仅含出链): **{report['orphan_notes']}**")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    log(f"健康自检: 笔记 {report['total_notes']} | 断链 {report['broken_links']} | "
        f"孤儿 {report['orphan_notes']} | 缺FM {report['missing_frontmatter']} -> {out_path.name}")
    return report


def step_homepage():
    log("刷新 Home.md (实时 git)...")
    rc, out = run_script("homepage_generator.py", timeout=120)
    log(f"homepage 退出码={rc} | {out[-200:]}")
    return rc == 0


def step_git():
    """仅当有改动时 commit + push github。"""
    r = subprocess.run(["git", "status", "--porcelain"], cwd=str(VAULT),
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if not r.stdout.strip():
        log("无改动, 跳过 git 提交。")
        return True
    n = len(r.stdout.strip().splitlines())
    msg = f"chore(self-evolve): 每日自生长 {TODAY} — 概念图谱/交叉链接/门户刷新 ({n} 文件)"
    try:
        subprocess.run(["git", "add", "-A"], cwd=str(VAULT), check=True,
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
        subprocess.run(["git", "commit", "-q", "-m", msg], cwd=str(VAULT), check=True,
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
        log(f"已提交 {n} 个文件。")
        p = subprocess.run(["git", "push", "github", "main"], cwd=str(VAULT),
                           capture_output=True, text=True, encoding="utf-8", errors="ignore")
        if p.returncode == 0:
            log("已推送 github main。")
        else:
            log(f"⚠️ push 失败(可能配额/网络): {p.stderr[-200:]}")
        return True
    except subprocess.CalledProcessError as e:
        log(f"⚠️ git 步骤失败: {e}")
        return False


def main():
    log("=== 自进化编排开始 ===")
    results = {}
    results["compile"] = step_compile_if_new()
    results["grow"] = step_grow()
    results["health"] = step_vault_health()
    results["homepage"] = step_homepage()
    results["git"] = step_git()
    # 写日志
    entry = {"date": TODAY, "time": NOW.isoformat(), "steps": results,
             "log": [m for _, m in log_entries]}
    history = []
    if LOG_FILE.exists():
        try:
            history = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except Exception:
            history = []
    history.append(entry)
    history = history[-60:]  # 保留最近 60 次
    LOG_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"=== 自进化编排结束 | 各步: {results} ===")


if __name__ == "__main__":
    main()
