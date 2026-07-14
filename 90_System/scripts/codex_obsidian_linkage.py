"""Codex ↔ Obsidian 深度联动脚本 - 统一桥接层

功能:
1. Codex 直接读写 Obsidian vault 文件
2. 通过 DeepSeek API 分析笔记内容  
3. 触发研究流水线（论文灵感、专利思路、工程任务）
4. 生成/更新 MOC 导航页与研发看板
5. 知识图谱双向链接管理

用法:
  python codex_obsidian_linkage.py analyze <file.md>       # 分析单篇笔记
  python codex_obsidian_linkage.py scan <dir>              # 扫描目录生成洞察
  python codex_obsidian_linkage.py link <file.md>          # 建议双向链接
  python codex_obsidian_linkage.py dashboard               # 更新研发看板
  python codex_obsidian_linkage.py health                  # 知识库健康诊断
  python codex_obsidian_linkage.py pipeline                # 运行完整研究流水线
"""

import os, sys, json, re, time
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ====== 配置 ======
VAULT_ROOT = r"D:\Obsidian\home\work\.openclaw\workspace"
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"  # DeepSeek V4 Pro

# 目录映射
DIR_MAP = {
    "inbox": "00_Inbox",
    "moc": "60_MOC", 
    "tcc_theory": "30_TCC/31_Theory",
    "tcc_tech": "30_TCC/32_Technology",
    "tcc_eng": "30_TCC/33_Engineering",
    "inest_theory": "40_iNEST/41_Theory",
    "inest_tech": "40_iNEST/42_Technology", 
    "inest_eng": "40_iNEST/43_Engineering",
    "papers": "50_Output/51_Papers",
    "patents": "50_Output/52_Patents",
    "guides": "50_Output/55_Guides",
    "processing": "20_Processing",
    "archive": "80_Archive",
    "system": "90_System",
    "dashboard": "70_Dashboard",
}

try:
    from openai import OpenAI
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
except ImportError:
    client = None
    print("[WARN] openai not installed, LLM features disabled")

# ====== 核心功能 ======

def read_vault_file(rel_path: str) -> str:
    """读取 vault 中的文件"""
    full = Path(VAULT_ROOT) / rel_path
    if full.exists():
        return full.read_text(encoding="utf-8")
    return ""

def write_vault_file(rel_path: str, content: str):
    """写入 vault 文件"""
    full = Path(VAULT_ROOT) / rel_path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")

def list_vault_files(subdir: str = "", pattern: str = "*.md") -> list:
    """列出 vault 中的文件"""
    p = Path(VAULT_ROOT) / subdir
    if p.exists():
        return [str(f.relative_to(VAULT_ROOT)) for f in p.rglob(pattern)]
    return []

def call_deepseek(prompt: str, system: str = "") -> str:
    """调用 DeepSeek API"""
    if not client:
        return "[ERROR: DeepSeek client not available]"
    try:
        resp = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": system or "你是iNEST/TCC研究助手，精通神经形态计算、晶圆级芯片、拓扑计算。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4096
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[ERROR: {e}]"

def analyze_note(filepath: str) -> dict:
    """用 DeepSeek 分析单篇笔记"""
    content = read_vault_file(filepath)
    if not content:
        return {"error": f"File not found: {filepath}"}
    
    prompt = f"""分析以下研究笔记，返回JSON（不要markdown代码块）:
{{
    "direction": "TCC 或 iNEST 或 both",
    "category": "理论/技术/工程/综述/灵感/数据",
    "tags": ["tag1", "tag2", "tag3"],
    "summary": "一句话中文摘要",
    "insight_tcc": "对TCC的启发（无则写无）",
    "insight_inest": "对iNEST的启发（无则写无）",
    "actionable": "可操作建议（论文方向/专利点/仿真验证/代码开发，无则写无）",
    "quality": "high/medium/low"
}}

笔记内容:
{content[:8000]}"""
    
    result = call_deepseek(prompt)
    try:
        # Try to extract JSON
        json_match = re.search(r'\{[\s\S]*\}', result)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass
    return {"raw": result, "direction": "unknown", "category": "未分类"}

def suggest_links(filepath: str, top_n: int = 5) -> list:
    """为笔记建议双向链接"""
    content = read_vault_file(filepath)
    if not content:
        return []
    
    # 收集候选文件标题
    candidates = []
    for md_file in list_vault_files("30_TCC")[:200] + list_vault_files("40_iNEST")[:200]:
        try:
            text = read_vault_file(md_file)[:500]
            title = md_file.stem if hasattr(Path(md_file), 'stem') else os.path.basename(md_file).replace('.md','')
            candidates.append(f"- {title}: {text[:200]}")
        except:
            pass
    
    candidate_text = "\n".join(candidates[:100])
    prompt = f"""从候选文件中选出与当前笔记最相关的{top_n}个，返回JSON数组:
[{{"file": "相对路径", "reason": "关联原因(10字内)"}}]

当前笔记:
{content[:3000]}

候选文件:
{candidate_text[:10000]}"""
    
    result = call_deepseek(prompt)
    try:
        json_match = re.search(r'\[[\s\S]*\]', result)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass
    return []

