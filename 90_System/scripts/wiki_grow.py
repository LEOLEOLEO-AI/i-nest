#!/usr/bin/env python3
"""
wiki_grow.py — Knowledge-graph growth & consolidation stage.
Complements wiki_compiler.py (which distills raw -> articles/concepts).

Responsibilities:
  1. De-duplicate concepts that collide after slug-normalization.
  2. Build a connected graph by injecting [[wikilinks]] between
     concepts and articles (alias + name-phrase matching), replacing the
     empty "Related Work" placeholders left by wiki_compiler.
  3. Refresh wiki/index.md (with link counts), wiki/backlinks.md,
     wiki/health.md.

Idempotent: re-running updates links in place; existing link sections
are replaced, orphan count should only ever shrink.
"""
import os, sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\vault")
WIKI = VAULT / "wiki"
ART = WIKI / "articles"
CPT = WIKI / "concepts"
TODAY = datetime.now().strftime("%Y-%m-%d")

# Reuse the curated term->concept alias patterns from wiki_compiler
sys.path.insert(0, str(VAULT / "90_System" / "scripts"))
try:
    import wiki_compiler as wc
    CONCEPT_PATTERNS = wc.CONCEPT_PATTERNS
except Exception:
    CONCEPT_PATTERNS = []

# ----------------------------------------------------------------------------
# Curated aliases (term -> canonical concept slug) for high-precision linking
# of Chinese / abbreviated mentions that CamelCase name-matching would miss.
# ----------------------------------------------------------------------------
CURATED_ALIASES = {
    "忆阻器": None, "memristor": None, "rram": None,        # bound to Memristor_* below
    "脉冲神经网络": "Spiking_Neural_Network", "snn": "Spiking_Neural_Network",
    "spiking": "Spiking_Neural_Network", "脉冲神经": "Spiking_Neural_Network",
    "储备池计算": "Reservoir_Computing", "reservoir": "Reservoir_Computing",
    "自组织临界": "Self_Organized_Criticality", "临界": "Self_Organized_Criticality",
    "criticality": "Self_Organized_Criticality",
    "涌现": "Intelligence_Emergence", "emergence": "Intelligence_Emergence",
    "类脑": "Neuromorphic_Computing", "神经形态": "Neuromorphic_Computing",
    "neuromorphic": "Neuromorphic_Computing",
    "芯粒": "Chiplet_Heterogeneous_Integration", "chiplet": "Chiplet_Heterogeneous_Integration",
    "片上网络": "Network_on_Chip", "noc": "Network_on_Chip", "network-on-chip": "Network_on_Chip",
    "晶圆级": "Wafer_Scale_Integration", "wafer-scale": "Wafer_Scale_Integration", "晶圆": "Wafer_Scale_Integration",
    "拓扑": "Network_Topology_Design", "topology": "Network_Topology_Design",
    "存内计算": "In_Memory_Computing", "in-memory": "In_Memory_Computing", "processing-in-memory": "In_Memory_Computing",
    "sdi": "SDI_Bond", "software-defined interconnect": "SDI_Bond", "软件定义互连": "SDI_Bond",
    "stdp": "STDP_Plasticity", "spike-timing": "STDP_Plasticity", "可塑性": "Synaptic_Plasticity",
    "plasticity": "Synaptic_Plasticity", "突触": "Synaptic_Plasticity",
    "复杂系统": "Complex_System_Theory", "complex system": "Complex_System_Theory",
    "非线性": "Nonlinear_Gain", "nonlinear": "Nonlinear_Gain", "增益": "Nonlinear_Gain",
    "铁电": "Ferroelectric_Devices", "ferroelectric": "Ferroelectric_Devices",
    "脑图谱": "Brain_Connectome", "connectome": "Brain_Connectome", "连接组": "Brain_Connectome",
    "异构集成": "Heterogeneous_Integration", "heterogeneous integration": "Heterogeneous_Integration",
    "事件驱动": "Event_Driven_Architecture", "event-driven": "Event_Driven_Architecture",
}

