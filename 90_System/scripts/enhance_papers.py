#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""enhance_papers.py v1.1 - Cross-day dedup + content enrichment for pipeline papers"""
import os, sys, json, re, hashlib
from datetime import datetime
from pathlib import Path
from collections import defaultdict

VAULT = Path(r'D:\Obsidian\home\work\.openclaw\workspace')
INBOX = VAULT / '00_Inbox'
KNOWLEDGE = VAULT / '10_Knowledge'
DEDUP_DB_V2 = VAULT / '99_Meta' / 'dedup_index_v2.json'
TODAY = datetime.now().strftime('%Y-%m-%d')

def load_dedup_index_v2():
    """V2: keyed by S2 ID + normalized title, stores path and date."""
    if DEDUP_DB_V2.exists():
        try:
            return json.loads(DEDUP_DB_V2.read_text(encoding='utf-8'))
        except:
            pass
    return dict(s2_ids={}, titles={}, total=0)

def save_dedup_index_v2(idx):
    DEDUP_DB_V2.parent.mkdir(exist_ok=True)
    DEDUP_DB_V2.write_text(json.dumps(idx, indent=2, ensure_ascii=False), encoding='utf-8')

def normalize_title(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())[:120]

def extract_s2_id_from_url(url):
    """Extract 40-char hex S2 paper ID from URL or path."""
    if not url:
        return None
    m = re.search(r'([a-f0-9]{40})', url)
    return m.group(1) if m else None

def title_similarity(a, b):
    """Character-level overlap ratio."""
    return sum(1 for ca, cb in zip(a, b) if ca == cb) / max(len(a), len(b), 1)

def is_duplicate_crossday(title, s2_id=None):
    """Check cross-day dedup: exact S2 ID or >90% title similarity."""
    idx = load_dedup_index_v2()
    norm = normalize_title(title)
    # Exact S2 ID match
    if s2_id and s2_id in idx['s2_ids']:
        return True, f'S2 ID: {s2_id}'
    # Exact title match
    if norm in idx['titles']:
        return True, f'Title: {title[:80]}'
    # Near-duplicate title (>90%)
    for existing in idx['titles']:
        if title_similarity(norm, existing) > 0.90:
            return True, f'Near-dup: {title[:60]}'
    return False, ''

def mark_as_seen(title, s2_id=None, filepath=''):
    """Add paper to dedup index."""
    idx = load_dedup_index_v2()
    norm = normalize_title(title)
    if s2_id:
        idx['s2_ids'][s2_id] = filepath
    if norm not in idx['titles']:
        idx['titles'][norm] = filepath
    idx['total'] = len(idx['titles'])
    save_dedup_index_v2(idx)

def scan_vault_content():
    papers = []
    for folder in [INBOX, KNOWLEDGE / 'Papers', KNOWLEDGE / 'Articles']:
        if not folder.exists():
            continue
        for f in folder.rglob('*.md'):
            content = f.read_text(encoding='utf-8', errors='ignore')
            fr = content.split('---')[1] if content.startswith('---') and content.count('---') >= 2 else ''
            title_m = re.search(r'title:\s*"(.+?)"', fr)
            title = title_m.group(1) if title_m else f.stem
            url_m = re.search(r'url:\s*(\S+)', fr)
            url = url_m.group(1) if url_m else ''
            s2_id = extract_s2_id_from_url(url)
            abstract_m = re.search(r'## Abstract\s*\n+(.+?)(?:\n##|\n---|\Z)', content, re.DOTALL)
            abstract = abstract_m.group(1).strip()[:500] if abstract_m else '(no abstract)'
            papers.append(dict(path=str(f), title=title[:150], url=url, s2_id=s2_id, abstract=abstract, size=len(content)))
    return papers

