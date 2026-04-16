# Changelog

All notable changes to the `tracing-cards` skill.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-04-17

First distribution-ready release.

### Added
- `SKILL.md` — authoritative spec conforming to `/skill-creator` layout (frontmatter with pushy description + trigger keywords, interview flow, lexicon of ~50 kindergarten words, generation steps, Hershey half-advance table, rules with rationale, verification checklist).
- `assets/template.html` — outer HTML shell with Hershey Futural a–z `<path>` defs and strict-A4 CSS.
- `assets/snippets.html` — reusable `PAGE_WRAPPER` / `CARD` / `ROW_TRACE` / `ROW_BLANK` fragments.
- `references/example.html` — reference output (4 cards) for visual comparison.
- `evals/evals.json` — 4 regression test cases: `basic-animals-theme`, `hard-letter-coverage`, `unknown-word-asks-user`, `uppercase-auto-lowercase`.
- Strict A4 print sizing: `@page { size: A4; margin: 0 }` + `.page { height: 297mm; overflow: hidden; page-break-inside: avoid }` with flex column layout so 4 cards per page distribute vertically without overflow or blank trailing pages.
- `-webkit-print-color-adjust: exact` so four-line grid colors survive browser print.
- Verification step 4: grep output for `height: 297mm`, `@page`, and `overflow: hidden` to catch CSS regressions during template edits.

### Design decisions
- Lowercase-only tracing — Hershey defs cover `a-z` only; uppercase is lowercased transparently.
- Never fabricate phonetics or meanings — if a word is outside the built-in lexicon, the skill stops and asks the user rather than guess.
- Fully offline — everything inline (SVG + emoji + system fonts), no Google Fonts or external CSS/JS, so worksheets print correctly from devices without internet.

### Known limitations
- Max ~20 characters per word (Hershey advance widths must fit viewBox 1000).
- 4 cards per A4 page is hard-coded (tuned for readable tracing row height on a single sheet).
- Built-in lexicon is kindergarten-scoped (~50 words); larger vocabularies require user-provided meanings/phonetics.
