# 更新日志

`tracing-cards` skill 的所有重要变更都会记录在这里。

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] — 2026-04-17

首个可分发的正式版本。

### 新增

- `SKILL.md` — 权威规范，符合 `/skill-creator` 布局（frontmatter 含触发关键词、访谈流程、约 50 词的幼儿园词库、生成步骤、Hershey 半宽表、带原因说明的规则清单、验证清单）。
- `assets/template.html` — HTML 外壳，内嵌 Hershey Futural a–z 的 `<path>` defs，以及严格 A4 CSS。
- `assets/snippets.html` — 可复用的 `PAGE_WRAPPER` / `CARD` / `ROW_TRACE` / `ROW_BLANK` 片段。
- `references/example.html` — 4 卡参考输出，用于视觉比对。
- `evals/evals.json` — 4 个回归测试用例：`basic-animals-theme`、`hard-letter-coverage`、`unknown-word-asks-user`、`uppercase-auto-lowercase`。
- 严格 A4 打印尺寸：`@page { size: A4; margin: 0 }` + `.page { height: 297mm; overflow: hidden; page-break-inside: avoid }` 配合 flex 列式布局，保证每页 4 张卡片纵向均分，不溢出也不产生空白尾页。
- `-webkit-print-color-adjust: exact`，让四线格颜色在浏览器打印时不会被吞掉。
- 验证步骤 4：对生成文件 grep `height: 297mm`、`@page`、`overflow: hidden`，避免改模板时 CSS 被意外削弱。

### 设计决策

- **只支持小写描红** — Hershey defs 仅覆盖 `a-z`；大写输入会被静默转小写。
- **绝不瞎编音标或释义** — 词库里没有的词，skill 会停下来问用户，而不是猜。错误的 IPA 或中文对学龄前小朋友是主动误导。
- **完全离线** — SVG + emoji + 系统字体，全部内嵌，没有 Google Fonts、没有外链 CSS/JS，在没有网络的设备上也能正确打印。

### 已知限制

- 单词最多约 20 字符（累加字宽必须装进 viewBox 1000）。
- 每页固定 4 张卡片（按单张 A4 上合理的描红行高调过，不建议改）。
- 内置词库限于幼儿园范围（约 50 词）；超出这个范围的词需要用户自己提供音标和释义。
