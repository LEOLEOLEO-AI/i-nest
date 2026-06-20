#!/usr/bin/env python3
"""
Vault重组脚本 v2 — 展开式逐文件迁移
"""
import os, shutil, re
from pathlib import Path

VAULT = Path("/home/work/obsidian-vault")

NEW_DIRS = [
    "NCC计算范式/01_论文",
    "NCC计算范式/02_专利",
    "NCC计算范式/03_项目策划",
    "NCC计算范式/04_产品与原型",
    "NCC计算范式/05_关键技术",
    "智能涌现范式/01_论文",
    "智能涌现范式/02_专利",
    "智能涌现范式/03_项目策划",
    "智能涌现范式/04_产品与原型",
    "智能涌现范式/05_关键技术",
    "Inbox/NCC计算范式",
    "Inbox/智能涌现范式",
    "Inbox/待分类",
    "Journal",
    "Projects",
    "99-Attachments",
    "99-Templates",
]

# 系统目录：不动
SKIP = {".git", ".obsidian", ".smart-env", ".openclaw",
        "99-Attachments", "99-Templates",
        "NCC计算范式", "智能涌现范式", "Inbox", "Journal", "Projects",
        "reorganize.py"}

# 根目录保留的系统文件
ROOT_KEEP = {"AGENTS.md","HEARTBEAT.md","IDENTITY.md","SOUL.md",
             "TOOLS.md","USER.md",".kb_sync_state.json","reorganize.py"}

# ── 分类函数 ──────────────────────────────────────────────
def classify(rel: str) -> str:
    """根据相对路径判断目标目录"""
    r = rel.replace("\\", "/")
    n = Path(r).name.lower()

    # ── 附件/图片（最高优先级，先判断）
    if r.startswith("02_Papers_论文/Figures"): return "99-Attachments/论文图表"
    if "海河实验室" in r and "Figures" in r: return "99-Attachments/项目图表"

    # ── NCC计算范式 论文
    NCC_paper_kw = ["sdi","ncc","p-mapping","route-transform","uccp",
                    "b组_sdi","b7_","b2_","b5_","b3_","论文a_","论文b_","论文c_",
                    "p1_","p2_","p3_","p4_","ncc_专利",
                    "00_专利清单","00_论文总清单","论文计划"]
    if any(k in n for k in NCC_paper_kw): return "NCC计算范式/01_论文"
    if r.startswith("02_Papers_论文/B组"): return "NCC计算范式/01_论文"
    if r.startswith("02_Papers_论文/NCC_专利"): return "NCC计算范式/02_专利"

    # ── NCC计算范式 专利
    if "专利" in n and any(k in n for k in ["p1","p2","p3","p4","ncc"]): return "NCC计算范式/02_专利"

    # ── NCC计算范式 项目策划
    NCC_proj_kw = ["海河实验室","nsfc","基金委","ncc_专项","重大专项",
                   "集成电路","换道超车"]
    if any(k in n for k in NCC_proj_kw): return "NCC计算范式/03_项目策划"
    if r.startswith("05_Projects_项目/海河"): return "NCC计算范式/03_项目策划"
    if r.startswith("05_Projects_项目/NSFC"): return "NCC计算范式/03_项目策划"
    if r.startswith("05_Projects_项目/基金委"): return "NCC计算范式/03_项目策划"
    if r.startswith("05_Projects_项目/发改委_集成电路"): return "NCC计算范式/03_项目策划"

    # ── NCC计算范式 产品原型
    if "inest_mvp" in n or "mvp" in n: return "NCC计算范式/04_产品与原型"

    # ── NCC计算范式 关键技术/代码
    NCC_tech_kw = ["nano_sdio","ncc_comprehensive","uccp","collective_comm",
                   "trae_bridge","wiki_gen","get_import","kb_engine",
                   "idea_sdi","simulator","make_","gen_figure","audit",
                   "cst_40_","full_8comp","x4_normal","uccp_final","uccp_full"]
    if any(k in n for k in NCC_tech_kw): return "NCC计算范式/05_关键技术"
    if r.startswith("04_Code_代码"): return "NCC计算范式/05_关键技术"

    # ── 智能涌现范式 论文
    CST_kw = ["cst_intelligence","cst_theory","v22","v23","v24","v25",
              "cst六阈值","a组_cst","智能涌现","intelligence_emergence",
              "engineering_format","idea_ann","idea_tau","idea_the_one",
              "cst_40","full_8","make_engineering","make_uccp"]
    if any(k in n for k in CST_kw): return "智能涌现范式/01_论文"
    if r.startswith("02_Papers_论文/A组"): return "智能涌现范式/01_论文"

    # ── 智能涌现范式 项目策划
    if "卫星" in n or "ooda" in n: return "智能涌现范式/03_项目策划"
    if r.startswith("05_Projects_项目/卫星"): return "智能涌现范式/03_项目策划"

    # ── Projects（跨范式）
    PROJ_kw = ["发改委","项目布局","专项时间点","双轨战略","折子","立项"]
    if any(k in n for k in PROJ_kw): return "Projects"
    if r.startswith("05_Projects_项目/发改委"): return "Projects"
    if r.startswith("05_Projects_项目/项目布局"): return "Projects"

    # ── Journal（日记 / 会议 / 工作日志）
    JOUR_kw = ["日记","diary","会议","meeting","2026-04"]
    if any(k in n for k in JOUR_kw): return "Journal"
    if re.match(r"^\d{4}-\d{2}-\d{2}\.md$", Path(r).name): return "Journal"

    # ── Inbox NCC
    INBOX_NCC_kw = ["dtco","stco","tpu","集合通信","ccpu","ccu","晶圆",
                    "fpga","aegis","备胎","台积电","copos","hnlpu",
                    "synchron","ai网络","为什么说","copyнcc","copyncc",
                    "ncc-ltc","全球pnn","liquid","类脑动态","阿里给cpo",
                    "从dtco","从晶圆","集合通信处理器"]
    if any(k in n for k in INBOX_NCC_kw): return "Inbox/NCC计算范式"

    # ── Inbox 智能涌现
    INBOX_CST_kw = ["海马","位置细胞","时间细胞","神经信息学","自主系统",
                    "物理人工智能","physical ai","集智","复杂系统","涌现",
                    "计算神经","结构模仿"]
    if any(k in n for k in INBOX_CST_kw): return "Inbox/智能涌现范式"

    # ── Inbox 待分类
    INBOX_OTHER_kw = ["obsidian","无标题","网页无法","全网疯传","知识库搭建",
                      "修改方法","指令","fix_gitee","init_vault","未命名",
                      "本地数据库","base","指南","索引","术语","文档依赖",
                      "配置与工作流","get笔记"]
    if any(k in n for k in INBOX_OTHER_kw): return "Inbox/待分类"
    if n.endswith(".bat") or n.endswith(".base") or n.endswith(".canvas"):
        return "Inbox/待分类"

    # 其余Papers/Projects/代码默认
    if r.startswith("02_Papers_论文"): return "NCC计算范式/01_论文"
    if r.startswith("05_Projects_项目"): return "Projects"

    return "Inbox/待分类"


