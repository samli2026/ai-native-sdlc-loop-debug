#!/usr/bin/env python3
"""PreToolUse 测试保护。

当仓库里存在 .claude/fix-mode 标记时，阻止 agent 编辑测试文件，
防止「改测试让 bug 通过」。修完删除标记即可。

平时（没有标记）完全放行，不影响正常开发。
"""
import json
import os
import re
import sys

PROJECT = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
FIX_MODE = os.path.join(PROJECT, ".claude", "fix-mode")
TEST_PATTERN = re.compile(
    r"(^|/)(tests?|__tests__|spec|specs)/|(_test\.|\.test\.|\.spec\.|test_.*\.py$)"
)


def allow() -> None:
    sys.exit(0)


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }, ensure_ascii=False))
    sys.exit(0)


def main() -> None:
    if not os.path.exists(FIX_MODE):
        allow()
    try:
        data = json.load(sys.stdin)
    except Exception:
        allow()
    path = str((data.get("tool_input") or {}).get("file_path", ""))
    if path and TEST_PATTERN.search(path.replace(PROJECT, "")):
        deny(
            "当前处于修 bug 模式（.claude/fix-mode 存在）：不允许修改测试文件。\n"
            "请修改实现代码让已有测试通过；如果确实需要改测试，先向人说明理由并删除该标记。"
        )
    allow()


if __name__ == "__main__":
    main()
