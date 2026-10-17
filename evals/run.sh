#!/usr/bin/env bash
# 本地/CI 通用：逐条运行 evals/*.eval.json。
# 依赖：git、python3、claude（npm i -g @anthropic-ai/claude-code）
set -uo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" || exit 2
EVALS_COPY="$(mktemp -d)"
cp -r evals "$EVALS_COPY/evals"
failed=0
total=0

for eval in "$EVALS_COPY"/evals/*.eval.json; do
  [ -e "$eval" ] || { echo "没有找到 *.eval.json"; exit 0; }
  total=$((total + 1))
  name=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["name"])' "$eval")
  from=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["from"])' "$eval")
  prompt=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["prompt"])' "$eval")

  work="$(mktemp -d)"; rm -rf "$work"
  result="$(mktemp)"; rm -f "$result"
  git worktree add -q --detach "$work" "$from" || { echo "SKIP $name: 找不到 $from"; failed=$((failed+1)); continue; }
  rm -rf "$work/evals" "$work/.claude"
  cp -r CLAUDE.md .claude "$work/" 2>/dev/null || true
  git -C "$work" add -A && git -C "$work" commit -q --allow-empty -m "configuration under test"

  ( cd "$work" && claude -p "$prompt" \
      --allowedTools "Read,Edit,Bash(make test),Bash(make lint)" \
      --output-format json > "$result" )
  # 检查必须在「那次运行的工作树」里做，结果文件留在工作树之外（避免被判为越界改动）
  ( cd "$work" && python3 "$ROOT/evals/check.py" "$eval" "$result" ) || failed=$((failed+1))
  git worktree remove --force "$work" 2>/dev/null || true
done

echo "$failed eval(s) failed / $total total"
[ "$failed" -eq 0 ]
