# LLM Wiki for Claude Code

Build and maintain a persistent, compounding knowledge base as interlinked markdown files.
Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## When This Activates

Use this workflow when the user:
- Asks to create, build, or start a wiki or knowledge base
- Asks to ingest, add, or process a source into their wiki
- Asks a question and an existing wiki is present
- Asks to lint, audit, or health-check their wiki
- References their wiki, knowledge base, or "notes" in a research context

## Wiki Location

Default: `~/wiki`. Set via `WIKI_PATH` env var if different.

```bash
WIKI="${WIKI_PATH:-$HOME/wiki}"
```

The wiki is just a directory of markdown files — open it in Obsidian, VS Code, or any editor. No database required.

## Architecture: Three Layers

```
wiki/
├── SCHEMA.md           # Conventions, structure rules, domain config
├── index.md            # Sectioned content catalog with one-line summaries
├── log.md              # Chronological action log (append-only, rotated yearly)
├── raw/                # Layer 1: Immutable source material
│   ├── articles/       # Web articles, clippings
│   ├── papers/         # PDFs, arxiv papers
│   ├── transcripts/    # Meeting notes, interviews
│   └── assets/         # Images, diagrams referenced by sources
├── entities/           # Layer 2: Entity pages (people, orgs, products, models)
├── concepts/           # Layer 2: Concept/topic pages
├── comparisons/        # Layer 2: Side-by-side analyses
└── queries/            # Layer 2: Filed query results worth keeping
```

**Layer 1 — Raw Sources:** Immutable. Read but never modify.
**Layer 2 — The Wiki:** Markdown files you create, update, and cross-reference.
**Layer 3 — The Schema:** `SCHEMA.md` defines structure, conventions, and tag taxonomy.

## Resuming an Existing Wiki (CRITICAL)

Always orient yourself before doing anything:

1. **Read `SCHEMA.md`** — understand the domain, conventions, and tag taxonomy.
2. **Read `index.md`** — learn what pages exist and their summaries.
3. **Scan recent `log.md`** — read the last 20-30 entries to understand recent activity.

Use `cat`, `head`, `tail`, `grep`, or any file reading tool available in Claude Code.

## Initializing a New Wiki

1. Determine the wiki path (from `$WIKI_PATH` env var, or ask the user; default `~/wiki`)
2. Create the directory structure above using `mkdir -p`
3. Ask the user what domain the wiki covers — be specific
4. Write `SCHEMA.md` customized to the domain (see template below)
5. Write initial `index.md` with sectioned header
6. Write initial `log.md` with creation entry
7. Confirm the wiki is ready and suggest first sources to ingest

### SCHEMA.md Template

```markdown
# Wiki Schema

## Domain
[What this wiki covers — e.g., "AI/ML research", "personal health", "startup intelligence"]

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `transformer-architecture.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance markers:** On pages that synthesize 3+ sources, append `^[raw/articles/source-file.md]`
  at the end of paragraphs whose claims come from a specific source.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
# Optional quality signals:
confidence: high | medium | low
contested: true
contradictions: [other-page-slug]
---
```

### raw/ Frontmatter
```yaml
---
source_url: https://example.com/article
ingested: YYYY-MM-DD
sha256: <hex digest of the raw content below the frontmatter>
---
```

## Tag Taxonomy
[Define 10-20 top-level tags for the domain. Add new tags here BEFORE using them.]

Example for AI/ML:
- Models: model, architecture, benchmark, training
- People/Orgs: person, company, lab, open-source
- Techniques: optimization, fine-tuning, inference, alignment, data
- Meta: comparison, timeline, controversy, prediction

Rule: every tag on a page must appear in this taxonomy.

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index

## Entity Pages
One page per notable entity. Include:
- Overview / what it is
- Key facts and dates
- Relationships to other entities ([[wikilinks]])
- Source references

## Concept Pages
One page per concept or topic. Include:
- Definition / explanation
- Current state of knowledge
- Open questions or debates
- Related concepts ([[wikilinks]])

## Comparison Pages
Side-by-side analyses. Include:
- What is being compared and why
- Dimensions of comparison (table format preferred)
- Verdict or synthesis
- Sources

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report
```

### index.md Template

```markdown
# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: YYYY-MM-DD | Total pages: N

## Entities
<!-- Alphabetical within section -->

## Concepts

## Comparisons

## Queries
```

### log.md Template

```markdown
# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [YYYY-MM-DD] create | Wiki initialized
- Domain: [domain]
- Structure created with SCHEMA.md, index.md, log.md
```

## Core Operations

### 1. Ingest

When the user provides a source (URL, file, paste), integrate it into the wiki:

① **Capture the raw source:**
   - URL → fetch content (use `curl`, browser, or any available tool), save to `raw/articles/`
   - PDF → extract text, save to `raw/papers/`
   - Pasted text → save to appropriate `raw/` subdirectory
   - Name the file descriptively: `raw/articles/karpathy-llm-wiki-2026.md`
   - **Add raw frontmatter** (`source_url`, `ingested`, `sha256` of the body)

② **Discuss takeaways** with the user — what's interesting, what matters for the domain.

③ **Check what already exists** — search `index.md` and grep across wiki files for existing pages.

