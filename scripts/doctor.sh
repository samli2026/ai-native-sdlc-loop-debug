#!/usr/bin/env bash
# AI 原生 SDLC 准备度体检。不改任何文件，只报告。
set -uo pipefail

cd "$(dirname "$0")/.." || exit 2
ROOT="$(pwd)"
pass=0; warn=0; fail=0

ok()   { printf "  ✅ %s\n" "$1"; pass=$((pass+1)); }
warn() { printf "  ⚠️  %s\n     → %s\n" "$1" "$2"; warn=$((warn+1)); }
bad()  { printf "  ❌ %s\n     → %s\n" "$1" "$2"; fail=$((fail+1)); }

echo "AI 原生 SDLC 准备度体检：$ROOT"
echo

echo "阶段 1 · 基座"
if [ -d "$ROOT/.git" ]; then ok "git 仓库"; else warn "不是 git 仓库根目录" "cd 到仓库根目录再跑"; fi
if [ -f CLAUDE.md ]; then
  lines=$(wc -l < CLAUDE.md | tr -d ' ')
  ok "CLAUDE.md 存在（$lines 行）"
  [ "$lines" -gt 120 ] && bad "CLAUDE.md 超过 120 行" "砍到一页：只留命令、约定、架构、常错项"
  if grep -qiE "verifying|验证|完成前" CLAUDE.md; then ok "CLAUDE.md 含验证要求"; else bad "缺少「Verifying your work」" "把「跑完再报告并贴输出」写进去"; fi
else bad "缺少 CLAUDE.md" "跑 claude /init 或从模板复制"; fi
if [ -f Makefile ] && grep -qE "^test:" Makefile && ! grep -A2 "^test:" Makefile | grep -q "尚未配置"; then
  ok "一键测试已配置"
else bad "make test 未配置" "编辑 Makefile，让失败时非零退出"; fi

echo
echo "阶段 2 · 工件链与知识"
missing=""
for f in intent/_template/intent.md intent/_template/spec.md intent/_template/plan.md; do [ -f "$f" ] || missing="$missing $f"; done
if [ -z "$missing" ]; then ok "intent/spec/plan 模板齐全"; else bad "缺少模板:$missing" "从套件拷入"; fi
n=$(find .claude/skills -name SKILL.md 2>/dev/null | wc -l | tr -d ' ')
[ "$n" -ge 1 ] && ok "skill 数量：$n" || bad "没有 skill" "挑一条执行不一致的政策写成 SKILL.md"
[ -d .claude/agents ] && [ -n "$(ls -A .claude/agents 2>/dev/null)" ] && ok "已定义 subagent" || warn "没有 subagent" "可选：先从 verifier 开始"

echo
echo "阶段 3 · 评审与门"
if [ -f REVIEW.md ] && grep -qiE "passes|## pass" REVIEW.md; then ok "REVIEW.md 存在且定义 pass"; else bad "缺少 REVIEW.md 或 pass 定义" "按模板写 bug/security/compliance 三 pass"; fi
if [ -f CODEOWNERS ]; then ok "CODEOWNERS 存在（多人协作必需）"; else warn "没有 CODEOWNERS" "多人协作时按 docs/roles.md 指定 code owner"; fi
if python3 -c "import json;json.load(open('.claude/settings.json'))" 2>/dev/null; then ok "settings.json 合法"; else bad ".claude/settings.json 不是合法 JSON" "修 syntax，否则 Claude Code 不加载 hooks"; fi
hooks=$(grep -c '"type": "command"' .claude/settings.json 2>/dev/null || echo 0)
[ "$hooks" -ge 1 ] && ok "已配置 $hooks 个 hook" || warn "没有 hook" "需要确定性拦截时再加，别一开始就上"
for h in .claude/hooks/*.py; do
  [ -e "$h" ] && { [ -x "$h" ] && ok "$(basename "$h") 可执行" || warn "$(basename "$h") 不可执行" "chmod +x .claude/hooks/*.py"; }
done

echo
echo "阶段 4 · evals 与 CI"
n=$(find evals -name "*.eval.json" ! -name "_*" 2>/dev/null | wc -l | tr -d ' ')
[ "$n" -ge 1 ] && ok "eval 用例：$n" || warn "还没有 eval 用例" "先收 20 个真实任务"
[ -f .github/workflows/agent-evals.yml ] && ok "eval CI 已配置" || warn "没有 eval CI" "启用前先配 ANTHROPIC_API_KEY"
[ -f evals/check.py ] && python3 -c "import ast;ast.parse(open('evals/check.py').read())" 2>/dev/null && ok "eval 检查器可用" || warn "check.py 有问题" "python3 -m py_compile evals/check.py 看报错"

echo
echo "阶段 5 · 指标闭环"
if [ -f bands.yaml ] && [ -f scripts/detect_band.py ]; then
  python3 scripts/detect_band.py --self-test >/dev/null 2>&1 && ok "控制带检测器自测通过" || bad "detect_band.py 自测失败" "跑 python3 scripts/detect_band.py --self-test"
else warn "指标闭环未配置" "阶段 5 再做，先别急"; fi

echo
echo "汇总：✅ $pass   ⚠️ $warn   ❌ $fail"
if [ "$fail" -gt 0 ]; then
  echo "下一步：先清掉 ❌，再考虑加新东西。"
else
  echo "没有阻塞项。按 搭建指南.md 进入下一阶段。"
fi
