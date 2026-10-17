# Spec: 理赔状态自助查询
From: intent.md (samli2026). Status: ready for product owner review.
Skills applied: api-security

## Requirements
- R1. 已登录客户可查看每笔开放理赔的状态、下一步、预计日期。
- R2. 状态为四种之一：received / in_review / approved / paid。
- R3. 响应只带这三个字段。
- R4. 数据最多 60 秒旧。

## Areas of concern
1. 第三方查勘员无门户账号，本次不做。Owner: security