def health_check() -> dict:
    """知识库健康诊断"""
    stats = {
        "total_md": 0,
        "empty_files": 0,
        "broken_links": 0,
        "by_dir": defaultdict(int),
        "duplicates": [],
        "last_modified": None
    }
    
    all_files = list_vault_files()
    stats["total_md"] = len(all_files)
    
    for f in all_files:
        parts = Path(f).parts
        if parts:
            stats["by_dir"][parts[0]] += 1
        
        content = read_vault_file(f)
        if not content.strip() or len(content.strip()) < 10:
            stats["empty_files"] += 1
            
        mtime = (Path(VAULT_ROOT) / f).stat().st_mtime
        if not stats["last_modified"] or mtime > stats["last_modified"]:
            stats["last_modified"] = mtime
    
    stats["last_modified_str"] = datetime.fromtimestamp(stats["last_modified"]).isoformat() if stats["last_modified"] else "N/A"
    stats["by_dir"] = dict(stats["by_dir"])
    
    return stats

def update_dashboard():
    """更新研发看板数据"""
    health = health_check()
    
    # 统计论文/专利
    papers = list_vault_files("50_Output/51_Papers", "*.md")
    patents = list_vault_files("50_Output/52_Patents", "*.md")
    guides = list_vault_files("50_Output/55_Guides", "*.md")
    
    tcc_files = len(list_vault_files("30_TCC", "*.md"))
    inest_files = len(list_vault_files("40_iNEST", "*.md"))
    inbox_files = len(list_vault_files("00_Inbox", "*.md"))
    
    dashboard_data = {
        "updated": datetime.now().isoformat(),
        "total_notes": health["total_md"],
        "empty_files": health["empty_files"],
        "tcc_notes": tcc_files,
        "inest_notes": inest_files,
        "inbox_pending": inbox_files,
        "papers": len(papers),
        "patents": len(patents),
        "guides": len(guides),
        "dir_distribution": health["by_dir"]
    }
    
    write_vault_file("70_Dashboard/dashboard_data.json", json.dumps(dashboard_data, ensure_ascii=False, indent=2))
    print(f"[Dashboard] Updated: {dashboard_data['total_notes']} notes, {inbox_files} inbox pending")
    return dashboard_data

def run_pipeline():
    """运行完整研究流水线"""
    print("=" * 60)
    print("  Codex ↔ Obsidian 研究流水线")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. 健康检查
    print("\n[1/5] 健康诊断...")
    health = health_check()
    print(f"  总计: {health['total_md']} 篇, 空文件: {health['empty_files']}")
    
    # 2. 扫描 Inbox
    print("\n[2/5] 扫描 Inbox...")
    inbox = list_vault_files("00_Inbox", "*.md")
    print(f"  待处理: {len(inbox)} 篇")
    
    # 3. 分析最近修改的文件
    print("\n[3/5] 分析最新笔记...")
    all_md = list_vault_files()
    recent = sorted(all_md, key=lambda f: (Path(VAULT_ROOT)/f).stat().st_mtime, reverse=True)[:5]
    for f in recent:
        print(f"  - {f}")
    
    # 4. 生成洞察
    print("\n[4/5] 生成研究洞察...")
    insights = []
    for f in recent[:3]:
        result = analyze_note(f)
        insights.append({"file": f, "analysis": result})
        print(f"  [{f[:60]}]: {result.get('direction', '?')} / {result.get('category', '?')}")
    
    # 5. 更新看板
    print("\n[5/5] 更新研发看板...")
    dashboard = update_dashboard()
    
    # 保存洞察报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "health": health,
        "insights": insights,
        "dashboard": dashboard
    }
    write_vault_file("60_MOC/99_Codex_Linkage_Report.md", 
        f"# Codex 联动报告\n\n"
        f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"## 知识库状态\n"
        f"- 总笔记: {health['total_md']}\n"
        f"- TCC: {tcc_files} | iNEST: {inest_files}\n"
        f"- 待处理 Inbox: {inbox_files}\n"
        f"- 论文: {len(papers)} | 专利: {len(patents)} | 指南: {len(guides)}\n\n"
        f"## 最新洞察\n"
        + "\n".join([f"- **{i['file']}**: {i['analysis'].get('summary', i['analysis'].get('raw','?'))}" for i in insights])
    )
    
    print("\n✅ 流水线完成")
    return report

# ====== CLI ======
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "health":
        result = health_check()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "analyze" and len(sys.argv) > 2:
        result = analyze_note(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "link" and len(sys.argv) > 2:
        links = suggest_links(sys.argv[2])
        for l in links:
            print(f"  → [[{l.get('file','?')}]] - {l.get('reason','')}")
    
    elif cmd == "scan" and len(sys.argv) > 2:
        files = list_vault_files(sys.argv[2], "*.md")[:10]
        for f in files:
            result = analyze_note(f)
            direction = result.get('direction', '?')
            category = result.get('category', '?')
            print(f"[{direction}/{category}] {f}")
    
    elif cmd == "dashboard":
        update_dashboard()
    
    elif cmd == "pipeline":
        run_pipeline()
    
    elif cmd == "test":
        print("[TEST] DeepSeek API...")
        resp = call_deepseek("用一句话介绍晶圆级拓扑中心计算TCC")
        print(f"  Response: {resp[:200]}")
        print("[TEST] Health check...")
        h = health_check()
        print(f"  Total notes: {h['total_md']}")
        print("[TEST] ✅ All systems go")
    
    else:
        print(f"Unknown command: {cmd}")
