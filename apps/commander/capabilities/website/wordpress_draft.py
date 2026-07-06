#!/usr/bin/env python3
"""WordPress Draft Only capability for M8A Website Operator.

This module is intentionally narrow:
- create post drafts only
- never publish
- never delete
- never update existing published content
"""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from urllib.parse import urljoin


TITLE = "HK620 Skeleton Door Strip Processing for the USA Market"
SLUG = "hk620-skeleton-door-strip-processing-usa"
META_TITLE = "HK620 Skeleton Door Strip Processing | Saiyu"
META_DESCRIPTION = "HK620 skeleton door strip processing solution for factories targeting efficient grooved profile and edge banding preparation."


@dataclass
class WebsiteCapabilityResult:
    artifact_type: str
    title: str
    content_json: dict
    simulation_status: str
    event_type: str
    event_message: str


def build_wordpress_draft_payload() -> dict:
    content = """<!-- wp:heading -->
<h2>Draft Review Required</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Draft Review Required:</strong> This article is prepared by M8A for internal review. It must be checked by Saiyu before any public use. No automatic publishing is allowed.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>HK620 and the Need for a Better Skeleton Door Strip Process</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>HK620 is positioned for factories that need a more organized way to prepare skeleton door strips for modern door and furniture applications. In many factories, skeleton door strip processing can involve several separate steps, including edge banding, grooving, trimming, and cutting. When these steps are handled manually or across disconnected equipment, the process can become slower, less consistent, and harder to control during repeated production.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>For the USA market, buyers often care about repeatability, clear process logic, labor efficiency, and whether a machine can help a factory prepare grooved profiles more consistently. This draft explains the process value of HK620 without making unverified public claims. Any technical parameter, customer case, or market statement must be confirmed before publication.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Factory Pain Points</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Door factories and custom furniture producers may face pressure from changing interior styles, more demanding profile designs, and the need to produce decorative strip components with stable quality. If short strips are cut first and then processed later, edge banding can become difficult because the workpiece may not have enough stable length for ordinary feeding and pressing. Manual work can also increase dependence on experienced operators, which makes production harder to standardize.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Another common pain point is process fragmentation. A factory may use one method for edge banding, another method for grooving, and another method for cutting. Each transfer creates room for alignment errors, inconsistent surface quality, and extra handling time. When demand grows, these small inefficiencies can become a bottleneck for stable output.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>HK620 Solution Direction</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>HK620 is designed around a process direction that combines edge banding, grooving, and cutting preparation in a more integrated line. The key logic is to complete edge banding before grooving and final cutting, so the material is still long enough to move through the machine in a controlled way. This helps the factory reduce manual handling and prepare strip components with a clearer sequence.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>The approved internal knowledge for HK620 describes a process including edge banding-related operations, grooving, and cutting-related preparation. Some workstation names, adjustment ranges, servo upgrade plans, and customer evidence remain review-sensitive. Those details should only be published after Saiyu confirms which statements are suitable for public use.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Application Scenarios</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>HK620 is relevant for door factories, furniture manufacturers, and production teams exploring skeleton door strip processing. It may be especially useful where a company wants to reduce manual strip preparation, improve process consistency, or create a repeatable workflow for grooved profile components. The machine should be positioned carefully: it is not a universal claim for every factory, and real suitability depends on material, strip dimensions, product design, and production expectations.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>What Buyers Should Confirm</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Before purchasing or promoting HK620 for a specific market, buyers should confirm workpiece size, edge banding material, groove style, output expectations, operator workflow, and after-sales support requirements. Saiyu should also confirm which technical specifications can be made public and which details should remain internal until further evidence is available.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2>Call To Action</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>If your factory is studying skeleton door strip production for the USA market, HK620 can be reviewed as a possible process solution. Contact Saiyu to discuss your material, strip design, current production method, and review requirements. This draft should remain in WordPress draft status until a human reviewer confirms the final public version.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>This article draft intentionally avoids unverified absolute claims. It does not claim that HK620 is unique, first, or suitable for every buyer. The final version should be checked against approved product knowledge, sales policy, after-sales notes, and public communication rules before it is used on any website.</p>
<!-- /wp:paragraph -->"""
    return {
        "title": TITLE,
        "slug": SLUG,
        "status": "draft",
        "meta_title": META_TITLE,
        "meta_description": META_DESCRIPTION,
        "content": content,
        "content_preview": "Draft Review Required: HK620 article draft for USA skeleton door strip processing. Human review is required before public use.",
    }


