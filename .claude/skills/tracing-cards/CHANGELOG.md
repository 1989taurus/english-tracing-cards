# 更新日志

`tracing-cards` skill 的所有重要变更都会记录在这里。

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.2.0] — 2026-04-19

### 新增

- **首份参考改为纯黑 `#000000`。** 原先首份描红参考是深蓝 `#5a9ed0`，对幼儿园孩子的视觉对比不够强。改成纯黑——接近真墨水、打印最稳、描红对照最清晰。浅蓝 `#b8d9ee` 副本保持不变，仍是孩子沿笔画描红的主体。`references/example.html` 同步重生成。
- **PDF 生成成功后自动送默认打印机**（Linux/macOS，CUPS `lp`）。`html_to_pdf.py` 在 PDF 落盘后探测 `lp`、查 `lpstat -d` 找默认打印机（或 `lpstat -p` 取第一台 idle 打印机），然后 `lp -d <name> <pdf>`。打印请求提交后 stderr 报 job id；超时/返回码非 0 / 无 `lp` / 无打印机——全部软降级，只发通知不抛异常。
- 新增 CLI 标志 `--no-print` 和环境变量 `TRACING_CARDS_AUTO_PRINT=0` 用于禁用自动打印；`TRACING_CARDS_PRINTER=<name>` 用于指定非默认打印机。

### 修复

- **lpstat 本地化输出解析兼容 `LC_ALL=C`。** 在中文 locale 下 `lpstat -p` 会输出"打印机 XXX 目前空闲"而不是 "printer XXX is idle"，导致打印机检测失败。`get_default_printer()` 和 `list_available_printers()` 现在显式传 `env={**os.environ, "LC_ALL": "C", "LANG": "C"}` 给 subprocess，强制英文输出。影响：中文 Linux Mint / Ubuntu 上自动打印路径在本版本前静默失败。

### 变更

- SKILL.md 规则 "描红行铺满" 首份颜色描述：深蓝 → 纯黑。
- SKILL.md 生成步骤 3 `X0` 注释：深色 → 纯黑。
- SKILL.md 步骤 7 标题 "生成 PDF" → "生成 PDF + 自动打印"，新增打印行为、软降级条件、禁用/指定打印机的方法。
- SKILL.md 验证步骤 5 新增 `grep stroke="#000000"` 校验（每卡至少 2 次）。
- CLAUDE.md 生成流水线 step 3 首份颜色同步为 `#000000` 纯黑。

## [1.1.1] — 2026-04-19

### 修复

- **v1.1.0 严重缺陷**：SKILL.md 声称会调用 `scripts/html_to_pdf.py` 生成 PDF，但该脚本实际在仓库根部 `scripts/` 而非 skill 目录下，`.skill` 包里没带它。按 README 第一条 `unzip dist/tracing-cards.skill -d ~/.claude/skills/` 装完后，skill 调用 PDF 脚本会找不到文件，PDF 功能完全不可用，HTML 仍可生成。**建议已装 v1.1.0 的用户立刻升到 v1.1.1。**
- 修复：把 `html_to_pdf.py` 从仓库根 `scripts/` 挪到 skill 自带的 `.claude/skills/tracing-cards/scripts/html_to_pdf.py`，随 `.skill` 分发。
- SKILL.md step 7 措辞："仓库脚本" → "skill 自带脚本 `<skill 根>/scripts/html_to_pdf.py`"，明确路径契约。
- `scripts/package_skill.sh`：打包排除规则新增 `__pycache__/` 和 `*.pyc`，避免把本地开发缓存打进分发包。

## [1.1.0] — 2026-04-19 — ⚠️ 已弃用

**此版本不要使用**。声称支持 PDF 生成，但 `html_to_pdf.py` 未随 `.skill` 打包分发，PDF 功能无法使用。用 v1.1.1。

### 新增

- **每行铺满副本。** ROW_TRACE 现在由首份深蓝 `#5a9ed0` 参考样例 + 若干浅蓝 `#b8d9ee` 副本组成，按 `N = floor((980 − word_width_svg) / (word_width_svg + 40))` 自动铺满整行。教学意图：深色是"长什么样"的参考，浅色才是给孩子描的本体。长词（`word_width_svg > 940`）自动回退为 N=0，只留首份。
- **HTML → A4 PDF 自动生成。** skill 在写完 HTML 后自动调用仓库根的 `scripts/html_to_pdf.py`，产出同名 `.pdf`。脚本内置双后端（系统 Chrome ≥ 109 优先，Playwright 降级），独立 `--user-data-dir`、`--no-pdf-header-footer`、`--virtual-time-budget=5000`、产物尺寸校验。两个后端都缺时软降级，不中止 skill —— HTML 仍是完整可用产物。
- Linux 彩色 emoji 字体探测（`fc-list`）：缺失时 stderr 发 WARNING 并透传到总结，PDF 仍会出但 emoji 退化为黑白轮廓。
- `references/example.html` 按新算法重新生成，cat/dog/pig/duck 每行 4–5 份副本。
- 验证新增两项：描红行 `<g transform="translate(` 计数 = `2 × (1 + N)` per card；PDF > 10 KB 且 `pdfinfo` 报 A4 页大小。

### 变更

- SKILL.md 生成步骤 3 从"发射单组 SVG"改为"按公式计算 N，发射 1+N 组"。
- 规则清单新增"描红行铺满"条目，解释为什么第二份起是浅色。

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
