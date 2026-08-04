# -*- coding: utf-8 -*-
"""
self_evolve.py — 知识库自进化 / 自生长 编排器 (Karpathy LLM-Wiki 风格)

设计目标: 可无人值守、可每日定时运行、不失控、幂等、失败不破坏数据。

执行链:
  1. 增量编译 raw/新来源 -> wiki (仅当存在未处理文件时调用 LLM, 带超时与失败隔离)
  2. wiki_grow: 概念图谱交叉链接 + 去重 + 刷新 index/backlinks/health (纯本地)
  3. 全库轻量健康自检 (断链/孤儿/缺 frontmatter, 纯本地无 LLM) -> 99_Meta/vault_health.md
  4. 自我生长: 补全高频缺失概念占位 (纯本地无 LLM)
  5. Phase4 自进化引擎: import_processor/task_recommender/research_evolution/cross_domain_insight
     (隔离+超时, 单步失败不影响其余; 产出 task_recommendations/evolution_report/cross_domain_insights)
  6. 刷新 Home.md (实时 git 状态 + 仪表盘数据)
  7. git add + commit + push github (仅当有改动)

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
    """运行 wiki_compiler (状态化/增量): 无新来源时仅做健康检查, 不调 LLM。

    wiki_compiler 内部用自身的 state 判断是否有未处理来源, 安全幂等,
    因此这里直接调用, 不必在编排层重复扫描。
    """
    log("运行 wiki_compiler (增量; 无新来源则仅健康检查, 不消耗 LLM)...")
    # 大积压时每篇约 5s, 300s 远不够; 提到 3600s 安全裕量
    rc, out = run_script("wiki_compiler.py", timeout=3600)
    log(f"wiki_compiler 退出码={rc} | {out[-300:]}")
    return rc == 0


def step_grow():
    log("运行 wiki_grow 交叉链接/去重...")
    rc, out = run_script("wiki_grow.py", timeout=300)
    log(f"wiki_grow 退出码={rc} | {out[-300:]}")
    return rc == 0


def extract_aliases(txt):
    """轻量解析 frontmatter 的 aliases: 列表(无需 yaml 依赖)。"""
    als = []
    if not txt.startswith("---"):
        return als
    end = txt.find("\n---", 3)
    if end == -1:
        return als
    fm = txt[3:end]
    in_alias = False
    for ln in fm.split("\n"):
        s = ln.strip()
        if s.startswith("aliases:"):
            in_alias = True
            continue
        if in_alias:
            if s.startswith("- "):
                v = s[2:].strip().strip('"').strip("'")
                if v:
                    als.append(v)
            elif s and not s.startswith("#"):
                in_alias = False
    return als


def analyze_links():
    """纯本地扫描全库链接, 返回解析集合与断链频率。无 LLM。

    链接解析贴近 Obsidian: 裸链接/路径链接/附件链接/文件夹链接, 以及
    frontmatter 中的 aliases: 别名解析。
    """
    note_basenames = set()
    note_paths = set()      # 相对路径(去 .md)
    file_paths = set()      # 所有文件相对路径(去扩展名 + 带扩展名)
    dirs = set()
    aliases = set()         # 各笔记 frontmatter 中的别名(也参与解析)
    link_re = re.compile(r"\[\[([^\]]+)\]]")
    for f in VAULT.rglob("*"):
        rel = f.relative_to(VAULT).as_posix()
        if rel.startswith(".git"):
            continue
        if f.is_dir():
            dirs.add(rel)
            continue
        if f.is_file():
            noext = rel[:-len(f.suffix)] if f.suffix else rel
            file_paths.add(rel)        # 带扩展名 (附件/路径+扩展名链接)
            file_paths.add(noext)      # 去扩展名 (路径式链接)
            if f.suffix.lower() == ".md":
                note_paths.add(noext)  # 路径式笔记链接
                note_paths.add(rel)    # [[Note.md]] 形式
                note_basenames.add(f.stem)
    missing_fm = 0
    outgoing = defaultdict(set)   # note basename -> {targets}
    for f in VAULT.rglob("*.md"):
        rel = f.relative_to(VAULT).as_posix()
        if rel.startswith(".git"):
            continue
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if not txt.lstrip().startswith("---"):
            missing_fm += 1
        else:
            for a in extract_aliases(txt):
                aliases.add(a)
        for m in link_re.findall(txt):
            raw = m.replace("\\|", "|")          # Obsidian 转义别名分隔符 [[A\|B]]
            tgt = raw.split("|")[0].split("#")[0].strip().rstrip("\\").strip()
            if tgt:
                outgoing[f.stem].add(tgt)
    broken_freq = defaultdict(int)   # 断链目标 -> 被引用次数
    incoming = defaultdict(set)
    for name, tgts in outgoing.items():
        for t in tgts:
            ok = (t in note_basenames) or (t in note_paths) or \
                 (t in file_paths) or (t in dirs) or (t in aliases)
            if ok and (t in note_basenames or t in note_paths):
                incoming[t].add(name)
            if not ok and not t.isdigit():   # 纯数字链接(列表/脚注) 非真实断链, 不计
                broken_freq[t] += 1
    orphans = [n for n in note_basenames if n not in incoming]
    return note_basenames, note_paths, file_paths, dirs, broken_freq, orphans, missing_fm


def step_vault_health():
    """纯本地全库健康自检: 断链 / 孤儿 / 缺 frontmatter。无 LLM。

    链接解析规则(贴近 Obsidian):
      - 裸链接 [[Name]]  -> 解析为任意同名笔记 basename
      - 路径链接 [[a/b/Name]] -> 解析为相对路径(去扩展名)存在的文件
      - 附件链接 [[x.json]]/[[x.py]] 等 -> 若文件存在则合法
      - 文件夹链接 [[Folder]] -> 若匹配目录则合法
    仅上述均不匹配才计为真正断链。
    """
    log("运行全库健康自检 (纯本地, 贴近 Obsidian 链接解析)...")
    nb, np_, fp, dirs, broken_freq, orphans, missing_fm = analyze_links()
    broken = sum(broken_freq.values())
    broken_samples = sorted(broken_freq.items(), key=lambda x: -x[1])[:25]
    report = {
        "date": TODAY,
        "total_notes": len(nb),
        "missing_frontmatter": missing_fm,
        "broken_links": broken,
        "broken_samples": broken_samples,
        "orphan_notes": len(orphans),
    }
    out_path = VAULT / "99_Meta" / "vault_health.md"
    lines = [f"# 全库健康自检\n", f"> 生成: {TODAY}  ·  链接解析贴近 Obsidian 行为\n"]
    lines.append(f"- 笔记总数(可链接目标): **{report['total_notes']}**")
    lines.append(f"- 缺 frontmatter 笔记: **{report['missing_frontmatter']}**")
    lines.append(f"- 真正断链(目标不存在): **{report['broken_links']}**")
    if broken_samples:
        lines.append("\n## 断链样本(按被引用次数排序, 优先补全)\n")
        for tgt, c in broken_samples:
            lines.append(f"- (×{c}) `[[{tgt}]]`")
    lines.append(f"\n- 孤儿笔记(无入链): **{report['orphan_notes']}**")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    log(f"健康自检: 笔记 {report['total_notes']} | 真正断链 {report['broken_links']} | "
        f"孤儿 {report['orphan_notes']} | 缺FM {report['missing_frontmatter']} -> {out_path.name}")
    return report, broken_freq


# 明显非"概念"、不应自动补全为笔记的链接词(多为插件/UI 伪链接)
DENY_CONCEPT = {
    # Obsidian UI / 插件残留
    "双向链接", "嵌入", "标签", "附件", "看板", "图谱", "关系",
    "反链", "出链", "引用", "链接", "笔记", "标签", "搜索",
    "TOOLS", "Files", "Recent", "On Drop", "Stub", "undefined",
    "true", "false", "null", "none", "wikilinks", "arxiv-index",
    # 非概念的无意义碎片
    "笔记标题", "待分类", "资料分享", "PPT", "Slide1", "论文",
    "5期内容", "300″", "Brainnews", "算力网络", "对外展示",
    "getnote", "gsk", "01_论文",
    # 文献检索工具/数据库名(非研究概念)
    "arXiv", "PubMed", "IEEE Xplore", "Google Scholar", "Web of Science",
    # 通用期刊名(非论文本体)
    "Nature Electronics", "《中国科学基金》", "Nature Communications", "Nature Neuroscience",
    "美国国家科学院院刊 (PNAS)", "w3cschool",
}
# 概念名正则拒绝模式(优先级高于 DENY_CONCEPT 的字面匹配)
DENY_CONCEPT_RE = re.compile(
    r'^(\d{1,3}|[A-Z]{2,8}|[a-z_]+|getnote|gsk|_dup\d*)$'
    r'|三原则|全景导航|Map of Content|_dup\d*$'
    r'|w3cschool'
)


def step_grow_missing_concepts(broken_freq, max_new=10, min_refs=3):
    """自我生长: 为高频被引用却不存在的裸概念名自动生成占位笔记。

    仅处理: 裸笔记名(无 / \\ 与扩展名)、长度 2-50、被引用≥min_refs、
    不在 DENY_CONCEPT、且库内尚未存在。每轮最多 max_new 篇, 防止爆炸。
    生成的占位笔记带 frontmatter + 回链来源, 下一轮 wiki_grow 会自动交叉链接。
    """
    log("自我生长: 补全高频缺失概念占位笔记...")
    created = []
    out_dir = VAULT / "wiki" / "concepts"
    out_dir.mkdir(parents=True, exist_ok=True)
    nb, np_, fp, dirs, _, _, _ = analyze_links()
    candidates = []
    for tgt, c in broken_freq.items():
        if c < min_refs:
            continue
        if "/" in tgt or "\\" in tgt:        # 路径式链接, 非裸概念
            continue
        if "." in tgt:                        # 附件/带扩展名, 跳过
            continue
        if not (2 <= len(tgt) <= 50):
            continue
        if tgt.isdigit():          # 纯数字链接(footnote/列表) 非概念, 跳过
            continue
        if tgt in DENY_CONCEPT:
            continue
        if "日记" in tgt or "全景导航" in tgt or "Map of Content" in tgt:
            continue  # 导航/MOC/日记页, 非概念, 跳过
        if DENY_CONCEPT_RE.search(tgt):
            continue  # 正则模式拒绝(纯数字/全大写缩写/垃圾词)
        if tgt in nb or tgt in np_ or tgt in fp or tgt in dirs:
            continue
        candidates.append((tgt, c))
    candidates.sort(key=lambda x: -x[1])
    for tgt, c in candidates[:max_new]:
        # 文件名净化(Obsidian 不允许 : / \ 等)
        safe = re.sub(r'[:/\\*?"<>|#^\[\]]', "_", tgt).strip()
        if not safe:
            continue
        path = out_dir / f"{safe}.md"
        if path.exists():
            continue
        # 找最多 6 个引用来源
        sources = []
        for f in VAULT.rglob("*.md"):
            rel = f.relative_to(VAULT).as_posix()
            if rel.startswith(".git"):
                continue
            try:
                txt = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if tgt in txt:
                sources.append(f.stem)
                if len(sources) >= 6:
                    break
        alias_line = f'aliases:\n- "{tgt}"\n' if safe != tgt else ""
        body = [f"---\nprovenance: derived\ntype: concept-stub\nauto: true\n"
                f"created: {TODAY}\nrefs: {len(sources)}\n" + alias_line + "---\n",
                f"# {tgt}\n",
                f"> 由 self_evolve 自动生成的占位概念（被引用 {c} 次，来源尚未成稿）。\n"]
        if sources:
            body.append("\n## 引用来源\n")
            for s in sources:
                body.append(f"- [[{s}]]")
        body.append("\n\n_待补充：定义、与 iNEST/TCC 体系的关系、关键文献。_")
        path.write_text("\n".join(body), encoding="utf-8")
        created.append(tgt)
    if created:
        log(f"已补全 {len(created)} 个缺失概念: {created}")
    else:
        log("无新的缺失概念需补全(或已达上限/已有)。")
    return created


def step_phase4():
    """运行 Phase 4 自进化引擎 (隔离+超时, 单步失败不影响其余)。

    产出:
      - wiki/task_recommendations.md   (task_recommender)
      - wiki/evolution_report.md        (research_evolution)
      - wiki/cross_domain_insights.md   (cross_domain_insight)
      - import_processor: 监控 Genspark/得到大脑/Codex 新导入并归入待编译
    均为纯本地启发式脚本(无 LLM、无破坏性操作), 安全纳入每日循环。
    """
    log("运行 Phase 4 自进化引擎 (import/task/evolution/cross-domain)...")
    steps = {
        "import_processor": ("import_processor.py", 120),
        "task_recommender": ("task_recommender.py", 180),
        "research_evolution": ("research_evolution.py", 180),
        "cross_domain_insight": ("cross_domain_insight.py", 180),
    }
    results = {}
    for name, (rel, to) in steps.items():
        rc, out = run_script(rel, timeout=to)
        results[name] = rc == 0
        log(f"{name} 退出码={rc} | {out[-200:]}")
    return results


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
        # 精确添加预期变更目录, 避免 git add -A 吞入 AI 工具残留
        add_dirs = ["wiki/", "60_MOC/", "70_Dashboard/", "99_Meta/", "state/",
                    "Home.md", "00_Inbox/", "logs/", "30_TCC/", "40_iNEST/",
                    "50_Output/", "80_Archive/", "raw/", "knowledge_graph/"]
        subprocess.run(["git", "add", "--"] + add_dirs, cwd=str(VAULT), check=True,
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
        subprocess.run(["git", "commit", "-q", "-m", msg], cwd=str(VAULT), check=True,
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
        log(f"已提交 {n} 个文件。")
        p = subprocess.run(["git", "push", "github", "main"], cwd=str(VAULT),
                           capture_output=True, text=True, encoding="utf-8", errors="ignore")
        if p.returncode == 0:
            log("已推送 github main。")
        else:
            # non-fast-forward 恢复: 远端有新提交时 pull 后重推
            log(f"push 失败, 尝试 pull --no-rebase 后重推: {p.stderr[-200:]}")
            subprocess.run(["git", "pull", "github", "main", "--no-rebase", "--no-edit"],
                           cwd=str(VAULT), capture_output=True, text=True,
                           encoding="utf-8", errors="ignore")
            p2 = subprocess.run(["git", "push", "github", "main"], cwd=str(VAULT),
                                capture_output=True, text=True, encoding="utf-8", errors="ignore")
            if p2.returncode == 0:
                log("pull 后重推成功。")
            else:
                log(f"⚠️ 重推仍失败: {p2.stderr[-200:]}")
        return True
    except subprocess.CalledProcessError as e:
        log(f"⚠️ git 步骤失败: {e}")
        return False


def main():
    log("=== 自进化编排开始 ===")
    results = {}
    results["compile"] = step_compile_if_new()
    results["grow"] = step_grow()
    health_report, broken_freq = step_vault_health()
    results["health"] = health_report
    results["grow_concepts"] = step_grow_missing_concepts(broken_freq)
    results["phase4"] = step_phase4()
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
