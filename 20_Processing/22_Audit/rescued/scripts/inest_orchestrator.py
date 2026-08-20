#!/usr/bin/env python3
"""
iNEST Orchestrator - ToolUniverse x Obsidian x Neuromorphic Tools
==================================================================
Four-channel research-to-production pipeline:
  Channel A: ˼· (Paper)    - Literature  Hypothesis  Simulation  Draft
  Channel B: ר (Patent)   - Insight  Prior Art  Novelty  Claims
  Channel C: ʵ (Engineer) - Simulation  Code  IP  Reusable Module
  Channel D: Ŀ߻ (Project)  - Research  Roadmap  Proposal  Guidelines

Integrates: D:\\Obsidian\\Agent (ToolUniverse), Obsidian Vault, D:\iNEST\neuromorphic_tools
"""

import sys, io, os, re, json, yaml, time, shutil, subprocess, argparse
from pathlib import Path
from datetime import datetime
from openai import OpenAI

#  Paths 
AGENT_ROOT = Path(r"D:\\Obsidian\\Agent")
OBSIDIAN = Path(r"D:\Obsidian\vault")
NMT_ROOT = Path(r"D:\iNEST\neuromorphic_tools")  # Neuromorphic Tools
INEST_WRITE = Path(r"D:\iNEST\Write")
SCRIPTS_DIR = AGENT_ROOT / "scripts" / "inest_channels"

#  API 
API_KEY = os.environ.get("SILICONFLOW_API_KEY", "")
API_BASE = "https://api.siliconflow.cn/v1"
MODEL = "deepseek-ai/DeepSeek-V4-Pro"

#  Tool Mapping 
TOOL_MAP = {
    # Tool name -> (channel, executable, venv, description)
    "brian2":       (["A","C"], "python", None, "Spiking neural simulator"),
    "nest-simulator":(["A","C"], "nest", None, "Large-scale neural simulator"),
    "snntorch":     (["A","C"], "python", None, "SNN training in PyTorch"),
    "snngrow":      (["C"], "python", None, "SNN growth/pruning"),
    "lnn":          (["A","C"], "python", None, "Liquid Neural Networks"),
    "reservoirpy":  (["A","C"], "python", None, "Reservoir Computing"),
    "networkx":     (["A","B","C","D"], "python", None, "Graph analysis"),
    "pytorch_geometric":(["A","C"], "python", None, "Graph Neural Networks"),
    "snap":         (["A"], "python", None, "Network analysis"),
    "gephi":        (["D"], "gephi", None, "Graph visualization"),
    "PhysX":        (["C"], None, None, "Physics simulation"),
    "balsa":        (["C"], None, None, "Async circuit design"),
    "workcraft":    (["C"], None, None, "Async circuit toolkit"),
    "PySpike":      (["A"], "python", None, "Spike train analysis"),
    "sandia_tools": (["C","D"], None, None, "Sandia National Lab tools"),
    "cross-sim":    (["A","C"], "python", None, "Cross-simulator comparison"),
}

#  Channel configs 
CHANNELS = {
    "A": {
        "name": "˼·",
        "obsidian_dir": "iNEST_2_׫д",
        "description": "Literature  Hypothesis  Simulation  Draft",
        "template": """---
title: "{title}"
date: {date}
channel: paper
status: draft
tags: [paper, inest, {tags}]
---

# {title}

## о

## ׻

## 뷽

## ֤ (neuromorphic_tools)

## Ԥڹ

## дƻ
- [ ] 
- [ ] ʽ
- [ ] ʵ
- [ ] ׫д
- [ ] ޶Ͷ
"""
    },
    "B": {
        "name": "ר",
        "obsidian_dir": "iNEST_3_ר׫д",
        "description": "Insight  Prior Art  Novelty  Claims",
        "template": """---
title: "{title}"
date: {date}
channel: patent
status: ideation
tags: [patent, inest, {tags}]
---

# {title}

## 

## 

## 

### Ĵµ

### мԱ

## ȨҪݰ

## /ʵ֤

## ҵ

## ж嵥
- [ ] м
- [ ] µȷ
- [ ] ȨҪϸ
- [ ] ֤
- [ ] רͨ
"""
    },
    "C": {
        "name": "ʵ",
        "obsidian_dir": "iNEST_4_̿",
        "description": "Simulation  Code  IP  Reusable Module",
        "template": """---
title: "{title}"
date: {date}
channel: engineering
status: concept
tags: [engineering, ip, inest, {tags}]
---

# {title}

## 

## ܹ

## 湤
- : {tools}

## Ĵ

## IP װ

## ɸ

## ƻ
- [ ] ԭͷ
- [ ] 㷨ʵ
- [ ] ӿڶ
- [ ] IP 
- [ ] ĵ
"""
    },
    "D": {
        "name": "Ŀ߻",
        "obsidian_dir": "iNEST_1_Ŀ߻",
        "description": "Research  Roadmap  Proposal  Guidelines",
        "template": """---
title: "{title}"
date: {date}
channel: project
status: planning
tags: [project, inest, {tags}]
---

# {title}

## 붯

## о״

## ·

## ̱

## Դ

## 

## Ԥ
- : 
- ר: 
- IP: 
- Ŀָ: 

## ִмƻ
- [ ] н׶
- [ ] 
- [ ] ԭ֤
- [ ] ʽ
- [ ] ׶ν
"""
    },
}


