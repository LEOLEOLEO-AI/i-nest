#!/usr/bin/env python3
"""
wiki_compiler.py — Karpathy-style knowledge compiler
Implements: Summarize → Concept Extract → Cross-link → Index → Health Check
"""
import os, sys, json, re, time
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import urllib.request, urllib.parse, urllib.error

VAULT = Path(r"D:\Obsidian\vault")
RAW = VAULT / "raw"
WIKI = VAULT / "wiki"
STATE = VAULT / "state" / "wiki_compiler_state.json"
SCHEMA = WIKI / "schema.md"

# Load from .env
from dotenv import load_dotenv
load_dotenv(VAULT / ".env")
LLM_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
USE_LLM = bool(LLM_KEY)

TODAY = datetime.now().strftime("%Y-%m-%d")

# ============================================================
# Utility
# ============================================================

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding='utf-8'))
    return {"last_compile": None, "processed_files": {}, "concept_graph": {}}

def save_state(state):
    STATE.parent.mkdir(exist_ok=True, parents=True)
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')

def slugify(text):
    """Convert text to wiki-filename-friendly slug"""
    return re.sub(r'[^\w]', '_', text)[:80]

# ============================================================
# Phase 1: Find new/changed files in raw/
# ============================================================

def find_new_files(state):
    """Find raw files newer than their wiki counterparts"""
    new_files = []
    for md_file in RAW.rglob("*.md"):
        if "_FILE_INDEX" in md_file.name or "README" in md_file.name:
            continue
        rel = md_file.relative_to(RAW)
        key = str(rel).replace("\\", "/")
        last_processed = state["processed_files"].get(key)
        mtime = md_file.stat().st_mtime
        if last_processed is None or mtime > last_processed:
            new_files.append(md_file)
    return new_files

# ============================================================
# Phase 2: Summarize raw → wiki/articles/
# ============================================================

def extract_keywords(text):
    """Simple keyword extraction without LLM"""
    kw_set = set()
    for kw in ["SDI", "TCC", "iNEST", "wafer", "neuromorphic", "SNN", "topology",
               "chiplet", "interconnect", "NoC", "STDP", "spiking", "忆阻", "晶圆",
               "神经形态", "类脑", "拓扑", "互连", "封装", "芯粒"]:
        if kw.lower() in text.lower():
            kw_set.add(kw)
    return kw_set

def summarize_file(filepath):
    """Extract-structured summary from a raw file"""
    try:
        content = filepath.read_text(encoding='utf-8')[:5000]
    except:
        return None
    
    # Extract title
    title = filepath.stem
    lines = content.split('\n')
    first_title = ""
    for line in lines[:10]:
        line = line.strip()
        if line.startswith('# '):
            first_title = line[2:].strip()
            break
    
    keywords = extract_keywords(content)
    domain = "Cross"
    tcc_kw = {"TCC", "SDI", "wafer", "chiplet", "晶圆", "芯粒", "interconnect", "NoC", "互连", "封装", "拓扑"}
    inest_kw = {"iNEST", "neuromorphic", "SNN", "spiking", "STDP", "神经形态", "类脑", "neuron", "忆阻"}
    tcc_hits = len(keywords & tcc_kw)
    inest_hits = len(keywords & inest_kw)
    if tcc_hits > inest_hits:
        domain = "TCC"
    elif inest_hits > tcc_hits:
        domain = "iNEST"
    
    # Generate simple summary (no LLM needed for basic operation)
    summary_lines = []
    for line in lines[1:]:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and not stripped.startswith('!') and not stripped.startswith('|'):
            if len(stripped) > 20:
                summary_lines.append(stripped[:200])
            if len(summary_lines) >= 5:
                break
    
    summary = " ".join(summary_lines) if summary_lines else "(content extracted from source)"
    
    return {
        "title": first_title or title,
        "domain": domain,
        "source": str(filepath.relative_to(VAULT)),
        "date": TODAY,
        "summary": summary[:500],
        "keywords": sorted(keywords)
    }

def write_article(summary_data):
    """Write article to wiki/articles/"""
    WIKI.mkdir(exist_ok=True)
    articles_dir = WIKI / "articles"
    articles_dir.mkdir(exist_ok=True)
    
    slug = slugify(summary_data["title"])
    article_path = articles_dir / f"{slug}.md"
    
    content = f"""# {summary_data["title"]}

**Domain**: {summary_data["domain"]}
**Source**: {summary_data["source"]}
**Compiled**: {summary_data["date"]}

## Summary
{summary_data["summary"]}

## Keywords
{', '.join(summary_data["keywords"])}

---
*Auto-compiled by wiki_compiler.py*
"""
    article_path.write_text(content, encoding='utf-8')
    return article_path

# ============================================================
# Phase 3: Concept extraction (lightweight, no LLM required)
# ============================================================

