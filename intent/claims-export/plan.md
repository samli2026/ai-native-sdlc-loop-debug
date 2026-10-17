# Plan: 理赔数据导出 (from intent.md and spec.md)

## Files that change
- `src/claims_export.py`（new）
- `tests/test_claims_export.py`（new）
- `src/audit.py`（new）

## Order of work
1. 审计事件函数（R4）。
2. CSV 导出与行数上限（R1–R3）。
3. 测试覆盖 R2 列清单与 R3 上限。

## Risks
claims-core 分页不稳定；流式写出时异常会留下半截响应。

## Proof
`make test` 全绿；测试断言列顺序与 1 万行上限。