def safe_dest(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    for i in range(2, 100):
        candidate = dest.parent / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
    return dest.parent / f"{stem}_dup{suffix}"


def collect_items():
    """收集所有需要迁移的叶节点文件和目录"""
    items = []
    # 已处理过的目录（子项不重复处理）
    handled = set()

    # 遍历根目录一级
    for item in sorted(VAULT.iterdir()):
        name = item.name
        if name in SKIP or name in ROOT_KEEP or name.startswith("."):
            continue
        rel = str(item.relative_to(VAULT))
        dest_dir = classify(rel)
        dest = VAULT / dest_dir / item.name

        # 如果是整个目录需要整体移动到同一目标
        if item.is_dir():
            # 检查目录下的文件是否都去同一个目标
            sub_items = list(item.rglob("*"))
            sub_files = [x for x in sub_items if x.is_file()]
            if not sub_files:
                continue
            # 对每个文件单独分类
            sub_dests = set()
            for sf in sub_files:
                srel = str(sf.relative_to(VAULT))
                sub_dests.add(classify(srel))

            if len(sub_dests) == 1:
                # 整个目录同一目标 → 整体移动
                items.append(("DIR", item, VAULT / list(sub_dests)[0] / item.name))
                handled.add(str(item))
            else:
                # 目录内文件去不同目标 → 逐文件
                for sf in sub_files:
                    srel = str(sf.relative_to(VAULT))
                    sd = classify(srel)
                    items.append(("FILE", sf, VAULT / sd / sf.name))
                    handled.add(str(item))
        else:
            items.append(("FILE", item, dest))

    return items


if __name__ == "__main__":
    import sys
    dry = "--run" not in sys.argv

    # 创建目录
    for d in NEW_DIRS:
        (VAULT / d).mkdir(parents=True, exist_ok=True)

    items = collect_items()

    print(f"{'[DRY RUN] ' if dry else ''}迁移计划 ({len(items)} 项)\n")
    for kind, src, dest in items:
        print(f"  {'📁' if kind=='DIR' else '📄'} {src.relative_to(VAULT)}")
        print(f"     → {dest.relative_to(VAULT)}")

    if dry:
        print(f"\n[DRY RUN] 共 {len(items)} 项。确认无误后运行 --run 执行。")
        sys.exit(0)

    print("\n=== 执行 ===")
    ok = err = 0
    for kind, src, dest in items:
        if not src.exists():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest = safe_dest(dest)
        try:
            shutil.move(str(src), str(dest))
            print(f"  ✓ → {dest.relative_to(VAULT)}")
            ok += 1
        except Exception as e:
            print(f"  ✗ {src.name}: {e}")
            err += 1

    # 清理空目录
    for d in sorted(VAULT.rglob("*"), key=lambda x: len(x.parts), reverse=True):
        if d.is_dir() and d.parts[len(VAULT.parts)] not in SKIP and not any(d.iterdir()):
            try: d.rmdir()
            except: pass

    print(f"\n✅ 完成：{ok} 成功，{err} 失败")
