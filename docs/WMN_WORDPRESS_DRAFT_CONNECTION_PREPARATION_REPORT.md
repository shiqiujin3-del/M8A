# M8A WMN WordPress Draft Connection Preparation Report

Date: 2026-07-06

## 1. WMN 接入对象确认

Confirmed:

```text
M8A_WORDPRESS_BASE_URL=https://woodmachinerynetwork.com
```

本次只确认 WMN 海外站，不接国内站，不接 saizontech.com。

## 2. REST API 只读检查

Checked endpoint:

```text
GET https://woodmachinerynetwork.com/wp-json/
```

Result:

```text
HTTP/2 200
content-type: application/json; charset=UTF-8
allow: GET
link: <https://woodmachinerynetwork.com/wp-json/>; rel="https://api.w.org/"
```

Conclusion:

```text
WMN WordPress REST API /wp-json/ is accessible.
```

Only `GET` was executed. No `POST`, `PUT`, `PATCH`, or `DELETE` request was executed.

## 3. Local .env

Created:

```text
/Users/shiqiujing/Documents/M8A/.env
```

Current content:

```text
M8A_WORDPRESS_BASE_URL=https://woodmachinerynetwork.com
M8A_WORDPRESS_USERNAME=
M8A_WORDPRESS_APP_PASSWORD=
```

No real username or password was written because they were not provided in this session.

## 4. Config Check

Command:

```text
source /Users/shiqiujing/Documents/M8A/.env
python3 /Users/shiqiujing/Documents/M8A/apps/commander/capabilities/website/check_wordpress_config.py
```

Output:

```text
BASE_URL configured
USERNAME missing
APP_PASSWORD missing
not_ready
```

Conclusion:

```text
WordPress configuration is not ready yet.
```

## 5. Application Password

Status:

```text
Not created by Codex.
```

Reason:

No WMN WordPress backend login/session or WordPress account permission was available in this environment.

Required Application Password name:

```text
M8A WMN Draft Writer
```

Recommended account:

```text
Dedicated WMN test account or permission-controlled account.
```

If an administrator account is used temporarily, mark it as:

```text
Temporary use only. Not a long-term solution.
```

## 6. Safety Confirmation

Confirmed:

- No WordPress draft was created.
- No WordPress post was published.
- No existing WordPress page/post was modified.
- No WordPress content was deleted.
- No WordPress password was printed.
- No WordPress password was written to code.
- No WordPress password was written to this report.
- No n8n connection was made.
- No social platform connection was made.
- Commander Console CEO Home was not changed.

## 7. Next Step

Next step is manual:

1. Log in to WMN WordPress backend.
2. Use a dedicated test or permission-controlled user.
3. Create Application Password named:

```text
M8A WMN Draft Writer
```

4. Fill:

```text
M8A_WORDPRESS_USERNAME=
M8A_WORDPRESS_APP_PASSWORD=
```

5. Re-run:

```text
python3 /Users/shiqiujing/Documents/M8A/apps/commander/capabilities/website/check_wordpress_config.py
```

Expected ready output:

```text
BASE_URL configured
USERNAME configured
APP_PASSWORD configured
ready
```

## 8. Can Proceed To Real Draft Verification?

NO

Reason:

The WMN REST API is reachable, but username and Application Password are still missing.