MEMRISTOR_CANDS = ["Memristor_Synapse", "Memristive_STDP", "STDP_iNEST_Memristive"]

# Vocabulary for shared-term (co-occurrence) linking
VOCAB = set(CURATED_ALIASES.keys())
for p, _, _, _ in CONCEPT_PATTERNS:
    # pull representative words out of the pattern
    for tok in re.findall(r'[A-Za-z][A-Za-z_\-]{3,}', p):
        VOCAB.add(tok.lower())
    for tok in re.findall(r'[一-鿿]{2,4}', p):
        VOCAB.add(tok)


def build_signature(text):
    """Set of vocabulary terms present in a piece of text (lowercased)."""
    low = text.lower()
    sig = set()
    for term in VOCAB:
        if term.lower() in low:
            sig.add(term.lower())
    return sig


def domain_of(text):
    if "**Domain**: TCC" in text:
        return "TCC"
    if "**Domain**: iNEST" in text:
        return "iNEST"
    return "Cross"


def load_concepts():
    data = {}
    for f in CPT.glob("*.md"):
        txt = f.read_text(encoding='utf-8', errors='ignore')
        data[f.stem] = {"file": f, "text": txt}
    return data


def slug_to_phrase(slug):
    """Memristor_Synapse -> 'Memristor Synapse'; keep as both forms."""
    sp = re.sub(r'[_\-]+', ' ', slug)
    sp = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', sp)
    return sp.strip()


def find_links(source_name, source_text, concept_names, alias_index):
    """Return set of concept slugs referenced by source_text."""
    found = set()
    low = source_text.lower()

    # 1) Curated alias dictionary
    for term, target in CURATED_ALIASES.items():
        if target is None:
            continue
        if term.lower() in low and target in concept_names:
            found.add(target)

    # 2) CONCEPT_PATTERNS regexes (high precision)
    for pattern, domain, cname, definition in CONCEPT_PATTERNS:
        if cname in concept_names and re.search(pattern, source_text, re.IGNORECASE):
            found.add(cname)

    # 3) Name-phrase matching (CamelCase slug -> human phrase)
    for cname in concept_names:
        if cname == source_name:
            continue
        phrase = slug_to_phrase(cname)
        # require the phrase to be reasonably distinctive
        if len(phrase) < 6:
            continue
        if re.search(r'(?i)\b' + re.escape(phrase) + r'\b', source_text):
            found.add(cname)
        # also match the raw slug
        if re.search(r'(?i)\b' + re.escape(cname) + r'\b', source_text):
            found.add(cname)

    # memristor -> pick best memristor concept if multiple candidates exist
    if "memristor" in low or "忆阻" in low:
        for mc in MEMRISTOR_CANDS:
            if mc in concept_names:
                found.add(mc)
                break

    found.discard(source_name)
    return found


