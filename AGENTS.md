# AGENTS.md

## 这个仓库是什么

一个单一用途的 HTML 生成器，用来产出可打印的英语描红卡。没有构建系统、没有包管理器、没有测试。

## 关键区分

- **根目录的 `*.html` 是生成产物，不是源码。** 不要手动改，要改请通过 skill 重新生成。
- **没有 `npm`/`pip`/`cargo` 之类。** 这不是一个软件项目。

## 工作流

当用户提到 英语描红 / 描红卡 / 描红 / 英文练字帖 / tracing worksheet / handwriting practice / kindergarten English，加载 tracing-cards skill，先跑访谈流程再开始生成。

## 生成描红卡

1. 跑访谈（通过 skill 的 `AskUserQuestion` 流程）——单词列表、主题名称、是否自动补全、输出路径。不要跳过。
2. 把片段替换到 `assets/template.html` 里生成 HTML。Hershey 版本需要按半宽表算每个字母的 x 偏移。
3. 验证：`<div class="card">` 数量 == 单词数，`<section class="page">` 数量 == ceil(单词数/4)。

## 不变式

- 描红词仅支持小写，最多约 20 字符（Hershey 字宽累加必须装进 viewBox 1000）
- 完全离线：内嵌 SVG + Hershey path + emoji，不引用任何外部资源
- SVG 网格：viewBox `0 0 1000 120`，线在 y=0, 40, 80, 120
- Hershey 渲染：`<use href="#l-X">` 加 `translate(20,17.143) scale(2.857143)` transform

## Skill

`.claude/skills/tracing-cards/` — Hershey Futural 单笔画 SVG path，本仓库唯一的 skill。

## 参考

完整规范和词库：`.claude/skills/tracing-cards/SKILL.md`
