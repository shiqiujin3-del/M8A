# M8A GSC / GA4 接入授权计划 V1

状态：已下达，准备执行。

## 分工

当前 Codex 负责：Google Search Console 与 GA4。

流程 Codex 负责：Gmail 与 YouTube。

## GSC 目标

读取网站收录、索引状态、搜索表现、关键词和页面表现。

允许只读读取，不允许修改站点所有权、删除站点或修改 GSC 设置。

## GA4 目标

读取网站访问量、来源、页面表现和转化基础数据。

允许只读读取，不允许修改 GA4 Property 设置、删除数据流或修改转化设置。

## 执行原则

所有授权通过 n8n Credential 完成。

不在报告中保存明文密码、token、Application Password、OAuth Client Secret。

## 当前阻塞预判

如果 Google OAuth Client ID / Secret 未配置，或 Google Cloud OAuth App 未加入 n8n 的 redirect URL，会出现 invalid_client 或 redirect_uri 错误。

遇到该问题时，只输出根因和需要 CEO 在 Google Cloud / n8n 中处理的字段，不盲目重试。
