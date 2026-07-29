# M8A 总控台一致性验收规则 V1

日期：2026-07-08

## 一、核心原则

```text
没有同步到总控台 = 没完成。
```

任何 API、AI 员工、n8n 工作流、平台连接、任务执行、日报、验收报告，如果只在局部完成，但没有同步到 M8A 总控台和报告索引，一律不得视为完成。

## 二、适用范围

本标准适用于 M8A 全部执行对象：

- Commander
- Mission Control
- Worker Runner
- AI Employee
- Access Manager
- Website Agent
- SEO / GEO / QA / Publishing Agent
- n8n Workflow
- WordPress / Gmail / YouTube / GA4 / GSC 等平台能力
- 所有任务报告
- 所有 CEO Review 项

## 三、必须同步的五类总控状态

任何任务完成后，必须根据任务类型同步以下文件。

### 1. 凭证和平台授权状态

必须同步：

```text
apps/commander/employees/registry/credential_registry.json
```

适用场景：

- API 授权完成
- OAuth 授权完成
- n8n 凭证验证完成
- 平台只读验收完成
- Draft Only / Publish / Send / Upload 能力变化

要求：

- 只记录账号、凭证位置、权限范围、状态。
- 禁止记录明文密码、token、Application Password、OAuth Secret。
- 状态必须明确，例如：
  - pending_authorization
  - connected_read_verified
  - connected_draft_only_verified
  - connected_publish_approved
  - blocked

### 2. n8n 工作流绑定状态

必须同步：

```text
apps/commander/integrations/n8n_workflow_bindings.json
```

适用场景：

- 新 n8n 工作流创建
- 工作流绑定 AI Employee
- 工作流验收成功
- 工作流失败或被暂停

要求：

- 记录 workflow 名称。
- 记录负责员工。
- 记录输入/输出。
- 记录允许动作和禁止动作。
- 记录是否需要 CEO Approval。
- 记录最近一次执行结果。

### 3. AI 员工状态

必须同步：

```text
apps/commander/employees/runtime/employee_status.json
apps/commander/employees/runtime/employee_health.json
apps/commander/employees/runtime/employee_queue.json
apps/commander/employees/runtime/employee_activity_log.json
```

适用场景：

- 员工开始任务
- 员工完成任务
- 员工失败
- 员工等待审批
- 员工进入 paused / offline / busy / idle 状态

要求：

- 页面显示的员工状态必须与真实任务状态一致。
- 员工已上岗，不得在页面继续显示为未上岗或空闲。
- 员工失败，不得在页面显示为 completed。
- 员工等待审批，必须进入 CEO Review。

### 4. Dashboard 数据

必须同步：

```text
apps/dashboard/commander_dashboard_data.json
apps/dashboard/employee_workbench_data.json
apps/dashboard/platform_connector_status.json
```

适用场景：

- 总控台首页指标变化
- 平台接入状态变化
- 员工工作台状态变化
- Mission / Task / Artifact / Approval 状态变化

要求：

- API 已接通，总控台不得显示未连接。
- 平台已只读验收，总控台不得显示 pending。
- 任务已完成，总控台不得显示 running。
- 有待审批事项，总控台必须显示在 CEO Review / Approval 区域。

### 5. 报告索引

必须同步：

```text
docs/M8A_REPORT_INDEX.json
docs/M8A_REPORT_INDEX.md
```

适用场景：

- 任意 Mission 完成
- 任意验收报告生成
- 任意平台接入状态变化
- 任意重大失败或恢复完成
- 任意 CEO Review 项新增或关闭

要求：

每条记录至少包含：

```text
mission_id
mission_name
module
branch
commit
report_path
status
tests
ceo_review_status
next_action
```

## 四、完成定义

一个任务只有同时满足以下条件，才算完成：

1. 实际动作完成。
2. 本地记录完成。
3. Dashboard 数据完成。
4. 报告索引完成。
5. CEO Review 状态明确。
6. 安全边界写清楚。
7. JSON 校验通过。

否则状态必须是：

```text
completed_but_dashboard_not_synced
```

或者：

```text
blocked_dashboard_sync_required
```

## 五、禁止状态漂移

禁止以下情况：

- API 已接通，但总控台显示未连接。
- 员工已上岗，但页面显示空闲。
- 任务已完成，但日报没有写。
- 平台已授权，但 credential registry 没更新。
- n8n 工作流已成功，但 workflow bindings 没更新。
- 报告已生成，但 report index 没登记。
- CEO 已批准，但 Approval 状态仍 pending。
- 任务失败，但 Dashboard 没显示失败。

## 六、每个角色的责任

### Commander

负责统一判断 Mission 是否真正完成。

### Commander Reporting Agent

负责把报告写入 report index，并更新日报和 CEO Review List。

### Access Manager Agent

负责更新 credential registry，不保存明文密钥。

### Automation Agent

负责更新 n8n workflow bindings 和执行状态。

### Website Agent / Publishing Agent / Video Agent / Sales Agent

负责把业务产出写成 Artifact，并同步 Dashboard。

### QA Agent

负责检查：业务结果、总控状态、报告索引是否一致。

## 七、验收流程

任何任务完成后必须执行：

```text
1. 检查业务输出
2. 检查相关 JSON 状态文件
3. 检查 Dashboard 是否显示正确
4. 检查 report index 是否登记
5. 检查 CEO Review List 是否需要更新
6. 执行 JSON 校验
7. 输出中文验收报告
```

## 八、CEO 可引用标准

CEO 后续可以直接引用本标准：

```text
没有同步到总控台 = 没完成。
```

如果任何员工、API、工作流声称任务完成，但总控台、Dashboard 数据、报告索引、CEO Review List 没有同步，CEO 可以直接判定该任务未完成。

## 九、安全边界

同步总控台不代表允许外部动作。

以下动作仍必须单独 CEO Approval：

- WordPress 发布
- Gmail 发送
- YouTube 上传或发布
- 社媒发布
- 删除内容
- 修改平台权限
- 修改 OAuth 密钥
- 保存或迁移真实凭证

## 十、当前状态

本标准自写入 M8A 项目起生效。

状态：active
