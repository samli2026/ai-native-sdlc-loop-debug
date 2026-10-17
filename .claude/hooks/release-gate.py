#!/usr/bin/env python3
"""PreToolUse 发布门模板。

规则（按环境分级）：
  dev        -> allow
  staging    -> 来自 main 的管道发布 allow，否则 ask
  production -> 必须带已批准的 CHG-xxxx 工单，否则 deny

启用前：
  1. 把 CHANGE_TICKET_CMD 指向你们变更系统的 CLI（输出 JSON，含 state/version/approver）；
  2. 或改成调用你们自己的审批 API。
"""
import json
import os
import re
import shlex
import subprocess
import sys


def decide(kind: str, reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": kind,
            "permissionDecisionReason": reason,
        }
    }, ensure_ascii=False))
    sys.exit(0)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        decide("deny", "无法解析 hook 输入，按 fail-closed 处理。")

    tool = data.get("tool_name", "")
    args = data.get("tool_input", {}) or {}
    version = str(args.get("version", ""))
    ticket = str(args.get("ticket") or "")

    if not tool.endswith("__release"):
        decide("allow", "非发布工具，放行。")

    if tool.startswith("mcp__deploy-dev__"):
        decide("allow", "dev 环境无需审批。")

    if tool.startswith("mcp__deploy-staging__"):
        if os.environ.get("GITHUB_REF") == "refs/heads/main":
            decide("allow", "来自 main 的管道发布，已批准的 merge 即批准。")
        decide("ask", f"即将把 {version or '(未指定版本)'} 发布到 staging。请确认你负责这次发布。")

    # production：只认已批准的变更工单
    route = ("在变更系统创建工单，拿到 CHG-编号并审批通过后，"
             "带 ticket 参数重新调用 release。")
    if not re.fullmatch(r"CHG-\d+", ticket):
        decide("deny", f"生产发布需要变更工单号。{route}")
    if not re.fullmatch(r"[0-9a-f]{7,40}", version):
        decide("deny", f"生产发布需要完整的 commit SHA。{route}")

    cmd = os.environ.get("CHANGE_TICKET_CMD", "").strip()
    if not cmd:
        decide("deny",
               "未配置 CHANGE_TICKET_CMD，无法校验工单，按 fail-closed 拒绝。"
               "请联系平台工程师完成配置。")

    try:
        out = subprocess.run(
            shlex.split(cmd) + ["--ticket", ticket, "--format", "json"],
            capture_output=True, text=True, timeout=15, check=False,
        )
        info = json.loads(out.stdout or "{}")
    except Exception as exc:  # noqa: BLE001
        decide("deny", f"工单校验失败（{exc}），按 fail-closed 拒绝。")

    if info.get("state") == "approved" and info.get("version") == version:
        decide("allow", f"{ticket} 已由 {info.get('approver', '发布经理')} 批准。")
    decide("deny", f"{ticket} 未针对版本 {version} 批准。{route}")


if __name__ == "__main__":
    main()
