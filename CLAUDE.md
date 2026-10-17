# <项目名>  （TODO：改成真实项目名）

## Commands
<!-- TODO：换成真实命令，并给一个「健康输出」样例 -->
- Build: `make build`（成功时最后一行 `Build succeeded`）
- Test: `make test`（全绿；不要跳过或删除失败测试）
- Lint: `make lint`（0 warning）
- Run: `make run`

## Conventions
<!-- TODO：只写「不说就会写错」的约定，3–6 条 -->
- 语言/框架：<例如 Python 3.12 + FastAPI / TypeScript + React>
- 每个端点必须有测试，放在 `tests/`
- 日期跨 API 一律用 ISO 8601，不用格式化文本

## Architecture
<!-- TODO：目录职责 + 谁调谁 + 硬约束（限流、缓存、数据分级） -->
- `<dir>/` 是 <职责>，`<dir>/` 是 <职责>
- 只有 <服务 A> 调 <服务 B>，<服务 C> 不直接调
- <外部系统> 限流 <N> rps，必须缓存，不许轮询

## Things Claude gets wrong
<!-- 只写真实犯过两次以上的错；犯了再加 -->
- 不要在 <服务> 里打印请求/响应体，可能含 PII
- 不要升级依赖版本，平台团队统一管理

## Verifying your work
- Build: `make build`（必须出现 `Build succeeded`）
- Test: `make test`（全绿；永远不要跳过或删除失败测试）
- Lint: `make lint`（0 warning）

报告任何任务完成之前，跑完以上三条并贴出输出。
测试失败就改代码，不要改测试。
