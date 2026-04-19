# CLAUDE.md

这份文件用来指导 Claude Code（claude.ai/code）在本仓库里该怎么干活。

## 仓库用途

这个仓库用来生成**可打印的 A4 英语单词描红练习卡**，面向 3–6 岁幼儿园年龄段的小朋友。没有构建系统、没有包管理器、没有测试。唯一的产物是一份自包含的 HTML 文件，用浏览器打开后打到 A4 纸上。

## 架构

`.claude/skills/tracing-cards/` 是本仓库唯一的 skill，遵循 `/skill-creator` 的标准布局——`SKILL.md`（权威规范：访谈流程、词库、生成步骤）加上 `assets/`（`template.html` HTML 外壳含 `{{PAGES}}` 占位符，`snippets.html` 可复用片段）、`references/`（`example.html` 参考输出）、`scripts/html_to_pdf.py`（HTML → A4 PDF，随 `.skill` 分发）、`evals/`（skill 迭代用的测试 prompt，不打包进 `.skill`）。

### 渲染方式

用 **Hershey Futural 单笔画字体**，以 SVG `<path>` 嵌在全局 `<defs>` 里，通过 `<use href="#l-X">` 引用，x 偏移量按每个字母的半宽累加得出。线条干净、单笔画，最适合描红。

### 片段结构

`PAGE_WRAPPER` → `CARD`（每页 ×4）→ 2 × `ROW_TRACE` + 2 × `ROW_BLANK`。

### 生成产物

根目录的 `tracing-cards-*.html` 是**生成产物，不是源码**。命名约定：`tracing-cards-<主题 slug>.html`。以 `*-test.html` 结尾的是调试用迭代文件。要改内容请重新跑 skill，不要手动改。

## 生成流水线

1. **访谈用户** — 用 `AskUserQuestion` 问四件事：单词列表、主题名称、是否自动补全、输出路径。不要跳过。
2. 对每个单词：从词库或用户输入里取 emoji/音标/释义（词库没有就问用户，绝不瞎猜），单词转小写，填到 CARD 片段里。
3. 对 `tracing-cards/`（Hershey）：按 SKILL.md 里的半宽表算出每个字母的 x 偏移，用 `<use>` 元素加缩放 `<g>` transform 组装 SVG。每行描红按公式 `N = floor((1210 − word_width_svg) / (word_width_svg + 60))` 生成 1 份纯黑 `#000000` 参考 + N 份浅蓝 `#b8d9ee` 副本，再用动态 `gap = (1210 − (1+N)·W) / N` 把剩余空间均分到 N 个间隔，`Xk = 20 + k · (W + gap)`——**v1.4.0 起始终铺满行**（justify 风格，gap ≥ GAP_MIN = 60）。**v1.3.0 架构**：ROW_TRACE 拆为双 SVG —— 网格层 `preserveAspectRatio="none"` viewBox `0 0 1000 120` 铺满容器宽度；字母层 viewBox `0 0 1250 120` `preserveAspectRatio="xMinYMid meet"` 保持字母原比例。`<g>` transform 只发射到字母层的 `{{LETTER_GROUPS}}` 占位符。
4. 每 4 张卡片组成一个 PAGE_WRAPPER（`{{THEME}}` 填用户指定的主题名），塞进 `assets/template.html` 的 `{{PAGES}}` 位置。
5. **验证**：读回前 30 行、数 `<div class="card">` 等于单词数、数 `<section class="page">` 等于 ceil(单词数/4)、把计数报告给用户。
6. **生成 PDF**（默认开启）：调用 skill 自带 `<skill 根>/scripts/html_to_pdf.py <html 路径>`，在 HTML 同目录产 `.pdf`。双后端（系统 Chrome ≥ 109 优先，Playwright 降级），都没有时软降级并 stderr 报警——**HTML 仍是完整可用产物**。

## 硬性约束（无必要不要动）

**SVG 网格**（双 SVG 架构，v1.3.0+）：
- 网格层 viewBox `0 0 1000 120`，四线三格的线在 **y=0, 40, 80, 120**，`preserveAspectRatio="none"` 铺满容器全宽，`vector-effect="non-scaling-stroke"` 防止线宽被拉伸。
- 字母层 viewBox `0 0 1250 120`，`preserveAspectRatio="xMinYMid meet"` 保持字母比例。
- 两个 SVG 通过 `.row { position: relative }` 容器加 `position: absolute; inset: 0` 叠放，字母层 DOM 顺序在后，覆盖网格。

**Hershey 渲染**（只针对 `tracing-cards/`）：
- a–z 的 `<path>` defs 在 `assets/template.html` 里，靠 `<use href="#l-X">` 引用。
- Transform：`translate(Xk, 17.143) scale(2.857143)`——scale = 40/14，TY = 80 − 2.857×22；`X0=20`（首份纯黑），`Xk = 20 + k * (word_width_svg + gap)`（k ≥ 1 浅蓝副本），`gap = (1210 − (1+N)·W) / N` 动态均分（N=0 时只发射首份）。
- 描边：首份 `stroke="#000000"`、浅蓝副本 `stroke="#b8d9ee"`；其余 `fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"` 共用。
- 单词长度上限约 20 字符（累加字宽必须装进字母层 viewBox 1250）。

**通用**：
- **仅支持小写** — Hershey defs 不覆盖 A–Z。大写输入静默转小写。
- **完全离线**：SVG + emoji + 系统字体，全部内嵌。没有 Google Fonts、没有外链 CSS、没有网络资源。
- 描红词要清洗标点、拒绝非 ASCII（中文/emoji 在 meaning/emoji 字段里没问题）。
- **不要**自动在浏览器里打开文件——用户可能在无头环境下工作。

## 触发

命中以下任意一条就启动 skill：英语描红 / 描红卡 / 英文练字帖 / 单词描红 / tracing worksheet / handwriting practice / kindergarten English。启动后一定要先跑访谈流程，再开始生成。
