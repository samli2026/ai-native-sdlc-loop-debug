# Plan: 理赔状态自助查询 (from intent.md and spec.md)

## Files that change
- `src/claims_status.py`（new）
- `tests/test_claims_status.py`（new）

## Order of work
1. 实现状态查询函数（R1–R3）。
2. 加 60 秒缓存（R4）。
3. 补测试。

## Risks
claims-core 限 50 rps，必须缓存。

## Proof
`make test` 全绿；缓存命中用例覆盖。
