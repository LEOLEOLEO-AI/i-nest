# Open-Source AI Research-Agent Projects — Primary-Source Findings

Method: all files fetched raw (raw.githubusercontent.com) / arXiv HTML; claims below are quoted or paraphrased from those artifacts. Scratch copies kept in `D:\Obsidian\_tmp_research_agents\` (disposable).

---

## A) SakanaAI/AI-Scientist (v1)

### A1. Pipeline stages, in order, with real modules

Paper states three phases + review ([arXiv:2408.06292](https://arxiv.org/abs/2408.06292), §1/§3): *"(1) Idea Generation, (2) Experimental Iteration, and (3) Paper Write-up"*, then §4 automated review.

Entrypoint [`launch_scientist.py`](https://github.com/SakanaAI/AI-Scientist/blob/main/launch_scientist.py):

| # | Stage | Module / function | Evidence |
|---|---|---|---|
| 1 | Idea generation (+ self-reflection, `NUM_REFLECTIONS = 3`) | `ai_scientist/generate_ideas.py::generate_ideas(base_dir, client, model, max_num_generations, num_reflections)` | reads `templates/<exp>/prompt.json` (`prompt["system"]`, `prompt["task_description"]`) and `seed_ideas.json`; writes `templates/<exp>/ideas.json` |
| 2 | Novelty check (literature search) | `ai_scientist/generate_ideas.py::check_idea_novelty(ideas, base_dir, engine="semanticscholar"\|"openalex")`; `search_for_papers()` hits `https://api.semanticscholar.org/graph/v1/paper/search` | sets `idea["novel"] = novel`; `launch_scientist.py:363` keeps only `novel_ideas` |
| 3 | Code writing + experiment iteration | `ai_scientist/perform_experiments.py::perform_experiments(idea, folder_name, coder, baseline_results)` driving an **Aider** `Coder` (`edit_format="diff"`, `fnames=[experiment.py, plot.py, notes.txt]`) | `launch_scientist.py:209-225` |
| 4 | Experiment execution + plotting | `run_experiment(folder_name, run_num, timeout=7200)` → `python experiment.py --out_dir=run_{i}`; `run_plotting()` → `python plot.py` | `MAX_RUNS = 5`, `MAX_ITERS = 4`; failures feed stderr back to Aider; success prompt requires `'ALL_COMPLETED'` to stop |
| 5 | Paper writing (LaTeX) | `ai_scientist/perform_writeup.py::perform_writeup(...)`, `generate_latex(coder, folder_name, pdf_file, timeout=30, num_error_corrections=5)`, `compile_latex()` | `compile_latex` runs `pdflatex -interaction=nonstopmode template.tex` → `bibtex template` → `pdflatex` ×2; `chktex {writeup_file} -q -n2 -n24 -n13 -n1` |
| 5b | Citation collection | `get_citation_aider_prompt(...)` loop in `perform_writeup.py`, default `num_cite_rounds=20` | Semantic Scholar/OpenAlex bibtex injected into `references.bib`; prompt: *"You must use \cite or \citet to reference papers, do not manually type out author names."* |
| 6 | Automated review | `ai_scientist/perform_review.py::load_paper()` + `perform_review()` | writes `results/<exp>/<idea>/review.txt` (JSON) |
| 6b | Optional improvement loop (`--improvement`) | `perform_improvement(review, coder)` + `generate_latex(...)` → `review_improved.txt` | `launch_scientist.py:285-308` |

### A2. The "automated reviewer"

