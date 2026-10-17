# Intent: 理赔数据导出
Author: samli2026. Status: draft.

## Problem
理赔运营每月手工从后台导出理赔数据做对账，一次约 3 小时，且字段口径不一致。

## Proposed outcome
运营在门户自助导出指定时间范围的 CSV（最多 1 万行），字段与对账模板一致。

## Affected users and systems
理赔运营、门户、claims-api。

## Constraints
不新增 PII 字段；导出动作必须留审计记录；单次导出 ≤ 1 万行。

## Open questions
是否需要按机构维度拆分权限？
