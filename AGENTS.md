# AGENTS.md

## What this repo is

Single-purpose HTML generator for printable English tracing worksheets. No build system, no package manager, no tests.

## Critical distinctions

- **Root `*.html` files are generated output, not source.** Do not hand-edit them. Regenerate via the skill.
- **No `npm`/`pip`/`cargo`/etc.** This is not a software project.

## Workflow

When the user mentions 英语描红 / 描红卡 / 描红 / 英文练字帖 / tracing worksheet / handwriting practice / kindergarten English, load the tracing-cards skill and run the interview flow before generating.

## Generating tracing cards

1. Run the interview (via the skill's `AskUserQuestion` flow) — word list, theme name, auto-fill, output path. Do not skip.
2. Generate HTML by substituting snippets into `assets/template.html`. For the Hershey skill, compute per-letter x offsets from the half-advance table.
3. Verify: count `<div class="card">` == word count, `<section class="page">` == ceil(words/4).

## Invariants

- Lowercase tracing words only (max ~20 chars for Hershey, ~12 for OC)
- Fully offline: inline SVG + Hershey paths + emoji, no external assets
- SVG grid: viewBox `0 0 1000 120`, lines at y=0, 40, 80, 120
- Hershey rendering: `<use href="#l-X">` with `translate(20,17.143) scale(2.857143)` transform

## Skills

| Skill | Approach | Status |
|---|---|---|
| `.claude/skills/tracing-cards/` | Hershey Futural single-stroke SVG paths | Current / preferred |
| `.claude/skills/tracing-cards-oc/` | Comic Sans outline with stroke-dasharray | Legacy alternative |

## Reference

Full spec and lexicon: `.claude/skills/tracing-cards/SKILL.md`
