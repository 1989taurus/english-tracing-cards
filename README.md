# english-tracing-cards

一个 Claude Code skill，用来生成**可打印 A4 英语单词描红练习卡**，面向幼儿园年龄段（3–6 岁）的小朋友。

每张作业都是一个自包含、完全离线的 HTML 文件，特性如下：

- 每页 4 张卡片，严格 `height: 297mm`，正好打印到一张 A4 纸
- 每张卡片：emoji + 单词 + 音标 + 中文释义
- 2 行描红，**每行首份深蓝参考 + 若干浅蓝副本铺满整行**（小朋友按浅色笔画描红）
- 2 行空白练习，印在 四线三格 格子上
- Hershey Futural 单笔画 SVG 字母，实线描红、非虚线
- 内置约 50 个幼儿园常用词（动物、水果、颜色、数字、家庭等）
- **同时生成 HTML 和 A4 PDF**（基于系统 Chrome 或 Playwright 任一）

![layout](https://img.shields.io/badge/layout-A4%20297mm-blue) ![skill](https://img.shields.io/badge/claude--code-skill-7c3aed) ![license](https://img.shields.io/badge/license-MIT-green)

> 本仓库由 **Claude Opus 4.7** 在 Claude Code 中协作完成，包括 skill 规范设计、Hershey 字体布局、严格 A4 CSS、官方 `.skill` 格式打包、以及本文档本身。

## 效果预览

执行 skill 后，浏览器打开生成的 HTML → `Ctrl/Cmd+P` → 选 A4 → 勾选 **"背景图形 / Background graphics"** 让四线格颜色能打出来 → 打印即可。

样例版式见 [`.claude/skills/tracing-cards/references/example.html`](.claude/skills/tracing-cards/references/example.html)（4 卡参考页）。

## 安装 skill

### 方式一 · 直接解压打包好的 `.skill`

```bash
unzip dist/tracing-cards.skill -d ~/.claude/skills/
```

### 方式二 · 直接拷贝源目录

```bash
cp -r .claude/skills/tracing-cards ~/.claude/skills/
```

或者放到项目级目录：`<你的项目>/.claude/skills/tracing-cards/`。

无需 npm / pip，无需构建。Claude Code 下次启动会自动识别。

## 怎么用

打开 Claude Code，对它说任意一种触发语：

- `给孩子做一份英文描红卡，单词：cat dog pig …`
- `帮我生成英语字帖，主题"小动物"，单词 cat dog cow`
- `Make a tracing worksheet for apple, book, pen`

Claude 会简短地问你四件事：**单词列表 / 主题名称 / 是否自动补全音标和释义 / 输出路径**，然后把 `tracing-cards-<主题>.html` 和同名 `.pdf` 写到你选的目录。

完整规范 + 全部触发关键词见 [`.claude/skills/tracing-cards/SKILL.md`](.claude/skills/tracing-cards/SKILL.md)。

## 生成 PDF

HTML 生成后，skill 会自动调用 [`scripts/html_to_pdf.py`](scripts/html_to_pdf.py) 产出同名 A4 PDF。也可以独立调用：

```bash
python3 scripts/html_to_pdf.py tracing-cards-animals.html
# → 在同目录写出 tracing-cards-animals.pdf
```

**后端**（按优先级自动探测）：

1. 系统 Chrome / Chromium ≥ 109（推荐，零依赖）
2. Playwright（`pip install playwright && python -m playwright install chromium`，免 sudo，适合沙箱环境）

**前置**：Python 3.8+。Linux 用户如需彩色 emoji，额外安装 `fonts-noto-color-emoji`（否则 emoji 退化为黑白轮廓，PDF 仍可用）。

详细用法见 [`scripts/README.md`](scripts/README.md)。

## 仓库目录

```
.
├── .claude/
│   └── skills/
│       ├── tracing-cards/            # 当前主推方案 — Hershey 单笔画 SVG
│       │   ├── SKILL.md              # 权威规范（访谈流程、词库、规则）
│       │   ├── README.md             # skill 内部说明
│       │   ├── CHANGELOG.md
│       │   ├── LICENSE               # MIT
│       │   ├── assets/
│       │   │   ├── template.html     # A4 外壳 + Hershey a–z <defs>
│       │   │   └── snippets.html     # 页 / 卡 / 行 片段
│       │   ├── references/
│       │   │   └── example.html      # 4 卡参考输出
│       │   └── evals/
│       │       └── evals.json        # 回归测试用例
│       └── tracing-cards-oc/         # 旧方案 — Comic Sans 虚线轮廓
├── dist/
│   └── tracing-cards.skill           # 官方格式打包产物（解压到 ~/.claude/skills/）
├── scripts/
│   ├── html_to_pdf.py                # HTML → A4 PDF 转换器（双后端）
│   └── README.md                     # 脚本用法 / 环境变量 / 退出码
├── AGENTS.md                         # 本仓库内 Claude Code agent 的工作流
├── CLAUDE.md                         # 每次会话自动载入的项目指令
└── README.md                         # 就是你正在看的这份
```

## 两套 skill 的差异

| Skill | 渲染方式 | 状态 |
|---|---|---|
| [`tracing-cards/`](.claude/skills/tracing-cards/) | Hershey Futural 单笔画 SVG path | **主推 / 推荐** |
| [`tracing-cards-oc/`](.claude/skills/tracing-cards-oc/) | Comic Sans `<text>` + `stroke-dasharray` | 旧方案 / 兜底 |

Hershey 版线条干净、单笔画，最适合描红；OC 版实现更简单但依赖系统字体，打印效果不稳定。

## 硬性约束（不要随便改）

- **仅支持小写 a–z** — Hershey defs 不覆盖 A–Z，大写输入会静默转小写。
- **单词长度 ≤ 约 20 字符** — 字宽累加必须装进 SVG viewBox `0 0 1000 120`。
- **完全离线** — 没有 Google Fonts、没有外链 CSS/JS/图片，生成的 HTML 在断网环境也能打开和打印。
- **严格 A4** — `@page { size: A4; margin: 0 }` + `.page { height: 297mm; overflow: hidden }` 配合 flex 布局。每个 page 严格 1 张 A4，不会出空白尾页。
- **绝不瞎编音标或释义** — 词库里没有的词，skill 会停下来问用户，而不是猜。错误的 IPA 会误导学龄前的小朋友。

## 打包

`.skill` 文件由 Anthropic 官方 `skill-creator` 工具生成：

```bash
# 前提：本地装有 claude-plugins-official 插件
python3 -m scripts.package_skill \
  /home/<用户>/Projects/english/.claude/skills/tracing-cards \
  /home/<用户>/Projects/english/dist
```

`evals/` 目录会被官方脚本自动剔除（它是开发期的回归资产，只保留在源仓库，不随分发包发布）。

## 贡献方式

个人小项目，如果你想扩展：

- **加词库** — 编辑 `.claude/skills/tracing-cards/SKILL.md` 里的词表（emoji + IPA + 中文 三列）。
- **改版式** — 调 `assets/template.html` 的 CSS；改完要跑一遍 `evals/evals.json` 确认没退化。
- **加测试** — 在 `evals/evals.json` 里加一条：`id` / `name` / `prompt` / `expected_output` / `assertions[]`。

## 许可证

MIT — 详见 [`.claude/skills/tracing-cards/LICENSE`](.claude/skills/tracing-cards/LICENSE)。
