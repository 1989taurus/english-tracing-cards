---
name: tracing-cards
description: Generate printable A4 English word tracing practice worksheets for kindergarten-age children (3-6 years old). Produces a self-contained, fully offline HTML file featuring 四线三格 (four-line three-space) handwriting grid, Hershey Futural solid single-stroke SVG tracing letters, emoji illustrations, IPA phonetics, and Chinese meanings. Use this skill whenever a user mentions 英语描红, 描红卡, 描红练习, 单词描红, 英文练字帖, tracing worksheet, tracing cards, handwriting practice, kindergarten English, preschool English writing, printable word practice for kids, or asks a parent/teacher-style request to create printable letter/word practice sheets for young children — even when they don't literally say 描红卡 or tracing. Also trigger for requests like 给孩子做一份英文单词练习打印, 幼儿园英语字帖, preschool handwriting sheet.
license: MIT
metadata:
  version: 1.0.0
  authors:
    - shengjia
---

# Tracing Cards

Generate A4-printable English word tracing worksheets for kindergarten-age children. Each card has emoji + word + phonetic + 中文 meaning, followed by 2 tracing rows (Hershey single-stroke letters) and 2 blank practice rows on a 四线三格 grid.

## When to Activate

Trigger when the user wants printable English word practice material for young children. Typical signals:

- 用户提到：英语描红、描红卡、描红练习、单词描红、英文练字帖、字帖、幼儿英语字帖、tracing worksheet、tracing cards、handwriting practice、kindergarten English、preschool English writing
- 家长/老师说要给小朋友做英文单词练习、打印的字帖、暑假练习本
- 用户想要把一组单词做成可打印的练习单

If the user's request plausibly fits this goal, prefer to activate this skill rather than hand-rolling a one-off HTML — the skill guarantees correct grid coordinates, offline self-containment, and consistent card layout.

## Skill Layout

```
tracing-cards/
├── SKILL.md              ← you are here
├── assets/
│   ├── template.html     ← outer HTML shell + Hershey a-z <defs>
│   └── snippets.html     ← PAGE_WRAPPER / CARD / ROW_TRACE / ROW_BLANK fragments
├── references/
│   └── example.html      ← reference output (4 words, cat/dog/pig/duck)
└── evals/
    └── evals.json        ← test prompts for this skill
```

Read `assets/template.html` and `assets/snippets.html` at generation time. `references/example.html` is only for reference when you're unsure what correct output looks like.

## Interview Flow

Run this interview first with `AskUserQuestion`. Skipping hurts output quality because: (a) the word list drives everything downstream, (b) the theme name is baked into the page header and filename, (c) missing meanings would force guessing. Only skip individual questions whose answer is already unambiguous from the user's prompt.

Ask up to 4 questions in one batch:

1. **单词列表** — "请提供要练习的单词（空格或逗号分隔）"
   - Skip if the user already listed words in their message.
   - Accept 3-20 words; if >20, warn the user — too many cards on one worksheet overwhelms a 3-6 year old.

2. **主题名称** — "给这份练习起个名字？" e.g. "小动物单词练习"
   - Used in page header (via `{{THEME}}`) and filename slug.
   - Default: "英语描红练习".

3. **是否自动补全中文释义和音标** — yes/no
   - yes: fill in from the built-in lexicon below; if a word is missing there, ask the user rather than fabricate.
   - no: ask the user to provide meanings inline (e.g. `cat=猫`).

4. **输出路径** — 保存到当前目录 / 桌面 / 用户指定路径
   - Default: `./tracing-cards-<slug>.html` in the current working directory.

Do not ask about: tracing style, rows per word, words per page, file format. These were fixed during skill design — HTML + 四线三格 + 2 tracing rows + 2 blank rows + 4 cards per A4 page — to keep output consistent across runs and printable in a single pass.

## Built-in Lexicon (Kindergarten Level)

Use this for emoji/phonetic/meaning when auto-fill is chosen. If a word isn't here, ask the user rather than guess — wrong phonetics or meanings actively harm early learners.

