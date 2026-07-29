# M8A GA4 与 Google Search Console 接入报告 V1

生成时间：2026-07-07T14:02:31Z

## 一、结论

GA4 与 Google Search Console 已完成 n8n OAuth 接入。

本次操作没有保存任何明文密钥到报告或登记表。

## 二、已完成事项

1. Google Cloud OAuth 测试用户已添加：shiqiujin3@gmail.com。
2. n8n 已保存 Google Analytics 凭证：Google Analytics account。
3. Google Analytics OAuth 授权成功，页面显示 Connection successful。
4. n8n 已保存 Google Search Console 凭证：M8A Google Search Console。
5. Google Search Console OAuth 授权成功，页面显示 Connection successful。
6. M8A Credential Registry 已更新 GA4 与 GSC 状态。

## 三、n8n 凭证状态

| 平台 | n8n 凭证 | 类型 | 状态 |
|---|---|---|---|
| GA4 / Google Analytics | Google Analytics account | googleAnalyticsOAuth2 | 已授权 |
| Google Search Console | M8A Google Search Console | googleOAuth2Api | 已授权 |

## 四、权限边界

GA4：允许读取 Google Analytics 数据。禁止修改属性设置、删除数据或保存密钥。

Google Search Console：使用只读权限 `webmasters.readonly`。允许读取站点与搜索表现数据。禁止修改站点所有权、设置或权限。

## 五、风险说明

今天操作过程中，Google OAuth Client Secret 曾被误粘贴到对话中。当前未写入任何本地报告或登记表。

建议在今天主流程跑完后，重新生成 Google OAuth Client Secret，并替换 n8n 中相关 Google 凭证，完成一次安全轮换。

## 六、下一步

1. 创建 GA4 只读验收 Workflow，确认能读取账号或属性数据。
2. 创建 GSC 只读验收 Workflow，确认能读取站点列表或搜索表现数据。
3. 将 GA4/GSC 数据读取能力接入 M8A 数据中心与 Website/SEO Agent 的报告流程。