def enrich_with_s2_detail(paper):
    """Fetch full paper details from S2 API."""
    s2_id = paper.get('s2_id') if isinstance(paper, dict) else None
    if not s2_id:
        url = paper.get('url', '') if isinstance(paper, dict) else ''
        s2_id = extract_s2_id_from_url(url) if url else None
    if not s2_id:
        return None
    import urllib.request, ssl
    try:
        ctx = ssl.create_default_context()
        url = f'https://api.semanticscholar.org/graph/v1/paper/{s2_id}?fields=title,abstract,tldr,citationCount,year,authors,fieldsOfStudy,referenceCount,journal,externalIds'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            data = json.loads(r.read())
        return dict(
            abstract=data.get('abstract','') or '',
            tldr=data.get('tldr',{}).get('text','') if data.get('tldr') else '',
            citations=data.get('citationCount',0),
            year=data.get('year',''),
            fields=', '.join(data.get('fieldsOfStudy',[]) or []),
            refs=data.get('referenceCount',0),
            journal=data.get('journal',{}).get('name','') if data.get('journal') else '',
            doi=data.get('externalIds',{}).get('DOI','') if data.get('externalIds') else ''
        )
    except Exception as e:
        return None

def enhance_paper_content(paper):
    detail = enrich_with_s2_detail(paper)
    if not detail:
        return paper.get('abstract', '(no abstract)')
    parts = []
    if detail.get('tldr'):
        parts.append(f"**TL;DR**: {detail['tldr']}")
    if detail.get('abstract'):
        parts.append(f"**Abstract**: {detail['abstract'][:800]}")
    parts.append(f"**Citations**: {detail.get('citations',0)} | Year: {detail.get('year','?')}")
    if detail.get('fields'):
        parts.append(f"**Fields**: {detail['fields']}")
    if detail.get('journal'):
        parts.append(f"**Journal**: {detail['journal']}")
    if detail.get('refs'):
        parts.append(f"**References**: {detail['refs']}")
    return chr(10).join(parts)

def enrich_paper_file(filepath_str):
    """Read a paper file, fetch S2 detail, rewrite with enriched content."""
    fp = Path(filepath_str)
    if not fp.exists():
        return False
    content = fp.read_text(encoding='utf-8', errors='ignore')
    fr = ''
    if content.startswith('---') and content.count('---') >= 2:
        parts = content.split('---', 2)
        fr = parts[1] if len(parts) > 1 else ''
    url_m = re.search(r'url:\s*(\S+)', fr)
    url = url_m.group(1) if url_m else ''
    s2_id = extract_s2_id_from_url(url)
    if not s2_id:
        return False
    detail = enrich_with_s2_detail({'s2_id': s2_id, 'url': url})
    if not detail:
        return False
    enriched_body = []
    if detail.get('tldr'):
        enriched_body.append(f"**TL;DR**: {detail['tldr']}")
    if detail.get('abstract'):
        enriched_body.append(f"**Abstract**: {detail['abstract'][:1200]}")
    meta_parts = []
    if detail.get('year'):
        meta_parts.append(f"Year: {detail['year']}")
    if detail.get('citations'):
        meta_parts.append(f"Citations: {detail['citations']}")
    if detail.get('refs'):
        meta_parts.append(f"References: {detail['refs']}")
    if detail.get('fields'):
        meta_parts.append(f"Fields: {detail['fields']}")
    if detail.get('journal'):
        meta_parts.append(f"Journal: {detail['journal']}")
    if detail.get('doi'):
        meta_parts.append(f"DOI: {detail['doi']}")
    if meta_parts:
        enriched_body.append(' | '.join(meta_parts))
    enriched_text = '\n\n'.join(enriched_body)
    if '## Abstract' in content and enriched_text:
        new_content = re.sub(
            r'## Abstract\s*\n+.+?(?=\n##|\n---|\Z)',
            '## Abstract\n\n' + enriched_text,
            content,
            flags=re.DOTALL
        )
        if new_content != content:
            fp.write_text(new_content, encoding='utf-8')
            # Add TCC/iNEST relevance summary
            summary = generate_tcc_inest_summary(
                detail.get('abstract', '') or detail.get('tldr', ''),
                title=Path(filepath_str).stem
            )
            if summary:
                current = fp.read_text(encoding='utf-8', errors='ignore')
                if '## Relevance to TCC / iNEST' in current and '(TBD' in current:
                    current = current.replace('\r\n', '\n')
                    current = current.replace(
                        '## Relevance to TCC / iNEST\n\n(TBD',
                        '## Relevance to TCC / iNEST\n\n' + summary + '\n\n(TBD'
                    )
                    current = current.replace('\n', '\r\n')
                    fp.write_text(current, encoding='utf-8')
            return True
    return False