| word | emoji | phonetic | 中文 |
|---|---|---|---|
| cat | 🐱 | /kæt/ | 猫 |
| dog | 🐶 | /dɔːɡ/ | 狗 |
| pig | 🐷 | /pɪɡ/ | 猪 |
| cow | 🐮 | /kaʊ/ | 奶牛 |
| duck | 🦆 | /dʌk/ | 鸭子 |
| bird | 🐦 | /bɜːrd/ | 鸟 |
| fish | 🐟 | /fɪʃ/ | 鱼 |
| bear | 🐻 | /ber/ | 熊 |
| lion | 🦁 | /ˈlaɪən/ | 狮子 |
| tiger | 🐯 | /ˈtaɪɡər/ | 老虎 |
| apple | 🍎 | /ˈæpl/ | 苹果 |
| banana | 🍌 | /bəˈnænə/ | 香蕉 |
| orange | 🍊 | /ˈɔːrɪndʒ/ | 橙子 |
| grape | 🍇 | /ɡreɪp/ | 葡萄 |
| pear | 🍐 | /per/ | 梨 |
| red | 🟥 | /red/ | 红色 |
| blue | 🟦 | /bluː/ | 蓝色 |
| green | 🟩 | /ɡriːn/ | 绿色 |
| yellow | 🟨 | /ˈjeloʊ/ | 黄色 |
| pink | 🌸 | /pɪŋk/ | 粉色 |
| one | 1️⃣ | /wʌn/ | 一 |
| two | 2️⃣ | /tuː/ | 二 |
| three | 3️⃣ | /θriː/ | 三 |
| four | 4️⃣ | /fɔːr/ | 四 |
| five | 5️⃣ | /faɪv/ | 五 |
| sun | ☀️ | /sʌn/ | 太阳 |
| moon | 🌙 | /muːn/ | 月亮 |
| star | ⭐ | /stɑːr/ | 星星 |
| tree | 🌳 | /triː/ | 树 |
| flower | 🌷 | /ˈflaʊər/ | 花 |
| car | 🚗 | /kɑːr/ | 汽车 |
| bus | 🚌 | /bʌs/ | 公交车 |
| bike | 🚲 | /baɪk/ | 自行车 |
| ball | ⚽ | /bɔːl/ | 球 |
| book | 📖 | /bʊk/ | 书 |
| pen | 🖊️ | /pen/ | 笔 |
| bag | 🎒 | /bæɡ/ | 书包 |
| hand | ✋ | /hænd/ | 手 |
| eye | 👁️ | /aɪ/ | 眼睛 |
| ear | 👂 | /ɪr/ | 耳朵 |
| mom | 👩 | /mɑːm/ | 妈妈 |
| dad | 👨 | /dæd/ | 爸爸 |
| boy | 👦 | /bɔɪ/ | 男孩 |
| girl | 👧 | /ɡɜːrl/ | 女孩 |
| cake | 🍰 | /keɪk/ | 蛋糕 |
| milk | 🥛 | /mɪlk/ | 牛奶 |
| egg | 🥚 | /eɡ/ | 鸡蛋 |
| rain | 🌧️ | /reɪn/ | 雨 |
| snow | ❄️ | /snoʊ/ | 雪 |
| cloud | ☁️ | /klaʊd/ | 云 |
| hat | 🎩 | /hæt/ | 帽子 |

## Generation Steps

1. Read `assets/template.html` and `assets/snippets.html`. The Hershey `<path>` defs for a-z are already embedded in `template.html` — no need to inline them yourself.

2. For each word, build one CARD:
   - Resolve emoji / phonetic / meaning from the lexicon or user-provided input.
   - Lowercase the word. Kindergarten tracing is lowercase convention, and the Hershey defs in the template only cover a-z.
   - Substitute `{{EMOJI}} {{WORD}} {{PHONETIC}} {{MEANING}}` into the CARD snippet.
   - Replace each `{{ROW_TRACE}}` marker with a complete SVG (see step 3).
   - Replace each `{{ROW_BLANK}}` marker with the ROW_BLANK snippet verbatim (grid only, no letters).

3. Build each `{{ROW_TRACE}}` SVG by laying out Hershey letters:
   - Look up each letter's half-advance `o` value from the table below.
   - Compute cumulative x offsets: `x[0] = 0`, `x[n] = sum(2 * o[i] for i in 0..n-1)`.
   - Do not add 20 to each x offset — the left padding is already applied by the `translate(20, ...)` on the group transform. Adding it twice pushes letters past the right edge of the viewBox.
   - Emit SVG with grid lines at y=0/40/80/120, then a `<g transform="translate(20,17.143) scale(2.857143)" fill="none" stroke="#5a9ed0" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke">` containing `<use href="#l-LETTER" x="OFFSET"/>` per letter.

