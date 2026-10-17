# 文件 ↔ play 对照

| 阶段 | play | 套件文件 | 验收 |
|---|---|---|---|
| Plan | Capture as intent.md | `intent/_template/intent.md`、`intent/` 目录 | 第一个非工程同事独立提交 intent |
| Design | Requirements and design | `intent/_template/spec.md`、`.claude/skills/*` | spec 里每个 concern 有 owner |
| Build | Plan mode | `intent/_template/plan.md` | reviewer 能对着 plan 逐条查 diff |
| Build | CLAUDE.md | `CLAUDE.md` | 新成员只读它就完成一次构建+测试 |
| Build | Skills | `.claude/skills/<name>/SKILL.md` | 3 种问法都能触发 |
| Build | 并行会话与 subagent | `.claude/agents/verifier.md` | 2 个会话 + verifier 稳定一周 |
| Test | Feedback loop | `Makefile`、`CLAUDE.md#verifying` | agent 报告前会跑并贴输出 |
| Test | Continuous evals | `evals/`、`.github/workflows/agent-evals.yml` | 配置变差被拦住一次 |
| Deploy | PR review 环 | `REVIEW.md` | 首个 review 时间降到分钟级 |
| Deploy | Hooks 审批门 | `.claude/settings.json`、`.claude/hooks/release-gate.py` | 无工单发布被拒，且提示申请路径 |
| Deploy | CI/CD | 参考手册第 5.11 节 | 生产无 release 权限；回滚一条命令 |
| Maintain | 指标闭环 | `bands.yaml`、`scripts/detect_band.py` | 越界 10 分钟内产出 intent.md |
| —— | 自查 | `scripts/doctor.sh` | 每阶段结束跑一次 |
