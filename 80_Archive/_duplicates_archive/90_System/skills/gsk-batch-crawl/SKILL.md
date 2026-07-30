---
name: gsk-batch-crawl
version: 1.0.0
description: Crawl multiple URLs in parallel and answer specific questions from each. More efficient than calling gsk crawl multiple times.
metadata:
  category: general
  requires:
    bins:
    - gsk
  cliHelp: gsk batch_crawl_url_and_answer --help
---

# gsk-batch-crawl

**PREREQUISITE:** Read `../gsk-shared/SKILL.md` for auth, global flags, and security rules.

Crawl multiple URLs in parallel and answer specific questions from each. More efficient than calling `gsk crawl` multiple times.

## Usage

```bash
gsk batch_crawl_url_and_answer '[{"url":"<url1>","questions_to_answer":["<q1>"]},{"url":"<url2>","questions_to_answer":["<q2>"]}]'
```

**Aliases:** `batch-crawl`

## Input Format

JSON array of job objects:

| Field | Required | Description |
|-------|----------|-------------|
| `url` | Yes | URL to crawl |
| `questions_to_answer` | Yes | List of questions to answer from the page content |

## When to Use

**Prefer `gsk batch-crawl` over multiple `gsk crawl` calls** when you need to read 2+ URLs. It crawls all URLs in parallel, reducing total time and credits.

- Expect ~30-50% of URLs to fail; select reliable sources (official sites, major news outlets)
- Use `gsk crawl` for single URLs or when you need the full page content without specific questions

## Example

```bash
# Crawl two product pages and extract specific information
gsk batch_crawl_url_and_answer '[
  {"url":"https://openai.com/pricing","questions_to_answer":["What are the pricing tiers?","Is there a free plan?"]},
  {"url":"https://anthropic.com/pricing","questions_to_answer":["What models are available?","What are the token limits?"]}
]'
```