[`ai_scientist/perform_review.py`](https://github.com/SakanaAI/AI-Scientist/blob/main/ai_scientist/perform_review.py)

- System prompt: `reviewer_system_prompt_base = "You are an AI researcher who is reviewing a paper that was submitted to a prestigious ML venue." + "Be critical and cautious in your decision."`; default `reviewer_system_prompt=reviewer_system_prompt_neg` (adds *"If a paper is bad or you are unsure, give it bad scores and reject it."*).
- **It is a NeurIPS rubric** — the prompt form variable is literally `neurips_form`, and it lists: Originality / Quality / Clarity / Significance (1–4 low→very high); **Soundness / Presentation / Contribution (1–4 poor/fair/good/excellent)**; **Overall 1–10 (very strong reject → award quality)**; Confidence 1–5; **Decision ∈ {Accept, Reject}** (explicitly forbidding Weak/Borderline/Strong variants). Prompt references the *"NeurIPS ethics guidelines"*.
- Robustification: `num_reflections` (reflexion loop, exits on `"I am done"`), `num_fs_examples` (few-shot from `ai_scientist/fewshot_examples/{132_automated_relational,attention,2_carpe_diem}.{pdf,json}`), `num_reviews_ensemble` (batch responses at T=0.75, then `get_meta_review()` with `meta_reviewer_system_prompt = "You are an Area Chair at a machine learning conference."`, and each score overwritten with `int(round(np.mean(scores)))`).
- Invocation in the pipeline: `num_reflections=5, num_fs_examples=1, num_reviews_ensemble=5, temperature=0.1, model="gpt-4o-2024-05-13"`.
- **Used as a quality filter/selection signal**: paper §1 point 2 — *"The reviews further enable The AI Scientist to select the best ideas for 'publication' to an ever-growing archive of scientific discoveries"*.

### A3. v1 template / seed-idea constraint, and how v2 removed it

- v1: README *Introduction* — *"We provide three templates, which were used in our paper, covering the following domains: NanoGPT, 2D Diffusion, and Grokking."* New templates require a fixed file contract: `experiment.py`, `plot.py`, `prompt.json`, **`seed_ideas.json`**, `latex/template.tex` (README §"Making Your Own Template"). Example seed ideas exist per template, e.g. [`templates/2d_diffusion/seed_ideas.json`](https://github.com/SakanaAI/AI-Scientist/blob/main/templates/2d_diffusion/seed_ideas.json) = one idea `learning_rate_schedule` with `Interestingness/Feasibility/Novelty`. Paper §3: *"We provide The AI Scientist with a starting code template that reproduces a lightweight baseline training run…"*. README FAQ: *"In this current iteration, this is restricted to ideas that can be expressed in code."*
- v2 removal: v2 README — *"the AI Scientist-v2 removes reliance on human-authored templates, generalizes across Machine Learning (ML) domains, and employs a progressive agentic tree search, guided by an experiment manager agent."* v2 paper §3.2 "Removing Template Dependency": *"The AI Scientist-v1 also depended on the predefined template code as a starting baseline implementation. The LLM-driven code changes were then limited to sequential code adaptations."* Replacement mechanism = topic-Markdown-driven ideation (`ai_scientist/perform_ideation_temp_free.py`) + Experiment Progress Manager (4 stages) + parallelized agentic tree search + Hugging Face `datasets.load_dataset` data loading.

### A4. Exact numbers (quoted only)

**Reviewer benchmark** — v1 paper Table 1, "Performance of The AI Scientist's automated LLM reviewing system on **500 ICLR 2022 papers**" ([arXiv:2408.06292](https://arxiv.org/abs/2408.06292)):

| Reviewer | Balanced Acc. | Accuracy | F1 | AUC | FPR | FNR |
|---|---|---|---|---|---|---|
| Human (NeurIPS consistency experiment) | **0.66** | **0.73** | **0.49** | **0.65** | **0.17** | **0.52** |
| GPT-4o (1-shot) @6 (best AI reviewer) | **0.65** ±0.04 | **0.66** ±0.04 | **0.57** ±0.05 | **0.65** ±0.04 | **0.31** ±0.05 | **0.39** ±0.07 |

Paper text: *"achieves 70% accuracy when combining 5 rounds of self-reflection, 5 ensembled reviews, and a 1-shot review example"*; *"superhuman F1 Scores (0.57 vs. 0.49) and human-level AUC (0.65 for both) when thresholding the decision at a score of 6"*; *"human-level accuracy (0.65% vs. 0.66%)"* [sic — paper typo for 0.65 vs 0.66]; inter-human reviewer score correlation **0.14** vs LLM-vs-mean-human **0.18**; *"Each review is generated for $0.25 to $0.50 in API costs."* Cost per generated paper: *"less than $15 per paper"* (paper abstract/§1; README FAQ: *"Typically less than $15 per paper with Claude Sonnet 3.5"*).

**"ICLR workshop acceptance claim" for v1: does not exist.** The v1 paper's 10 `ICLR` mentions all concern the ICLR-2022 OpenReview benchmark set; the v1 [blog post](https://sakana.ai/ai-scientist/) contains **0** occurrences of `ICLR`, `workshop`, or `accept`. v1's actual claim is weaker and self-graded: *"The AI Scientist can produce papers that exceed the acceptance threshold at a top machine learning conference **as judged by our automated reviewer**"* (paper §1). The peer-reviewed-workshop-acceptance claim is **v2's** (see B3). v1 case-study paper's own automated review: `"Soundness": 3, "Presentation": 3, "Contribution": 3, "Overall": 5, "Confidence": 4, "Decision": "Reject"` (paper Appendix).

---

## B) SakanaAI/AI-Scientist-v2

### B1. Agentic tree search, concretely

Search space = **experiment nodes**. v2 paper §3.2.2 defines a node as: *"a collection comprising an experiment script (e.g., a Python file), a textual description of the high-level plan implemented in the script, an execution error trace (if applicable), experiment runtime, performance metrics recorded during the experiment, feedback from an LLM after running the script, a visualization script, file paths to the generated figures, feedback from a VLM on those figures, and the node's final status (either buggy or non-buggy)."*

**Selection/expansion policy** — [`ai_scientist/treesearch/parallel_agent.py::ParallelAgent._select_parallel_nodes`](https://github.com/SakanaAI/AI-Scientist-v2/blob/main/ai_scientist/treesearch/parallel_agent.py) (`while len(nodes_to_process) < self.num_workers`), in this priority order:
1. **Drafting**: if `len(self.journal.draft_nodes) < search_cfg.num_drafts` → append `None` (a new root tree).
2. **Debug branch** with probability `debug_prob`: pick `random.choice` of `journal.buggy_nodes` filtered by `n.is_leaf and n.debug_depth <= search_cfg.max_debug_depth`.
3. **Stage 4** (`stage_name.startswith("4_")`) → always expand `self.best_stage3_node`.
4. **Stage 2** (`"2_"`) → always expand `self.best_stage1_node`.
5. **Stages 1 & 3 — "normal best-first search"**: `best_node = self.journal.get_best_node(cfg=self.cfg)`; prefer a node from a not-yet-processed tree; otherwise iterate `sorted(good_nodes, key=lambda n: n.metric, reverse=True)`.

**"Promising" determination** — [`journal.py::Journal.get_best_node`](https://github.com/SakanaAI/AI-Scientist-v2/blob/main/ai_scientist/treesearch/journal.py): candidates = `good_nodes`; if >1 node, an **LLM evaluator** picks the best. Prompt: *"You are an experienced AI researcher evaluating different implementations of an experiment to select the best one. You should consider all aspects including performance metrics, training dynamics, generated plots quality."* … *"Avoid relying too heavily on validation loss alone…"*; called via `query(..., func_spec=node_selection_spec, model="gpt-4o", temperature=0.3)` (defaults), with **fallback `max(nodes, key=lambda n: n.metric)`** on parse/selection failure. `good_nodes = [n for n in nodes if n.is_buggy is False and n.is_buggy_plots is False]`; `draft_nodes = [n for n in nodes if n.parent is None]`.

**Buggy/debug loop** — `MinimalAgent._debug(parent_node)`: prompt = *"Your previous code for research experiment had a bug, so based on the information below, you should revise it in order to fix this bug."* with `Previous (buggy) implementation`, `Execution output` (`parent_node.term_out`), `Feedback based on generated plots` (`vlm_feedback_summary`), `Feedback about execution time`, and a required *"brief natural language description (3-5 sentences) of how the issue in the previous implementation can be fixed."* Bug status set in `parse_exec_result`: `node.is_buggy = response["is_bug"] or node.exc_type is not None`. Path abandoned at `debug_depth > max_debug_depth`.

**Config** — [`bfts_config.yaml`](https://github.com/SakanaAI/AI-Scientist-v2/blob/main/bfts_config.yaml): `agent.type: parallel`, `num_workers: 4`, `search: {max_debug_depth: 3, debug_prob: 0.5, num_drafts: 3}`, `stages.stage{1,2,3,4}_max_iters: 20/12/12/18`, `multi_seed_eval.num_seeds: 3`, `exec.timeout: 3600`, `agent.code.model: anthropic.claude-3-5-sonnet-20241022-v2:0`, `agent.feedback.model`/`vlm_feedback.model: gpt-4o-2024-11-20`.

**AIDE lineage** — v2 README *Acknowledgement*: *"The tree search component implemented within the `ai_scientist` directory is built on top of the AIDE project"* ([WecoAI/aideml](https://github.com/WecoAI/aideml)). Live UI panel title in `perform_experiments_bfts_with_agentmanager.py`: `'AIDE is working on experiment: "…"'`.

**Four stages (Experiment Progress Manager)** — [`agent_manager.py`](https://github.com/SakanaAI/AI-Scientist-v2/blob/main/ai_scientist/treesearch/agent_manager.py): `main_stage_dict = {1: "initial_implementation", 2: "baseline_tuning", 3: "creative_research", 4: "ablation_studies"}`; initial `Stage(name="1_initial_implementation_1_preliminary", …, num_drafts=cfg.agent.search.num_drafts, stage_number=1)`; additional `Stage`/sub-stage goals are LLM-generated (`generate_substage_goals`, `generate_stage_config`, `evaluate_stage_completion/progression`). Node variants: hyperparameter nodes (Stage 2), ablation nodes (Stage 4), replication nodes (multi-seed), aggregation nodes (no new experiment).

### B2. VLM reviewer — yes, it reads the plots

[`ai_scientist/perform_vlm_review.py`](https://github.com/SakanaAI/AI-Scientist-v2/blob/main/ai_scientist/perform_vlm_review.py): `encode_image_to_base64`; `extract_figure_screenshots(pdf_path, img_folder_path)` crops figure screenshots from the PDF by regexing `Figure X.` / `Fig.` captions and pairing them with main-text figrefs; `perform_imgs_cap_ref_review()` sends `[prompt, img["images"], ...]` to the vision API. Required JSON keys: `Img_description`, `Img_review`, `Caption_review`, `Figrefs_review` (+ `Overall_comments`, `Containing_sub_figures`, `Informative_review`), plus `detect_duplicate_figures()`. Used at **two** points: during tree search (`MinimalAgent._analyze_plots_with_vlm` → sets `node.is_buggy_plots`) and during manuscript reflection (called from `launch_scientist_bfts.py:312`). v2 paper §3.4: *"The AI Scientist-v2 incorporates VLMs at two phases… VLMs provide immediate feedback on generated figures… VLM feedback, we significantly enhance the visual quality."*

### B3. "Workshop-level" claim — verified, quoted

- v2 README: *"a generalized end-to-end agentic system that has generated the first workshop paper written entirely by AI and accepted through peer review."*
- v2 abstract ([arXiv:2504.08066](https://arxiv.org/abs/2504.08066)): *"one manuscript achieved high enough scores to exceed the average human acceptance threshold, marking the first instance of a fully AI-generated paper successfully navigating a peer review."*
- v2 paper §4/§4.1 (exact numbers): *"It received peer-review scores of 6 (weak accept), 7 (accept), and 6 (weak accept) before meta-review and ranked among the top 45% submitted workshop papers."*; *"one manuscript achieved a sufficiently high average reviewer score (**6.33 out of 10**, with individual scores of 6, 6, and 7) to surpass the workshop's acceptance threshold. The remaining two submissions received lower scores and were not accepted."* Venue = ICLR 2025 workshop *"I Can't Believe It's Not Better"* (ICBINB), 3 AI manuscripts among **43 total submissions**, blind review, *"Reviewers were informed in advance that some submissions might be AI-generated, but were not told which"*, opt-out allowed, IRB UBC **H24-02652**.
- **Critical caveat, authors' own**: *"Prior to the workshop submission, we arranged… that any accepted AI-generated manuscripts would be withdrawn after the review process."* And §5: *"the acceptance occurred at a workshop level rather than at the main conference track, and only one of the three AI-generated submissions was accepted… acceptance rates at workshops (typically 60-80%) are notably higher"*; internal review concluded *"none of the manuscripts met the quality standards typical of top-tier main-track conferences."*

### B4. LaTeX, compilation, citations

Yes — it writes and compiles LaTeX. [`ai_scientist/perform_writeup.py`](https://github.com/SakanaAI/AI-Scientist-v2/blob/main/ai_scientist/perform_writeup.py): `compile_latex(cwd, pdf_file, timeout=30)` = `pdflatex -interaction=nonstopmode template.tex` → `bibtex template` → `pdflatex` ×2; `chktex {writeup_file} -q -n2 -n24 -n13 -n1` linting inside the reflection loop (`n_writeup_reflections=3`, exit on `"I am done"`); `detect_pages_before_impact()` enforces `page_limit` (8 for `--writeup-type normal`, 4 for `icbinb`, default). Citation handling: `launch_scientist_bfts.py` calls `gather_citations(idea_dir, num_cite_rounds=20, small_model=model_citation)` and passes `citations_text` in; bibtex comes from Semantic Scholar (`papers[i]["citationStyles"]["bibtex"]`, `ai_scientist/tools/semantic_scholar.py`); prompts require `\cite`/`\citet` and *"Ensure no paper is cited without a corresponding reference in the `references.bib` file."* LaTeX templates shipped: `ai_scientist/blank_icbinb_latex/`, `ai_scientist/blank_icml_latex/`. Known failure admitted in §4.1: *"The AI Scientist-v2 occasionally introduced inaccuracies in citations, similar to the well-known 'hallucination' issue."*

---

## C) langchain-ai/local-deep-researcher

Graph file: [`src/ollama_deep_researcher/graph.py`](https://github.com/langchain-ai/local-deep-researcher/blob/main/src/ollama_deep_researcher/graph.py) (registered by `langgraph.json` as `./src/ollama_deep_researcher/graph.py:graph`).

### C1. Exact node/edge topology

Nodes (exact identifiers):
```
builder.add_node("generate_query",     generate_query)
builder.add_node("web_research",       web_research)
builder.add_node("summarize_sources",  summarize_sources)
builder.add_node("reflect_on_summary", reflect_on_summary)
builder.add_node("finalize_summary",   finalize_summary)
```
Edges (exact):
```
START -> generate_query -> web_research -> summarize_sources -> reflect_on_summary
add_conditional_edges("reflect_on_summary", route_research)   # -> "web_research" | "finalize_summary"
finalize_summary -> END
```
> Correction to the task's assumed names: the reflection node is **`reflect_on_summary`** (not `reflection`); `generate_query`, `web_research`, `summarize_sources`, `finalize_summary` are as assumed. There is **no** edge `web_research -> reflect_on_summary` directly; summarization always sits between them.

Router: `route_research(state, config)` returns `"web_research"` if `state.research_loop_count <= configurable.max_web_research_loops` else `"finalize_summary"`; the counter is incremented in `web_research` (`"research_loop_count": state.research_loop_count + 1`).

### C2. The reflection node + iteration cap

`reflect_on_summary(state, config)`: formats `reflection_instructions.format(research_topic=state.research_topic)` from `prompts.py`, appends either `tool_calling_reflection_instructions` or `json_mode_reflection_instructions`, sends `SystemMessage + HumanMessage("Reflect on our existing knowledge: … identify a knowledge gap and generate a follow-up web search query:")`, and extracts structured output via tool class `FollowUpQuery(BaseModel)` with fields `follow_up_query: str` ("Write a specific question to address this gap") and `knowledge_gap: str` ("Describe what information is missing or needs clarification") — or JSON mode. It returns `{"search_query": ...}` through the shared helper `generate_search_query_with_structured_output(...)`, with `fallback_query=f"Tell me more about {state.research_topic}"`. So: it identifies knowledge gaps and emits the next query, which `web_research` consumes.

**Iteration cap**: `Configuration.max_web_research_loops: int = Field(default=3, title="Research Depth")` in `configuration.py`; overridable via env `MAX_WEB_RESEARCH_LOOPS` (README) or LangGraph Studio config. Priority: env vars > LangGraph UI config > defaults in `Configuration`.

### C3. Single-agent or multi-agent?

**Single-agent.** One LLM in a loop: every node instantiates one `ChatOllama` / `ChatLMStudio` (`get_llm()` and the inline instance in `summarize_sources`), temperature 0. There is no supervisor/worker split, no handoff, no second agent, no separate tool-using policy — the graph is a 5-node cyclic state machine over one model. `use_tool_calling` (default `False`) only switches *structured-output transport* (JSON mode vs bind_tools) for `generate_query`/`reflect_on_summary`; it adds no agent.

### C4. Search backends and local model support

`SearchAPI(Enum) = PERPLEXITY | TAVILY | DUCKDUCKGO | SEARXNG`; `search_api` default `"duckduckgo"`. Implementations in [`utils.py`](https://github.com/langchain-ai/local-deep-researcher/blob/main/src/ollama_deep_researcher/utils.py): `duckduckgo_search` (max_results=3), `searxng_search` (3), `tavily_search` (`api.tavily.com`), `perplexity_search` (`POST https://api.perplexity.ai/chat/completions`); `fetch_raw_content()` pulls full pages when `fetch_full_page=True`; `deduplicate_and_format_sources(..., max_tokens_per_source=1000)` (`MAX_TOKENS_PER_SOURCE = 1000`, `CHARS_PER_TOKEN = 4`).

Local models: **Ollama** (`ChatOllama`, `OLLAMA_BASE_URL` default `http://localhost:11434/`) and **LMStudio** (`ChatLMStudio` in `lmstudio.py`, `LMSTUDIO_BASE_URL` default `http://localhost:1234/v1`, OpenAI-compatible); `LOCAL_LLM` default `llama3.2`; `llm_provider: Literal["ollama","lmstudio"]`. **No llama.cpp / llama-cpp-python backend exists in the repo** (tree: `graph.py, state.py, configuration.py, utils.py, prompts.py, lmstudio.py, __init__.py`). README warns `gpt-oss` models don't support JSON mode in Ollama → set `use_tool_calling`. README also points to a third-party TS port (`PacoVK/ollama-deep-researcher-ts`, no Perplexity).

### C5. State storage / export

[`state.py`](https://github.com/langchain-ai/local-deep-researcher/blob/main/src/ollama_deep_researcher/state.py): `SummaryState` = `research_topic`, `search_query`, `web_research_results: Annotated[list, operator.add]`, `sources_gathered: Annotated[list, operator.add]`, `research_loop_count: int`, `running_summary: str`. Input schema `SummaryStateInput(research_topic)`; output schema `SummaryStateOutput(running_summary)` — i.e. **the markdown report is the graph state, not a file on disk**. `finalize_summary` builds `f"## Summary\n{state.running_summary}\n\n ### Sources:\n{all_sources}"` after de-duplicating source lines. I found **no repo-level file write** for the report (no `open(...,"w")` in the package); persistence is whatever LangGraph Studio / the LangGraph API checkpointer provides, and the README's *"The output of the graph is a markdown file containing the research summary, with citations to the sources used"* refers to that state view.

---

## D) nickscamara/open-deep-research

### D1. Architecture — what Firecrawl does, the loop, the "reasoning" step

Entry: [`app/(chat)/api/chat/route.ts`](https://github.com/nickscamara/open-deep-research/blob/main/app/(chat)/api/chat/route.ts). `FirecrawlApp` from `@mendable/firecrawl-js` supplies **search** (`app.search(query)`) and **extract** (`app.extract(urls, {...})`). Allowed tools: `firecrawlTools = ['search','extract','scrape']`, plus `deepResearch` only when the client sets `experimental_deepResearch`. The outer chat call is `streamText({ ..., maxSteps: 10, experimental_activeTools: ... })`.

The **`deepResearch` tool** is the actual research agent (`execute: async ({ topic, maxDepth = 7 })`, `timeLimit = 4.5 * 60 * 1000`, `maxFailedAttempts: 3`, `totalExpectedSteps: maxDepth * 5`). Loop `while (researchState.currentDepth < maxDepth)`:
1. **search** — `app.search(researchState.nextSearchTopic || topic)`; returns `searchResult.data` → sources streamed via `addSource`.
2. **extract** — `extractFromUrls(urls)` fans out `app.extract([url], {...})` per URL into `researchState.findings: {text, source}[]`.
3. **"reasoning" step** — `analyzeAndPlan(findings)` calls `generateText({ model: customModel(reasoningModel.apiIdentifier, true), prompt: ... })` with a prompt that includes minutes remaining and asks *"What has been learned? What gaps remain? What specific aspects should be investigated next if any?"* and must return JSON `{"analysis": {"summary", "gaps": [...], "nextSteps": [...], "shouldContinue": bool, "nextSearchTopic", "urlToSearch"}}`. Results set `researchState.nextSearchTopic`, `urlToSearch`, `summaries`; loop exits when `!analysis.shouldContinue || analysis.gaps.length === 0`, else `topic = analysis.gaps.shift() || topic`.
4. **final synthesis** — one more `generateText` with the reasoning model: *"Create a comprehensive long analysis of … Include citations to sources where appropriate. This analysis should be very comprehensive and full of details."* → emits `{findings, analysis: finalAnalysis.text, completedSteps, totalSteps}`.

Progress is streamed with `dataStream.writeData({type: 'progress-init' | 'source-delta' | 'activity-delta' | 'depth-delta' | ...})`, where activity types are `'search' | 'extract' | 'analyze' | 'reasoning' | 'synthesis' | 'thought'`. UI: `components/deep-research.tsx`, `components/extract-results.tsx`, `components/search-results.tsx`, `components/scrape-results.tsx`, `lib/deep-research-context.tsx`. So the cycle is **plan/seed → search → extract → analyze(reflect) → search… → synthesize**; there is no explicit separate "plan" LLM call before the first search (the topic seeds it).

### D2. Stack and multi-agent?

**TypeScript / Next.js — yes.** `app/` App Router with RSC + Server Actions, `next.config.ts`, Tailwind + shadcn/ui + Radix, Vercel AI SDK, Drizzle ORM (`lib/db/migrations/0000…0005`), NextAuth (`app/(auth)/`), Vercel Postgres (Neon) for chat history and Vercel Blob for files. Default model `gpt-4o`; `REASONING_MODEL` env (default `o1-mini`; also `deepseek-ai/DeepSeek-R1` via TogetherAI with `BYPASS_JSON_VALIDATION=true`); OpenRouter supported. `MAX_DURATION` default 300 s (README warns Hobby tier needs 60 s).

**Multi-agent — no.** There is one chat agent in a `streamText` tool loop; the "reasoning model" is a distinct *model binding* for structured analysis, not an autonomous peer agent. No agent registry, no handoff, no planner/executor/critic separation.

### D3. Maintenance status

- Last commit: **2025-05-07T15:38:26Z** (`eea0962c8be343230d9571cbdeb82df12504ad72`, message "Update README.md"); `pushed_at = 2025-05-07T15:38:28Z`; repo `created_at = 2025-02-03T16:02:40Z` (GitHub REST API).
- `archived: false`; branches `main`, `nsc/improvements`.
- README contains **no** deprecation / archive / "no longer maintained" / fork notice (grep for `archiv|maintain|deprecat|no longer|sunset|fork` → 0 hits).
- Verdict: **dormant, not formally archived** — roughly a single ~3-month burst (Feb–May 2025) of activity, then no commits through 2026. Stars 6,285 at time of query.
- Successor check: `GET /repos/firecrawl/open-deep-research` returned **404**; the highest-starred same-named repos are `langchain-ai/open_deep_research` (12,687★, pushed 2026-08-10) and `btahir/open-deep-research` (2,141★, pushed 2025-12-15). Whether Firecrawl published a renamed successor is **unverified**.

---

## Unverified / explicitly not claimed

- No aggregate "reviewer score" distribution for v1's generated papers was found in README or paper beyond single case-study reviews — **unverified**.
- v1→v2 comparison of paper quality numbers: v2 README explicitly declines (*"doesn't necessarily produce better papers than v1"*) — no headline metric.
- Successor-maintainer status of open-deep-research beyond the 404 above — **unverified**.
- Star counts are point-in-time from the GitHub REST API and may drift.