def extract_concepts(summary_data, existing_concepts):
    """Extract concepts from summary using keyword analysis"""
    concept_names = []
    text = summary_data["summary"] + " " + " ".join(summary_data["keywords"])
    
    # Pre-defined concept patterns
    patterns = [
        (r'\b(SDI)\b', "TCC", "Software-Defined Interconnect bonding mechanism"),
        (r'(wafer.scale|晶圆)', "TCC", "Wafer-scale integration and chip design"),
        (r'(chiplet|芯粒)', "TCC", "Chiplet-based heterogeneous integration"),
        (r'(topolog\w+|拓扑)', "TCC", "Network topology and interconnection patterns"),
        (r'(neuromorphic|神经形态)', "iNEST", "Neuromorphic computing architecture"),
        (r'(spik\w+|脉冲)', "iNEST", "Spiking neural network dynamics"),
        (r'(STDP)', "iNEST", "Spike-timing-dependent plasticity learning rule"),
        (r'(memristor|忆阻)', "iNEST", "Memristor-based synaptic devices"),
        (r'(brain.atlas|脑图谱|connectome)', "iNEST", "Brain connectome and structural mapping"),
        (r'(NoC|network.on.chip)', "TCC", "Network-on-Chip communication architecture"),
        (r'(3D.IC|2\.5D)', "TCC", "3D/2.5D integrated circuit packaging"),
        (r'(ARC.AGI)', "Cross", "Abstraction and Reasoning Corpus for AGI"),
    ]
    
    for pattern, domain, desc in patterns:
        if re.search(pattern, text, re.IGNORECASE) and any(c not in existing_concepts for c in [slugify(desc.split(' - ')[0])]):
            concept_names.append({
                "name": slugify(desc.split(' - ')[0])[:80],
                "domain": domain,
                "definition": desc
            })
    
    return concept_names[:5]  # Max 5 new concepts per compile

def write_concept(concept_data):
    """Write concept file to wiki/concepts/"""
    concepts_dir = WIKI / "concepts"
    concepts_dir.mkdir(exist_ok=True)
    
    name = concept_data["name"]
    concept_path = concepts_dir / f"{name}.md"
    
    if concept_path.exists():
        # Merge: update last_updated and add source
        existing = concept_path.read_text(encoding='utf-8')
        existing = re.sub(r'\*\*Last updated\*\*: .*', f'**Last updated**: {TODAY}', existing)
        concept_path.write_text(existing, encoding='utf-8')
        return concept_path
    
    content = f"""# {name}

**Domain**: {concept_data["domain"]}
**First mentioned**: auto-extracted
**Last updated**: {TODAY}

## Definition
{concept_data["definition"]}

## Context
Auto-extracted concept from raw material compilation.

## Related Work
*(Cross-links will be generated by link engine)*

## Sources
- See wiki/articles/ for source article summaries

## Open Questions
- *(Explore connections to other concepts)*
"""
    concept_path.write_text(content, encoding='utf-8')
    return concept_path

# ============================================================
# Phase 4: Cross-linking
# ============================================================

def update_index():
    """Regenerate wiki/index.md from concept graph"""
    concepts_dir = WIKI / "concepts"
    if not concepts_dir.exists():
        return
    
    tcc_concepts = []
    inest_concepts = []
    cross_concepts = []
    
    for concept_file in sorted(concepts_dir.glob("*.md")):
        content = concept_file.read_text(encoding='utf-8')
        name = concept_file.stem
        if "**Domain**: TCC" in content:
            tcc_concepts.append(name)
        elif "**Domain**: iNEST" in content:
            inest_concepts.append(name)
        else:
            cross_concepts.append(name)
    
    index_content = f"""# Wiki Index

*Auto-generated: {TODAY}*

## TCC — Topology-Centric Computing ({len(tcc_concepts)} concepts)
"""
    for c in tcc_concepts:
        index_content += f"- [[{c}]]\n"
    
    index_content += f"\n## iNEST — In-Network Neuromorphic ({len(inest_concepts)} concepts)\n"
    for c in inest_concepts:
        index_content += f"- [[{c}]]\n"
    
    index_content += f"\n## Cross-Domain ({len(cross_concepts)} concepts)\n"
    for c in cross_concepts:
        index_content += f"- [[{c}]]\n"
    
    index_content += f"\n---\n**Total**: {len(tcc_concepts) + len(inest_concepts) + len(cross_concepts)} concepts\n"
    index_content += f"**Articles**: {len(list((WIKI/'articles').glob('*.md'))) if (WIKI/'articles').exists() else 0}\n"
    
    (WIKI / "index.md").write_text(index_content, encoding='utf-8')

