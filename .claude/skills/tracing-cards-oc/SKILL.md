---
name: tracing-cards-oc
description: Generate printable English word tracing practice cards for young children (ages 3-6). Produces a self-contained HTML file with 四线三格 (four-line three-space) grid, SVG dashed tracing letters, emoji illustrations, phonetics, and Chinese meanings. Use when the user asks for 英语描红 / 描红卡 / 英文练字帖 / tracing worksheet / 幼儿英语单词练习 / 单词描红.
origin: user
---

# Tracing Cards

Generate A4-printable English word tracing worksheets for kindergarten-age children. Each card has emoji + word + phonetic + 中文 meaning, followed by 2 dashed-letter tracing rows and 2 blank practice rows on a 四线三格 grid.

## When to Activate

- 用户提到：英语描红、描红卡、描红练习、单词描红、英文练字帖、tracing worksheet、tracing cards、handwriting practice、kindergarten English
- 用户想为幼儿/小朋友做英语单词练习材料
- 用户要打印一份可手写练习的英文单词卡

## Interview Flow (Mandatory)

Always run this interview first using `AskUserQuestion`. Never skip — defaults only apply if the user explicitly says "用默认" or "just go".

Ask up to 4 questions in one batch:

1. **单词列表** — "请提供要练习的单词（空格或逗号分隔）"
   - If user gives them in the same message, skip this question
   - Accept 3-20 words; warn if >20 (太多会压垮幼儿)

2. **主题名称** — "给这份练习起个名字？" e.g. "小动物单词练习"
   - Used in page header and filename
   - Default: "英语描红练习"

3. **是否自动补全中文释义和音标** — yes/no
   - yes: you fill in from the built-in lexicon below; ask user to verify unknown words
   - no: ask user to provide meanings inline (e.g. `cat=猫`)

4. **输出路径** — 保存到当前目录 / 桌面 / 用户指定路径
   - Default: `./tracing-cards-<slug>.html` in the current working directory

Do NOT ask about: tracing style, rows per word, words per page, file format.
Those were fixed during skill design: **HTML, 四线三格 + 虚线字, 2 dashed + 2 blank rows, 4 words per A4 page**.

## Built-in Lexicon (Kindergarten Level)

Use these for emoji/phonetic/meaning when auto-fill is chosen. If a word is missing here, ask the user to provide those fields rather than guessing.

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

1. Read `template.html` and `snippets.html` (in this skill directory).
2. For each word:
   - Resolve emoji / phonetic / meaning (lexicon or user-provided).
   - Lowercase the word (tracing is lowercase — kindergarten convention). Preserve user case only if they explicitly ask for uppercase.
   - Build one CARD by substituting `{{EMOJI}} {{WORD}} {{PHONETIC}} {{MEANING}}` into the CARD snippet.
   - Inside the card, each `{{ROW_TRACE}}` becomes the ROW_TRACE snippet with `{{WORD}}` substituted (same lowercase word).
   - Each `{{ROW_BLANK}}` becomes the ROW_BLANK snippet verbatim.
3. Group cards into pages, **4 cards per page**. Build PAGE_WRAPPER for each page, filling `{{PAGE_NUM}}`, `{{PAGE_TOTAL}}`, and `{{CARDS}}`.
4. Concatenate all pages into `{{PAGES}}` in `template.html`. Fill `{{TITLE}}` with the theme name.
5. Write the final HTML to the output path the user chose.
6. Print a short summary:
   - Output file path
   - Word count
   - Page count
   - How to use: "在浏览器打开 → Ctrl/Cmd+P → 选 A4 → 打印"

## Rules

- **Never hardcode unknown words.** If a word isn't in the lexicon and the user didn't provide meaning, stop and ask.
- **Lowercase by default.** Kindergarten tracing uses lowercase letters unless explicitly asked otherwise.
- **No external assets.** Everything must be inline (SVG + emoji + system fonts). The HTML must work offline.
- **No network fonts.** Comic Sans / Chalkboard / fallback cursive only. Do not inject Google Fonts.
- **Preserve the four-line grid coordinates** (0 / 40 / 80 / 120) and font-size 80 when generating SVG — they are tuned so that Comic Sans descenders (g, p, q, y) and ascenders (b, d, h, k, l) land inside the correct zones.
- **Max 12 characters per word** for the tracing row (otherwise letter-spacing breaks). Warn the user if a word is longer.
- **Do not remove the `letter-spacing="6"` attribute** — it separates traced letters so kids can see each one clearly.
- **Sanitize user words**: strip punctuation, reject non-ASCII letters in the tracing word itself (emoji/中文 are fine in meaning fields).

## Verification

After writing the file, ALWAYS:
1. Read the first 30 lines back to confirm it's not empty.
2. Count `<div class="card">` occurrences — must equal the word count.
3. Count `<section class="page">` — must equal `ceil(words / 4)`.
4. Report counts to the user.

Do NOT auto-open the file in a browser (user may be on a headless system).
