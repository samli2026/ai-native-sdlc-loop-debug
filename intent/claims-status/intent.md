# Intent: 理赔状态自助查询
Author: samli2026. Status: accepted.

## Problem
客户致电客服询问理赔进度；客服约 1/3 通话时间用于回答纯状态查询。

## Proposed outcome
客户在门户看到状态、下一步与预计日期。

## Affected users and systems
理赔客服、门户团队、claims-core API。

## Constraints
门户会话不新增 PII；沿用既有鉴权。

## Open questions
第三方查勘员是否需要访问？
