# -*- coding: utf-8 -*-
"""
vault_restructure.py — 知识库目录重组（合并 / 精简 / 结构去重）

设计原则（对齐 Karpathy LLM-Wiki 自进化框架）:
  源材料层(只读) → 编译知识层(wiki/, 自动生成) → 产出层(50_Output/)

安全约束（硬性，不可绕过）:
  1. 绝不删除任何含文件的目录；只有"递归为空"的目录才可删
  2. 移动采用合并语义；目标同名文件存在且内容不同时，加 __dupN 后缀保留，绝不覆盖
  3. 全程 DRY RUN 优先，--apply 才真正执行
  4. 运行时基础设施目录 (raw/ logs/ state/ knowledge_graph/) 列入保护名单，永不触碰
"""
import sys
import shutil
import hashlib
from pathlib import Path

VAULT = Path(r"D:/obsidian/vault")
APPLY = "--apply" in sys.argv

# 运行时基础设施：被 import_processor / pipeline_guard / pipeline_v3 等硬引用，永不移动
PROTECTED = {"raw", "logs", "state", "knowledge_graph", ".git", ".obsidian",
             ".workbuddy", "wiki", "node_modules"}

# 扫描空目录时需跳过的第三方/缓存目录
SKIP_SCAN = {".git", ".obsidian", ".workbuddy", "node_modules", "__pycache__",
             ".venv", "venv", "_vendor", "site-packages"}

actions = []


def log(kind, msg):
    actions.append((kind, msg))
    print(f"[{kind}] {msg}", flush=True)


def md5(p):
    try:
        return hashlib.md5(p.read_bytes()).hexdigest()
    except Exception:
        return None


def merge_dir(src_rel, dst_rel):
    """把 src 目录内容合并进 dst，逐文件搬运；同名同内容跳过，同名异内容保留副本。"""
    src, dst = VAULT / src_rel, VAULT / dst_rel
    if not src.exists():
        log("SKIP", f"源不存在: {src_rel}")
        return
    files = [f for f in src.rglob("*") if f.is_file()]
    if not files:
        log("SKIP", f"源为空(交由空目录清理处理): {src_rel}")
        return
    log("MERGE", f"{src_rel}  →  {dst_rel}   ({len(files)} 文件)")
    for f in files:
        rel = f.relative_to(src)
        target = dst / rel
        if target.exists():
            if md5(f) == md5(target):
                log("  dup-same", f"内容一致，丢弃源副本: {rel.as_posix()}")
                if APPLY:
                    f.unlink()
                continue
            n = 1
            while True:
                cand = target.with_name(f"{target.stem}__dup{n}{target.suffix}")
                if not cand.exists():
                    target = cand
                    break
                n += 1
            log("  dup-diff", f"同名异内容，另存: {target.relative_to(VAULT).as_posix()}")
        if APPLY:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(target))


def purge_empty_dirs(keep_gitkeep):
    """自底向上删除递归为空的目录；语义骨架目录改为写入 .gitkeep 保留。"""
    removed, kept = [], []
    while True:
        # 每轮重新扫描，处理"删掉子目录后父目录变空"的级联情况
        cands = []
        for d in VAULT.rglob("*"):
            if not d.is_dir():
                continue
            parts = d.relative_to(VAULT).parts
            if any(s in parts for s in SKIP_SCAN):
                continue
            if parts and parts[0] in PROTECTED:
                continue
            if not any(f.is_file() for f in d.rglob("*")):
                cands.append(d)
        if not cands:
            break
        progressed = False
        for d in sorted(cands, key=lambda x: -len(x.parts)):
            if not d.exists():
                continue
            rel = d.relative_to(VAULT).as_posix()
            if any(rel == k or rel.startswith(k + "/") for k in keep_gitkeep):
                # 语义骨架：保留目录本体，写 .gitkeep 占位
                if rel in keep_gitkeep:
                    kept.append(rel)
                    if APPLY:
                        (d / ".gitkeep").write_text("", encoding="utf-8")
                    progressed = True
                continue
            removed.append(rel)
            if APPLY:
                shutil.rmtree(d, ignore_errors=True)
            progressed = True
        if not APPLY or not progressed:
            break
    return removed, kept