def call_llm(prompt: str, max_tokens=2000, temperature=0.5) -> str:
    """Call DeepSeek for structured output."""
    client = OpenAI(api_key=API_KEY, base_url=API_BASE, timeout=120)
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"system","content":"You output ONLY valid JSON, no markdown fences."},
                  {"role":"user","content":prompt}],
        max_tokens=max_tokens, temperature=temperature
    )
    raw = r.choices[0].message.content.strip()
    if raw.startswith("```"): raw = raw.split("\n",1)[1][:-3] if raw.endswith("```") else raw.split("\n",1)[1]
    return raw


def list_available_tools():
    """List which neuromorphic tools are available."""
    available = {}
    for name, (channels, exe, venv, desc) in TOOL_MAP.items():
        tool_dir = NMT_ROOT / name
        if tool_dir.exists():
            available[name] = {"channels": channels, "description": desc,
                               "path": str(tool_dir)}
    return available


def list_existing_notes(channel: str):
    """List existing notes in the channel's Obsidian directory."""
    obs_dir = OBSIDIAN / CHANNELS[channel]["obsidian_dir"]
    if not obs_dir.exists():
        return []
    return sorted(obs_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)


def list_literature():
    """Get recent literature analysis results."""
    digest_dir = AGENT_ROOT / "generated_docs"
    digests = sorted(digest_dir.glob("llm_analysis_*.json"), reverse=True)
    papers = []
    for d in digests[:3]:  # last 3 digests
        try:
            data = json.loads(d.read_text(encoding="utf-8"))
            papers.extend(data.get("papers", []))
        except: pass
    return papers[:30]


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# Channel A: ˼·
# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
def channel_paper(args):
    """Generate paper ideas from literature + LLM synthesis."""
    print("\n" + "="*60)
    print("Channel A: ˼· (Paper Ideas)")
    print("="*60)

    # 1. Load recent literature
    papers = list_literature()
    print(f"\n[1/5] Recent literature: {len(papers)} papers")

    # 2. LLM gap analysis
    print("[2/5] LLM gap analysis...")
    paper_summaries = "\n".join([
        f"- [{p.get('title','?')[:100]}] (score: {p.get('_score',0):.2f}, {p.get('source','?')})"
        for p in papers[:10]
    ])

    prompt = f"""You are a research strategist for iNEST (Physical Complex Network Intelligence Emergence).
Based on these recently analyzed papers, identify 3 concrete paper ideas with:
- A specific research question
- Which neuromorphic tools to use (brian2, nest-simulator, snntorch, lnn, reservoirpy, networkx, pytorch_geometric, PySpike)
- Expected contribution

Recent papers:
{paper_summaries}

Return JSON: [{{"title": "paper title", "question": "research question", "tools": ["tool1"], "contribution": "...", "tags": ["tag1"]}}]"""

    try:
        raw = call_llm(prompt, max_tokens=2000)
        ideas = json.loads(raw)
    except:
        ideas = [{"title":"Research Gap Analysis","question":"Auto-extract from literature","tools":["networkx"],"contribution":"Systematic gap analysis","tags":["literature-review"]}]

    # 3. Generate paper notes
    print(f"[3/5] Generated {len(ideas)} paper ideas")
    obs_dir = OBSIDIAN / CHANNELS["A"]["obsidian_dir"]
    obs_dir.mkdir(parents=True, exist_ok=True)

    created = []
    for idea in ideas:
        date_str = datetime.now().strftime("%Y-%m-%d")
        tags_str = ", ".join(idea.get("tags", ["paper-idea"]))
        tools_str = ", ".join(idea.get("tools", []))
        content = CHANNELS["A"]["template"].format(
            title=idea["title"], date=date_str, tags=tags_str,
        )
        # Add tools section
        content += f"\n## ù\n"
        for t in idea.get("tools", []):
            content += f"- **{t}**: {TOOL_MAP.get(t, ('','','','Unknown'))[3]}\n"
        content += f"\n## о\n{idea.get('question','')}\n"
        content += f"\n## Ԥڹ\n{idea.get('contribution','')}\n"

        filename = re.sub(r'[^\w\s-]','', idea["title"])[:80].strip()
        filepath = obs_dir / f"{date_str}_{filename}.md"
        if not args.dry_run:
            filepath.write_text(content, encoding="utf-8")
        created.append((filepath.name, idea["title"]))
        print(f"  -> {filepath.name}")

    # 4. Tool availability check
    print("\n[4/5] Tool availability:")
    tools = list_available_tools()
    sim_tools = [n for n in tools if "A" in tools[n]["channels"]]
    for t in sim_tools:
        print(f"  {t}: {tools[t]['description']}")

    # 5. Summary
    print(f"\n[5/5] Paper channel done. {len(created)} ideas generated.")
    return created


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# Channel B: ר
# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
def channel_patent(args):
    """Generate patent ideas from tech insights."""
    print("\n" + "="*60)
    print("Channel B: ר (Patent Ideas)")
    print("="*60)

    # 1. Scan existing tech notes for patentable ideas
    print("\n[1/5] Scanning tech knowledge base...")
    tech_dirs = ["AI-ML", "Chip-Hardware", "Neuroscience", "Concepts-Theory"]
    tech_notes = []
    for d in tech_dirs:
        p = OBSIDIAN / "03_Topics" / d
        if p.exists():
            for f in p.glob("*.md"):
                text = f.read_text(encoding="utf-8", errors="ignore")[:2000]
                keywords = ["","ϵͳ","װ","ܹ","оƬ","㷨","",""]
                if any(k in text for k in keywords):
                    tech_notes.append((f.stem, text[:800]))
                    if len(tech_notes) >= 20:
                        break

    print(f"  Found {len(tech_notes)} tech-relevant notes")

    # 2. LLM patent idea extraction
    print("[2/5] LLM patent mining...")
    snippets = "\n".join([f"- {t[:80]}: {c[:200]}" for t,c in tech_notes[:10]])

    prompt = f"""Identify 3 patentable inventions from these tech notes. For each output:
- title: patent name
- field: technical field
- innovation: what is novel
- prior_art_diff: how it differs from existing
- tools: which neuromorphic_tools apply
- claims: 3 draft claims
- tags: relevant categories

Tech notes:
{snippets}

Return JSON array of patent ideas."""

    try:
        raw = call_llm(prompt, max_tokens=2000)
        ideas = json.loads(raw)
    except:
        ideas = [{"title":"iNEST Patent Idea","field":"Neuromorphic Computing","innovation":"Auto-generated","prior_art_diff":"TBD","tools":["brian2"],"claims":["Claim 1 placeholder"],"tags":["patent-idea"]}]

    # 3. Generate patent notes
    print(f"[3/5] Generated {len(ideas)} patent ideas")
    obs_dir = OBSIDIAN / CHANNELS["B"]["obsidian_dir"]
    obs_dir.mkdir(parents=True, exist_ok=True)

    created = []
    for idea in ideas:
        date_str = datetime.now().strftime("%Y-%m-%d")
        tags_str = ", ".join(idea.get("tags", ["patent-idea"]))
        content = CHANNELS["B"]["template"].format(
            title=idea["title"], date=date_str, tags=tags_str,
        )
        content += f"\n## \n{idea.get('field','')}\n"
        content += f"\n## Ĵ\n{idea.get('innovation','')}\n"
        content += f"\n## м\n{idea.get('prior_art_diff','')}\n"
        content += f"\n## ÷湤\n"
        for t in idea.get("tools", []):
            content += f"- {t}\n"
        content += f"\n## ȨҪݰ\n"
        for i, claim in enumerate(idea.get("claims", []), 1):
            content += f"{i}. {claim}\n"

        filename = re.sub(r'[^\w\s-]','', idea["title"])[:80].strip()
        filepath = obs_dir / f"{date_str}_patent_{filename}.md"
        if not args.dry_run:
            filepath.write_text(content, encoding="utf-8")
        created.append((filepath.name, idea["title"]))
        print(f"  -> {filepath.name}")

    print(f"\n[5/5] Patent channel done. {len(created)} ideas generated.")
    return created


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# Channel C: ʵ
# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
def channel_engineering(args):
    """Generate engineering/IP specifications from tools."""
    print("\n" + "="*60)
    print("Channel C: ʵ (Engineering & IP)")
    print("="*60)

    # 1. List all available engineering tools
    print("\n[1/5] Engineering tool inventory:")
    tools = list_available_tools()
    eng_tools = [n for n in tools if "C" in tools[n]["channels"]]

    for t in eng_tools:
        tool_dir = NMT_ROOT / t
        has_examples = any((tool_dir).rglob("*.py")) or any((tool_dir).rglob("example*"))
        status = " (has examples)" if has_examples else ""
        print(f"  {t}: {tools[t]['description']}{status}")

    # 2. Scan for existing code
    print("\n[2/5] Scanning existing implementations...")
    code_samples = []
    for t in eng_tools[:10]:
        tool_dir = NMT_ROOT / t
        py_files = list(tool_dir.rglob("*.py"))[:3]
        for pf in py_files:
            try:
                code = pf.read_text(encoding="utf-8", errors="ignore")
                if len(code) > 50 and len(code) < 5000:
                    code_samples.append((t, pf.name, code[:500]))
            except: pass

    print(f"  Found {len(code_samples)} code samples")

    # 3. LLM IP module design
    print("[3/5] LLM IP module design...")
    tool_list = ", ".join(eng_tools[:8])
    prompt = f"""Design 3 reusable IP modules for iNEST neuromorphic engineering.
Available tools: {tool_list}

For each module output:
- title: module name
- purpose: what it does
- tools: required tools from the list
- interface: input/output specification
- reuse_scenario: where this IP can be applied
- complexity: low/medium/high
- tags: relevant categories

Return JSON array."""

    try:
        raw = call_llm(prompt, max_tokens=2000)
        modules = json.loads(raw)
    except:
        modules = [{"title":"iNEST IP Module","purpose":"Auto-generated","tools":["networkx"],"interface":"TBD","reuse_scenario":"Research","complexity":"medium","tags":["ip-module"]}]

    # 4. Generate engineering notes
    print(f"[4/5] Generated {len(modules)} IP modules")
    obs_dir = OBSIDIAN / CHANNELS["C"]["obsidian_dir"]
    obs_dir.mkdir(parents=True, exist_ok=True)

    created = []
    for mod in modules:
        date_str = datetime.now().strftime("%Y-%m-%d")
        tags_str = ", ".join(mod.get("tags", ["ip-module"]))
        tools_str = ", ".join(mod.get("tools", []))
        content = CHANNELS["C"]["template"].format(
            title=mod["title"], date=date_str, tags=tags_str, tools=tools_str,
        )
        content += f"\n## ;\n{mod.get('purpose','')}\n"
        content += f"\n## ӿڶ\n{mod.get('interface','')}\n"
        content += f"\n## ó\n{mod.get('reuse_scenario','')}\n"
        content += f"\n## Ӷ\n{mod.get('complexity','medium')}\n"

        filename = re.sub(r'[^\w\s-]','', mod["title"])[:80].strip()
        filepath = obs_dir / f"{date_str}_ip_{filename}.md"
        if not args.dry_run:
            filepath.write_text(content, encoding="utf-8")
        created.append((filepath.name, mod["title"]))
        print(f"  -> {filepath.name}")

    # 5. Link to tools
    print(f"\n[5/5] Engineering channel done. {len(created)} IP modules.")
    return created


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# Channel D: Ŀ߻
# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
def channel_project(args):
    """Generate project proposals and roadmaps."""
    print("\n" + "="*60)
    print("Channel D: Ŀ߻ (Project Planning)")
    print("="*60)

    # 1. Scan existing proposals
    print("\n[1/5] Scanning existing project docs...")
    existing = list(INEST_WRITE.glob("*.pdf")) + list(INEST_WRITE.glob("*.docx"))
    print(f"  Found {len(existing)} existing documents")

    # 2. LLM roadmap generation
    print("[2/5] LLM roadmap analysis...")
    doc_names = ", ".join([f.stem[:60] for f in existing[:10]])

    prompt = f"""Based on iNEST research documents, generate 2 concrete project proposals.
Each with: title, background, objectives, timeline_quarters (Q1-Q4), milestones, deliverables (papers/patents/IP), budget_estimate, team_requirements.

Existing docs: {doc_names}

Return JSON array of project proposals."""

    try:
        raw = call_llm(prompt, max_tokens=2000)
        proposals = json.loads(raw)
    except:
        proposals = [{"title":"iNEST Project Proposal","background":"Auto-generated","objectives":"TBD","timeline_quarters":"Q1-Q4","milestones":["M1"],"deliverables":{"papers":0,"patents":0,"ip":0},"budget_estimate":"TBD","team_requirements":"TBD","tags":["project-proposal"]}]

    # 3. Generate project notes
    print(f"[3/5] Generated {len(proposals)} proposals")
    obs_dir = OBSIDIAN / CHANNELS["D"]["obsidian_dir"]
    obs_dir.mkdir(parents=True, exist_ok=True)

    created = []
    for prop in proposals:
        date_str = datetime.now().strftime("%Y-%m-%d")
        tags_str = ", ".join(prop.get("tags", ["project-proposal"]))
        content = CHANNELS["D"]["template"].format(
            title=prop["title"], date=date_str, tags=tags_str,
        )
        content += f"\n## \n{prop.get('background','')}\n"
        content += f"\n## Ŀ\n{prop.get('objectives','')}\n"
        content += f"\n## ʱ\n{prop.get('timeline_quarters','Q1-Q4')}\n"
        content += f"\n## ̱\n"
        for m in prop.get("milestones", []):
            content += f"- {m}\n"
        content += f"\n## \n"
        dels_raw = prop.get("deliverables", {}); dels = dels_raw if isinstance(dels_raw, dict) else {}
        content += f"- : {dels.get('papers',0)}\n"
        content += f"- ר: {dels.get('patents',0)}\n"
        content += f"- IP: {dels.get('ip',0)}\n"
        content += f"\n## Ԥ\n{prop.get('budget_estimate','TBD')}\n"
        content += f"\n## Ŷ\n{prop.get('team_requirements','TBD')}\n"

        filename = re.sub(r'[^\w\s-]','', prop["title"])[:80].strip()
        filepath = obs_dir / f"{date_str}_proj_{filename}.md"
        if not args.dry_run:
            filepath.write_text(content, encoding="utf-8")
        created.append((filepath.name, prop["title"]))
        print(f"  -> {filepath.name}")

    print(f"\n[5/5] Project channel done. {len(created)} proposals.")
    return created


# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
# Main Orchestrator
# TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
def main():
    parser = argparse.ArgumentParser(description="iNEST Four-Channel Orchestrator")
    parser.add_argument("--channel", choices=["A","B","C","D","all"],
                        default="all", help="Which channel to run")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--auto", action="store_true", help="Run all channels in sequence")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("="*60)
    print(f"iNEST Orchestrator - {ts}")
    print(f"ToolUniverse + Obsidian + Neuromorphic Tools")
    print("="*60)

    # Tool inventory
    tools = list_available_tools()
    print(f"\nAvailable tools: {len(tools)}/{len(TOOL_MAP)}")
    for name, info in sorted(tools.items()):
        ch = ",".join(info["channels"])
        print(f"  [{ch}] {name}: {info['description']}")

    # Run channels
    all_results = {}

    if args.channel in ("A", "all"):
        all_results["A"] = channel_paper(args)
    if args.channel in ("B", "all"):
        all_results["B"] = channel_patent(args)
    if args.channel in ("C", "all"):
        all_results["C"] = channel_engineering(args)
    if args.channel in ("D", "all"):
        all_results["D"] = channel_project(args)

    # Summary
    print("\n" + "="*60)
    total = sum(len(v) for v in all_results.values())
    print(f"Generated {total} items across {len(all_results)} channels")
    for ch, items in all_results.items():
        if items:
            print(f"  Channel {ch} ({CHANNELS[ch]['name']}): {len(items)} items")
    print("="*60)

    if args.dry_run:
        print("\n[Dry-run mode] No files written. Use without --dry-run to write.")


if __name__ == "__main__":
    main()


