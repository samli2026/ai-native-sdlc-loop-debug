# Spec: 理赔数据导出
From: intent.md (samli2026). Status: ready for product owner review.
Skills applied: api-security

## Requirements
- R1. 已登录运营可选择起止日期导出 CSV。
- R2. 列固定为 claim_id, status, received_at, next_step, expected_date。
- R3. 单次导出最多 10000 行，超出提示缩小范围。
- R4. 每次导出写一条审计事件（actor、range、rows、timestamp）。

## Design
- `GET /claims/export?from=&to=`，网关 JWT，返回 text/csv。
- claims-api 从 claims-core 分页读取，流式写出。
- 导出动作发 audit 事件，不落 PII 字段。

## How each constraint in the intent is met
| Constraint | Met by |
| :---- | :---- |
| 不新增 PII 字段 | R2 列清单不含姓名/证件号 |
| 留审计记录 | R4 |
| ≤ 1 万行 | R3 |

## Open questions from the intent
- 按机构拆权限：未回答，carried forward as concern 1。

## Areas of concern
1. 机构维度权限未定义。Owner: security
