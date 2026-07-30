#!/usr/bin/env python3
"""CEO Approval Gate: Draft → Publish

Reads the latest bridge result, shows the draft for CEO review,
and handles the approval-to-publish flow.

Usage:
  python3 ceo_approval_gate.py                    # Show pending drafts for approval
  python3 ceo_approval_gate.py --approve <id>     # Approve and publish a specific draft
  python3 ceo_approval_gate.py --reject <id>      # Reject a draft
  python3 ceo_approval_gate.py --log              # Show approval history

Safety:
  - All publish actions are logged to audit trail
  - Only the latest bridge result is actionable
  - Drafts can only be published via explicit CEO approval
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(os.getenv("M8A_ROOT", str(Path(__file__).resolve().parents[3]))).resolve()
PUBLISHING_DIR = ROOT / "apps" / "commander" / "publishing_center_v1"
BRIDGE_RESULT_PATH = PUBLISHING_DIR / "last_bridge_result.v1.json"
APPROVAL_LOG_PATH = PUBLISHING_DIR / "ceo_approval_log.v1.json"
PUBLISH_WEBHOOK = os.getenv(
    "M8A_WORDPRESS_PUBLISH_WEBHOOK",
    "http://localhost:5678/webhook/m8a-hk620-publish-approved-v2"
)

# WordPress REST API direct publish (fallback when n8n webhook is broken)
WP_API_URL = os.getenv("M8A_WORDPRESS_BASE_URL", "https://woodmachinerynetwork.com")
WP_USERNAME = os.getenv("M8A_WORDPRESS_USERNAME", "admin")
WP_APP_PASSWORD = os.getenv("M8A_WORDPRESS_APP_PASSWORD", "FxZXNePNLAoCfy61YeT4Ohny")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_approval_log() -> dict[str, Any]:
    if not APPROVAL_LOG_PATH.exists():
        return {"version": "ceo_approval_v1", "log": []}
    return read_json(APPROVAL_LOG_PATH)


def save_approval_log(log: dict[str, Any]) -> None:
    log["updated_at"] = now_iso()
    write_json(APPROVAL_LOG_PATH, log)


def call_publish_webhook(post_id: int, title: str) -> tuple[bool, dict[str, Any], str | None]:
    """Call the n8n publish webhook to change draft to publish."""
    payload = {
        "action": "publish_approved_post",
        "post_id": post_id,
        "title": title,
        "approved_by": "CEO",
        "approved_at": now_iso(),
        "source": "ceo_approval_gate_v1",
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        PUBLISH_WEBHOOK,
        data=body,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "application/json",
            "Cache-Control": "no-cache",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            raw = response.read().decode("utf-8")
            return True, json.loads(raw or "{}"), None
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"raw": raw}
        return False, parsed, str(exc)
    except Exception as exc:
        return False, {}, str(exc)


def publish_via_wp_api(post_id: int, title: str) -> tuple[bool, str | None, str | None]:
    """Publish a draft directly via WordPress REST API (bypasses broken n8n webhook)."""
    auth = base64.b64encode(f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()).decode()
    data = json.dumps({"status": "publish"}).encode("utf-8")
    req = urllib.request.Request(
        f"{WP_API_URL}/wp-json/wp/v2/posts/{post_id}",
        data=data,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) M8A-Publisher/2.0",
            "Accept": "application/json",
            "Origin": WP_API_URL,
            "Referer": f"{WP_API_URL}/wp-admin/",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            public_url = result.get("link", "")
            return True, public_url, None
    except urllib.error.HTTPError as e:
        return False, None, f"HTTP {e.code}: {e.read().decode()[:200]}"
    except Exception as e:
        return False, None, str(e)


def show_pending() -> None:
    """Display the latest bridge result for CEO review."""
    if not BRIDGE_RESULT_PATH.exists():
        print("No pending drafts. Run pipeline_bridge.py --execute first.")
        return

    result = read_json(BRIDGE_RESULT_PATH)
    mode = result.get("mode", "unknown")

    if mode == "dry_run":
        print("=" * 60)
        print("  CEO Approval Gate — DRY RUN (not yet executed)")
        print("=" * 60)
        print(f"  Title:    {result.get('title', 'N/A')[:60]}")
        print(f"  QA Score: {result.get('qa_score', 'N/A')}")
        print(f"  Source:   {result.get('source_file', 'N/A')}")
        print()
        print("  Run pipeline_bridge.py --execute first to create Draft.")
        return

    success = result.get("success", False)
    post_id = result.get("post_id")
    draft_url = result.get("draft_url", "")
    edit_url = result.get("edit_url", "")

    print("=" * 60)
    print("  CEO Approval Gate — Pending Review")
    print("=" * 60)
    print(f"  Post ID:     {post_id}")
    print(f"  Title:       {result.get('title', 'N/A')[:55]}")
    print(f"  QA Score:    {result.get('qa_score', 'N/A')}")
    print(f"  Status:      {'Draft created' if success else 'FAILED'}")
    print(f"  Draft URL:   {draft_url}")
    print(f"  Edit URL:    {edit_url}")
    print()

    open_gaps = result.get("open_gaps", [])
    if open_gaps:
        print("  Warning — Open gaps before public publish:")
        for gap in open_gaps:
            print(f"    - {gap}")
        print()

    print("  To approve and publish:")
    print(f"    1. Review draft at: {edit_url or draft_url}")
    print(f"    2. Run: python3 ceo_approval_gate.py --approve {post_id}")
    print()
    print("  To reject:")
    print(f"    python3 ceo_approval_gate.py --reject {post_id}")
    print()


def approve(post_id: int) -> None:
    """Approve and publish a draft."""
    if not BRIDGE_RESULT_PATH.exists():
        print("ERROR: No bridge result found.")
        sys.exit(1)

    result = read_json(BRIDGE_RESULT_PATH)
    bridge_post_id = result.get("post_id")

    if bridge_post_id != post_id:
        print(f"ERROR: Post ID mismatch. Bridge has {bridge_post_id}, you specified {post_id}.")
        sys.exit(1)

    if not result.get("success"):
        print("ERROR: Bridge result shows failure. Cannot approve a failed draft.")
        sys.exit(1)

    title = result.get("title", "Unknown")
    print(f"Publishing Post {post_id}: {title[:60]}...")
    print("Calling n8n publish webhook...")

    success, response, error = call_publish_webhook(post_id, title)

    # Fallback to direct WP REST API if n8n webhook is broken
    public_url: str | None = None
    if not success:
        print(f"n8n webhook failed ({error}), falling back to direct WP REST API...")
        success, public_url, error = publish_via_wp_api(post_id, title)

    # Log the approval
    log = load_approval_log()
    log_entry = {
        "timestamp": now_iso(),
        "action": "approve_and_publish",
        "post_id": post_id,
        "title": title,
        "success": success,
        "response": response,
        "error": error,
    }
    log.setdefault("log", []).append(log_entry)
    save_approval_log(log)

    if success:
        if public_url is None:
            result_block = response.get("result", {}) if isinstance(response, dict) and isinstance(response.get("result"), dict) else {}
            public_url = result_block.get("url") or (response.get("url") if isinstance(response, dict) else None) or ""
        print()
        print("=" * 60)
        print("  PUBLISHED SUCCESSFULLY")
        print("=" * 60)
        if public_url:
            print(f"  URL: {public_url}")
        print(f"  Post ID: {post_id}")
        print()

        # Update bridge result
        result["published"] = True
        result["published_at"] = now_iso()
        result["public_url"] = public_url
        result["approval_log_entry"] = log_entry["timestamp"]
        write_json(BRIDGE_RESULT_PATH, result)
    else:
        print()
        print(f"PUBLISH FAILED: {error or response}")
        sys.exit(1)


def reject(post_id: int) -> None:
    """Reject a draft."""
    log = load_approval_log()
    log_entry = {
        "timestamp": now_iso(),
        "action": "rejected",
        "post_id": post_id,
        "reason": "CEO rejected",
    }
    log.setdefault("log", []).append(log_entry)
    save_approval_log(log)
    print(f"Post {post_id} rejected. Draft remains in WordPress (not published).")


def show_log() -> None:
    """Show approval history."""
    log = load_approval_log()
    entries = log.get("log", [])
    if not entries:
        print("No approval history.")
        return

    print("=" * 60)
    print("  CEO Approval History")
    print("=" * 60)
    for entry in entries[-20:]:  # last 20
        ts = entry.get("timestamp", "?")
        action = entry.get("action", "?")
        pid = entry.get("post_id", "?")
        title = entry.get("title", "")[:50]
        status = "OK" if entry.get("success") else "FAIL"
        print(f"  {ts} | {action:20s} | Post {pid} | {status}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="CEO Approval Gate")
    parser.add_argument("--approve", type=int, metavar="POST_ID", help="Approve and publish a draft")
    parser.add_argument("--reject", type=int, metavar="POST_ID", help="Reject a draft")
    parser.add_argument("--log", action="store_true", help="Show approval history")
    args = parser.parse_args()

    if args.log:
        show_log()
    elif args.approve:
        approve(args.approve)
    elif args.reject:
        reject(args.reject)
    else:
        show_pending()


if __name__ == "__main__":
    main()
