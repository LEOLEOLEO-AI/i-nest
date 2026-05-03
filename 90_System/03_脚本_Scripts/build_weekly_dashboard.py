import os
import glob
import re
from pathlib import Path
from datetime import datetime

def generate_weekly_dashboard(workspace_root: str):
    reports_dir = Path(workspace_root) / "20_Projects" / "Weekly_Reports"
    dashboard_path = Path(workspace_root) / "20_Projects" / "00_团队全局进度周报面板.md"
    
    if not reports_dir.exists():
        return
        
    md_files = glob.glob(str(reports_dir / "*.md"))
    
    # 提取最新的日期
    dates = []
    reports_by_date = {}
    
    for f in md_files:
        content = Path(f).read_text(encoding="utf-8")
        date_match = re.search(r'date:\s*"([^"]+)"', content)
        if date_match:
            date_str = date_match.group(1)
            if date_str not in reports_by_date:
                reports_by_date[date_str] = []
                dates.append(date_str)
            reports_by_date[date_str].append((Path(f).stem, content))
            
    if not dates:
        return
        
    dates.sort(reverse=True)
    latest_date = dates[0]
    latest_reports = reports_by_date[latest_date]
    
    dashboard_lines = [
        "---",
        "type: dashboard",
        "tags:",
        "  - weekly",
        "  - execution",
        "---",
        "",
        "# 团队全局进度周报面板",
        "",
        f"**最新统计周期**：{latest_date}",
        f"**已交周报组别**：{len(latest_reports)} 个组",
        "",
        "## 一、本周全局核心进展",
        ""
    ]
    
    # 汇总进展
    for name, content in latest_reports:
        group_match = re.search(r'group:\s*"([^"]+)"', content)
        group = group_match.group(1) if group_match else "未知"
        
        progress_match = re.search(r'## 1\. 本周核心进展(.*?)(?:## 2\.|$)', content, re.DOTALL)
        if progress_match:
            progress = progress_match.group(1).strip()
            dashboard_lines.append(f"### {group} 组进展")
            dashboard_lines.append(progress)
            dashboard_lines.append("")
            
    dashboard_lines.append("## 二、全局阻塞点与风险 (Blockers)")
    dashboard_lines.append("")
    
    # 汇总阻塞
    for name, content in latest_reports:
        group_match = re.search(r'group:\s*"([^"]+)"', content)
        group = group_match.group(1) if group_match else "未知"
        
        blocker_match = re.search(r'## 2\. 关键阻塞点与风险.*?Blockers\)(.*?)(?:## 3\.|$)', content, re.DOTALL)
        if blocker_match:
            blocker = blocker_match.group(1).strip()
            if blocker and blocker.replace('-', '').strip():
                dashboard_lines.append(f"**{group} 组**：\n{blocker}\n")
                
    dashboard_lines.append("## 三、下周全局计划池")
    dashboard_lines.append("")
    
    # 汇总计划
    for name, content in latest_reports:
        group_match = re.search(r'group:\s*"([^"]+)"', content)
        group = group_match.group(1) if group_match else "未知"
        
        plan_match = re.search(r'## 3\. 下周计划与里程碑(.*?)(?:## 4\.|$)', content, re.DOTALL)
        if plan_match:
            plan = plan_match.group(1).strip()
            dashboard_lines.append(f"**{group} 组**：\n{plan}\n")
            
    dashboard_lines.extend([
        "## 四、导航",
        "",
        "- [[20_Projects/00_项目策划总览]]",
        "- [[20_Projects/00_项目-论文-专利-技术四线映射表]]",
        "- [[10_Knowledge/00_导航/Wiki/Home]]"
    ])
    
    dashboard_path.write_text("\n".join(dashboard_lines), encoding="utf-8")
    print(f"Generated dashboard at {dashboard_path}")

if __name__ == "__main__":
    generate_weekly_dashboard(r"d:\Obsidian\home\work\.openclaw\workspace")
