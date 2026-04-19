#!/usr/bin/env bash
# 重新打包一个 skill 为 dist/<name>.skill
# 用法：scripts/package_skill.sh <skill-name>
# 作用：把 .claude/skills/<name>/ 下除 evals/ 外的所有内容打成 zip，
#       产物写到 dist/<name>.skill（按官方 .skill 文件格式：根下一个同名目录）。

set -euo pipefail

SKILL_NAME="${1:?用法: scripts/package_skill.sh <skill-name>}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$REPO_ROOT/.claude/skills/$SKILL_NAME"
OUT="$REPO_ROOT/dist/$SKILL_NAME.skill"

[[ -d "$SRC" ]] || { echo "ERROR: 源目录不存在: $SRC" >&2; exit 1; }

mkdir -p "$REPO_ROOT/dist"
rm -f "$OUT"

(cd "$REPO_ROOT/.claude/skills" && zip -qr "$OUT" "$SKILL_NAME" \
  -x "$SKILL_NAME/evals/*" "$SKILL_NAME/evals")

SIZE=$(du -h "$OUT" | cut -f1)
FILES=$(unzip -l "$OUT" | tail -1 | awk '{print $2}')
echo "打包完成: dist/$SKILL_NAME.skill ($SIZE, $FILES 文件, evals/ 已排除)"
