# scripts/

仓库级辅助脚本。只包含 skill 打包和新鲜度检查，**不包含 skill 的 runtime 依赖**。

> **注意**：HTML → PDF 转换脚本 `html_to_pdf.py` 已迁移到 skill 内部（`.claude/skills/tracing-cards/scripts/html_to_pdf.py`），随 `.skill` 分发。它是 skill 的 runtime 依赖，不属于仓库级脚本。

## package_skill.sh

重新打包 `.claude/skills/<name>/` 为 `dist/<name>.skill`。

### 用法

```bash
scripts/package_skill.sh tracing-cards
```

就是一层 `zip -qr` + `-x 'evals/*' '**/__pycache__/*' '**/*.pyc'`，不依赖任何外部工具（官方 skill-creator 或 claude-plugins-official 都不是必需）。

`evals/` 按约定排除——它是开发期的回归资产，不随分发包发布。`__pycache__/` 和 `*.pyc` 也排除，避免把本地开发缓存打进分发包。

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
