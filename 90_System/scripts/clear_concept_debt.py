#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""clear_concept_debt.py — 清除 wiki 概念层的自动占位（用户 2026-09-18 指令）。

用户指令: "概念债都先清除掉，等正确的机制验证正确后再重新生成"

清什么（严格界定）:
    只删 `wiki/concepts/*.md` 中 frontmatter 含 `auto: true` 的文件
    —— 即 self_evolve.step_grow_missing_concepts 生成的**空占位**。
    实测 6123 个概念文件里 5940 个 (97.0%) 属此类，内容仅为
    "由 self_evolve 自动生成的占位概念（被引用 N 次，来源尚未成稿）" + "待补充"。

不清什么:
    * 非 auto 的概念（实测 183 个）—— 那是 wiki_compiler 从真实论文里抽的，
      即使命名不好也不是占位，保留。
    * wiki/articles、其他任何目录 —— 一律不动。

前置条件（已在代码层保证）:
    占位生成开关已停用：90_System/research_evolve/state/concept_stub_policy.json
    里 auto_stub_generation=false，self_evolve.step_grow_missing_concepts 会直接返回。
    若不停用，删掉的占位会在下一轮自进化里被**按同样的链接重新生成**。

已知副作用（用户已接受）:
    这些占位正是为了满足"某处 [[链接]] 指向不存在的概念"而生成的，
    删除后那些 [[链接]] 会变成未解析链接（断链）。用户明确要求
    "等正确的机制验证正确后再重新生成"，故接受此中间状态。

用法:
    python clear_concept_debt.py            # 默认 dry-run
    python clear_concept_debt.py --apply    # 打包备份后删除
"""
import json
import sys
import tarfile
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

VAULT = Path(r"D:\Obsidian\vault")
CONCEPTS = VAULT / "wiki" / "concepts"
BACKUP_DIR = Path(r"D:\Obsidian\_backups\concept_debt_20260918")
POLICY = VAULT / "90_System" / "research_evolve" / "state" / "concept_stub_policy.json"
EVOLVE_LOCK = VAULT / "state" / "self_evolve.lock"


def is_auto_stub(p: Path) -> bool:
    """占位判定：只看 frontmatter 前 400 字符里是否有 `auto: true`。"""
    try:
        return "auto: true" in p.read_text(encoding="utf-8", errors="ignore")[:400]
    except Exception:
        return False


def _pid_alive(pid: int) -> bool:
    """Windows 下判断 PID 存活；必须用 tasklist（os.kill(pid,0) 会真的杀进程）。"""
    import subprocess
    try:
        r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="ignore", timeout=20)
        return str(pid) in (r.stdout or "")
    except Exception:
        return False


def self_evolve_running() -> tuple[bool, str]:
    """检查 self_evolve 是否正在跑。

    实测(2026-09-19) 首次执行本脚本时报 FileNotFoundError: 156QubitScale.md ——
    因为 self_evolve 正在**并发写** wiki/concepts（20 分钟写入 384 个文件）。
    在单写者架构下，删除动作必须让路：否则既会与它抢文件，
    又会把删除混进它的下一次提交，无法审计。
    """
    if not EVOLVE_LOCK.exists():
        return False, "无锁文件"
    try:
        info = json.loads(EVOLVE_LOCK.read_text(encoding="utf-8"))
        pid = int(info.get("pid", -1))
        if pid > 0 and _pid_alive(pid):
            return True, f"self_evolve 正在运行 (PID={pid}, 启动于 {info.get('started')})"
        return False, f"锁文件存在但 PID {pid} 已不在"
    except Exception as e:
        return False, f"锁文件不可解析({type(e).__name__})"


def main():
    apply = "--apply" in sys.argv
    force = "--force" in sys.argv

    # 前置检查 0: 单写者 —— self_evolve 在跑时不动概念目录
    running, why = self_evolve_running()
    if running and not force:
        print(f"✗ 拒绝执行: {why}")
        print("  单写者架构下必须让路。等它结束后重跑；确认无碍可加 --force。")
        return 3
    print(f"✓ 单写者检查: {why}")

    # 前置检查 1: 生成开关必须已停用, 否则删了会被重建
    if POLICY.exists():
        pol = json.loads(POLICY.read_text(encoding="utf-8"))
        if pol.get("auto_stub_generation", False):
            print("✗ 拒绝执行: concept_stub_policy.json 里 auto_stub_generation 仍为 true。")
            print("  否则删除的占位会在下一轮自进化中被重新生成。请先改为 false。")
            return 2
        print(f"✓ 前置检查通过: 占位生成已停用（{pol.get('decided_at')} {pol.get('decided_by')}）")
    else:
        print("✗ 拒绝执行: 找不到 concept_stub_policy.json，无法确认生成已停用。")
        return 2

    all_files = sorted(CONCEPTS.glob("*.md"))
    stubs = [p for p in all_files if is_auto_stub(p)]
    stub_set = set(stubs)
    keep = [p for p in all_files if p not in stub_set]

    print(f"\n概念文件总数   : {len(all_files)}")
    print(f"  自动占位(待删): {len(stubs)}  ({100*len(stubs)/max(len(all_files),1):.1f}%)")
    print(f"  非占位(保留)  : {len(keep)}")

    total_bytes = 0
    live_stubs = []
    for p in stubs:
        try:
            total_bytes += p.stat().st_size
            live_stubs.append(p)
        except FileNotFoundError:
            pass  # 并发写入导致消失，跳过（也正是需要让路的原因）
    stubs = live_stubs
    print(f"  待删总字节    : {total_bytes/1024:.0f} KB")

    if not apply:
        print("\n[dry-run] 未删除任何文件。加 --apply 执行（会先打包备份）。")
        return 0

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    tgz = BACKUP_DIR / "concept_stubs_backup.tar.gz"
    print(f"\n打包备份 -> {tgz}")
    with tarfile.open(tgz, "w:gz") as tf:
        for p in stubs:
            tf.add(p, arcname=p.relative_to(VAULT).as_posix())
    print(f"  备份体积: {tgz.stat().st_size/1024:.0f} KB")

    manifest = {"generated": datetime.now().isoformat(),
                "reason": "用户指令: 概念债先清除, 待正确机制验证后再生成",
                "criteria": "wiki/concepts/*.md with frontmatter 'auto: true'",
                "policy": str(POLICY.relative_to(VAULT)),
                "backup": str(tgz),
                "before": {"total": len(all_files), "stubs": len(stubs), "kept": len(keep)},
                "deleted": []}

    deleted = failed = 0
    for p in stubs:
        try:
            sz = p.stat().st_size
            p.unlink()
            manifest["deleted"].append(
                {"path": p.relative_to(VAULT).as_posix(), "bytes": sz})
            deleted += 1
        except Exception as e:
            failed += 1
            print(f"  删除失败 {p.name}: {e}")

    after = len(list(CONCEPTS.glob("*.md")))
    manifest["after"] = {"total": after}
    (BACKUP_DIR / "MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n已删除 {deleted} 个占位（失败 {failed}）")
    print(f"概念文件: {len(all_files)} -> {after}")
    print(f"备份   : {tgz}")
    print(f"清单   : {BACKUP_DIR / 'MANIFEST.json'}")
    print(f"回滚   : tar -xzf \"{tgz}\" -C \"{VAULT}\"")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
