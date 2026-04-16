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

为幼儿园年龄段（3–6 岁）的小朋友生成可打印 A4 英语单词描红练习卡。每张卡片由 emoji + 单词 + 音标 + 中文释义构成，下面接 2 行描红（Hershey 单笔画字母）和 2 行空白练习，统一印在四线三格上。

## 何时激活

当用户想要为小朋友打印英语单词练习材料时激活本 skill。典型信号：

- 用户提到：英语描红、描红卡、描红练习、单词描红、英文练字帖、字帖、幼儿英语字帖、tracing worksheet、tracing cards、handwriting practice、kindergarten English、preschool English writing
- 家长/老师说要给小朋友做英文单词练习、打印的字帖、暑假练习本
- 用户想要把一组单词做成可打印的练习单

只要用户的请求合理地落在这个目标范围内，优先启用本 skill，而不是临时手搓一份 HTML —— skill 能保证网格坐标正确、完全离线自包含、每张卡片的版式统一。

## Skill 目录

```
tracing-cards/
├── SKILL.md              ← 就是你正在读的这份
├── assets/
│   ├── template.html     ← HTML 外壳 + Hershey a-z <defs>
│   └── snippets.html     ← PAGE_WRAPPER / CARD / ROW_TRACE / ROW_BLANK 片段
├── references/
│   └── example.html      ← 参考输出（4 个词：cat/dog/pig/duck）
└── evals/
    └── evals.json        ← 本 skill 的测试 prompt
```

生成时读取 `assets/template.html` 和 `assets/snippets.html`。`references/example.html` 只在你不确定正确输出该长什么样时参考。

## 访谈流程

用 `AskUserQuestion` 先做访谈。为什么不能跳过：(a) 词列表决定了后续一切；(b) 主题名会写进页眉和文件名；(c) 缺释义就只能乱猜。只有当用户的 prompt 已经把某一项说得清清楚楚时，才可以略过该问题。

一次性最多问 4 题：

1. **单词列表** — "请提供要练习的单词（空格或逗号分隔）"
   - 如果用户已经在消息里列了单词，跳过。
   - 建议 3–20 词；超过 20 要提醒用户——单张练习卡太多词会让 3–6 岁的小朋友抓不住重点。

2. **主题名称** — "给这份练习起个名字？" 例如 "小动物单词练习"
   - 会出现在页眉（`{{THEME}}`）和文件名 slug 里。
   - 默认："英语描红练习"。

3. **是否自动补全中文释义和音标** — yes/no
   - yes：从下面的内置词库里取；词库里没有的，**停下来问用户**，不要猜。
   - no：让用户在单词后面用 `cat=猫` 形式给出释义。

4. **输出路径** — 当前目录 / 桌面 / 用户自己指定
   - 默认：当前工作目录下的 `./tracing-cards-<slug>.html`。

**不要问**：描红样式、每词几行、每页几张、文件格式。这些在 skill 设计阶段就固定了——HTML + 四线三格 + 2 行描红 + 2 行空白 + 每 A4 页 4 卡——目的是跨次运行保证一致，一次打印就能用。

## 内置词库（幼儿园级别）

选择"自动补全"时用这份表取 emoji / 音标 / 释义。词库里没有的词，问用户，不要猜——错误的音标或释义对早期学习者的伤害比多问一个问题大得多。

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

## 生成步骤

1. 读取 `assets/template.html` 和 `assets/snippets.html`。a–z 的 Hershey `<path>` defs 已经嵌在 `template.html` 里，不用自己内联。

2. 对每个词构建一张 CARD：
   - 从词库或用户输入里取 emoji / 音标 / 释义。
   - 把单词转小写。幼儿园的描红约定是小写，而且模板里的 Hershey defs 只覆盖 a–z。
   - 把 `{{EMOJI}} {{WORD}} {{PHONETIC}} {{MEANING}}` 填到 CARD 片段里。
   - 把每个 `{{ROW_TRACE}}` 标记替换成完整 SVG（见第 3 步）。
   - 把每个 `{{ROW_BLANK}}` 标记按 ROW_BLANK 片段原样替换（只有网格，没有字母）。

3. 通过排列 Hershey 字母来构建每一行 `{{ROW_TRACE}}` SVG：
   - 从下面的半宽表里查出每个字母的半宽 `o`。
   - 累加 x 偏移：`x[0] = 0`，`x[n] = sum(2 * o[i] for i in 0..n-1)`。
   - **不要**在每个 x 偏移上再加 20——左侧 padding 已经在 group 的 `translate(20, ...)` transform 里处理了。再加一次会把字母推到 viewBox 右边界之外。
   - 发射 SVG：先画 y=0/40/80/120 的网格线，然后是一个 `<g transform="translate(20,17.143) scale(2.857143)" fill="none" stroke="#5a9ed0" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke">`，里面每个字母用一个 `<use href="#l-LETTER" x="OFFSET"/>`。