def replace_section(text, header, body):
    """Replace (or append) a '## header' section with body lines."""
    lines = text.split('\n')
    out = []
    i = 0
    replaced = False
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith(f"## {header}"):
            # skip until next '## ' or end
            out.append(f"## {header}")
            out.append("")
            out.extend(body)
            out.append("")
            replaced = True
            j = i + 1
            while j < len(lines) and not lines[j].startswith("## "):
                j += 1
            i = j
            continue
        out.append(line)
        i += 1
    if not replaced:
        out.append("")
        out.append(f"## {header}")
        out.append("")
        out.extend(body)
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main():
    print(f"[{datetime.now():%H:%M:%S}] wiki_grow start")
    concepts = load_concepts()
    concept_names = set(concepts.keys())
    print(f"  concepts loaded: {len(concept_names)}")

    # ---- Step 1: merge exact-normalized duplicate slugs ----
    def norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())
    groups = defaultdict(list)
    for c in concept_names:
        groups[norm(c)].append(c)
    merged = 0
    rename_map = {}  # deleted -> canonical
    for k, members in groups.items():
        if len(members) < 2:
            continue
        # canonical: prefer one present as a CONCEPT_PATTERNS key, else longest, else sorted
        canonical = None
        pattern_slugs = {p[2] for p in CONCEPT_PATTERNS}
        for m in members:
            if m in pattern_slugs:
                canonical = m
                break
        if canonical is None:
            canonical = max(members, key=lambda x: (len(x), x))
        for m in members:
            if m != canonical:
                # fold content into canonical
                cf = concepts[canonical]["file"]
                mf = concepts[m]["file"]
                extra = concepts[m]["text"]
                body = cf.read_text(encoding='utf-8', errors='ignore')
                if "## Merged From" not in body:
                    body = body.rstrip() + f"\n\n## Merged From\n- {m} (merged {TODAY})\n"
                    cf.write_text(body, encoding='utf-8')
                try:
                    mf.unlink()
                except Exception:
                    pass
                rename_map[m] = canonical
                merged += 1
    if rename_map:
        # fix references across wiki
        for f in list(ART.glob("*.md")) + list(CPT.glob("*.md")):
            t = f.read_text(encoding='utf-8', errors='ignore')
            nt = t
            for old, new in rename_map.items():
                nt = re.sub(r'\[\[' + re.escape(old) + r'(\|[^\]]*)?\]\]', f'[[{new}]]', nt)
                nt = re.sub(r'\b' + re.escape(old) + r'\b', new, nt)
            if nt != t:
                f.write_text(nt, encoding='utf-8')
        print(f"  merged {merged} duplicate concept(s): {rename_map}")
        concepts = load_concepts()
        concept_names = set(concepts.keys())

    # ---- Step 2: build links ----
    # article texts for concept linking
    art_texts = {}
    for f in ART.glob("*.md"):
        art_texts[f.stem] = f.read_text(encoding='utf-8', errors='ignore')

    # precompute signatures + domains for shared-term linking
    sigs = {c: build_signature(info["text"]) for c, info in concepts.items()}
    doms = {c: domain_of(info["text"]) for c, info in concepts.items()}

    outgoing = defaultdict(set)   # concept -> linked concepts
    art_links = {}                # article -> linked concepts

    # link concepts against all concept + article texts
    for cname, info in concepts.items():
        src = info["text"]
        links = find_links(cname, src, concept_names, None)
        outgoing[cname] = links

    # shared-term (co-occurrence) linking: same domain, >=2 shared vocab terms
    for cname in concept_names:
        for other in concept_names:
            if other == cname or other in outgoing[cname]:
                continue
            # only connect within same domain (or one is Cross as bridge)
            if not (doms[cname] == doms[other] or doms[cname] == "Cross" or doms[other] == "Cross"):
                continue
            shared = sigs[cname] & sigs[other]
            if len(shared) >= 2:
                outgoing[cname].add(other)
                if len(outgoing[cname]) >= 10:
                    break

    # link articles -> concepts (alias + pattern + name phrase)
    for aname, atext in art_texts.items():
        links = set()
        low = atext.lower()
        for term, target in CURATED_ALIASES.items():
            if target and term.lower() in low and target in concept_names:
                links.add(target)
        for p, _, cn, _ in CONCEPT_PATTERNS:
            if cn in concept_names and re.search(p, atext, re.IGNORECASE):
                links.add(cn)
        for cname in concept_names:
            if cname in atext:
                links.add(cname)
                continue
            if re.search(r'(?i)\b' + re.escape(slug_to_phrase(cname)) + r'\b', atext):
                links.add(cname)
            if len(links) >= 12:
                break
        art_links[aname] = links

    # ---- Step 3: write links into files ----
    linked_concepts = 0
    for cname, links in outgoing.items():
        info = concepts[cname]
        f = info["file"]
        body = sorted(f"[[{l}]]" for l in links) if links else ["*(no related concepts yet)*"]
        new_text = replace_section(info["text"], "Related Work", body)
        f.write_text(new_text, encoding='utf-8')
        if links:
            linked_concepts += 1

    for aname, links in art_links.items():
        f = ART / f"{aname}.md"
        if not f.exists():
            continue
        t = f.read_text(encoding='utf-8', errors='ignore')
        body = sorted(f"[[{l}]]" for l in links) if links else ["*(no linked concepts yet)*"]
        new_text = replace_section(t, "Related Concepts", body)
        f.write_text(new_text, encoding='utf-8')

    # ---- Step 4: recompute graph + refresh index/backlinks/health ----
    concepts = load_concepts()
    concept_names = set(concepts.keys())
    incoming = defaultdict(set)
    for cname, info in concepts.items():
        for other in concept_names:
            if other != cname and other in info["text"]:
                incoming[other].add(cname)

    orphans = [n for n in concept_names if not incoming.get(n)]
    print(f"  concepts now: {len(concept_names)} | linked: {linked_concepts} | orphans: {len(orphans)}")

    # index.md with link counts
    tcc, inest, cross = [], [], []
    for f in sorted(CPT.glob("*.md")):
        txt = f.read_text(encoding='utf-8', errors='ignore')
        deg = len(incoming.get(f.stem, set())) + len(outgoing.get(f.stem, set()))
        line = f"- [[{f.stem}]] ({deg})"
        if "**Domain**: TCC" in txt:
            tcc.append(line)
        elif "**Domain**: iNEST" in txt:
            inest.append(line)
        else:
            cross.append(line)
    idx = f"# Wiki Index\n\n*Auto-generated: {TODAY}*\n\n"
    idx += f"## TCC — Topology-Centric Computing ({len(tcc)})\n" + "\n".join(tcc) + "\n\n"
    idx += f"## iNEST — In-Network Neuromorphic ({len(inest)})\n" + "\n".join(inest) + "\n\n"
    idx += f"## Cross-Domain ({len(cross)})\n" + "\n".join(cross) + "\n\n"
    idx += f"---\n**Total**: {len(concept_names)} concepts | **Articles**: {len(list(ART.glob('*.md')))} | **Orphans**: {len(orphans)}\n"
    (WIKI / "index.md").write_text(idx, encoding='utf-8')

    # backlinks.md
    bl = f"# Backlinks Index\n\n*Auto-generated: {TODAY}*\n\n"
    for target in sorted(incoming):
        srcs = sorted(incoming[target])
        if srcs:
            bl += f"## [[{target}]]\nReferenced by: " + ", ".join(f"[[{s}]]" for s in srcs) + "\n\n"
    (WIKI / "backlinks.md").write_text(bl, encoding='utf-8')

    # health.md
    health = f"""# Knowledge Health Report

**Generated**: {TODAY}
**Last Grow**: {TODAY}

## Stats
- **Total Concepts**: {len(concept_names)}
- **Total Articles**: {len(list(ART.glob('*.md')))}
- **Orphan Concepts**: {len(orphans)}
- **Knowledge Graph Density**: {'Low' if len(concept_names) < 50 else 'Medium' if len(concept_names) < 200 else 'High'}

## Orphan Concepts (no incoming links)
"""
    if orphans:
        for o in sorted(orphans)[:40]:
            health += f"- [[{o}]]\n"
        if len(orphans) > 40:
            health += f"- ... {len(orphans)-40} more\n"
    else:
        health += "*No orphan concepts found.*\n"
    health += f"""
## Next Steps
1. Run `[[wiki_compiler.py]]` after each new raw import.
2. Run `[[wiki_grow.py]]` to connect concepts (post-compile).
3. Review concepts in [[index|Wiki Index]] for accuracy.
4. Manually enrich high-priority concept definitions.
"""
    (WIKI / "health.md").write_text(health, encoding='utf-8')

    print(f"  index/backlinks/health refreshed.")
    print(f"[{datetime.now():%H:%M:%S}] wiki_grow done — orphans {len(orphans)}/{len(concept_names)}")


if __name__ == "__main__":
    main()
