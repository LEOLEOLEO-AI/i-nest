---
name: paper-monitor
version: 1.0.0
description: Tracks new papers and patents in a specific research domain — queries arXiv API, Semantic Scholar API, and Google Patents, deduplicates against previous runs, and delivers a structured digest with relevance scoring
metadata:
  category: researcher
  requires:
    bins:
      - gsk
    env:
      - SEMANTIC_SCHOLAR_API_KEY  # optional — free at semanticscholar.org/product/api; raises rate limit from 100 to 1000 req/day
    files:
      - ~/.openclaw/workspace/skills/paper-monitor/config.json   # topics, keywords, sources
      - ~/.openclaw/workspace/skills/paper-monitor/state.json    # seen paper/patent IDs for deduplication
---

# paper-monitor

Track new academic papers and patents in one or more research domains. Queries structured APIs directly for reliable, real-time results — not web search.

## Data Sources and Retrieval Method

### 1. arXiv (papers, no auth required)

Query the arXiv API for each configured topic:

```
GET https://export.arxiv.org/api/query
  ?search_query=all:{keywords}
  &sortBy=submittedDate
  &sortOrder=descending
  &start=0
  &max_results=50
```

Keyword construction:
- Combine topic keywords with `AND`/`OR`: e.g. `all:("large language model" OR "LLM") AND all:(agent OR reasoning)`
- Use `cat:{category}` to restrict by arXiv category (e.g. `cs.AI`, `cs.LG`, `q-bio`, `econ.GN`)

Filter results: only include papers where `published` date is within the configured lookback window (default: 7 days).

Parse the Atom XML response: extract `id`, `title`, `summary`, `author[]`, `published`, `category[]`, `link[@href]`.

### 2. Semantic Scholar (papers, optional API key)

For higher-quality relevance scoring and citation data:

```
GET https://api.semanticscholar.org/graph/v1/paper/search
  ?query={keywords}
  &fields=paperId,title,abstract,authors,year,publicationDate,citationCount,influentialCitationCount,openAccessPdf
  &publicationDateOrYear={start_date}:{end_date}
  &limit=50
```

If `SEMANTIC_SCHOLAR_API_KEY` is set, include header `x-api-key: {key}`.

Without the key, rate limit is 100 requests/5 min — sufficient for daily runs with ≤10 topics.

### 3. Google Patents (patents, no auth required)

For each topic, run a targeted search:

```
gsk search 'site:patents.google.com "{keyword}" after:{date_7_days_ago}'
```

Also query the USPTO full-text search for US patents:

```
GET https://efts.uspto.gov/LATEST/search-fields?query={keywords}&dateRangeField=datePublished&startDate={start}&endDate={end}&hits.hits._source=patentTitle,patentAbstract,applicationNumber,filingDate,assigneeEntityName
```

Extract: patent title, abstract snippet, assignee, filing date, patent URL.

---

## Config File (`config.json`)

Created interactively on first run. Stores user preferences.

```json
{
  "topics": [
    {
      "name": "LLM Agents",
      "arxiv_query": "(\"large language model\" OR LLM) AND (agent OR reasoning OR planning)",
      "arxiv_categories": ["cs.AI", "cs.LG", "cs.CL"],
      "semantic_scholar_query": "LLM agent reasoning planning",
      "patent_keywords": ["language model agent", "AI reasoning system"]
    }
  ],
  "lookback_days": 7,
  "max_results_per_topic": 20,
  "relevance_threshold": 0.6,
  "delivery_method": "email",
  "include_patents": true,
  "include_abstracts": true
}
```

---

## Relevance Scoring

For each result, compute a simple relevance score (0–1):

1. **Keyword density**: count how many of the topic's keywords appear in the title + abstract. Score = matched / total keywords, capped at 1.0.
2. **Title match bonus**: +0.2 if any keyword appears in the title.
3. **Recency bonus**: +0.1 if published within the last 3 days.
4. **Citation signal** (Semantic Scholar only): if `influentialCitationCount > 0`, +0.15.

Discard results with `score < relevance_threshold` (default 0.6). Sort remaining by score descending.

---

## Deduplication

Load `state.json` from the previous run. Skip any result whose ID (arXiv ID, Semantic Scholar paperId, or patent application number) already appears in state. After processing, write all new IDs to `state.json`.

```json
{
  "last_run": "2026-03-21T09:00:00Z",
  "seen_ids": ["2403.12345", "2403.98765", "US20260001234A1"]
}
```

---

## Report Format

```
## Paper & Patent Monitor — {topic name} — {date}

### New Papers ({count} new, {count} filtered out as low-relevance)

**1. {Title}** — score: {0.xx}
Authors: {Author1}, {Author2}, ...
Published: {date} | arXiv: {id} | [PDF]({url})
> {first 2 sentences of abstract}

**2. ...**

---

### New Patents ({count} new)

**1. {Patent Title}**
Assignee: {company} | Filed: {date} | [{application number}]({url})
> {abstract snippet}

---

### Summary
- {count} new papers across {count} topics
- {count} patents
- Top theme this week: {most common keyword cluster}
```

If no new results for a topic: output "No new papers in the past {N} days for this topic."

---

## First-time Setup

On first run, the skill will:

1. Ask the user what research topics or domains to monitor (e.g. "LLM agents", "CRISPR", "quantum computing")
2. For each topic, help construct the arXiv query string and select relevant arXiv categories
3. Ask whether to include patents
4. Ask for lookback window (default: 7 days)
5. Ask for delivery method (this chat / email / WhatsApp)
6. Optionally ask for a Semantic Scholar API key (free, instructions provided)
7. Write `config.json` and an empty `state.json`

---

## Error Handling

- arXiv API unavailable: retry once after 10 seconds; if still failing, skip arXiv for this run and note in report
- Semantic Scholar rate limit hit (429): fall back to arXiv-only for this run; note in report
- USPTO API unavailable: fall back to `gsk search` for patent queries
- `state.json` corrupt or missing: treat all results as new for this run, recreate file
- Empty results for a topic: note "no new activity" — never silently skip a configured topic

