# M8A HK620 WordPress Draft QA 检查报告 V1

日期：2026-07-07
QA Agent：QA Agent
任务：Website Agent 首次正式任务（真实业务）
对象：HK620 骨骼线专用封边机 WordPress Draft

## 一、QA 结论

QA 状态：V1 不通过；V2 已纠正，等待 CEO 复审。

结论：原草稿不能作为客户文章发布。原因是正文包含内部审核说明、CEO 审核提示、不得发布提示、仍需人工确认等内部管理语言。该内容属于内部报告口吻，不适合出现在网站前台。

已通过 n8n 对 WordPress Post ID 434 进行纠正更新。当前仍为 Draft，未发布。

## 二、检查对象

- WordPress Post ID：434
- 当前 Draft 标题：HK620 骨骼线专用封边机：面向门厂线条加工的连续工艺方案
- Draft 状态：draft
- 编辑链接：https://woodmachinerynetwork.com/wp-admin/post.php?post=434&action=edit
- REST 链接：https://woodmachinerynetwork.com/wp-json/wp/v2/posts/434
- 原创建 n8n Execution ID：8
- 纠正更新 n8n Execution ID：9

## 三、检查结果

| 检查项 | 结果 | 说明 |
|---|---|---|
| WordPress 状态 | PASS | 文章仍为 Draft，未发布。 |
| 外部发布安全 | PASS | 没有 Publish，没有删除文章，没有修改已发布文章。 |
| 原 V1 正文客户可读性 | FAIL | 包含内部审核说明，不适合客户阅读。 |
| 原 V1 内容口吻 | FAIL | 更像内部任务报告，不像网站产品文章。 |
| V2 正文客户可读性 | NEEDS_REVIEW | 已改为面向门厂、采购和生产负责人的客户语言。 |
| 未证实参数控制 | PASS | 未写功率、电压、速度、价格、交期、ROI、客户案例、行业唯一等未批准信息。 |
| 敏感信息 | PASS | 未包含密码、密钥、令牌。 |
| 公开发布条件 | NEEDS_REVIEW | HK620 当前知识状态仍为 approved_internal，Public Use 仍为 No；正式发布前必须由 CEO/产品负责人审批。 |

## 四、主要问题

1. 原草稿把内部审核说明写进了正文。
2. 原 QA 结论错误地把该草稿判断为可进入发布审核。
3. Website Agent 需要增加“客户可读性”和“内部话术过滤”两个硬性检查。
4. HK620 的公开资料仍不完整，缺少图片、视频、参数表和公开确认口径。

## 五、纠正动作

1. 将 Post ID 434 从内部审核口吻改写为客户可读草稿。
2. 保持 WordPress 状态为 Draft。
3. 未创建新文章。
4. 未发布。
5. 未删除任何文章。
6. 未修改任何已发布文章。
7. 新增质量纠正报告：M8A_HK620_DRAFT_QUALITY_CORRECTION_REPORT_V1.md。

## 六、下一步建议

建议 CEO 先审查 V2 客户可读草稿。

发布前必须确认：

1. 是否允许公开“HK620 骨骼线专用封边机”表述。
2. 是否允许公开“先封边，再开槽，最后切割”的工艺顺序。
3. 是否需要补充产品图片、视频、参数表。
4. 是否需要生成英文版或双语版本。
5. 是否需要销售或产品负责人确认公开话术。

## 七、最终 QA 判断

Website Agent 原 V1 草稿不通过。

当前 Post ID 434 已更新为 V2 客户可读草稿，但仍然只允许作为 Draft 等待 CEO 复审，不允许发布。