4. 把卡片按 4 张一页分组。每一页把 `{{PAGE_NUM}}`、`{{PAGE_TOTAL}}`、`{{THEME}}`（用户给的主题名）、`{{CARDS}}` 填进 PAGE_WRAPPER。

5. 把所有页串起来塞进 `template.html` 的 `{{PAGES}}` 位置，`{{TITLE}}` 填主题名。

6. 把最终 HTML 写到用户指定的输出路径。

7. 打印一条简短总结：输出路径、词数、页数，以及使用提示：**"在浏览器打开 → Ctrl/Cmd+P → 选 A4 → 打印"**。

## Hershey Futural 字母半宽表

累加 x 偏移依赖这张字母半宽表：

| a:10 | b:9 | c:9 | d:10 | e:9 | f:7 | g:10 | h:10 | i:4 | j:5 | k:8 | l:4 |
| m:15 | n:10 | o:10 | p:9 | q:10 | r:6 | s:9 | t:7 | u:10 | v:8 | w:11 | x:9 | y:8 | z:9 |

公式：`x[0] = 0，x[n] = sum(2 * o[i] for i in 0..n-1)`。

## 规则

- **绝不瞎编音标或释义。** 词库里没有、用户也没给的词，停下来问。错误的 IPA 或中文会主动误导一个刚学字母的小朋友——比多问一句问题糟糕得多。
- **仅支持小写。** Hershey defs 只覆盖 a–z。大写输入静默转小写；如果用户明确要大写，解释当前字体只能渲染小写，然后按小写继续。
- **输出完全离线自包含。** 所有资源必须内联（SVG + emoji + 系统字体）。不用 Google Fonts、不用外部 CSS、不用网络资源。原因：练习卡经常要在没网的设备上打印，外部字体拉不下来就毁了整张纸。
- **保留四线格坐标**（viewBox `0 0 1000 120` 中 y = 0 / 40 / 80 / 120）。这四条线定义了四线三格的书写区，挪动就把教学用意毁了。
- **Hershey 单笔画渲染。** 所有字母通过 `<use href="#l-X">` 引用 `template.html` 里的 defs，实线蓝色描边（实线非虚线）。只描边、不填充。
- **单词长度 ≤ 约 20 字符。** 累加字宽必须装进 viewBox `1000`。超过的词，字母会挤出右边界——提醒用户并建议拆分。
- **清洗描红词。** 去掉标点、拒绝非 ASCII 字母作为描红词本体。释义字段里出现 emoji 和中文没问题，只是被描红的单词不能有。
- **严格 A4 页面尺寸。** 每一个 `<section class="page">` 打印时必须正好占满一张 A4。`assets/template.html` 里的 CSS 负责保证这点，不要改弱：
  - `@page { size: A4; margin: 0 }`——打印机边距为 0；页内留白在 `.page` 内部处理。
  - `.page { width: 210mm; height: 297mm; padding: 10mm 12mm; overflow: hidden; page-break-after: always; page-break-inside: avoid; display: flex; flex-direction: column }`——固定 A4 盒，flex 列让页眉/卡片区/页脚纵向分布。
  - `.cards-area { flex: 1 1 auto; display: flex; flex-direction: column; justify-content: space-between; gap: 4mm; min-height: 0 }` 加 `.card { flex: 1 1 0; min-height: 0 }` 和 `.row { flex: 1 1 0; min-height: 0 }`——4 张卡片均分剩余纵向空间，永远不溢出。
  - `@media print { html, body { width: 210mm; margin: 0; padding: 0; background: #fff } }` + body 上的 `-webkit-print-color-adjust: exact`——颜色能印出来，body margin 也不会再给每页后面塞一个空白尾页。
  - **历史坑**：早期版本用过 `min-height: 297mm` + `@page margin: 12mm 14mm`，padding 被算了两遍，每张练习卡后都跟一张空白纸。**不要**再在 `.page` 上用 `min-height`，必须用固定 `height` 让浏览器没法把盒撑大。
  - 给用户的打印提示："浏览器打开 → Ctrl/Cmd+P → 选 A4 → 勾选'背景图形'保留四线格颜色"。

## 验证

写完文件后，一定跑以下检查，并把计数结果报告给用户。这能以最低成本抓住常见的退化（空文件、卡数错、页数错）：

1. 读回前 30 行——确认文件不是空的，页眉里有主题名。
2. 数 `<div class="card">` 出现次数——应等于词数。
3. 数 `<section class="page">`——应等于 `ceil(词数 / 4)`。
4. 对输出 grep `height: 297mm`、`@page`、`overflow: hidden`——确认严格 A4 CSS 经过模板替换后仍在位。任何一项缺失，文件都会打出空白尾页或溢出。

**不要**自动在浏览器里打开文件。用户可能在无头系统上，起一个 GUI 程序要么响亮失败、要么静悄悄生出僵尸进程。

## 测试

本 skill 的测试 prompt 在 `evals/evals.json` 里。改 skill 的时候重新跑一遍，确认输出仍然通过上面的验证清单。
