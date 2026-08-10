---
provenance: external
---

# schema.md — iNEST Research Wiki Compiler

_LLM instructions for compiling raw materials into structured knowledge._

## Architecture

```
raw/                → NEVER modify. Original materials only.
  inbox/            → Genspark, Codex, 得到大脑 imports
  tcc/papers/       → TCC research papers (from 30_TCC)
  tcc/fragments/    → TCC literature fragments
  inest/papers/     → iNEST research papers (from 40_iNEST)
  inest/fragments/  → iNEST literature fragments
  imports/          → Inbox classified imports

wiki/               → LLM-compiled structured knowledge. ALWAYS updated by LLM.
  concepts/         → Individual concept files (one concept per file)
  articles/         → Paper/article summaries with extracted insights
  index.md          → Global index with topic clusters
  backlinks.md      → Reverse link index
  health.md         → Knowledge health report with gaps & recommendations
```

## Compilation Pipeline

Trigger: after each automated import or daily pipeline run.

### Phase 1: Summarize
- Read each file in raw/(papers|imports) that is NEWER than its wiki/ counterpart
- Generate a 200-word summary capturing: problem, method, key result, relevance to TCC/iNEST
- Output to wiki/articles/{source}_{date}.md

### Phase 2: Concept Extraction
- From each new summary, extract 3-7 key concepts
- Each concept gets its own file at wiki/concepts/{concept_name}.md
- Concept file format:
  ```markdown
  # {Concept Name}
  
  **Domain**: TCC | iNEST | Cross
  **First mentioned**: {source} ({date})
  **Last updated**: {date}
  
  ## Definition
  {1-2 sentence clear definition}
  
  ## Context
  {2-3 sentences on why this matters in TCC/iNEST research}
  
  ## Related Work
  - : {relationship}
  - : {relationship}
  
  ## Sources
  - {source_reference_1}
  - {source_reference_2}
  
  ## Open Questions
  - {question_1}
  - {question_2}
  ```

### Phase 3: Cross-linking
- For each new/modified concept, scan ALL concepts for related entries
- Insert [[wikilinks]] bidirectionally
- Update backlinks.md

### Phase 4: Index Update
- Update wiki/index.md with topic clusters:
  ```markdown
  # Wiki Index
  
  ## TCC — Topology-Centric Computing
  ### Core Concepts
  - [[SDI_Bond]] — Software-Defined Interconnect bonding mechanism
  - [[Meta_Topology]] — Meta-topology framework
  - ...
  
  ### Active Papers
  - [[P-Paradigm_NatureElectronics_2026]] — P-Paradigm paper
  - ...
  
  ## iNEST — In-Network Neuromorphic
  ### Core Concepts
  - [[Spike_Timing_Dependent_Plasticity]] — STDP learning rule
  - ...
  
  ## Cross-Domain Bridges
  - [[Wafer_Scale_Neuromorphic]] ← TCC wafer-scale × iNEST neuromorphic
  - ...
  ```

### Phase 5: Health Check
- Find orphan concepts (no incoming links)
- Find broken links (target doesn't exist)
- Find concept gaps (mentioned but not defined)
- Find research contradictions (conflicting claims across sources)
- Generate health.md report
- Suggest next steps

## Prompt Templates

### Concept Extraction Prompt
```
You are a research knowledge compiler for TCC (Topology-Centric Computing) and iNEST (In-Network Neuromorphic) domains.

Given this research paper summary, extract all key concepts. A concept is:
- A technical term with a specific definition in this research context
- A method, algorithm, or architecture component
- A theoretical framework or mathematical construct
- A hardware/software component with domain significance

For each concept, provide:
1. Name (precise, used as wikilink target)
2. Domain (TCC/iNEST/Cross)
3. Definition (1-2 sentences)
4. Importance (why it matters)
5. Related concepts (from existing wiki if known)

Output JSON array.
```

### Research Direction Analysis Prompt
```
You are an AI research strategist for TCC + iNEST domains.
Based on the current wiki state:
- Identify 3-5 knowledge gaps (concepts mentioned without deep exploration)
- Propose 3-5 research directions bridging gaps between TCC and iNEST
- Identify 3-5 papers/concepts that should be read next given current research trajectory
- Suggest 2-3 hypotheses that could be tested computationally

Be specific. Cite actual concept names from the wiki.
```

## File Naming Conventions
- Concepts: `Camel_Case_With_Underscores.md` (e.g., `SDI_Bond.md`, `Spike_Timing_Plasticity.md`)
- Articles: `{first_author}_{year}_{topic_keyword}.md` (e.g., `Zhang_2026_wafer_scale_interconnect.md`)
- Always use English filenames, Obsidian aliases for Chinese names

## Update Rules
- raw/ files: NEVER modify. Only READ.
- wiki/ files: ALWAYS update via compilation pipeline.
- Concept files: merge incremental updates (don't overwrite).
- Index: regenerate from concept graph each compilation.
- Backlinks: regenerate from concept graph each compilation.
- Health: regenerate on each compilation run.
