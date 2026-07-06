# HK620 Retrieval Test Report

Date: 2026-07-06
Workflow: `HK620_KNOWLEDGE_RETRIEVAL_TEST`
Collection: `m8a_product_knowledge_v1`
Product: HK620
Embedding method: `local_semantic_placeholder_v1`
Review status: `review_pending`

## Summary

| Item | Result |
|---|---|
| Golden Knowledge Record read | PASS |
| PostgreSQL chunks available | PASS |
| Qdrant chunks available | PASS |
| Retrieval workflow created | PASS |
| Questions tested | 10 |
| Answers cite source chunks | PASS |
| Unknown information handled as unconfirmed | PASS |

## Important Boundary

The current retrieval uses `local_semantic_placeholder_v1` because real OpenAI Embedding is not configured yet. It validates the product knowledge retrieval structure, source citation behavior, and no-fabrication answer policy. After OpenAI Embedding is available, the same chunks should be re-embedded with the real embedding model.

## Test Results

### 1. HK620 是什么设备？

Answer: HK620 是一台用于 skeleton door strips 的特殊封边设备。当前已确认资料显示，它把封边、开槽和切割组合在一个流程中。

Source Chunks:

1. Overview / hk620_overview_v1 / score 0.8222
2. FAQ / hk620_faq_v1 / score 0.7749
3. Advantages / hk620_advantages_v1 / score 0.7470

### 2. HK620 适合哪些客户？

Answer: HK620 的已确认应用是 skeleton door strip processing。门厂、家具厂、木工生产企业和经销商等客户类型目前仍属于 review-pending，暂无已确认资料可作为正式客户定位。

Source Chunks:

1. Applications / hk620_applications_v1 / score 0.5917
2. Sales / hk620_sales_v1 / score 0.3725
3. FAQ / hk620_faq_v1 / score 0.2594

### 3. HK620 有哪些核心功能？

Answer: HK620 的已确认核心功能是：面向 skeleton door strips，组合封边、开槽和切割三个工序，并支持比拆分工序更集成的处理流程。

Source Chunks:

1. Overview / hk620_overview_v1 / score 0.7581
2. Sales / hk620_sales_v1 / score 0.7004
3. FAQ / hk620_faq_v1 / score 0.6964

### 4. HK620 与普通封边机有什么区别？

Answer: 当前已确认的是：HK620 是面向 skeleton door strips 的特殊封边设备，并把封边、开槽、切割组合在一个流程中。与普通封边机的更详细差异暂无已确认资料。

Source Chunks:

1. Advantages / hk620_advantages_v1 / score 0.8304
2. Overview / hk620_overview_v1 / score 0.7364
3. FAQ / hk620_faq_v1 / score 0.7149

### 5. HK620 有哪些技术参数？

Answer: HK620 已确认的技术信息包括：它是用于 skeleton door strips 的特殊封边设备，已确认组合工序为封边、开槽和切割。功率、电压、尺寸、重量、速度、封边带厚度、工件范围、控制系统等暂无已确认资料。

Source Chunks:

1. Technical Specifications / hk620_technical_specifications_v1 / score 0.5583
2. Troubleshooting / hk620_troubleshooting_v1 / score 0.4053
3. FAQ / hk620_faq_v1 / score 0.3536

### 6. HK620 哪些信息仍未确认？

Answer: HK620 目前仍未确认的信息包括完整技术参数、性能指标、价格、交期、保修、售后、材料兼容范围、工件尺寸、维护要求和操作人员要求。暂无已确认资料时，不应对外承诺。

Source Chunks:

1. Troubleshooting / hk620_troubleshooting_v1 / score 0.5653
2. FAQ / hk620_faq_v1 / score 0.2717
3. Advantages / hk620_advantages_v1 / score 0.2319

### 7. HK620 的主要应用是什么？

Answer: HK620 是一台用于 skeleton door strips 的特殊封边设备。当前已确认资料显示，它把封边、开槽和切割组合在一个流程中。

Source Chunks:

1. Applications / hk620_applications_v1 / score 0.7042
2. Overview / hk620_overview_v1 / score 0.5989
3. FAQ / hk620_faq_v1 / score 0.5922

### 8. HK620 的优势是什么？

Answer: HK620 的已确认优势是把多个工序合并到一个流程中，减少封边、开槽和切割分开处理的割裂，并针对 skeleton door strip production 提供聚焦方案。效率、ROI、节省人工等量化优势暂无已确认资料。

Source Chunks:

1. Advantages / hk620_advantages_v1 / score 0.5398
2. Sales / hk620_sales_v1 / score 0.3705
3. FAQ / hk620_faq_v1 / score 0.3671

### 9. HK620 可以怎么做销售介绍？

Answer: 可作为 review-pending 的销售表述：HK620 适用于 skeleton door strip processing，并把封边、开槽、切割放在同一流程中。不得在没有来源时承诺速度、产量、ROI、价格、交期或材料兼容性。

Source Chunks:

1. Sales / hk620_sales_v1 / score 0.5206
2. Troubleshooting / hk620_troubleshooting_v1 / score 0.4638
3. FAQ / hk620_faq_v1 / score 0.2467

### 10. HK620 的价格、交期和保修信息有确认吗？

Answer: HK620 目前仍未确认的信息包括完整技术参数、性能指标、价格、交期、保修、售后、材料兼容范围、工件尺寸、维护要求和操作人员要求。暂无已确认资料时，不应对外承诺。

Source Chunks:

1. Troubleshooting / hk620_troubleshooting_v1 / score 0.5116
2. FAQ / hk620_faq_v1 / score 0.2197
3. Sales / hk620_sales_v1 / score 0.1919

## Final Result

P4-B PASS for local Product Knowledge retrieval MVP.

HK620 is now retrievable, answerable, and citeable through Product Knowledge Center chunks. Public-facing use is still blocked until human review and real source documents are added.
