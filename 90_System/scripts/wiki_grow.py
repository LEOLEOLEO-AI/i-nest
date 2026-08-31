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

try:
    import ahocorasick
    HAVE_AC = True
except ImportError:
    HAVE_AC = False

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


def build_union_regex(concept_names, source_name=None):
    """Build BUCKETED combined regexes matching all concept slugs+phrases.

    A single giant alternation over 3.6k+ concepts makes Python's re
    compiler degrade badly (slow compile, pathological backtracking). We
    bucket by first character instead: each bucket has ~100-200 patterns,
    which compile fast and match fast.
    """
    buckets = {}
    for cname in concept_names:
        if source_name is not None and cname == source_name:
            continue
        if not cname:
            continue
        key = cname[0].lower()
        parts = buckets.setdefault(key, [])
        if "_" in cname or "-" in cname:
            parts.append(re.escape(cname))
            phrase = slug_to_phrase(cname)
            if phrase != cname and len(phrase) >= 4:
                parts.append(re.escape(phrase))
        else:
            parts.append(re.escape(cname))
    compiled = {}
    reverse = {}
    for cname in concept_names:
        if source_name is not None and cname == source_name:
            continue
        if not cname:
            continue
        reverse[cname] = cname
        if "_" in cname or "-" in cname:
            phrase = slug_to_phrase(cname)
            if phrase != cname and len(phrase) >= 4:
                reverse[phrase] = cname
    for key, parts in buckets.items():
        if parts:
            compiled[key] = re.compile("(?i)" + "|".join(parts))
    return compiled, reverse


def build_ac(concept_names):
    """Build an Aho-Corasick automaton mapping lowercased slugs/phrases
    to their canonical concept slug. Single-pass, linear-time matching —
    ~900x faster than the regex-alternation fallback for 5k+ concepts."""
    A = ahocorasick.Automaton()
    seen = {}
    for cname in concept_names:
        variants = [cname]
        if "_" in cname or "-" in cname:
            phrase = slug_to_phrase(cname)
            if phrase != cname and len(phrase) >= 4:
                variants.append(phrase)
        for v in variants:
            low = v.lower()
            if low not in seen:
                A.add_word(low, cname)
                seen[low] = cname
    A.make_automaton()
    return A


def union_find_links(source_text, union_re, found):
    """Add all concept matches from the bucketed union regexes to found."""
    if not union_re:
        return
    union_re, reverse = union_re
    for key, rx in union_re.items():
        for m in rx.finditer(source_text):
            slug = reverse.get(m.group(0), m.group(0))
            found.add(slug)


