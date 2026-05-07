# gsk hermes-brain

Personal memory, wiki, and skill management system. Stores user preferences, domain knowledge, and reusable workflows that persist across sessions.

## Authentication

Uses `$GSK_API_KEY` automatically (same as other gsk commands).

## Memory

User-scoped persistent memory: profile (who the user is), knowledge (domain topics), and recent activity.

### Load full memory context (recommended at task start)
```bash
gsk hermes-brain memory_context
```
Returns formatted markdown with profile + knowledge + recent 2 days. Use this to understand user preferences before starting work.

### Read user profile
```bash
gsk hermes-brain memory_profile
```

### Read knowledge topics
```bash
# All topics
gsk hermes-brain memory_knowledge

# Specific topic (identity, preferences, skills, projects)
gsk hermes-brain memory_knowledge -p identity
```

### Save a memory entry
```bash
gsk hermes-brain memory_save -c "User prefers HTML reports with dark theme and structured tables"
```
Appends to today's daily log. Only save genuinely reusable insights, not task-specific details.

## Wiki

Persistent knowledge base organized by category. Good for domain knowledge, entity profiles, comparisons.

### List wiki pages
```bash
# All pages
gsk hermes-brain wiki_list

# Filter by category (entities, concepts, comparisons, queries)
gsk hermes-brain wiki_list --category entities
```

### Search wiki
```bash
gsk hermes-brain wiki_search -q "RL post-training"
```

### Read a wiki page
```bash
gsk hermes-brain wiki_read -p "entities/anthropic"
```

### Write a wiki page
```bash
gsk hermes-brain wiki_write -p "entities/anthropic" \
  -c "# Anthropic\nAI safety company, maker of Claude..." \
  --summary "AI safety company behind Claude"
```
Path format: `category/slug`. Valid categories: entities, concepts, comparisons, queries.

### Delete a wiki page
```bash
gsk hermes-brain wiki_delete -p "entities/anthropic"
```

## Skills

Hermes-auto-extracted reusable workflows. List, read, patch, or delete.

### List all skills
```bash
gsk hermes-brain skill_list
```

### Read a skill
```bash
gsk hermes-brain skill_read -n "daily-report-generator"
```

### Update a skill
```bash
gsk hermes-brain skill_patch -n "daily-report-generator" \
  -c "---\nname: daily-report-generator\ndescription: ...\n---\n\n# Steps\n..."
```

### Delete a skill
```bash
gsk hermes-brain skill_delete -n "daily-report-generator"
```

### View usage statistics
```bash
# All skills
gsk hermes-brain skill_stats

# Specific skill
gsk hermes-brain skill_stats -n "daily-report-generator"
```

## Session Search

Search past project sessions for relevant context.

```bash
gsk hermes-brain session_search -q "arXiv agent paper summary"
```
Returns top 5 matching past sessions with summaries, skills used, and key outputs.

## Best Practices

1. **Start of task**: Run `memory_context` to load user preferences
2. **During task**: Save reusable insights with `memory_save` (not task-specific details)
3. **Domain knowledge**: Use `wiki_write` for persistent reference material
4. **End of task**: If you developed a reusable multi-step workflow, save it with `skill_patch`
5. **Cross-session context**: Use `session_search` to find relevant past work