def main():
    mode = "APPLY 实际执行" if APPLY else "DRY RUN 演练(不改动任何文件)"
    print("=" * 72)
    print(f"知识库目录重组 — {mode}")
    print("=" * 72)

    # ---------- 阶段 1: 编号撞车修复 ----------
    print("\n【阶段 1】编号撞车修复 —— 40_iNEST 混入 TCC 编号 / 43&44 双撞车\n")
    # TCC 的 3x 编号错放进 iNEST，归位到 4x
    merge_dir("40_iNEST/31_Theory/01_论文", "40_iNEST/41_Theory/01_论文")
    merge_dir("40_iNEST/31_Theory", "40_iNEST/41_Theory")
    # 43 撞车：43_Engineering(2个 .v 硬件源码) 并入 43_Engineering
    merge_dir("40_iNEST/43_Engineering", "40_iNEST/43_Engineering")
    # 44 撞车：44_Dev 为空，交由空目录清理
    # iNEST 侧 Papers 归入 41_Theory/01_论文
    merge_dir("40_iNEST/Papers", "40_iNEST/41_Theory/01_论文")

    # ---------- 阶段 2: 自嵌套拍平 + 同义目录合并 ----------
    print("\n【阶段 2】自嵌套拍平 + 中文/编号同义目录合并\n")
    merge_dir("50_Output/Reports/Reports", "50_Output/Reports")
    merge_dir("40_iNEST/44_Projects/Projects", "40_iNEST/44_Projects")
    merge_dir("30_TCC/31_Theory/_attachments/01_论文/01_论文",
              "30_TCC/31_Theory/_attachments/01_论文")
    # 同义：无编号「论文」并入规范的「01_论文」
    merge_dir("30_TCC/31_Theory/论文", "30_TCC/31_Theory/01_论文")
    merge_dir("40_iNEST/41_Theory/论文", "40_iNEST/41_Theory/01_论文")
    # TCC 侧散落 Papers / Code 归位
    merge_dir("30_TCC/Papers", "30_TCC/31_Theory/01_论文")
    merge_dir("30_TCC/Code", "30_TCC/33_Engineering")

    # ---------- 阶段 3: 原型产品层 ----------
    print("\n【阶段 3】建立 50_Output/56_Prototypes 原型产品层\n")
    proto = VAULT / "50_Output" / "56_Prototypes"
    log("MKDIR", "50_Output/56_Prototypes")
    if APPLY:
        proto.mkdir(parents=True, exist_ok=True)
    merge_dir("40_iNEST/44_Projects/investor_demo",
              "50_Output/56_Prototypes/iNEST_investor_demo")
    merge_dir("70_Dashboard/investor",
              "50_Output/56_Prototypes/dashboard_investor")

    # ---------- 阶段 4: 空目录清理 ----------
    print("\n【阶段 4】空目录清理（语义骨架保留 .gitkeep）\n")
    # 语义骨架：属于既定编号契约的位，保留占位维持结构完整性
    keep = {
        "30_TCC/31_Theory/01_论文", "30_TCC/31_Theory/02_Analysis",
        "30_TCC/31_Theory/03_Inbox_文献与碎片", "30_TCC/31_Theory/05_关键技术",
        "30_TCC/35_Simulation/01_论文",
        "40_iNEST/41_Theory/01_论文", "40_iNEST/41_Theory/03_项目策划",
        "40_iNEST/44_Projects/99_参考资料", "40_iNEST/45_Simulation/99_参考资料",
        "50_Output/51_Papers/B组_SDI-CC互连体系", "50_Output/56_Prototypes",
    }
    removed, kept = purge_empty_dirs(keep)
    print(f"\n  将删除空目录: {len(removed)} 个")
    for r in removed[:40]:
        print(f"    - {r}")
    if len(removed) > 40:
        print(f"    ... 其余 {len(removed)-40} 个省略")
    print(f"\n  保留并写入 .gitkeep 的语义骨架: {len(kept)} 个")
    for k in sorted(kept):
        print(f"    + {k}")

    print("\n" + "=" * 72)
    print(f"完成 — {mode} | 动作总数 {len(actions)} | 删空目录 {len(removed)} | 骨架占位 {len(kept)}")
    if not APPLY:
        print("这是演练。确认无误后加 --apply 参数真正执行。")
    print("=" * 72)


if __name__ == "__main__":
    main()
