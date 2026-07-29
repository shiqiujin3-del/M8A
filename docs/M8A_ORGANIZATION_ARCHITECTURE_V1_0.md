# M8A 组织架构 V1.0

## 状态

本文件为 CEO 冻结后的 M8A 唯一正式组织架构标准。

冻结时间：2026-07-07T05:33:25Z

未经 CEO 批准，不得随意修改组织架构，不得新增同级中心。

## 第一层

首席执行官（CEO）

↓

M8A AI 自动运营中心

↓

总指挥中心（Commander）

Commander 是整个 AI 公司的总控制中心，负责任务管理、AI 员工管理、调度、报告和 Dashboard。

Commander 本身不直接执行业务。

## 第二层

Commander 下设五个中心：

1. 任务中心
2. AI 员工中心
3. 知识中心
4. 数据中心
5. 调度中心

## 第三层：AI 员工部门

### 网站部门

负责网站建设、WordPress、SEO、GEO 和网站 QA。

AI 员工：Website Agent、SEO Agent、GEO Agent、QA Agent。

### 知识部门

负责产品知识、行业研究、RAG、知识库和 FAQ。

AI 员工：Research Agent、Knowledge Agent。

### 营销部门

负责内容发布、社交媒体和邮件营销。

AI 员工：Publishing Agent。

后续可增加：Email Agent、Social Media Agent。

### 视频部门（规划）

负责视频脚本、视频生成、视频剪辑和视频审核。

后续 AI 员工：Script Agent、Video Generation Agent、Video Editing Agent、Thumbnail Agent。

### 运营部门

负责自动化、日报、周报和系统运行。

AI 员工：Automation Agent、Commander Reporting Agent。

## 执行工具层

WordPress、GitHub、n8n、GA4、Google Search Console、即梦、可灵、剪映、CapCut、Gmail、YouTube、Codex、Coze 等均属于执行工具。

它们不是组织架构的一部分。

AI 员工通过执行工具完成任务。

## n8n 定位

n8n 是 M8A 自动化执行引擎。

n8n 不是总控，不是 Commander，不是 AI 员工，也不是组织中心。

所有 n8n Workflow 按业务分类管理：知识中心工作流、网站中心工作流、视频中心工作流、营销中心工作流、数据分析工作流、基础设施工作流。

## 开发原则

1. 不新增重复中心。
2. 优先完善现有模块。
3. 优先让 AI 员工正式上岗，而不是继续增加框架。
4. 所有外部平台统一作为执行工具接入。
5. 所有开发遵循本组织架构。

## 配套机器可读文件

- `apps/commander/governance/organization_architecture_v1_0.json`
- `apps/commander/governance/directory_ownership_v1_0.json`
- `apps/commander/employees/registry/department_registry.json`