def validate_draft_payload(payload: dict) -> None:
    status = payload.get("status")
    if status != "draft":
        raise ValueError("WordPress safety check failed: only status=draft is allowed.")
    serialized = json.dumps(payload, ensure_ascii=False).lower()
    blocked = ["\"status\": \"publish\"", "\"status\":\"publish\"", "/delete", "force=true"]
    if any(token in serialized for token in blocked):
        raise ValueError("WordPress safety check failed: publish/delete operations are not allowed.")
    word_count = len(payload.get("content", "").split())
    if word_count < 600:
        raise ValueError("WordPress draft content must contain at least 600 words.")


def wordpress_env():
    base_url = os.environ.get("M8A_WORDPRESS_BASE_URL", "").strip()
    username = os.environ.get("M8A_WORDPRESS_USERNAME", "").strip()
    app_password = os.environ.get("M8A_WORDPRESS_APP_PASSWORD", "").strip()
    missing = [
        name for name, value in [
            ("M8A_WORDPRESS_BASE_URL", base_url),
            ("M8A_WORDPRESS_USERNAME", username),
            ("M8A_WORDPRESS_APP_PASSWORD", app_password),
        ] if not value
    ]
    return base_url, username, app_password, missing


def local_payload_result(payload: dict, missing: list[str]) -> WebsiteCapabilityResult:
    content_json = {
        "business_output": "WordPress Draft Payload",
        "platform": "wordpress",
        "configured": False,
        "configuration_status": "waiting_config",
        "missing_env": missing,
        "publish": False,
        **{key: payload[key] for key in ["title", "slug", "status", "meta_title", "meta_description", "content_preview"]},
        "content_word_count": len(payload["content"].split()),
        "message": "WordPress 未配置，当前仅生成本地 Draft Payload。",
    }
    return WebsiteCapabilityResult(
        artifact_type="draft_payload",
        title="WordPress Draft Payload - Waiting Config",
        content_json=content_json,
        simulation_status="waiting_config",
        event_type="wordpress_config_missing",
        event_message="WordPress environment variables are missing. Local draft payload was saved; no WordPress connection was attempted.",
    )


def create_wordpress_post_draft(base_url: str, username: str, app_password: str, payload: dict) -> dict:
    endpoint = urljoin(base_url.rstrip("/") + "/", "wp-json/wp/v2/posts")
    auth = base64.b64encode(f"{username}:{app_password}".encode("utf-8")).decode("ascii")
    body = {
        "title": payload["title"],
        "slug": payload["slug"],
        "status": "draft",
        "content": payload["content"],
        "excerpt": payload["meta_description"],
        "meta": {
            "m8a_meta_title": payload["meta_title"],
            "m8a_meta_description": payload["meta_description"],
        },
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def create_wordpress_draft() -> WebsiteCapabilityResult:
    payload = build_wordpress_draft_payload()
    validate_draft_payload(payload)
    base_url, username, app_password, missing = wordpress_env()
    if missing:
        return local_payload_result(payload, missing)

    try:
        wp_response = create_wordpress_post_draft(base_url, username, app_password, payload)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")[:500]
        raise RuntimeError(f"WordPress draft creation failed with HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"WordPress draft creation failed: {exc.reason}") from exc

    wp_status = wp_response.get("status")
    if wp_status != "draft":
        raise RuntimeError("WordPress safety check failed after creation: returned post is not draft.")

    content_json = {
        "business_output": "WordPress Draft",
        "platform": "wordpress",
        "configured": True,
        "wp_post_id": wp_response.get("id"),
        "wp_status": wp_status,
        "wp_edit_url": wp_response.get("edit_link"),
        "wp_link": wp_response.get("link"),
        **{key: payload[key] for key in ["title", "slug", "meta_title", "meta_description", "content_preview"]},
        "publish": False,
        "message": "WordPress draft created. It remains draft and requires CEO review.",
    }
    return WebsiteCapabilityResult(
        artifact_type="wordpress_draft",
        title="WordPress Draft",
        content_json=content_json,
        simulation_status="draft_created",
        event_type="wordpress_draft_created",
        event_message="WordPress draft was created with status=draft. No publish action executed.",
    )

