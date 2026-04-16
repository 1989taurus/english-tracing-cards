# tracing-cards

一个 Claude Code skill，用来生成可打印 A4 英语单词描红卡，面向幼儿园年龄段（3–6 岁）的小朋友。

**版本：** 1.0.0 · **许可证：** MIT · **输出完全离线**

> 本 skill 由 **Claude Opus 4.7** 在 Claude Code 中协作完成：规范起草、Hershey 字体布局、严格 A4 CSS、官方 `.skill` 格式打包。

## 你能拿到什么

- 自包含的 HTML 文件（无联网、无构建），可直接 A4 打印。
- 每张卡片：emoji + 单词 + IPA 音标 + 中文释义。
- 每张卡片 4 行，印在 四线三格 格子上：
  - 2 行 Hershey Futural 单笔画字母描红（实线，非虚线）
  - 2 行空白练习
- 每页 4 张卡片，严格 `height: 297mm`，正好打印 1 张 A4 纸。
- 内置约 50 个幼儿园常用词（动物、水果、颜色、数字、家庭等）。

## 安装

把整个 `tracing-cards/` 目录放到以下任意一个位置：

- 项目级：`<你的项目>/.claude/skills/tracing-cards/`
- 用户级：`~/.claude/skills/tracing-cards/`

最终目录结构：

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

无需 npm / pip，无需构建。Claude Code 下次启动会自动识别。

## 使用

打开 Claude Code，对它说以下任意一句：

- `给孩子做一份英文描红卡，单词：cat dog pig …`
- `帮我生成英语字帖，主题"小动物"，单词 cat dog cow`
- `Make a tracing worksheet for apple, book, pen`

Claude 会问你：**单词列表 / 主题名称 / 是否自动补全音标释义 / 输出路径**，然后把 `tracing-cards-<主题>.html` 写到你指定的目录。浏览器打开 → `Ctrl/Cmd+P` → 选 A4 → 勾选 **"背景图形 / Background graphics"** 让四线格颜色印出来 → 打印完成。

## 运行要求

- Claude Code（任意近期版本）。
- 能打印到 A4 的浏览器（Chrome / Edge / Safari / Firefox 都可以）。
- 打开或打印生成的 HTML 不需要联网。

## 约束

- 仅支持小写 a–z。大写输入会静默转小写（Hershey defs 不包含 A–Z）。
- 单词最多约 20 字符（字宽累加必须装进 1000 单位的 viewBox）。
- 如果单词不在内置词库里，skill 会**停下来问你** emoji / 音标 / 释义，而不是瞎编——错误的 IPA 会误导学龄前小朋友。

## 测试

回归用例放在 `evals/evals.json`，4 个测试覆盖：基本主题生成、难字母组合、未知单词处理、大写输入归一化。

## 更新日志

见 [CHANGELOG.md](CHANGELOG.md)。
