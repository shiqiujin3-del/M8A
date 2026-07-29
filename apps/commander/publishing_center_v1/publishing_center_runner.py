#!/usr/bin/env python3
"""Publishing Center V1 minimal runner.

Scope:
- publish_article -> WordPress Draft-only provider
- reuse existing n8n Draft-only webhook
- write Publishing Queue / Result / Audit records

Safety:
- no publish
- no delete
- no update published post
- no Gmail
- no YouTube
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(os.getenv("M8A_ROOT", str(Path(__file__).resolve().parents[3]))).resolve()
PUBLISHING_DIR = ROOT / "apps" / "commander" / "publishing_center_v1"
EXTERNAL_EXECUTOR_DIR = ROOT / "apps" / "commander" / "external_executor_v1"
ENDPOINT = os.getenv("M8A_WORDPRESS_DRAFT_WEBHOOK", "http://localhost:5678/webhook/m8a-hk620-draft-only")
WORKFLOW_PATH = "m8a-hk620-draft-only"
PROHIBITED_WORKFLOW = "CWbGujhdNKFpa5JZ"

QUEUE_RUNTIME_PATH = PUBLISHING_DIR / "publishing_queue.runtime.v1.json"
LAST_RESULT_PATH = PUBLISHING_DIR / "last_publishing_wordpress_draft_result.v1.json"
AUDIT_PATH = PUBLISHING_DIR / "publishing_audit_log.v1.json"
EXTERNAL_LAST_RESULT_PATH = EXTERNAL_EXECUTOR_DIR / "real_execution" / "last_publishing_center_wp_draft_result.v1.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_audit(event: dict[str, Any]) -> None:
    audit = read_json(AUDIT_PATH, {"version": "publishing_center_v1", "events": []})
    audit.setdefault("events", []).append(event)
    audit["updated_at"] = now_iso()
    write_json(AUDIT_PATH, audit)


def make_ids() -> dict[str, str]:
    stamp = int(time.time() * 1000)
    return {
        "mission_id": f"mission_publish_article_wp_draft_{stamp}",
        "publishing_mission_id": f"pub_article_wp_draft_{stamp}",
        "queue_item_id": f"pub_queue_{stamp}",
        "trace_id": f"trace_publishing_wp_draft_{stamp}",
    }


def build_publishing_mission(ids: dict[str, str]) -> dict[str, Any]:
    created_at = now_iso()
    return {
        "publishing_mission_id": ids["publishing_mission_id"],
        "mission_id": ids["mission_id"],
        "publishing_type": "publish_article",
        "priority": "P1",
        "target_platform": "wordpress",
        "target_provider": "wordpress_provider",
        "content_ref": "hk620_publishing_center_wordpress_draft_v1",
        "approval_status": "approved",
        "runtime_status": "queued",
        "title": "Publishing Center V1 WordPress Draft-only Integration Test",
        "created_at": created_at,
        "updated_at": created_at,
        "safety": {
            "draft_only": True,
            "publish": False,
            "update_published_post": False,
            "delete_post": False,
            "send_gmail": False,
            "upload_youtube": False,
            "prohibited_workflow": PROHIBITED_WORKFLOW,
        },
    }


def dispatch_wordpress_provider(publishing_mission: dict[str, Any]) -> dict[str, Any]:
    if publishing_mission.get("publishing_type") != "publish_article":
        raise ValueError("Only publish_article is supported by this V1 runner.")
    if publishing_mission.get("target_platform") != "wordpress":
        raise ValueError("Only wordpress target_platform is supported by this V1 runner.")
    return {
        "publishing_mission_id": publishing_mission["publishing_mission_id"],
        "mission_id": publishing_mission["mission_id"],
        "selected_provider": "wordpress_provider",
        "runtime_action": "create_wordpress_draft_only",
        "resource_type": "wordpress_article",
        "status": "queued",
        "reason": "Publishing Center selected WordPress Provider for publish_article.",
    }


def build_external_payload(ids: dict[str, str], publishing_mission: dict[str, Any], dispatcher_result: dict[str, Any]) -> dict[str, Any]:
    title = "M8A Publishing Center V1 WordPress Draft-only Test"
    return {
        "mission_id": ids["mission_id"],
        "publishing_mission_id": ids["publishing_mission_id"],
        "trace_id": ids["trace_id"],
        "source": "publishing_center_v1",
        "employee": "Publishing Center V1",
        "priority": publishing_mission["priority"],
        "provider": dispatcher_result["selected_provider"],
        "product": "HK620",
        "market": "美国",
        "language": "English",
        "title": title,
        "article_draft": {
            "title": title,
            "summary": "This draft verifies that Publishing Center can route publish_article to WordPress Draft-only Provider through Runtime Core compatible execution.",
            "sections": [
                "Publishing Center accepted the article mission.",
                "Dispatcher selected WordPress Provider.",
                "External Executor called Draft-only workflow.",
                "Safety boundary forbids publish, delete, update published content, Gmail, and YouTube."
            ],
            "cta": "Review this draft in WordPress before any publish decision.",
            "source_note": "Generated by M8A Publishing Center V1 integration runner."
        },
        "qa_report": {
            "qa_standard": "Website Agent QA V2",
            "qa_score": 92,
            "qa_status": "passed",
            "reason": "Integration draft is safe for Draft-only verification. Publishing is not allowed.",
            "publish_allowed": False
        },
        "qa_score": 92,
        "action": "create_wordpress_draft_only",
        "dry_run": False,
        "publish": False,
        "update_published_post": False,
        "delete_post": False,
        "send_gmail": False,
        "upload_youtube": False,
        "workflow_path": WORKFLOW_PATH,
        "prohibited_workflow": PROHIBITED_WORKFLOW,
        "safety": publishing_mission["safety"],
    }


def call_wordpress_draft_provider(payload: dict[str, Any]) -> tuple[int | None, dict[str, Any], str | None]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw or "{}"), None
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"raw": raw}
        return exc.code, parsed, str(exc)
    except Exception as exc:  # noqa: BLE001
        return None, {}, str(exc)


def normalize_result(
    ids: dict[str, str],
    started_at: str,
    finished_at: str,
    http_status: int | None,
    response: dict[str, Any],
    error: str | None,
) -> dict[str, Any]:
    result = response.get("result") if isinstance(response.get("result"), dict) else {}
    post_id = result.get("post_id") or response.get("post_id")
    draft_url = result.get("draft_url") or response.get("draft_url")
    execution_id = str(response.get("execution_id") or response.get("n8n_execution_id") or "")
    success = bool(response.get("success") is True or response.get("ok") is True) and bool(post_id) and bool(draft_url)
    error_payload = None if success else {
        "error_code": response.get("error_code") or "WORDPRESS_DRAFT_RESULT_MISSING",
        "error_message": response.get("error_message") or error or "Webhook response missing post_id or draft_url.",
        "retryable": True,
    }
    return {
        "success": success,
        "publishing_mission_id": ids["publishing_mission_id"],
        "mission_id": ids["mission_id"],
        "execution_id": execution_id,
        "provider": "wordpress",
        "resource_type": "wordpress_draft",
        "status": "completed" if success else "failed",
        "resource_id": str(post_id) if post_id else None,
        "resource_url": draft_url,
        "started_at": started_at,
        "finished_at": finished_at,
        "retry_count": 0,
        "http_status": http_status,
        "error": error_payload,
        "runtime_core": {
            "execution_contract_compatible": True,
            "runtime_status": "completed" if success else "failed",
        },
        "raw_response": response,
        "requires_execution_lookup": False,
        "safety_result": {
            "draft_only": True,
            "publish": False,
            "update_published_post": False,
            "delete_post": False,
            "send_gmail": False,
            "upload_youtube": False,
            "old_workflow_called": False,
            "prohibited_workflow": PROHIBITED_WORKFLOW,
        },
    }


def update_queue(queue_item: dict[str, Any]) -> None:
    queue = read_json(QUEUE_RUNTIME_PATH, {"version": "publishing_center_v1", "queue": []})
    queue.setdefault("queue", []).append(queue_item)
    queue["updated_at"] = now_iso()
    write_json(QUEUE_RUNTIME_PATH, queue)


def run(execute: bool) -> dict[str, Any]:
    ids = make_ids()
    mission = build_publishing_mission(ids)
    dispatcher_result = dispatch_wordpress_provider(mission)
    payload = build_external_payload(ids, mission, dispatcher_result)
    queued_at = now_iso()
    queue_item = {
        "queue_item_id": ids["queue_item_id"],
        "publishing_mission_id": ids["publishing_mission_id"],
        "mission_id": ids["mission_id"],
        "publishing_type": mission["publishing_type"],
        "target_platform": mission["target_platform"],
        "selected_provider": dispatcher_result["selected_provider"],
        "status": "queued",
        "priority": mission["priority"],
        "approval_status": mission["approval_status"],
        "runtime_execution_id": None,
        "created_at": queued_at,
        "started_at": None,
        "finished_at": None,
        "error": {"error_code": None, "error_message": None},
    }
    update_queue(queue_item)
    append_audit({
        "event": "publishing_mission_created",
        "timestamp": queued_at,
        "mission": mission,
        "dispatcher_result": dispatcher_result,
        "external_call_executed": False,
    })

    if not execute:
        preview = {
            "success": True,
            "mode": "preview_only",
            "mission": mission,
            "dispatcher_result": dispatcher_result,
            "payload": payload,
        }
        write_json(LAST_RESULT_PATH, preview)
        return preview

    started_at = now_iso()
    queue_item["status"] = "running"
    queue_item["started_at"] = started_at
    update_queue(queue_item)
    append_audit({
        "event": "publishing_execution_started",
        "timestamp": started_at,
        "mission_id": ids["mission_id"],
        "publishing_mission_id": ids["publishing_mission_id"],
        "endpoint": ENDPOINT,
        "workflow_path": WORKFLOW_PATH,
        "safety": payload["safety"],
    })
    http_status, response, error = call_wordpress_draft_provider(payload)
    finished_at = now_iso()
    result = normalize_result(ids, started_at, finished_at, http_status, response, error)

    queue_item["status"] = result["status"]
    queue_item["finished_at"] = finished_at
    queue_item["runtime_execution_id"] = result["execution_id"] or None
    if result["error"]:
        queue_item["error"] = {
            "error_code": result["error"]["error_code"],
            "error_message": result["error"]["error_message"],
        }
    update_queue(queue_item)
    write_json(LAST_RESULT_PATH, result)
    write_json(EXTERNAL_LAST_RESULT_PATH, result)
    append_audit({
        "event": "publishing_execution_completed" if result["success"] else "publishing_execution_failed",
        "timestamp": finished_at,
        "result": result,
    })
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Call the approved WordPress Draft-only webhook.")
    args = parser.parse_args()
    print(json.dumps(run(execute=args.execute), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

