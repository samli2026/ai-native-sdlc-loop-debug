# Review instructions

## Passes
每次 review 跑三个 pass，并给每条 finding 標注所属 pass：
- Bugs：逻辑错误、边界条件、隐蔽回归
- Security：注入风险、鉴权缺口、日志中的 PII
- Compliance：变更是否符合 `intent/` 下的 `spec.md`、`plan.md` 与设计原则

## What Important means here
只有「会破坏行为、泄露数据、违反政策」才算 Important；风格与命名是 Nit。

## Cap the nits
每次最多 5 条 Nit，其余只给数量。

## Do not report
`dist/`、`build/`、`*.gen.*` 等生成产物，以及 CI 已经强制的内容。

## Escalate
<!-- TODO：把组织里必须升级的情况写进来 -->
- 改动鉴权、加密、审计日志
- 新增外部依赖
- 触碰生产配置或 migration
