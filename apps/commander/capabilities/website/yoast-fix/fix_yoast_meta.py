#!/usr/bin/env python3
"""Fix Yoast SEO meta persistence for WordPress posts.

Problem:
  Yoast SEO meta (_yoast_wpseo_title, _yoast_wpseo_metadesc) does NOT persist
  when set via the WordPress REST API meta field, because WordPress treats
  underscore-prefixed meta keys as protected by default.

Solution:
  This script uses the M8A custom REST endpoint (wp-json/m8a/v1/yoast-meta)
  to set Yoast SEO meta after draft creation or after publish.

Prerequisites:
  The m8a-yoast-meta-rest.php plugin must be installed on the WordPress server.
  Upload it via WordPress Admin → Plugins → Add New → Upload Plugin,
  or place it in wp-content/mu-plugins/ (requires SSH/SFTP).

Usage:
  python fix_yoast_meta.py --post-id 481 --meta-title "My SEO Title" --meta-desc "My SEO Description"
  python fix_yoast_meta.py --post-id 481 --article-json path/to/seo_v4.json
  python fix_yoast_meta.py --check --post-id 481
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin


def load_env() -> tuple[str, str, str, list[str]]:
    """Load WordPress credentials from environment or .env file."""
    base_url = os.environ.get("M8A_WORDPRESS_BASE_URL", "").strip()
    username = os.environ.get("M8A_WORDPRESS_USERNAME", "").strip()
    app_password = os.environ.get("M8A_WORDPRESS_APP_PASSWORD", "").strip()

    if not all([base_url, username, app_password]):
        # Try loading from .env, matching wordpress_draft.py approach
        script_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(script_dir, "..", "..", "..", "..", "..", ".env"),  # .../M8A/.env
            os.path.join(script_dir, "..", "..", "..", "..", ".env"),         # .../website/.env
            os.path.join(script_dir, "..", "..", "..", ".env"),               # .../capabilities/.env
        ]
        for env_path in candidates:
            abs_path = os.path.abspath(env_path)
            if os.path.isfile(abs_path):
                with open(abs_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, _, v = line.partition("=")
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k.startswith("M8A_WORDPRESS_") and k not in os.environ:
                            os.environ[k] = v
                break
        base_url = os.environ.get("M8A_WORDPRESS_BASE_URL", "").strip()
        username = os.environ.get("M8A_WORDPRESS_USERNAME", "").strip()
        app_password = os.environ.get("M8A_WORDPRESS_APP_PASSWORD", "").strip()

    missing = [n for n, v in [("BASE_URL", base_url), ("USERNAME", username), ("APP_PASSWORD", app_password)] if not v]
    return base_url, username, app_password, missing


def make_auth(username: str, app_password: str) -> str:
    return base64.b64encode(f"{username}:{app_password}".encode()).decode()


def check_yoast_meta(base_url: str, username: str, app_password: str, post_id: int) -> dict:
    """Check current Yoast SEO meta values for a post."""
    auth = make_auth(username, app_password)

    # Check via standard REST API first
    endpoint = urljoin(base_url.rstrip("/") + "/", f"wp-json/wp/v2/posts/{post_id}")
    req = urllib.request.Request(
        endpoint,
        headers={
            "Authorization": f"Basic {auth}",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        post = json.loads(resp.read().decode())

    meta = post.get("meta", {})

    # Also try the Yoast REST API endpoint if available
    yoast_data = {}
    try:
        yoast_endpoint = urljoin(base_url.rstrip("/") + "/", f"wp-json/yoast/v1/get_head?post_id={post_id}")
        yoast_req = urllib.request.Request(
            yoast_endpoint,
            headers={
                "Authorization": f"Basic {auth}",
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            },
        )
        with urllib.request.urlopen(yoast_req, timeout=30) as yoast_resp:
            yoast_data = json.loads(yoast_resp.read().decode())
    except Exception:
        pass

    return {
        "post_id": post_id,
        "post_title": post.get("title", {}).get("rendered", ""),
        "post_status": post.get("status"),
        "yoast_title_from_meta": meta.get("_yoast_wpseo_title", ""),
        "yoast_desc_from_meta": meta.get("_yoast_wpseo_metadesc", ""),
        "yoast_is_set": bool(meta.get("_yoast_wpseo_title") or meta.get("_yoast_wpseo_metadesc")),
        "yoast_api_data": yoast_data,
    }


def set_yoast_meta(base_url: str, username: str, app_password: str, post_id: int,
                   meta_title: str | None = None, meta_description: str | None = None,
                   focus_keyword: str | None = None) -> dict:
    """Set Yoast SEO meta for a post via M8A custom REST endpoint."""
    auth = make_auth(username, app_password)

    payload = {"post_id": post_id}
    if meta_title:
        payload["meta_title"] = meta_title
    if meta_description:
        payload["meta_description"] = meta_description
    if focus_keyword:
        payload["focus_keyword"] = focus_keyword

    endpoint = urljoin(base_url.rstrip("/") + "/", "wp-json/m8a/v1/yoast-meta")
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": f"{base_url.rstrip('/')}/wp-admin/",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            result["_status"] = "success"
            return result
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")[:500]
        return {
            "_status": "failed",
            "error": f"HTTP {exc.code}: {detail}",
            "note": "The m8a-yoast-meta-rest.php plugin may not be installed. Upload it via WordPress Admin → Plugins → Add New.",
        }


def fix_from_article_json(base_url: str, username: str, app_password: str, article_json_path: str) -> dict:
    """Fix Yoast SEO meta using an article SEO JSON file (e.g., hk620_us_customer_article_seo_v4.json)."""
    with open(article_json_path) as f:
        article = json.load(f)

    post_id = article.get("wp_post_id")
    if not post_id:
        return {"_status": "failed", "error": "No wp_post_id found in article JSON"}

    return set_yoast_meta(
        base_url=base_url,
        username=username,
        app_password=app_password,
        post_id=post_id,
        meta_title=article.get("meta_title"),
        meta_description=article.get("meta_description"),
        focus_keyword=article.get("focus_keywords", [None])[0] if article.get("focus_keywords") else None,
    )


def main():
    parser = argparse.ArgumentParser(description="Fix Yoast SEO meta for WordPress posts")
    parser.add_argument("--post-id", type=int, help="WordPress post ID")
    parser.add_argument("--meta-title", type=str, help="SEO meta title")
    parser.add_argument("--meta-desc", type=str, help="SEO meta description")
    parser.add_argument("--focus-kw", type=str, help="Focus keyword")
    parser.add_argument("--article-json", type=str, help="Path to article SEO JSON file")
    parser.add_argument("--check", action="store_true", help="Check current Yoast meta (read-only)")
    args = parser.parse_args()

    base_url, username, app_password, missing = load_env()
    if missing:
        print(json.dumps({"_status": "failed", "error": f"Missing env: {missing}"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    if args.check and args.post_id:
        result = check_yoast_meta(base_url, username, app_password, args.post_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["yoast_is_set"] else 1)

    if args.article_json:
        result = fix_from_article_json(base_url, username, app_password, args.article_json)
    elif args.post_id and (args.meta_title or args.meta_desc):
        result = set_yoast_meta(base_url, username, app_password, args.post_id,
                                args.meta_title, args.meta_desc, args.focus_kw)
    else:
        print(json.dumps({"_status": "failed", "error": "Provide --post-id with --meta-title/--meta-desc, or --article-json, or --check"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get("_status") == "success" else 1)


if __name__ == "__main__":
    main()