def find_links(source_name, source_text, concept_names, alias_index,
               phrase_re_idx=None, slug_re_idx=None, union_re=None, ac=None):
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

    # 3) Name-phrase matching — AC automaton (fast) or union regex (fallback)
    if ac is not None:
        for _end, cname in ac.iter(low):
            found.add(cname)
    elif union_re is not None:
        union_find_links(source_text, union_re, found)
    else:
        # Fallback: per-concept precompiled regexes (slower path)
        for cname in concept_names:
            if cname == source_name:
                continue
            if cname in source_text:
                found.add(cname)
                continue
            if phrase_re_idx and cname in phrase_re_idx:
                if phrase_re_idx[cname].search(source_text):
                    found.add(cname)
            if slug_re_idx and cname in slug_re_idx:
                if slug_re_idx[cname].search(source_text):
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
    # NOTE: keep CJK + alphanumerics; only strip separators/punctuation so that
    # distinct Chinese slugs (e.g. 神经网络 vs 神经形态计算) are NOT collapsed
    # into the same group (the old [^a-z0-9] rule erased all CJK -> "" bug).
    def norm(s): return re.sub(r'[\s_\-\./\\:，。？！、（）()\[\]【】“”"\'’]', '', s.lower())
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
                    _merged_dir = WIKI / "_merged"
                    _merged_dir.mkdir(exist_ok=True)
                    mf.rename(_merged_dir / mf.name)
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
    # Precompile regexes for name-phrase matching (massive speedup)
    print(f"  precompiling regexes...")
    phrase_re_idx = {}
    slug_re_idx = {}
    for cname in concept_names:
        phrase = slug_to_phrase(cname)
        if len(phrase) >= 6:
            phrase_re_idx[cname] = re.compile(r'(?i)\b' + re.escape(phrase) + r'\b')
        slug_re_idx[cname] = re.compile(r'(?i)\b' + re.escape(cname) + r'\b')
    print(f"  regexes ready: {len(phrase_re_idx)} phrases + {len(slug_re_idx)} slugs")
    # Build ONE matcher over all concept slugs+phrases (single-pass matching)
    # Prefer Aho-Corasick (linear, ~900x faster); fall back to union regex.
    ac = None
    union_re = None
    if HAVE_AC:
        ac = build_ac(concept_names)
        print(f"  AC automaton built ({len(concept_names)} concepts)")
    else:
        union_re = build_union_regex(concept_names)  # (regexes, reverse)
        print(f"  union regex built ({len(concept_names)} concepts) — AC unavailable")

    # article texts for concept linking
    art_texts = {}
    for f in ART.glob("*.md"):
        art_texts[f.stem] = f.read_text(encoding='utf-8', errors='ignore')

    # precompute signatures + domains for shared-term linking
    sigs = {c: build_signature(info["text"]) for c, info in concepts.items()}
    doms = {c: domain_of(info["text"]) for c, info in concepts.items()}

    outgoing = defaultdict(set)   # concept -> linked concepts
    art_links = {}                # article -> linked concepts

    # link concepts against all concept texts
    print(f"  linking concepts...")
    for cname, info in concepts.items():
        src = info["text"]
        links = find_links(cname, src, concept_names, None,
                           phrase_re_idx=phrase_re_idx, slug_re_idx=slug_re_idx,
                           union_re=union_re, ac=ac)
        outgoing[cname] = links

    # shared-term (co-occurrence) linking: same domain, >=2 shared vocab terms
    print(f"  shared-term linking...")
    inverted = defaultdict(set)
    for c, terms in sigs.items():
        for t in terms:
            inverted[t].add(c)

    for cname in concept_names:
        cooccurs = defaultdict(int)
        for term in sigs[cname]:
            for other in inverted[term]:
                if other != cname:
                    cooccurs[other] += 1

        candidates = sorted(
            ((other, cnt) for other, cnt in cooccurs.items() if cnt >= 2),
            key=lambda x: (-x[1], x[0])
        )

        for other, cnt in candidates:
            if other in outgoing[cname]:
                continue
            if not (doms[cname] == doms[other] or doms[cname] == "Cross" or doms[other] == "Cross"):
                continue
            outgoing[cname].add(other)
            if len(outgoing[cname]) >= 10:
                break

    # Build incoming from outgoing
    incoming = defaultdict(set)
    for cname, links in outgoing.items():
        for other in links:
            incoming[other].add(cname)

    # link articles -> concepts (alias + pattern + name phrase, precompiled)
    print(f"  linking articles...")
    for aname, atext in art_texts.items():
        links = set()
        low = atext.lower()
        for term, target in CURATED_ALIASES.items():
            if target and term.lower() in low and target in concept_names:
                links.add(target)
        for p, _, cn, _ in CONCEPT_PATTERNS:
            if cn in concept_names and re.search(p, atext, re.IGNORECASE):
                links.add(cn)
        # fast name-phrase matching — AC automaton (or union regex) single pass
        if ac is not None:
            for _end, cname in ac.iter(atext.lower()):
                links.add(cname)
        elif union_re is not None:
            union_find_links(atext, union_re, links)
        else:
            for cname in concept_names:
                if cname in atext:
                    links.add(cname)
                    continue
                if cname in phrase_re_idx and phrase_re_idx[cname].search(atext):
                    links.add(cname)
                if len(links) >= 12:
                    break
        art_links[aname] = links
        # sync article -> concept links into incoming
        for cname in links:
            incoming[cname].add(aname)

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

    # ---- Step 4: reload & refresh index/backlinks/health ----
    concepts = load_concepts()
    concept_names = set(concepts.keys())
    # incoming already fully built in Step 2-3

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
