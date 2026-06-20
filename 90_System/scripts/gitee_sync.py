#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gitee 三平台同步 — 跨平台入口脚本
适用于: Genspark / Claw Computer / 任意 Linux/macOS/WSL 环境

用法:
  python gitee_sync.py              # 完整同步 (pull → commit → push)
  python gitee_sync.py --status     # 仅查看状态
  python gitee_sync.py --dry-run    # 预览不执行
"""

import os, sys, json, subprocess
from pathlib import Path
from datetime import datetime

REPO_URL = "https://gitee.com/iBrainNest/i-nest.git"
BRANCH = "main"
REPO_DIR = Path.home() / "i-nest-sync"

# ---- 内容分类 ----
CATEGORY_MAP = {
    "代码":     ["**/iNEST_4_工程开发/**", "**/TCC_4_工程开发/**", "scripts/**", "skills/**", "copilot/**"],
    "论文":     ["papers/**", "**/iNEST_2_论文撰写/**", "**/TCC_2_论文撰写/**"],
    "专利":     ["**/iNEST_3_专利撰写/**", "**/TCC_3_专利撰写/**"],
    "知识库":   ["knowledge_graph/**", "01_MOC/**", "03_Topics/**", "99_Journal/**"],
    "仿真":     ["simulation/**"],
    "灵感":     ["iNEST_灵感池/**", "00_Inbox/**"],
}

def run(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.stdout.strip(), result.returncode

def init():
    if not (REPO_DIR / ".git").exists():
        print(f"首次运行，克隆仓库到 {REPO_DIR}...")
        REPO_DIR.parent.mkdir(parents=True, exist_ok=True)
        out, code = run(f'git clone {REPO_URL} "{REPO_DIR}"')
        if code != 0:
            print(f"克隆失败: {out}")
            sys.exit(1)
        print("克隆完成")
    os.chdir(REPO_DIR)
    run(f"git checkout {BRANCH}")

def sync():
    print("\n========== Gitee 同步 ==========")
    init()

    # 1. Fetch
    print("Step 1/4: 获取远程更新...")
    run("git fetch origin " + BRANCH)
    behind, _ = run(f"git rev-list --count HEAD..origin/{BRANCH}")
    behind = int(behind or 0)

    # 2. Pull
    if behind > 0:
        print(f"Step 2/4: 远程有 {behind} 个新提交，拉取中...")
        out, code = run(f"git pull origin {BRANCH} --no-rebase")
        if code != 0:
            run("git stash")
            run(f"git pull origin {BRANCH} --no-rebase")
            run("git stash pop")
        print("远程更新已合并")
    else:
        print("Step 2/4: 远程无新内容")

    # 3. Detect
    print("Step 3/4: 检测本地变更...")
    status, _ = run("git status --porcelain")
    lines = [l for l in status.split('\n') if l.strip()]
    
    if not lines:
        print("没有本地变更，同步完成")
        return

    added = [l[3:] for l in lines if l[:2].strip() in ('??', 'A')]
    modified = [l[3:] for l in lines if 'M' in l[:2]]
    deleted = [l[3:] for l in lines if 'D' in l[:2]]

    # 分类
    stats = {}
    for f in added + modified:
        cat = "其他"
        for c, patterns in CATEGORY_MAP.items():
            import fnmatch
            for p in patterns:
                if fnmatch.fnmatch(f.replace('\\', '/'), p.replace('\\', '/')):
                    cat = c
                    break
            if cat != "其他":
                break
        stats[cat] = stats.get(cat, 0) + 1

    print(f"\n  新增: {len(added)}  修改: {len(modified)}  删除: {len(deleted)}")
    for cat, cnt in sorted(stats.items()):
        print(f"  [{cat}] {cnt} 个文件")
    
    if "--status" in sys.argv or "--dry-run" in sys.argv:
        if "--status" in sys.argv:
            print("\n详细变更:")
            for f in sorted(added): print(f"  + {f}")
            for f in sorted(modified): print(f"  ~ {f}")
            for f in sorted(deleted): print(f"  - {f}")
        return

    # 4. Commit & Push
    parts = [f"[{c}]{n}" for c, n in sorted(stats.items())]
    msg = f"sync: {' '.join(parts)} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    print(f"\nStep 4/4: 提交 ({msg})")
    
    run("git add -A")
    run(f'git commit -m "{msg}"')
    out, code = run(f"git push origin {BRANCH}")
    
    if code == 0:
        hash_out, _ = run("git rev-parse --short HEAD")
        print(f"\n========== 同步成功 ==========")
        print(f"  提交: {msg}")
        print(f"  哈希: {hash_out}")
        print(f"  文件: {len(added)+len(modified)} 个")
    else:
        print(f"\n推送失败: {out}")

if __name__ == "__main__":
    if "--status" in sys.argv:
        sys.argv.append("--dry-run")
    sync()
