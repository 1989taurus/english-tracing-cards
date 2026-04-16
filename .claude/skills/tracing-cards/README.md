# tracing-cards

Claude Code skill that generates printable A4 English word tracing worksheets for kindergarten-age children (3–6 years old).

**Version:** 1.0.0 · **License:** MIT · **Offline-only output**

## What you get

- Self-contained HTML file (no network, no build step), print-ready on A4.
- Each card: emoji + word + IPA phonetic + 中文 meaning.
- 4 rows per card on a 四线三格 (four-line three-space) grid:
  - 2 tracing rows with Hershey Futural single-stroke letters (实线，非虚线描红)
  - 2 blank practice rows
- 4 cards per A4 page, strict `height: 297mm` so it prints on exactly one sheet.
- Built-in lexicon of ~50 kindergarten words (animals, fruit, colors, numbers, family, etc.).

## Install

Drop the whole `tracing-cards/` directory into one of:

- Per-project: `<your-project>/.claude/skills/tracing-cards/`
- Per-user: `~/.claude/skills/tracing-cards/`

Final layout:

```
tracing-cards/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── assets/
│   ├── template.html
│   └── snippets.html
├── references/
│   └── example.html
└── evals/
    └── evals.json
```

No package manager, no build. Claude Code picks it up on the next session.

## Use

Start a Claude Code session and say one of:

- 给孩子做一份英文描红卡，单词：cat dog pig…
- 帮我生成英语字帖，主题"小动物"，单词 cat dog cow
- Make a tracing worksheet for apple, book, pen

Claude will interview you for: word list, theme name, auto-fill yes/no, output path. Then it writes `tracing-cards-<slug>.html` to your chosen directory. Open in a browser, `Ctrl/Cmd+P`, select A4, tick **"背景图形 / Background graphics"** so the four-line grid prints, and you're done.

## Requirements

- Claude Code (any recent version).
- A browser that can print to A4 (Chrome/Edge/Safari/Firefox all work).
- No internet required to open or print the generated HTML.

## Constraints

- Lowercase a–z only. Uppercase input is silently lowercased (Hershey defs don't cover A–Z).
- Max ~20 characters per word (advance widths must fit the 1000-unit viewBox).
- If a word isn't in the built-in lexicon, the skill **asks** for emoji/phonetic/meaning rather than fabricate one — wrong IPA actively mis-teaches a young learner.

## Testing

Regression prompts live in `evals/evals.json` — 4 cases covering basic themes, letter coverage, unknown-word handling, and uppercase normalization.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
