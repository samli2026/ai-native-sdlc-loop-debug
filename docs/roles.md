# 角色、权限与协作模式

> 这套工作流的协作对象不是「会话」，而是 Git 里的工件。所以单人能跑，多人更顺；但**批准动作**需要真人有权限、有留痕。

## 1. 角色表

| 角色 | 对什么负责 | 关键动作 |
|---|---|---|
| 发起人（任何人） | 问题与意图 | 和 Claude 写 `intent.md`，纠正误解 |
| 产品负责人 | 值不值得做、范围 | 接受/关闭 intent；签核 spec；分派 concern |
| 工程师 | 实现与计划 | plan mode 出 `plan.md`；提交 PR；自检 |
| 技术负责人 / code owner | 技术风险与合并 | 批准 PR；审 `REVIEW.md` 变更 |
| 平台工程师 | 控制面 | 托管设置、hooks、MCP、CI、权限 |
| 安全 / 合规 owner | 政策真相源 | 签核 policy 对应的 skill；处理 concern |
| 发布经理 | 生产发布授权 | 批准变更工单（生产 gate） |
| 值班 / 服务 owner | 生产与 triage | 处理控制带告警与 intent 队列 |

## 2. 工件 × 角色矩阵

R = 负责产出，A = 批准/签核，C = 需咨询，I = 知会

| 工件 | 发起人 | 产品负责人 | 工程师 | 技术负责人 | 平台 | 安全/合规 | 发布经理 |
|---|---|---|---|---|---|---|---|
| `intent.md` | R | A | I | I | I | C | — |
| `spec.md` | I | A | C | C | — | C（政策 owner） | — |
| `plan.md` | — | I | R | A（高风险） | — | — | — |
| PR / diff | — | I | R | A | — | C | — |
| `SKILL.md` | — | — | R | A | C | A（政策 owner） | — |
| `settings.json` / hooks | — | — | C | C | R+A | C | — |
| eval 用例 | — | — | R | C | A | C | — |
| `bands.yaml` / 阈值 | — | I | C | C | A | — | C |
| 生产 release | — | — | C | — | C | — | A |

## 3. 三种规模怎么用

### A. 单人（1 人 + Claude）

角色全部合并到一个人，**但不要合并「动作痕迹」**：

1. 仍然走分支 + PR：自己 review 自己的 PR 没意义，但 PR 是证据链，也是让 Claude 做 review 的载体。
2. **让 Claude 做对抗式 review**：明确要求「找出三个最可能出问题的地方，别只夸」。这是单人模式下最接近第二双眼睛的东西。
3. **生产发布保留一道人工确认**：即使是你自己，也要求带 `CHG-` 工单或第二条命令确认——防止 agent 误触发。
4. 每周花 10 分钟回看：review findings、eval 通过率、返工记录，把重复两次的错误写进 `CLAUDE.md`。
5. 风险：**自审自批**。单人模式下可接受的边界是「低风险变更」，触碰鉴权/支付/数据删除时，找一个人看一眼。

### B. 小团队（3–10 人，推荐形态）

| 角色 | 建议兼任 |
|---|---|
| 产品负责人 | PM 或业务 owner（1 人） |
| 技术负责人 / code owner | 资深工程师（1–2 人） |
| 平台工程师 | 1 人（可兼） |
| 安全/合规 owner | 按政策领域分（可兼） |
| 发布经理 | 轮值 |

协作靠三样东西，不靠会：
- **工件代替会议**：`intent.md` 接受即触发 spec，spec 签核即触发 plan。
- **SLA 代替催促**：intent 48 小时内必须响应；spec concern 3 个工作日内分派；PR 首个 review 当天。
- **门代替口头约定**：生产发布必须过 hook；`CLAUDE.md`/`REVIEW.md`/skill 变更必须 code owner 批准。

### C. 大型 / 受监管（10+ 人）

- 平台团队下发**托管设置**（MDM/管理控制台），个人关不掉 hook、权限、沙箱、MCP 白名单。
- 分支保护强制 code owner 批准；PR 即审计记录。
- 职责分离：写代码的 agent 无权 approve；发布经理与工程师分离。
- 用 OpenTelemetry / Compliance API 接审计与监控，不新建系统。

## 4. 怎么把角色写进仓库

1. **CODEOWNERS**：按目录指定 owner（见仓库根 `CODEOWNERS` 模板），GitHub 会自动请求 review。
2. **分支保护**（GitHub）：

```bash
gh api -X PUT repos/:owner/:repo/branches/main/protection \
  -f required_pull_request_reviews.required_approving_review_count=1 \
  -F required_pull_request_reviews.require_code_owner_reviews=true \
  -F enforce_admins=true
```

3. **托管设置**：平台团队按手册 5.10 节下发（deny/allow、sandbox、credentials、版本下限）。
4. **值班与 triage**：给 `intent` 的告警来源指定轮值人，否则控制带闭环会变成噪音。

## 5. 单人 → 多人的升级信号

出现以下任一情况，就该从单人模式切到小团队：
- 同一天有 2 个以上变更在等 review；
- 出现一次「自己批准的高风险变更」；
- `CLAUDE.md` 开始被多人同时修改；
- 生产事故需要第二个人一起回滚。
