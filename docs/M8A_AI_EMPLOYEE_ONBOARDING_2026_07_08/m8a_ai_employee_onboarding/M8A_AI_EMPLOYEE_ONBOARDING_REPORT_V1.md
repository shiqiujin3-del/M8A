# M8A AI 员工正式上岗报告 V1

生成日期：2026-07-08

## 一、结论

第一批 AI 员工已完成上岗方案登记。

本次上岗重点不是新增 API，而是把已经验收成功的平台能力分配给对应 AI 员工。

本次正式上岗员工：

- Website Agent
- SEO Agent
- Data Agent
- Publishing Agent
- Video Agent

## 二、为什么先做 AI 员工上岗

API 授权已经完成主要链路：

- WordPress 已跑通。
- GA4 已只读验收。
- Google Search Console 已只读验收。
- Gmail 已只读验收。
- YouTube 已只读验收。
- n8n 本地执行层已跑通。

因此现在最快的推进方式是让 AI 员工先上岗，把职责、工具、权限边界和第一批任务固定下来。

## 三、上岗员工与职责

### 1. Website Agent

部门：网站部门

职责：

- WordPress Draft
- 网站内容创建
- 页面维护
- 提交 QA 检查

已绑定能力：

- WordPress Draft Only
- n8n 网站工作流

禁止：

- 未经 CEO 审批发布文章
- 删除文章
- 修改已发布文章
- 修改 WordPress 用户、插件、主题和权限

第一任务：

准备下一篇真实业务文章 Draft，不发布，交 QA Agent 审核。

### 2. SEO Agent

部门：网站部门

职责：

- SEO 检查
- GSC 数据读取
- 页面优化建议

已绑定能力：

- Google Search Console 只读

禁止：

- 修改 Search Console 设置
- 修改站点所有权
- 执行高风险站点操作

第一任务：

准备 HK620 页面 SEO 检查报告 V1。

### 3. Data Agent

部门：数据部门

职责：

- GA4 数据读取
- 网站日报
- 流量和转化观察

已绑定能力：

- GA4 只读

禁止：

- 删除分析数据
- 修改 GA4 属性设置
- 创建未审批数据导出

第一任务：

建立 M8A 数据日报字段清单。

### 4. Publishing Agent

部门：营销部门

职责：

- 内容发布准备
- 邮件草稿流程
- 营销发布队列

已绑定能力：

- Gmail 只读

禁止：

- 自动发送邮件
- 删除邮件
- 读取邮件正文
- 修改邮箱标签或邮件状态

第一任务：

设计 Gmail Draft Only 工作流，不发送邮件。

### 5. Video Agent

部门：视频部门

职责：

- 视频脚本
- 视频工作流准备
- YouTube 私有/草稿上传方案

已绑定能力：

- YouTube 只读

禁止：

- 自动上传公开视频
- 公开发布视频
- 删除视频
- 修改频道设置

第一任务：

设计 YouTube Private/Draft Only 工作流，不公开发布。

## 四、当前安全边界

允许：

- 只读验收工作流
- WordPress Draft Only
- 内部报告生成
- CEO 已批准的本地工作流

禁止：

- 自动发送 Gmail
- 自动发布 YouTube
- 自动发布 WordPress
- 删除外部平台内容
- 修改外部平台权限或设置
- 在报告中保存密钥、Token 或密码

## 五、已生成落地文件

本次生成以下文件：

- `m8a_ai_employee_onboarding/ai_employee_onboarding_v1.json`
- `m8a_ai_employee_onboarding/employee_status_patch_v1.json`
- `m8a_ai_employee_onboarding/n8n_workflow_bindings_patch_v1.json`
- `m8a_ai_employee_onboarding/M8A_AI_EMPLOYEE_ONBOARDING_REPORT_V1.md`

## 六、需要同步到 Commander 的内容

需要同步到：

- `apps/commander/employees/registry/ai_employee_registry.json`
- `apps/commander/employees/runtime/employee_status.json`
- `apps/commander/integrations/n8n_workflow_bindings.json`
- `apps/dashboard/employee_workbench_data.json`

当前环境暂不允许直接写入 M8A 主目录，因此本次先生成上岗包，等待同步。

## 七、下一步

建议下一步执行：

1. 同步上岗包到 Commander。
2. 打开 AI 员工工作台，确认 5 名员工状态显示为“正式上岗”。
3. 让 Website Agent 开始下一篇 WordPress Draft。
4. 让 SEO Agent 输出 HK620 页面 SEO 检查报告。
5. 让 Data Agent 输出 M8A 数据日报模板。

## 八、最终结论

M8A 第一批 AI 员工已经具备上岗条件。

当前应进入“员工执行任务”阶段，而不是继续增加平台或框架。