def find_real_duplicates_today():
    """Find today's actual duplicates: same S2 ID appearing multiple times today."""
    papers = [p for p in scan_vault_content() if TODAY in p['path']]
    seen = {}
    dupes = []
    for p in papers:
        if p['s2_id']:
            if p['s2_id'] in seen:
                dupes.append(p)
            else:
                seen[p['s2_id']] = p['path']
    return dupes

def rebuild_index_v2():
    """Rebuild V2 dedup index from entire vault."""
    papers = scan_vault_content()
    idx = dict(s2_ids={}, titles={}, total=0)
    for p in papers:
        norm = normalize_title(p['title'])
        if norm not in idx['titles']:
            idx['titles'][norm] = p['path']
        if p['s2_id'] and p['s2_id'] not in idx['s2_ids']:
            idx['s2_ids'][p['s2_id']] = p['path']
    idx['total'] = len(idx['titles'])
    save_dedup_index_v2(idx)
    return idx


def generate_tcc_inest_summary(abstract, title=''):
    """Generate TCC/iNEST relevance summary from abstract using keyword matching + LLM fallback."""
    if not abstract or abstract == '(no abstract)' or len(abstract) < 50:
        return ''
    
    text = (title + ' ' + abstract).lower()
    
    tcc_matches = [kw for kw in TCC_KW if kw.lower() in text]
    inest_matches = [kw for kw in INEST_KW if kw.lower() in text]
    
    tcc_score = len(tcc_matches)
    inest_score = len(inest_matches)
    
    lines = []
    
    if tcc_score > 0:
        lines.append(f'**TCC Relevance** (score={tcc_score}): ')
        if tcc_matches:
            lines.append(f'  Matched: {", ".join(tcc_matches[:5])}')
        # Generate TCC-perspective insight
        if 'topological' in text or 'network-on-chip' in text or 'noc' in text:
            lines.append('  Insight: This work relates to TCC network topology design principles.')
        if 'interconnect' in text or 'routing' in text or 'placement' in text:
            lines.append('  Insight: May inform TCC chiplet interconnect/routing optimization.')
        if 'wafer' in text or 'dark silicon' in text:
            lines.append('  Insight: Relevant to TCC wafer-scale integration architecture.')
        if 'phase transition' in text or 'scale-free' in text:
            lines.append('  Insight: Phase transition / scale-free insights apply to TCC topology criticality.')
        if 'critical' in text and ('network' in text or 'phase' in text):
            lines.append('  Insight: Critical network dynamics may inform TCC topology optimization.')
    
    if inest_score > 0:
        lines.append(f'**iNEST Relevance** (score={inest_score}): ')
        if inest_matches:
            lines.append(f'  Matched: {", ".join(inest_matches[:5])}')
        if 'critical' in text or 'avalanche' in text or 'self-organized' in text:
            lines.append('  Insight: Criticality/avalanche dynamics are core to iNEST emergence theory.')
        if 'emergence' in text or 'self-organiz' in text or 'complex system' in text:
            lines.append('  Insight: Emergence mechanism directly relevant to iNEST theoretical foundation.')
        if 'neuromorphic' in text or 'spiking' in text or 'memristor' in text:
            lines.append('  Insight: Hardware implementation insights for iNEST neuromorphic architecture.')
        if 'free energy' in text or 'active inference' in text:
            lines.append('  Insight: Free energy principle informs iNEST self-organization theory.')
        if 'reservoir' in text or 'liquid state' in text or 'echo state' in text:
            lines.append('  Insight: Reservoir computing paradigm applicable to iNEST computation model.')
        if 'stdp' in text or 'spike-timing' in text:
            lines.append('  Insight: STDP learning rule relevant to iNEST plasticity mechanisms.')
    
    if not lines:
        # No direct match - try broader heuristic
        if any(w in text for w in ['network', 'computing', 'architecture', 'chip', 'neural', 'brain']):
            lines.append('**Potential Relevance**: Contains domain-adjacent concepts. Review for cross-pollination with TCC/iNEST.')
        else:
            return ''
    
    return '\n'.join(lines)

