---
name: api-security
description: 应用 API 安全标准。在创建或修改对外端点、审查 API 代码、生成 OpenAPI 规格时使用。
---
# API 安全审查

当你创建或修改一个 API 端点时：

1. **鉴权**：所有端点必须经过网关 JWT；除 `/health` 外不允许匿名路由。
2. **输入校验**：请求体按 OpenAPI schema 校验，拒绝未知字段。
3. **审计**：所有改变状态的端点必须发出审计事件，含 actor、action、entity、timestamp。
4. **数据分级**：schema 中标记为 `pii` 的字段不得出现在日志或错误信息里。

完成后，运行仓库的安全检查脚本（如果有），并把输出包含在总结里。

<!--
换成你们自己的政策时：
- description 写「什么时候必须加载」，不是主题名；
- 每条规则写成可判定的断言；
- 必须无条件成立的政策，再配一个 hook 兜底（见 .claude/hooks/）。
-->