def update_backlinks():
    """Generate backlinks from concept files"""
    concepts_dir = WIKI / "concepts"
    if not concepts_dir.exists():
        return
    
    backlinks = defaultdict(list)
    for concept_file in concepts_dir.glob("*.md"):
        content = concept_file.read_text(encoding='utf-8')
        for other in concepts_dir.glob("*.md"):
            if other.stem != concept_file.stem and other.stem in content:
                backlinks[other.stem].append(concept_file.stem)
    
    bl_content = f"# Backlinks Index\n\n*Auto-generated: {TODAY}*\n\n"
    for target, sources in sorted(backlinks.items()):
        bl_content += f"## [[{target}]]\nReferenced by: "
        bl_content += ", ".join(f"[[{s}]]" for s in sorted(set(sources)))
        bl_content += "\n\n"
    
    (WIKI / "backlinks.md").write_text(bl_content, encoding='utf-8')

# ============================================================
# Phase 5: Health Check
# ============================================================

def health_check(state):
    """Generate knowledge health report"""
    concepts_dir = WIKI / "concepts"
    articles_dir = WIKI / "articles"
    
    num_concepts = len(list(concepts_dir.glob("*.md"))) if concepts_dir.exists() else 0
    num_articles = len(list(articles_dir.glob("*.md"))) if articles_dir.exists() else 0
    
    # Find orphans (concepts with no incoming links)
    orphans = []
    if concepts_dir.exists():
        all_names = {f.stem for f in concepts_dir.glob("*.md")}
        backlink_map = defaultdict(set)
        for f in concepts_dir.glob("*.md"):
            content = f.read_text(encoding='utf-8')
            for name in all_names:
                if name != f.stem and name in content:
                    backlink_map[name].add(f.stem)
        orphans = [n for n in all_names if not backlink_map[n]]
    
    report = f"""# Knowledge Health Report

**Generated**: {TODAY}
**Last Compile**: {state.get("last_compile", "never")}

## Stats
- **Total Concepts**: {num_concepts}
- **Total Articles**: {num_articles}
- **Orphan Concepts**: {len(orphans)}
- **Knowledge Graph Density**: {'Low' if num_concepts < 50 else 'Medium' if num_concepts < 200 else 'High'}

## Orphan Concepts (no incoming links)
"""
    if orphans:
        for o in orphans[:20]:
            report += f"- [[{o}]]\n"
    else:
        report += "*No orphan concepts found.*\n"
    
    report += f"""
## Research Gaps
"""
    # Suggest gaps based on domain distribution
    tcc_count = 0
    inest_count = 0
    if concepts_dir.exists():
        for f in concepts_dir.glob("*.md"):
            content = f.read_text(encoding='utf-8')
            if "**Domain**: TCC" in content:
                tcc_count += 1
            elif "**Domain**: iNEST" in content:
                inest_count += 1
    
    if tcc_count < 10:
        report += "- **TCC domain is thin** — need more TCC concept extraction\n"
    if inest_count < 10:
        report += "- **iNEST domain is thin** — need more iNEST concept extraction\n"
    if tcc_count > 0 and inest_count > 0 and (tcc_count + inest_count) < 30:
        report += "- **Cross-domain bridges needed** — increase concept extraction from both domains\n"
    
    report += f"""
## Next Steps
1. Run `[[wiki_compiler.py]]` after each pipeline import
2. Review concepts in [[index|Wiki Index]] for accuracy
3. Add manual concept definitions for high-priority terms
4. Explore cross-domain connections between TCC ↔ iNEST concepts
"""
    
    (WIKI / "health.md").write_text(report, encoding='utf-8')

# ============================================================
# Main
# ============================================================

def main():
    log("=== Wiki Compiler v1.0 ===")
    log(f"LLM enabled: {USE_LLM}")
    
    state = load_state()
    log(f"Last compile: {state.get('last_compile', 'never')}")
    
    # Phase 1: Find new files
    new_files = find_new_files(state)
    log(f"Phase 1: Found {len(new_files)} new/changed raw files")
    
    if not new_files:
        log("No new files to process. Running health check only.")
        health_check(state)
        log("Done.")
        return
    
    # Phase 2: Summarize
    articles_written = 0
    concepts_created = 0
    
    for f in new_files:
        summary = summarize_file(f)
        if not summary:
            continue
        
        article_path = write_article(summary)
        articles_written += 1
        log(f"  Article: {article_path.name}")
        
        # Phase 3: Extract concepts
        existing = {c.stem for c in (WIKI / "concepts").glob("*.md")} if (WIKI / "concepts").exists() else set()
        concepts = extract_concepts(summary, existing)
        for c in concepts:
            cp = write_concept(c)
            concepts_created += 1
        
        # Update state
        rel = f.relative_to(RAW)
        state["processed_files"][str(rel).replace("\\", "/")] = f.stat().st_mtime
    
    log(f"Phase 2-3: {articles_written} articles, {concepts_created} concepts")
    
    # Phase 4: Cross-linking
    update_index()
    update_backlinks()
    log("Phase 4: Index and backlinks updated")
    
    # Phase 5: Health
    health_check(state)
    log("Phase 5: Health report generated")
    
    # Save state
    state["last_compile"] = TODAY
    save_state(state)
    
    log(f"=== Compile complete: {articles_written} articles, {concepts_created} concepts ===")

if __name__ == "__main__":
    main()