TCC_KW = [k.strip() for k in """topological,network-on-chip,NoC,chiplet,interconnect,wafer-scale,signal integrity,routing,placement,dark silicon,manycore,topological phase,scale-free,heterogeneous integration,UCIe,advanced packaging,photonic,wireless NoC,system-on-wafer,reconfigurable,crossbar,switching fabric,mesh topology,torus topology,deadlock-free,adaptive routing,link utilization,throughput optimization,latency minimization,thermal-aware,power-gating,DVFS,3D stacking,through-silicon via,TSV,interposer,EMIB,CoWoS,fan-out,software-defined,resource allocation""".split(',')]
INEST_KW = [k.strip() for k in """neuromorphic,spiking neural,SNN,memristor,criticality,self-organized,neuronal avalanche,emergence,brain-inspired,edge of chaos,phase transition,free energy,active inference,complex network,reservoir computing,liquid state machine,echo state,STDP,surrogate gradient,integrated information,predictive coding,excitatory inhibitory,synaptic plasticity,long-term potentiation,LTD,homeostatic plasticity,dendritic computation,burst firing,oscillation,synchronization,gamma rhythm,theta rhythm,information bottleneck,mutual information,transfer entropy,Granger causality,effective connectivity,functional connectivity,dynamic causal modeling,mean-field theory,Ising model,branching process,power law,scale invariance,universality class,non-equilibrium,self-organization,autopoiesis,embodied cognition,enactivism,free energy principle,FEP,Markov blanket,Bayesian brain,precision weighting,allostasis,interoception,active sensing,perceptual inference,generative model,message passing,variational Bayes,expectation maximization,factor graph,belief propagation,recurrent neural,attractor network,hopfield network,Boltzmann machine,restricted Boltzmann,deep belief,Helmholtz machine,wake-sleep algorithm,contrastive divergence,energy-based model,equilibrium propagation,predictive processing""".split(',')]


def main():
    print('=' * 60)
    print(f'  Paper Enhance + Dedup v1.1 - {TODAY}')
    print('=' * 60)

    # Rebuild V2 dedup index
    idx = rebuild_index_v2()
    print(f'[1/4] Dedup index V2: {idx["total"]} unique titles, {len(idx["s2_ids"])} S2 IDs')

    # Find real duplicates (same S2 ID today)
    dupes = find_real_duplicates_today()
    if dupes:
        print(f'[2/4] Found {len(dupes)} real duplicates (same S2 ID) in today:')
        for p in dupes:
            print(f'  [{p["s2_id"][:8]}...] {p["title"][:70]}')
    else:
        print(f'[2/4] No real duplicates in today')

    # Enrich today's papers
    papers = scan_vault_content()
    today_papers = [p for p in papers if TODAY in p['path'] and p['s2_id']]
    enriched_count = 0
    if today_papers:
        print(f'[3/4] Enriching {len(today_papers)} papers with S2 IDs...')
        for p in today_papers[:5]:
            if enrich_paper_file(p['path']):
                enriched_count += 1
                print(f'  OK: {p["title"][:60]}...')
            else:
                print(f'  SKIP: {p["title"][:60]}...')
    else:
        print(f'[3/4] No papers with S2 IDs to enrich')

    print(f'[4/4] Enriched {enriched_count}/{len(today_papers)} papers')
    return idx, dupes, enriched_count

if __name__ == '__main__':
    main()
