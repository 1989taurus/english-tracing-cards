#!/usr/bin/env python3
"""Stop hook: 阻止会话结束，如果任何 skill 源文件比 dist/*.skill 产物新。

设计：
  - 遍历 dist/*.skill，按文件名反查 .claude/skills/<name>/ 源目录
  - evals/ 不计入（打包时按约定排除）
  - 任一源文件 mtime 比 .skill 晚 → 输出 JSON decision=block 反馈给 Claude
  - 全部 fresh → 静默 exit 0

Claude Code 的 Stop hook 约定：
  - stdout 一个 JSON 对象 {"decision":"block","reason":"..."} 会阻止会话结束
    并把 reason 文本反馈给主 agent，让它有机会补动作
  - exit 0 + 无输出 = 放行

不依赖任何第三方包，只用 Python 3.8+ stdlib。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

EXCLUDED_TOP_LEVEL_DIRS = {"evals"}  # 打包时排除，比较时也应排除


def collect_stale_files(src_dir: Path, skill_mtime: float) -> list[str]:
    """返回源目录里 mtime 晚于 skill 包的文件相对路径（已排除 evals/）。"""
    stale = []
    for path in src_dir.rglob("*"):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(src_dir).parts
        if rel_parts and rel_parts[0] in EXCLUDED_TOP_LEVEL_DIRS:
            continue
        # 1 秒容差，避免同一打包动作里的 mtime 抖动
        if path.stat().st_mtime > skill_mtime + 1:
            stale.append("/".join(rel_parts))
    return sorted(stale)


def main() -> int:
    repo = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path.cwd())
    dist = repo / "dist"
    skills_root = repo / ".claude" / "skills"

    if not dist.is_dir() or not skills_root.is_dir():
        return 0

    stale_by_skill: dict[str, list[str]] = {}
    for pkg in sorted(dist.glob("*.skill")):
        name = pkg.stem
        src = skills_root / name
        if not src.is_dir():
            continue
        newer = collect_stale_files(src, pkg.stat().st_mtime)
        if newer:
            stale_by_skill[name] = newer

    if not stale_by_skill:
        return 0

    lines = ["以下 skill 源文件比 dist/ 产物新，发布前请重打包：", ""]
    for name, files in stale_by_skill.items():
        lines.append(f"• {name}  ({len(files)} 个文件变更)")
        for f in files[:5]:
            lines.append(f"    - {f}")
        if len(files) > 5:
            lines.append(f"    … 还有 {len(files) - 5} 个")
        lines.append(f"  重打: scripts/package_skill.sh {name}")
        lines.append("")
    lines.append(
        "修复后再结束会话。确定不需要重打时，可 `touch dist/<name>.skill` "
        "更新 mtime 绕过。"
    )

    print(json.dumps(
        {"decision": "block", "reason": "\n".join(lines)},
        ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
