# scripts/

本目录存放 skill 生成流水线使用的辅助脚本。

## html_to_pdf.py

把描红 HTML 转成 A4 PDF。被 `tracing-cards` skill 在生成步骤末尾自动调用，也可以独立使用。

### 用法

```bash
python3 scripts/html_to_pdf.py <input.html> [-o <output.pdf>] [--browser <path>]
```

- 不指定 `-o` 时输出路径为把 `.html` 替换为 `.pdf`
- `--browser` 或环境变量 `TRACING_CARDS_BROWSER` 可强制指定 Chrome 二进制

### 双后端策略

1. **系统 Chrome / Chromium ≥ 109**（优先）—— `--headless=new --print-to-pdf`，零依赖
2. **Playwright**（降级）—— 要求 `pip install playwright && python -m playwright install chromium`，安装到用户目录无需 sudo
3. 两者都不可用 → 退出码 1，stderr 打印平台相关安装指令

### 环境变量

| 变量 | 作用 |
|---|---|
| `TRACING_CARDS_BROWSER` | 指定 Chrome 二进制绝对路径，绕过自动探测 |

### 退出码

| 码 | 含义 |
|---|---|
| 0 | 成功 |
| 1 | 没有可用后端（看 stderr 安装指令） |
| 2 | 后端启动但产物无效（尺寸 < 1 KB 或缺失） |
| 3 | 参数或输入错误（文件不存在、不是 .html） |

### Linux 彩色 emoji 字体

Chromium 在 Linux 上不自带彩色 emoji，依赖系统字体。脚本启动时 `fc-list` 探测：
- 检测不到彩色 emoji 字体 → stderr 打印 `WARNING`，**继续生成 PDF**（emoji 退化为黑白轮廓）
- 修复：`sudo apt install fonts-noto-color-emoji`（Debian/Ubuntu）或 `sudo dnf install google-noto-emoji-color-fonts`（Fedora）

macOS 和 Windows 默认有彩色 emoji 字体，不触发警告。

### 质量保证

- **独立 `--user-data-dir`**：每次转换用临时目录启动 Chrome，避免和用户正开着的 Chrome 抢占导致静默失败
- **产物校验**：转换后断言文件存在且 > 1 KB，不合格直接 exit 2
- **`--no-pdf-header-footer`**：去掉 Chrome 默认的 URL/日期页眉页脚，保留 HTML 自己的 `@page margin: 0`
- **`--virtual-time-budget=5000`**：等 5 秒让布局彻底定型后再快照
- **`print_background: true`**（Playwright）/ `-webkit-print-color-adjust: exact` 本身在 HTML 中 —— 四线三格的颜色不会被当成背景色剥掉

### 系统要求

- Python 3.8+（仅用 stdlib）
- Chrome ≥ 109 或 Playwright 任一
- 可选：`poppler-utils`（提供 `pdfinfo`，让 skill 验证页数）

### 手动冒烟测试

```bash
# 转换仓库里已有的样张，人工确认视觉
python3 scripts/html_to_pdf.py tracing-cards-animals.html

# 用 pdfinfo 核对页数 = ceil(词数/4)
pdfinfo tracing-cards-animals.pdf | grep Pages
```

## package_skill.sh

重新打包 `.claude/skills/<name>/` 为 `dist/<name>.skill`。

### 用法

```bash
scripts/package_skill.sh tracing-cards
```

就是一层 `zip -qr` + `-x 'evals/*'`，不依赖任何外部工具（官方 skill-creator 或 claude-plugins-official 都不是必需）。

`evals/` 按约定排除——它是开发期的回归资产，不随分发包发布。

## check_skill_freshness.py

Stop hook：检测任一 `.claude/skills/<name>/` 源文件是否比 `dist/<name>.skill` 更新。

### 行为

- 遍历 `dist/*.skill`，反查对应源目录
- `evals/` 不计入比较（它本就不在包里）
- 任一源文件 mtime 晚于 `.skill`（1 秒容差）→ stdout 输出 `{"decision":"block","reason":"..."}`，Claude Code 把 reason 反馈给 agent、阻止会话结束
- 全部 fresh → 静默 exit 0

### 注册位置

`.claude/settings.json` 的 `hooks.Stop`。会话结束时自动触发，人工跑也行：

```bash
python3 scripts/check_skill_freshness.py
echo "exit=$?"
```

### 绕过

确实不需要重打时（例如只改了非分发内容），`touch dist/<name>.skill` 刷新 mtime。
