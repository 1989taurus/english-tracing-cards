# english-tracing-cards

A Claude Code skill that generates **printable A4 English word tracing worksheets** for kindergarten-age children (3–6 years old).

Each worksheet is a self-contained, fully offline HTML file with:
- 4 cards per A4 page (strict `height: 297mm`, prints on exactly one sheet)
- Each card: emoji + word + IPA phonetic + 中文 meaning
- 2 tracing rows (Hershey Futural single-stroke SVG letters — 实线，非虚线描红)
- 2 blank practice rows on a 四线三格 (four-line three-space) grid
- Built-in lexicon of ~50 kindergarten-level words

![layout](https://img.shields.io/badge/layout-A4%20297mm-blue) ![skill](https://img.shields.io/badge/claude--code-skill-7c3aed) ![license](https://img.shields.io/badge/license-MIT-green)

## Sample output

Run the skill, open the generated HTML in any browser, `Ctrl/Cmd+P` → select A4 → tick **"背景图形 / Background graphics"** to keep the four-line grid colors → print.

Preview layout: see [`.claude/skills/tracing-cards/references/example.html`](.claude/skills/tracing-cards/references/example.html) (4-card reference).

## Install the skill

### Option 1 — one-shot from the pre-built `.skill` bundle

```bash
unzip dist/tracing-cards.skill -d ~/.claude/skills/
```

### Option 2 — copy the source tree directly

```bash
cp -r .claude/skills/tracing-cards ~/.claude/skills/
```

Or drop it per-project at `<your-project>/.claude/skills/tracing-cards/`.

No package manager, no build step. Claude Code discovers it on the next session.

## Use it

Start a Claude Code session and say one of:

- `给孩子做一份英文描红卡，单词：cat dog pig …`
- `帮我生成英语字帖，主题"小动物"，单词 cat dog cow`
- `Make a tracing worksheet for apple, book, pen`

Claude will interview you briefly (word list, theme name, auto-fill yes/no, output path) and then write `tracing-cards-<slug>.html` to the directory you chose.

Full spec and trigger keywords: [`.claude/skills/tracing-cards/SKILL.md`](.claude/skills/tracing-cards/SKILL.md).

## Repository layout

```
.
├── .claude/
│   └── skills/
│       ├── tracing-cards/            # current, preferred — Hershey single-stroke SVG
│       │   ├── SKILL.md              # authoritative spec (interview, lexicon, rules)
│       │   ├── README.md             # skill-level usage
│       │   ├── CHANGELOG.md
│       │   ├── LICENSE               # MIT
│       │   ├── assets/
│       │   │   ├── template.html     # A4 shell + Hershey a–z <defs>
│       │   │   └── snippets.html     # page / card / row fragments
│       │   ├── references/
│       │   │   └── example.html      # 4-card reference output
│       │   └── evals/
│       │       └── evals.json        # regression test prompts
│       └── tracing-cards-oc/         # legacy alternative — Comic Sans dashed outline
├── dist/
│   └── tracing-cards.skill           # packaged release (unzip into ~/.claude/skills/)
├── AGENTS.md                         # workflow for Claude Code agents in this repo
├── CLAUDE.md                         # project instructions loaded into every session
└── README.md                         # you are here
```

## Two skills, one repo

| Skill | Approach | Status |
|---|---|---|
| [`tracing-cards/`](.claude/skills/tracing-cards/) | Hershey Futural single-stroke SVG paths | **current / preferred** |
| [`tracing-cards-oc/`](.claude/skills/tracing-cards-oc/) | Comic Sans `<text>` with `stroke-dasharray` | legacy alternative |

The Hershey version produces cleaner single-stroke outlines ideal for tracing; the OC version is simpler but depends on system fonts and renders less consistently.

## Hard invariants

- **Lowercase a–z only** — Hershey defs don't cover A–Z. Uppercase input is silently lowercased.
- **Max ~20 characters per word** — advance widths must fit the 1000-unit SVG viewBox.
- **Fully offline** — no Google Fonts, no external CSS/JS/images. Generated HTML opens and prints without network.
- **Strict A4** — `@page { size: A4; margin: 0 }` + `.page { height: 297mm; overflow: hidden }` with flex layout. Prints on exactly one sheet per page, no blank trailing page.
- **Never fabricate phonetics or meanings** — if a word is outside the built-in lexicon, the skill asks the user rather than guess. Wrong IPA actively mis-teaches a young learner.

## Packaging

The `.skill` bundle is produced by Anthropic's official `skill-creator` tooling:

```bash
# From inside an environment where claude-plugins-official is installed
python3 -m scripts.package_skill \
  /home/<user>/Projects/english/.claude/skills/tracing-cards \
  /home/<user>/Projects/english/dist
```

`evals/` is deliberately excluded from the `.skill` bundle (it's a dev-time regression asset, kept only in source).

## Contributing

This is a small personal project. If you want to extend:

- **Lexicon** — edit the table in `.claude/skills/tracing-cards/SKILL.md` (emoji + IPA + 中文 per word).
- **Grid / layout** — touch `assets/template.html` CSS carefully; re-run `evals/evals.json` after changes.
- **Test prompts** — add a new case to `evals/evals.json` with `id`, `name`, `prompt`, `expected_output`, `assertions[]`.

## License

MIT — see [`.claude/skills/tracing-cards/LICENSE`](.claude/skills/tracing-cards/LICENSE).
