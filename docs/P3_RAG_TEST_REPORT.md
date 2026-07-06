# P3 RAG Test Report

时间：2026-07-06

目标：验证 M8A 是否具备最基础的 RAG 检索链路：文本 -> 向量 -> Qdrant 写入 -> 相似度搜索 -> 返回结果。

## 1. Credential 状态

| Credential | 状态 | 说明 |
|---|---|---|
| `M8A Local Postgres` | PASS | P2 已建立，可用 |
| `M8A Local Redis` | PASS | P2 已建立，可用 |
| `M8A Local Qdrant` | PASS | P3 已建立，指向 `http://qdrant:6333` |
| `M8A OpenAI Reserved` | RESERVED | 已预留，但当前未配置真实 OpenAI API Key |
| `M8A WordPress Reserved` | RESERVED | 已预留，不连接真实网站 |

安全说明：

- 未接入真实业务。
- 未接入网站。
- 未接入公众号。
- 未接入社媒。
- 未输出任何密钥内容。

## 2. Qdrant Collection

Collection：

```text
m8a_p3_rag_test
```

配置：

```text
vector size = 8
distance = Cosine
status = green
```

说明：

- 当前 collection 用于 P3 本地 smoke test。
- 真实 OpenAI embedding 接入后，需要按实际 embedding 维度创建新的 production/test collection。

## 3. Workflow

Workflow：

```text
M8A_P3_RAG_TEST_WORKFLOW
```

结构：

1. `Manual Trigger`
2. `Set Test Text`
3. `Generate Test Embedding`
4. `Qdrant Upsert Vector`
5. `Qdrant Similarity Search`
6. `Return Search Results`

测试文本：

```text
M8A validates a minimal local RAG pipeline with Qdrant vector search.
```

Embedding：

```text
local_deterministic_test_embedding_v1
```

说明：

- 当前未发现 `OPENAI_API_KEY`，因此本次未调用真实 OpenAI Embedding API。
- 本次使用本地确定性测试 embedding，用于证明 RAG 数据链路和 Qdrant 检索能力。
- OpenAI credential 已预留，待配置真实 key 后可替换 embedding 节点。

## 4. Qdrant 写入验证

PASS

写入点：

```text
id = 3001
collection = m8a_p3_rag_test
project = M8A
phase = P3
embedding_model = local_deterministic_test_embedding_v1
```

Qdrant collection 状态：

```text
status = green
points_count = 2
```

备注：

- `id = 3001` 是 P3 workflow 写入的测试点。
- `id = 9001` 是本次验证 Qdrant endpoint 格式时创建的 smoke test 点。

## 5. 相似度搜索验证

PASS

搜索返回 top result：

```text
id = 3001
score = 0.9784038
project = M8A
phase = P3
text = M8A validates a minimal local RAG pipeline with Qdrant vector search.
```

结论：

- Qdrant 能接收向量。
- Qdrant 能保存 payload。
- Qdrant 能执行相似度搜索。
- n8n 能把文本、向量、写入和检索串成一个最小闭环。

## 6. n8n 执行日志

PASS

最新执行：

```text
execution id = 4
status = success
mode = manual
workflowId = M8A_P3_RAG_TEST_WORKFLOW
startedAt = 2026-07-06 01:39:03.127+00
stoppedAt = 2026-07-06 01:39:03.187+00
```

## 7. 最终结论

| 项目 | 结果 |
|---|---|
| 统一 Credential | PASS / RESERVED |
| Qdrant Collection | PASS |
| 测试 Workflow 创建 | PASS |
| 文本输入 | PASS |
| 测试 Embedding 生成 | PASS |
| Qdrant 写入 | PASS |
| Qdrant 相似度搜索 | PASS |
| n8n 执行日志 | PASS |
| OpenAI 真实 Embedding | RESERVED |

M8A 已具备最基础的 RAG 检索增强链路能力。

下一步进入真实 AI 前，需要先配置真实 OpenAI API Key，然后将 `Generate Test Embedding` 替换为真实 OpenAI Embedding 节点。
