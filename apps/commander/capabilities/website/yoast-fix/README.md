# M8A Yoast SEO Meta — Fix Instructions

## 问题

WordPress REST API 拒绝写入以 `_` 开头的 meta key（被视为受保护元数据），因此 `_yoast_wpseo_title` 和 `_yoast_wpseo_metadesc` 通过 REST API 设置后会被静默丢弃。

## 解决方案

安装 `m8a-yoast-meta-rest` 插件，它做两件事：
1. 将 `_yoast_wpseo_*` 注册为 REST-accessible meta
2. 提供专用 REST 端点 `POST /wp-json/m8a/v1/yoast-meta`

## 安装步骤（选一种）

### 方式 A：WordPress 管理后台上传（推荐）

1. 登录 https://woodmachinerynetwork.com/wp-admin/
2. 插件 → 安装插件 → 上传插件
3. 选择 `m8a-yoast-meta-rest.zip`
4. 安装并启用

### 方式 B：手动部署（需 SFTP/SSH）

```bash
scp m8a-yoast-meta-rest.php admin@47.236.185.172:/var/www/html/wp-content/plugins/m8a-yoast-meta-rest/
# 然后在 WordPress 后台启用插件
```

## 安装后验证

```bash
cd /path/to/M8A
python3 apps/commander/capabilities/website/yoast-fix/fix_yoast_meta.py --check --post-id 481
```

预期输出：
```json
{
  "post_id": 481,
  "yoast_title_from_meta": "HK620 Skeleton Door Profile Edge Banding Machine | Stable Production for Door & Furniture Profiles",
  "yoast_is_set": true
}
```

## 修复已发布文章

```bash
python3 apps/commander/capabilities/website/yoast-fix/fix_yoast_meta.py \
  --article-json apps/commander/content_center_v1/outputs/hk620_us_customer_article_seo_v4.json
```

## 自动修复

`wordpress_draft.py` 已在创建草稿后自动调用 M8A Yoast 端点。插件安装后，所有新草稿的 Yoast SEO meta 将自动写入。
