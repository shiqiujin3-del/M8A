# n8n 工作流绑定报告

## 当前结论

7 个 n8n 工作流已经绑定到 AI 员工。

## 绑定结果

1. PRODUCT_KNOWLEDGE_ACQUISITION_WORKFLOW：Research Agent 负责，Knowledge Agent 备用。
2. PRODUCT_KNOWLEDGE_REVIEW_WORKFLOW：Knowledge Agent 负责，QA Agent 备用。
3. HK620_KNOWLEDGE_COLLECTOR_WORKFLOW：Research Agent 负责，Knowledge Agent 备用。
4. HK620_KNOWLEDGE_RETRIEVAL_TEST：Knowledge Agent 负责，QA Agent 备用。
5. M8A_P3B_OPENAI_EMBEDDING_TEST：Automation Agent 负责，QA Agent 备用。
6. M8A_P3_RAG_TEST_WORKFLOW：Knowledge Agent 负责，Research Agent 备用。
7. M8A_P2_HEALTHCHECK_WORKFLOW：QA Agent 负责，Automation Agent 备用。

## 现在能做什么

M8N 可以把内部任务分派给 AI 员工，AI 员工再调用对应的 n8n 工作流。

## 仍然锁定的动作

发送邮件、公开视频、公开发布文章、删除数据、修改外部账号设置，仍然需要 CEO 单独确认。

生成时间：2026-07-07T03:54:18Z
