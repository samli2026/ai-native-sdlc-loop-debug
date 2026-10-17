#!/usr/bin/env python3
"""执行一条 eval 的全部检查。

用法：python3 evals/check.py <eval.json> <result.json>
从仓库根目录运行；失败的检查会打印出来并以非零码退出。
"""
import json
import os
import subprocess
import sys


def strays(eval_obj):
    out = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    allowed = eval_obj.get("may_change", [])
    bad = []
    for line in out.stdout.splitlines():
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if not path:
            continue
        if any(path == a or path.startswith(a.rstrip("/") + "/") for a in allowed):
            continue
        bad.append(path)
    return bad


def main() -> int:
    if len(sys.argv) != 3:
        print("用法: check.py <eval.json> <result.json>", file=sys.stderr)
        return 2
    eval_path, result_path = sys.argv[1], sys.argv[2]
    try:
        ev = json.load(open(eval_path, encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"无法读取 eval 定义: {exc}", file=sys.stderr)
        return 2

    name = ev.get("name", os.path.basename(eval_path))
    os.environ["EVALS"] = os.path.dirname(os.path.abspath(eval_path))
    total = len(ev.get("checks", []))

    report = ""
    try:
        res = json.load(open(result_path, encoding="utf-8"))
    except Exception:  # noqa: BLE001
        res = {}

    if res.get("is_error", True) is not False:
        msg = res.get("result") or ", ".join(res.get("errors", [])) or "结果文件为空或损坏"
        print(f"FAIL {name} (0/{total} checks)")
        print("  run ended in an error:", msg)
        return 1

    bad = strays(ev)
    if bad:
        print(f"FAIL {name} (0/{total} checks)")
        print("  changed files outside may_change:")
        for p in bad:
            print("   ", p)
        return 1

    passed = 0
    for chk in ev.get("checks", []):
        cmd = chk.get("run", "")
        proc = subprocess.run(["bash", "-lc", cmd], capture_output=True, text=True,
                              env={**os.environ, "EVALS": os.environ["EVALS"]})
        if proc.returncode == 0:
            passed += 1
        else:
            report += f"  failed: {chk.get('name', cmd)}\n"
            tail = (proc.stdout + proc.stderr).strip().splitlines()[:3]
            for line in tail:
                report += f"    {line}\n"

    after = strays(ev)
    if after:
        passed = 0
        report += "  a check changed files outside may_change:\n"
        for p in after:
            report += f"    {p}\n"

    if passed == total and total > 0:
        print(f"PASS {name} ({passed}/{total} checks)")
        return 0
    print(f"FAIL {name} ({passed}/{total} checks)")
    sys.stdout.write(report)
    return 1


if __name__ == "__main__":
    sys.exit(main())
