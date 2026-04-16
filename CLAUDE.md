# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repo produces **printable English word tracing worksheets** for kindergarten-age children (ages 3-6). No build system, no package manager, no tests. The only artifact is a self-contained HTML file opened in a browser and printed on A4 paper.

## Architecture

Two local skills live under `.claude/skills/`. The current `tracing-cards/` follows the `/skill-creator` layout — `SKILL.md` (authoritative spec with interview flow, lexicon, generation steps) plus `assets/` (`template.html` outer HTML shell with `{{PAGES}}`, `snippets.html` reusable fragments), `references/` (`example.html` reference output), and `evals/` (test prompts for skill iteration). The legacy `tracing-cards-oc/` still uses the older flat layout.

### `tracing-cards/` — current, preferred

Uses **Hershey Futural single-stroke font** embedded as SVG `<path>` elements in global `<defs>`, rendered via `<use href="#l-X">` with cumulative x offsets computed from per-letter half-advance values. Produces clean single-stroke outlines ideal for tracing.

### `tracing-cards-oc/` — legacy alternative

Uses Comic Sans MS `<text>` elements with `stroke-dasharray="4,3"` for dashed outlines. Simpler generation (no offset math) but depends on system font availability and renders less cleanly for tracing.

### Shared structure

Both skills follow the same snippets: `PAGE_WRAPPER` → `CARD` (×4 per page) → 2 `ROW_TRACE` + 2 `ROW_BLANK`. Both share the same interview flow, lexicon (~50 kindergarten words), and verification steps.

### Generated output

Root-level `tracing-cards-*.html` files are **generated output, not source**. Naming: `tracing-cards-<theme-slug>.html`. Files ending in `*-test.html` are iteration/debugging artifacts. Regenerate via the skill rather than hand-editing.

## Generation Pipeline

1. **Interview** the user via `AskUserQuestion` — word list, theme name, auto-fill yes/no, output path. Do not skip.
2. For each word: resolve emoji/phonetic/meaning from the lexicon (or ask user if unknown — never guess), lowercase the word, substitute into CARD snippet.
3. For `tracing-cards/` (Hershey): compute per-letter x offsets from the half-advance table in SKILL.md, build SVG with `<use>` elements inside a scaled `<g>` transform.
4. Group cards **4 per page** into PAGE_WRAPPER sections (fill `{{THEME}}` with user's theme name), inject into `assets/template.html` at `{{PAGES}}`.
5. **Verify**: read back first 30 lines, count `<div class="card">` == word count, count `<section class="page">` == ceil(words/4), report counts.

## Hard Invariants (do not change without reason)

**SVG grid** (both skills):
- viewBox `0 0 1000 120`, grid lines at **y=0, 40, 80, 120** (四线三格).

**Hershey rendering** (`tracing-cards/` only):
- `<path>` defs in `assets/template.html` for a–z, rendered via `<use href="#l-X">`.
- Transform: `translate(20, 17.143) scale(2.857143)` — scale = 40/14, TY = 80 − 2.857×22.
- Stroke: `fill="none" stroke="#5a9ed0" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"`.
- Max ~20 characters per word (advance widths must fit viewBox 1000).

**General**:
- **Lowercase only** — Hershey defs cover a-z only. Uppercase (A-Z) is not supported; reject gracefully.
- **Fully offline**: inline SVG + emoji + system fonts. No Google Fonts, no external CSS, no network assets.
- Strip punctuation, reject non-ASCII in tracing words (中文/emoji fine in meaning/emoji fields).
- Do not auto-open the file in a browser — user may be headless.

## Activation

Triggers on: 英语描红 / 描红卡 / 英文练字帖 / 单词描红 / tracing worksheet / handwriting practice / kindergarten English. Always run the interview flow before generating.