4. Group cards into pages (4 cards per page). For each page, substitute `{{PAGE_NUM}}`, `{{PAGE_TOTAL}}`, `{{THEME}}` (the user's theme name), and `{{CARDS}}` into PAGE_WRAPPER.

5. Concatenate all pages into `{{PAGES}}` inside `template.html`, and fill `{{TITLE}}` with the theme name.

6. Write the final HTML to the user's chosen output path.

7. Print a short summary: output path, word count, page count, and the usage hint: "在浏览器打开 → Ctrl/Cmd+P → 选 A4 → 打印".

## Hershey Futural Letter Half-Advances

Cumulative x offsets depend on these per-letter advance widths:

| a:10 | b:9 | c:9 | d:10 | e:9 | f:7 | g:10 | h:10 | i:4 | j:5 | k:8 | l:4 |
| m:15 | n:10 | o:10 | p:9 | q:10 | r:6 | s:9 | t:7 | u:10 | v:8 | w:11 | x:9 | y:8 | z:9 |

Formula: `x[0] = 0, x[n] = sum(2 * o[i] for i in 0..n-1)`.

## Rules

- **Never fabricate phonetics or meanings.** If a word isn't in the lexicon and the user didn't provide one, stop and ask. Wrong IPA or wrong 中文 actively mis-teaches a young learner — worse than asking one extra question.
- **Lowercase only.** Hershey defs only cover a-z. Uppercase input should be lowercased transparently; if the user explicitly asks for uppercase, explain that the current font only renders lowercase and proceed with lowercase.
- **Offline self-contained output.** Everything must be inline (SVG + emoji + system fonts). No Google Fonts, no external CSS, no network assets. Reason: the worksheet often prints from a device without internet, and broken fonts ruin the practice.
- **Preserve four-line grid coordinates** (y = 0 / 40 / 80 / 120 in viewBox `0 0 1000 120`). These define the 四线三格 handwriting zones; shifting them breaks the whole pedagogical intent.
- **Hershey single-stroke rendering.** All letters are rendered via `<use href="#l-X">` referencing the defs in `template.html`, with solid blue strokes (实线). No `fill`; stroke only.
- **Word length ≤ ~20 characters.** Total advance width must fit viewBox `1000`. For longer words the letters overflow the right edge — warn the user and suggest splitting.
- **Sanitize tracing words.** Strip punctuation, reject non-ASCII letters in the tracing word itself. Emoji and 中文 are fine in the meaning field, just not in the word that gets traced.
- **Strict A4 page sizing.** Each `<section class="page">` must fit exactly on one A4 sheet when printed. The CSS in `assets/template.html` enforces this and must not be weakened:
  - `@page { size: A4; margin: 0 }` — printer margins are zero; page padding is handled inside `.page`.
  - `.page { width: 210mm; height: 297mm; padding: 10mm 12mm; overflow: hidden; page-break-after: always; page-break-inside: avoid; display: flex; flex-direction: column }` — fixed A4 box, flex column so header/cards/footer distribute vertically.
  - `.cards-area { flex: 1 1 auto; display: flex; flex-direction: column; justify-content: space-between; gap: 4mm; min-height: 0 }` plus `.card { flex: 1 1 0; min-height: 0 }` and `.row { flex: 1 1 0; min-height: 0 }` — 4 cards split the remaining vertical space evenly, never overflow.
  - `@media print { html, body { width: 210mm; margin: 0; padding: 0; background: #fff } }` + `-webkit-print-color-adjust: exact` on body — colors print, no extra blank page from body margins.
  - Reason: a previous version used `min-height: 297mm` + `@page margin: 12mm 14mm`, which double-counted padding and produced a blank trailing page per worksheet. Do not reintroduce `min-height` on `.page`; use fixed `height` so the browser can't grow the box.
  - Print instruction for the user: "浏览器打开 → Ctrl/Cmd+P → 选 A4 → 勾选'背景图形'保留四线格颜色".

## Verification

After writing the file, always run these checks and include the counts in your reply. They catch the most common regressions (empty file, wrong card count, wrong page count) cheaply:

1. Read the first 30 lines back — confirm the file isn't empty and the header includes the theme name.
2. Count `<div class="card">` occurrences — should equal the word count.
3. Count `<section class="page">` — should equal `ceil(words / 4)`.
4. Grep the output for `height: 297mm`, `@page`, and `overflow: hidden` — confirm the strict-A4 CSS survived template substitution. If any is missing, the file will print with a blank trailing page or overflow.

Do not auto-open the file in a browser. The user may be on a headless system, and opening a GUI app there either fails loudly or silently spawns a zombie process.

## Testing

Test prompts for this skill live in `evals/evals.json`. When modifying the skill, re-run them and check that outputs still pass the verification checks above.