④ **Write or update wiki pages:**
   - **New entities/concepts:** Create pages only if they meet the Page Thresholds
   - **Existing pages:** Add new information, update facts, bump `updated` date
   - **Cross-reference:** Every new or updated page must link to at least 2 other pages via `[[wikilinks]]`
   - **Tags:** Only use tags from the taxonomy in SCHEMA.md
   - **Confidence:** For opinion-heavy or single-source claims, set `confidence: medium` or `low`

⑤ **Update navigation:**
   - Add new pages to `index.md` under the correct section, alphabetically
   - Update the "Total pages" count and "Last updated" date
   - Append to `log.md`: `## [YYYY-MM-DD] ingest | Source Title`

⑥ **Report what changed** — list every file created or updated.

### 2. Query

When the user asks a question about the wiki's domain:

① **Read `index.md`** to identify relevant pages.
② **For wikis with 100+ pages**, also grep across all `.md` files for key terms.
③ **Read the relevant pages** using file reading tools.
④ **Synthesize an answer** from the compiled knowledge. Cite the wiki pages you drew from.
⑤ **File valuable answers back** — if the answer is substantial, create a page in `queries/` or `comparisons/`.
⑥ **Update log.md** with the query and whether it was filed.

### 3. Lint

When the user asks to lint, health-check, or audit the wiki:

① **Orphan pages:** Find pages with no inbound `[[wikilinks]]` from other pages.
② **Broken wikilinks:** Find `[[links]]` that point to pages that don't exist.
③ **Index completeness:** Every wiki page should appear in `index.md`.
④ **Frontmatter validation:** Every wiki page must have all required fields.
⑤ **Stale content:** Pages whose `updated` date is >90 days old.
⑥ **Contradictions:** Pages with `contested: true` or `contradictions:` frontmatter.
⑦ **Quality signals:** List pages with `confidence: low`.
⑧ **Source drift:** Recompute sha256 hashes for raw files, flag mismatches.
⑨ **Page size:** Flag pages over 200 lines.
⑩ **Tag audit:** List all tags in use, flag any not in the SCHEMA.md taxonomy.
⑪ **Log rotation:** If log.md exceeds 500 entries, rotate it.
⑫ **Report findings** with specific file paths and suggested actions.
⑬ **Append to log.md:** `## [YYYY-MM-DD] lint | N issues found`

## Working with the Wiki

### Searching

```bash
# Find pages by content
grep -r "transformer" ~/wiki --include="*.md"

# Find pages by tag
grep -r "tags:.*alignment" ~/wiki --include="*.md"

# Recent activity
tail -20 ~/wiki/log.md
```

### Bulk Ingest

When ingesting multiple sources at once, batch the updates:
1. Read all sources first
2. Identify all entities and concepts across all sources
3. Check existing pages for all of them (one search pass, not N)
4. Create/update pages in one pass
5. Update index.md once at the end
6. Write a single log entry covering the batch

### Archiving

When content is fully superseded:
1. Create `_archive/` directory if it doesn't exist
2. Move the page to `_archive/` with its original path
3. Remove from `index.md`
4. Update any pages that linked to it
5. Log the archive action

### Obsidian Integration

The wiki directory works as an Obsidian vault out of the box:
- `[[wikilinks]]` render as clickable links
- Graph View visualizes the knowledge network
- YAML frontmatter powers Dataview queries

For best results:
- Set Obsidian's attachment folder to `raw/assets/`
- Enable "Wikilinks" in Obsidian settings
- Install Dataview plugin for queries

## Pitfalls

- **Never modify files in `raw/`** — sources are immutable. Corrections go in wiki pages.
- **Always orient first** — read SCHEMA + index + recent log before any operation.
- **Always update index.md and log.md** — skipping this makes the wiki degrade.
- **Don't create pages for passing mentions** — follow the Page Thresholds.
- **Don't create pages without cross-references** — isolated pages are invisible.
- **Frontmatter is required** — it enables search, filtering, and staleness detection.
- **Tags must come from the taxonomy** — freeform tags decay into noise.
- **Keep pages scannable** — a wiki page should be readable in 30 seconds.
- **Ask before mass-updating** — if an ingest would touch 10+ existing pages, confirm first.
- **Rotate the log** — when log.md exceeds 500 entries, rename it and start fresh.
- **Handle contradictions explicitly** — don't silently overwrite. Note both claims with dates.

## Automated Continuous Learning

When the user asks the agent to "become an expert" or "continuously learn" about a domain,
set up a scheduled task that runs on a schedule (e.g., hourly) to:

1. **Search** for new content in the domain
2. **Ingest** valuable sources into the wiki
3. **Synthesize** — create or update wiki pages with new insights
4. **Report** findings back to the user

### Context Window Management

For long-running automated learning:

1. **Page count threshold** (~20 pages): When exceeded, trigger consolidation
2. **Log rotation** (~500 entries): Rotate log.md
3. **Staleness review** (every 10 runs): Flag pages not updated in 90 days
4. **Index maintenance**: Keep index.md scannable
5. **Search-first approach**: Before creating any new page, always search existing content

## Related Tools

[llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler) is a Node.js CLI that
compiles sources into a concept wiki with the same Karpathy inspiration. It's Obsidian-compatible.
