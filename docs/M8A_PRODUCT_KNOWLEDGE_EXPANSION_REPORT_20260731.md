# M8A 产品知识库拓展报告 — 2026-07-31

## 执行概要

在 M8A 项目中建立了 HK680 正式知识库，以及 HK690、HK568、HK612A 三个产品的骨架文件。所有数据严格区分"已验证公开来源"和"[待CEO确认]"，未借用 HK620 或竞品参数填补空白。

## 一、产品盘点结果

| 产品 | 知识库状态 | 数据来源 | 公开审批 |
|------|-----------|---------|---------|
| HK620 | 完整（V1+V2 binding） | 内部资料 + CEO 审批 | public_approved (Post 481) |
| **HK680** | **正式知识库 V1** | **SYUTECH 官网验证** | **not_public_approved** |
| HK568 | 骨架（含公开参数） | SYUTECH 官网 | not_started |
| HK690 | 骨架（仅内部引用） | 创始人访谈提及 | not_started |
| HK612A | 骨架（仅规划提及） | 无 | not_started |

## 二、HK680 知识库详情

### 数据来源
- **官方英文页**: https://www.syutech.com/hk680-servo-edge-banding-machine-product/
- **官方中文页**: http://zh.syutech.com/hk680-servo-edge-banding-machine-product
- **展会证据**: 2024 年广州 CFF 展会展出（3月28-31日）

### 已验证规格（来自官方页面）

| 参数 | 值 | 状态 |
|------|-----|------|
| 型号 | HK680 | verified_public_source |
| 面板长度（最小） | 150 mm（边角修剪 45x300 mm） | verified_public_source |
| 面板宽度（最小） | 50 mm | verified_public_source |
| 封边带宽度 | 10-60 mm | verified_public_source |
| 封边厚度 | 0.4-3 mm | verified_public_source |
| 进给速度 | 16 / 18 / 22 m/min（三档） | verified_public_source |
| 总装机功率 | 17.56 kW | verified_public_source |
| 气压 | 0.7-0.9 MPa | verified_public_source |
| 整机尺寸 | 6700 x 710 x 1628 mm | verified_public_source |
| 机器重量 | 2500 kg | verified_public_source |

### 待 CEO 确认字段

| 参数 | 状态 | 说明 |
|------|------|------|
| 电压 | [待CEO确认] | 官网未标注，HK568 页面标注 380V/50Hz，但不假设相同 |
| 胶水类型 | [待CEO确认] | 官网写"一种胶水"，未指明 PUR/EVA |
| 保修政策 | [待CEO确认] | 无公开信息 |
| 适用板材 | [待CEO确认] | 基于品类推断但官网未明确列出 |

### 核心特征
1. **伺服控制**: 精修、圆角、刮边均为伺服驱动
2. **工艺流程**: 喷涂 → 铣削 → 涂胶 → 端部修整 → 伺服精修 → 伺服圆角 → 伺服刮边 → 平刮 → 清洁 → 抛光
3. **控制系统**: 汇川 PLC + 变频器 + 控制系统
4. **独立储气系统**: 独立储气罐确保气压稳定
5. **电脑触摸屏**: 互联网远程控制、预热、记忆功能、实时产能统计

### 与 HK620 的关键区别

| 方面 | HK620 | HK680 |
|------|-------|-------|
| 类型 | 骨骼门线条封边机 | 伺服板式封边机 |
| 工艺 | 封边→开槽→切断（线条导向） | 喷涂→铣削→涂胶→修整→刮边→抛光（板材导向） |
| 工件 | 线条、装饰条、门套 | 平面板材（MDF、刨花板等） |
| 伺服 | [待CEO确认] | 是（伺服精修、圆角、刮边） |

## 三、生成的文件清单

### HK680 知识库（3 个文件）
1. `knowledge/products/HK680/INDEX.md` — 产品知识索引
2. `knowledge/products/HK680/02_Technical_Specifications/hk680_technical_specifications_v1.md` — 技术规格表
3. `knowledge/products/HK680/bindings/website_agent_hk680.knowledge_binding.v1.json` — 知识绑定 V1

### HK680 系统文件（2 个文件）
4. `apps/commander/employees/website_agent_v1/knowledge_binding/hk680.knowledge_binding.v1.json` — Website Agent 绑定副本
5. `apps/commander/knowledge_center_v1/product_catalog/hk680.json` — 产品目录条目

### 骨架产品（3 个文件）
6. `knowledge/products/HK568/INDEX.md` — HK568 骨架（含 SYUTECH 官网公开参数）
7. `knowledge/products/HK690/INDEX.md` — HK690 骨架（仅内部引用）
8. `knowledge/products/HK612A/INDEX.md` — HK612A 骨架（仅规划提及）

**总计: 8 个新文件**

## 四、JSON 校验结果

### Schema 合规性
- **必需字段**: PASS（18/18）
- **额外属性**: PASS（0 个额外字段，完全符合 V1 schema）
- **字段类型**: PASS（18 个字段类型全部正确）
- **buyer_persona**: PASS（4 个字符串项）

### 与 HK620 V2 的对比
HK620 V2 binding 包含 6 个 V1 schema 之外的额外字段（`binding_id`, `upgrade_from`, `upgrade_date`, `upgrade_reason`, `content_standard_reference`, `customer_cases`），这些字段在 `additionalProperties: false` 下不合规。HK680 V1 binding 严格遵循 V1 schema，无此问题。

## 五、安全声明

- ❌ 未调用 n8n
- ❌ 未调用 WordPress
- ❌ 未发布任何内容
- ❌ 未上传 YouTube
- ❌ 未发送 Gmail
- ❌ 未修改任何外部平台
- ✅ 仅在本地 M8A 项目创建知识库文件

## 六、下一步建议

1. **CEO 审批**: HK680 知识库需 CEO 审核后方可用于公开内容
2. **补全待确认字段**: 电压、胶水类型、保修政策等需向工程部门确认
3. **素材收集**: 产品图片、演示视频、客户案例、销售 FAQ
4. **HK690 优先级**: CEO 需确认 HK690 是否为真实产品，以及"2cm 窄料"信息是否可进入公开资料
5. **HK568 扩展**: 如 CEO 确认优先级，可基于 SYUTECH 官网数据快速建立完整知识库
