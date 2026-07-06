#!/usr/bin/env python3
"""Local Worker Runner for M8A Mission Control V1.

The runner only performs local simulated work. It never connects to n8n,
WordPress, social platforms, WhatsApp, CRM, or any other external service.
External-facing actions produce draft payload artifacts plus CEO approvals.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path


DB_CONTAINER = "m8a-postgres"
DB_USER = "m8a"
DB_NAME = "m8a"
RUNNER_NAME = "local_worker_runner_v1"
ROOT = Path(__file__).resolve().parents[3]
COMMANDER_ROOT = Path(__file__).resolve().parents[1]
EXCEPTION_ROOT = COMMANDER_ROOT / "exception-framework"
sys.path.insert(0, str(COMMANDER_ROOT))
sys.path.insert(0, str(EXCEPTION_ROOT))

from capabilities.website.wordpress_draft import create_wordpress_draft
from exception_framework import create_exception_from_failure


def sql_str(value: str | None) -> str:
    if value is None:
        return "NULL"
    return "'" + value.replace("'", "''") + "'"


def sql_json(value: object) -> str:
    return sql_str(json.dumps(value, ensure_ascii=False)) + "::jsonb"


def new_id(prefix: str) -> str:
    return f"{prefix}_{time.time_ns()}"


def run_sql(sql: str) -> str:
    result = subprocess.run(
        ["docker", "exec", "-i", DB_CONTAINER, "psql", "-U", DB_USER, "-d", DB_NAME, "-v", "ON_ERROR_STOP=1", "-At"],
        input=sql,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def query_json(sql: str, default):
    output = run_sql(sql)
    if not output:
        return default
    return json.loads(output)


def event(mission_id: str, task_id: str | None, event_type: str, from_status: str | None, to_status: str | None, message: str, metadata=None):
    run_sql(
        """
        INSERT INTO commander_task_events (
          event_id, mission_id, task_id, event_type, from_status, to_status, actor, event_message, metadata
        ) VALUES (
        """
        + ", ".join([
            sql_str(new_id("evt")),
            sql_str(mission_id),
            sql_str(task_id),
            sql_str(event_type),
            sql_str(from_status),
            sql_str(to_status),
            sql_str(RUNNER_NAME),
            sql_str(message),
            sql_json(metadata or {}),
        ])
        + ");"
    )


def get_task(task_id: str):
    return query_json("SELECT row_to_json(t) FROM commander_tasks t WHERE task_id=" + sql_str(task_id) + ";", None)


def get_mission_tasks(mission_id: str):
    return query_json(
        """
        SELECT COALESCE(json_agg(t ORDER BY task_order), '[]'::json)
        FROM commander_tasks t
        WHERE t.mission_id = """ + sql_str(mission_id) + """;
        """,
        [],
    )


def update_mission_rollup(mission_id: str):
    tasks = get_mission_tasks(mission_id)
    if not tasks:
        return
    statuses = {task["status"] for task in tasks}
    if "failed" in statuses:
        to_status = "failed"
    elif "waiting_approval" in statuses:
        to_status = "waiting_approval"
    elif statuses == {"completed"}:
        to_status = "completed"
    elif statuses & {"claimed", "running"}:
        to_status = "running"
    else:
        to_status = "queued"
    mission = query_json("SELECT row_to_json(m) FROM commander_missions m WHERE mission_id=" + sql_str(mission_id) + ";", None)
    if mission and mission["status"] != to_status and mission["status"] != "archived":
        extra = ""
        if to_status == "running" and not mission.get("started_at"):
            extra += ", started_at=now()"
        if to_status == "completed":
            extra += ", completed_at=now()"
        run_sql(
            "UPDATE commander_missions SET status="
            + sql_str(to_status)
            + ", updated_at=now()"
            + extra
            + " WHERE mission_id="
            + sql_str(mission_id)
            + ";"
        )
        event(mission_id, None, "mission_status_changed", mission["status"], to_status, f"Mission changed to {to_status} by Worker Runner.")


def claim_next_task(mission_id: str | None = None):
    mission_filter = "" if mission_id is None else "AND mission_id=" + sql_str(mission_id)
    return query_json(
        """
        WITH picked AS (
          SELECT task_id
          FROM commander_tasks
          WHERE status='queued' """ + mission_filter + """
          ORDER BY created_at, task_order
          LIMIT 1
          FOR UPDATE SKIP LOCKED
        ),
        updated AS (
          UPDATE commander_tasks t
          SET status='claimed', claimed_by=""" + sql_str(RUNNER_NAME) + """, claimed_at=now(), updated_at=now()
          FROM picked
          WHERE t.task_id = picked.task_id AND t.status='queued'
          RETURNING t.*
        )
        SELECT row_to_json(updated) FROM updated;
        """,
        None,
    )


def mark_task(task, to_status: str, message: str, extra_sql: str = ""):
    from_status = task["status"]
    columns = ["status=" + sql_str(to_status), "updated_at=now()"]
    if to_status == "running":
        columns.append("started_at=COALESCE(started_at, now())")
    if to_status == "completed":
        columns.append("completed_at=now()")
    if to_status == "failed":
        columns.append("failed_at=now()")
    if extra_sql:
        columns.append(extra_sql)
    run_sql("UPDATE commander_tasks SET " + ", ".join(columns) + " WHERE task_id=" + sql_str(task["task_id"]) + ";")
    event(task["mission_id"], task["task_id"], "task_status_changed", from_status, to_status, message)
    updated = get_task(task["task_id"])
    update_mission_rollup(task["mission_id"])
    return updated


def artifact_exists(task_id: str):
    return query_json(
        """
        SELECT row_to_json(a)
        FROM commander_artifacts a
        WHERE a.task_id = """ + sql_str(task_id) + """
        ORDER BY created_at DESC
        LIMIT 1;
        """,
        None,
    )


def approval_exists(task_id: str, artifact_id: str | None = None):
    artifact_filter = "" if artifact_id is None else " AND artifact_id=" + sql_str(artifact_id)
    return query_json(
        """
        SELECT row_to_json(ap)
        FROM commander_approvals ap
        WHERE ap.task_id = """ + sql_str(task_id) + artifact_filter + """
        ORDER BY created_at DESC
        LIMIT 1;
        """,
        None,
    )


def read_hk620_source_summary():
    candidates = [
        ROOT / "docs" / "HK620_GOLDEN_KNOWLEDGE_RECORD_V2_REVIEW_PENDING.md",
        ROOT / "docs" / "HK620_GOLDEN_KNOWLEDGE_RECORD_V1.md",
        ROOT / "knowledge" / "products" / "HK620",
    ]
    for path in candidates:
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="ignore")
            return {
                "source": str(path),
                "source_type": "local_markdown",
                "summary": text[:900],
                "note": "Local HK620 knowledge source was read. Public-use claims still require approved status."
            }
        if path.is_dir():
            files = sorted(p for p in path.rglob("*") if p.is_file())[:20]
            return {
                "source": str(path),
                "source_type": "local_directory",
                "files": [str(p.relative_to(ROOT)) for p in files],
                "note": "HK620 knowledge directory exists. Runner produced a local index summary only."
            }
    return {
        "source": "mock_fallback",
        "source_type": "mock_fallback",
        "summary": "HK620 local knowledge was not reachable from runner. This fallback is for execution testing only.",
        "note": "Fallback used; do not treat as approved product knowledge."
    }


def qa_review_cotas_result(input_json: dict) -> dict:
    checks = []

    def add_check(name: str, passed: bool, notes: str):
        checks.append({"name": name, "passed": passed, "notes": notes})

    summary = input_json.get("summary", "")
    modified_files = input_json.get("modified_files", [])
    new_files = input_json.get("new_files", [])
    test_results = input_json.get("test_results", [])
    risks = input_json.get("risks", [])
    next_steps = input_json.get("next_steps", [])
    artifacts = input_json.get("artifacts", [])
    combined = json.dumps(input_json, ensure_ascii=False).lower()

    add_check("format_complete", bool(input_json.get("cotas_result_artifact_id") and summary), "COTAS result artifact and summary are present.")
    add_check("files_declared", bool(modified_files or new_files), "modified_files or new_files must be declared.")
    add_check("test_results_present", bool(test_results), "test_results must be present.")
    add_check("risks_present", bool(risks), "risks must be explicit.")
    add_check("next_steps_present", bool(next_steps), "next_steps must be explicit.")

    forbidden_tokens = [
        "published successfully",
        "deployed successfully",
        "production modified",
        "external platform modified",
        "live site modified",
        "正式站已修改",
        "已发布",
        "已部署",
    ]
    secret_tokens = ["api_key=", "secret=", "password=", "token=", "app_password=", "密钥明文"]
    external_tokens = ["real coze api was called", "external api called", "真实 coze api 已调用", "已连接外部平台"]
    safe_no_external = "no real coze api" in combined or "no external api call" in combined or "no external platform" in combined or "mock" in combined
    secret_leak = any(token in combined for token in secret_tokens)
    forbidden_action = any(token in combined for token in forbidden_tokens)
    external_modified = any(token in combined for token in external_tokens) and not safe_no_external

    add_check("no_forbidden_action", not forbidden_action, "No publish, deploy, or production modification should be reported.")
    add_check("no_secret_leak", not secret_leak, "No secret-like values should appear in result.")
    add_check("no_external_platform_modified", not external_modified, "Result must not report real external platform changes.")
    add_check("no_external_connection_declared", safe_no_external, "Result should explicitly declare mock/no external connection.")

    serious = forbidden_action or secret_leak or external_modified or not test_results
    failed_checks = [item for item in checks if not item["passed"]]
    if serious:
        raise ValueError("QA Agent found severe COTAS result issue: " + json.dumps(failed_checks, ensure_ascii=False))

    qa_status = "passed" if not failed_checks else "needs_human_review"
    return {
        "qa_status": qa_status,
        "summary": "QA Agent reviewed COTAS/Codex result with local rules. No real AI provider was called.",
        "checks": checks,
        "risks": risks + ([{"qa_risk": "Some checks need human review.", "failed_checks": failed_checks}] if failed_checks else []),
        "recommendation": "Proceed to CEO approval for next controlled step." if qa_status == "passed" else "Human review required before implementation.",
        "requires_ceo_approval": True,
        "source_cotas_result_artifact_id": input_json.get("cotas_result_artifact_id"),
        "original_cotas_task_id": input_json.get("original_cotas_task_id"),
        "external_ai_called": False,
        "external_platform_called": False,
    }


def handler_payload(task):
    action = task["action"]
    if action == "read_hk620_product_knowledge":
        source = read_hk620_source_summary()
        return "report", "HK620 Knowledge Artifact", {
            "business_output": "HK620 产品知识摘要",
            "product": "HK620",
            "source": source,
            "runner_source": source["source_type"],
            "public_use": False,
            "review_note": "Only approved content may be used externally."
        }, "not_applicable"
    if action == "generate_us_market_direction":
        return "report", "HK620 USA Market Direction", {
            "business_output": "美国市场分析",
            "product": "HK620",
            "market": "USA",
            "directions": [
                "Educate customers on skeleton door strip processing.",
                "Explain why edge banding must happen before grooving and cutting.",
                "Build a Topic Cluster around HK620, skeleton doors, and door factory process upgrades."
            ],
            "risk_note": "Uses internal knowledge only; no external analytics API connected."
        }, "not_applicable"
    if action == "generate_english_landing_page_structure":
        return "markdown", "HK620 Landing Page Draft Structure", {
            "business_output": "Landing Page Draft",
            "language": "English",
            "sections": [
                "Hero: HK620 for skeleton door strip processing",
                "Problem: manual strip processing bottleneck",
                "Process: edge banding, grooving, cutting in one line",
                "Applications: door factories and custom furniture producers",
                "FAQ: confirmed facts only",
                "Review notes: public claims require CEO approval"
            ],
            "publish": False
        }, "not_applicable"
    if action == "simulate_wordpress_draft":
        result = create_wordpress_draft()
        return result.artifact_type, result.title, {
            **result.content_json,
            "approval_action_type": "review_wordpress_draft",
            "approval_risk_level": "medium",
            "capability_event_type": result.event_type,
            "capability_event_message": result.event_message,
        }, result.simulation_status
    if action == "generate_social_distribution_drafts":
        return "draft_payload", "Social Distribution Drafts", {
            "business_output": "Facebook / LinkedIn / TikTok / YouTube 草稿",
            "platforms": ["Facebook", "LinkedIn", "TikTok", "YouTube"],
            "publish": False,
            "drafts": {
                "LinkedIn": "HK620 helps door factories explore a more integrated skeleton door strip process.",
                "Facebook": "New draft: HK620 process education for skeleton door strips.",
                "TikTok": "Short-video hook draft: why skeleton door strips need a different process.",
                "YouTube": "Video concept draft: HK620 process walkthrough for USA buyers."
            }
        }, "approval_required"
    if action == "generate_whatsapp_inquiry_reply":
        return "draft_payload", "WhatsApp Inquiry Reply Draft", {
            "business_output": "WhatsApp Reply",
            "channel": "WhatsApp",
            "send": False,
            "draft_reply": "Thanks for your interest in HK620. We can share confirmed technical details after our team reviews your product size, process requirements, and target material."
        }, "approval_required"
    if action == "generate_mission_summary":
        return "report", "HK620 US Growth Mission Summary", {
            "business_output": "Mission Summary",
            "summary": "HK620_US_GROWTH local mission produced knowledge, market, content, website, distribution, and sales draft assets. External actions remain approval-gated.",
            "next_step": "CEO reviews pending approvals; no external action will run automatically."
        }, "not_applicable"
    if action == "qa_review_cotas_result":
        qa_result = qa_review_cotas_result(task.get("input") or {})
        return "qa_review_result", "QA_RESULT", {
            **qa_result,
            "approval_action_type": "approve_qa_result",
            "approval_risk_level": "medium",
        }, "qa_review_completed"
    raise ValueError(f"Unsupported task action: {action}")


def approval_platform(action: str) -> str:
    if "wordpress" in action:
        return "WordPress"
    if action == "review_wordpress_draft":
        return "WordPress"
    if "social" in action:
        return "Facebook / LinkedIn / TikTok / YouTube"
    if "whatsapp" in action:
        return "WhatsApp"
    if action in ("approve_qa_result", "qa_review_cotas_result"):
        return "M8A"
    return "Internal"


def create_artifact_once(task, artifact_type: str, title: str, content_json: dict, simulation_status: str):
    existing = artifact_exists(task["task_id"])
    if existing:
        event(task["mission_id"], task["task_id"], "artifact_idempotent_skip", None, None, "Existing artifact reused; duplicate creation skipped.", {"artifact_id": existing["artifact_id"]})
        return existing
    artifact_id = new_id("artifact")
    run_sql(
        """
        INSERT INTO commander_artifacts (
          artifact_id, mission_id, task_id, artifact_type, title, content_json, quality_score, simulation_status, payload_snapshot
        ) VALUES (
        """
        + ", ".join([
            sql_str(artifact_id),
            sql_str(task["mission_id"]),
            sql_str(task["task_id"]),
            sql_str(artifact_type),
            sql_str(title),
            sql_json(content_json),
            "0.82",
            sql_str(simulation_status),
            sql_json(content_json),
        ])
        + ");"
    )
    event(task["mission_id"], task["task_id"], "artifact_created", None, None, f"{title} created by local Worker Runner.", {"artifact_id": artifact_id, "artifact_type": artifact_type})
    return artifact_exists(task["task_id"])


def create_approval_once(task, artifact, content_json: dict):
    existing = approval_exists(task["task_id"], artifact["artifact_id"])
    if existing:
        event(task["mission_id"], task["task_id"], "approval_idempotent_skip", None, None, "Existing approval reused; duplicate creation skipped.", {"approval_id": existing["approval_id"]})
        return existing
    approval_id = new_id("approval")
    request_payload = {
        "reason": task.get("approval_reason") or "CEO approval required before external/public action.",
        "artifact_id": artifact["artifact_id"],
        "payload": content_json,
        "no_external_action": True,
    }
    action_type = content_json.get("approval_action_type") or task["action"]
    risk_level = content_json.get("approval_risk_level") or "high"
    run_sql(
        """
        INSERT INTO commander_approvals (
          approval_id, mission_id, task_id, artifact_id, approval_type, platform, action_type, risk_level, status, approver_name, request_payload, payload_snapshot
        ) VALUES (
        """
        + ", ".join([
            sql_str(approval_id),
            sql_str(task["mission_id"]),
            sql_str(task["task_id"]),
            sql_str(artifact["artifact_id"]),
            sql_str(action_type),
            sql_str(approval_platform(action_type)),
            sql_str(action_type),
            sql_str(risk_level),
            sql_str("pending"),
            sql_str("石总"),
            sql_json(request_payload),
            sql_json(request_payload),
        ])
        + ");"
    )
    event(task["mission_id"], task["task_id"], "approval_created", None, "pending", f"CEO approval created for {approval_platform(task['action'])}.", {"approval_id": approval_id})
    return approval_exists(task["task_id"], artifact["artifact_id"])


def execute_task(task):
    running = mark_task(task, "running", "Worker Runner started local task execution.")
    artifact_type, title, content_json, simulation_status = handler_payload(running)
    artifact = create_artifact_once(running, artifact_type, title, content_json, simulation_status)
    if content_json.get("capability_event_type"):
        event(
            running["mission_id"],
            running["task_id"],
            content_json["capability_event_type"],
            None,
            simulation_status,
            content_json.get("capability_event_message", "Website Capability completed."),
            {"artifact_id": artifact["artifact_id"], "configured": content_json.get("configured")},
        )
    if running["requires_approval"]:
        create_approval_once(running, artifact, content_json)
        return mark_task(running, "waiting_approval", "Task produced approval-gated draft payload. No external action executed.")
    return mark_task(running, "completed", "Task completed locally and artifact was saved.")


def run_once(mission_id: str | None = None):
    task = claim_next_task(mission_id)
    if not task:
        return {"ran": False, "message": "No queued task available.", "task": None}
    event(task["mission_id"], task["task_id"], "task_claimed", "queued", "claimed", "Worker Runner claimed queued task.", {"runner": RUNNER_NAME})
    update_mission_rollup(task["mission_id"])
    try:
        result = execute_task(task)
        return {"ran": True, "task": result, "message": "Task executed locally."}
    except Exception as exc:
        latest = get_task(task["task_id"]) or task
        exception = create_exception_from_failure(
            source_mission_id=task["mission_id"],
            source_task_id=task["task_id"],
            source_system=f"Worker Runner / {task.get('worker_name')}",
            error_message=str(exc),
        )
        run_sql(
            "UPDATE commander_tasks SET status='failed', error_message="
            + sql_str(str(exc))
            + ", failed_at=now(), updated_at=now() WHERE task_id="
            + sql_str(task["task_id"])
            + ";"
        )
        event(
            task["mission_id"],
            task["task_id"],
            "exception_routed",
            latest.get("status"),
            "failed",
            "Worker Runner routed failure into Exception Framework.",
            {"error": str(exc), "exception_id": exception.get("exception_id"), "exception_mission_id": exception.get("exception_mission_id")},
        )
        update_mission_rollup(task["mission_id"])
        return {"ran": True, "task": get_task(task["task_id"]), "message": "Task failure routed into Exception Framework.", "error": str(exc), "exception": exception}


def run_mission(mission_id: str):
    results = []
    while True:
        result = run_once(mission_id)
        results.append(result)
        if not result["ran"]:
            break
    update_mission_rollup(mission_id)
    return {
        "mission_id": mission_id,
        "results": results,
        "executed_count": len([item for item in results if item["ran"]]),
        "mission": query_json("SELECT row_to_json(m) FROM commander_missions m WHERE mission_id=" + sql_str(mission_id) + ";", None),
    }


def runner_status():
    return query_json(
        """
        SELECT row_to_json(data) FROM (
          SELECT
            'local_worker_runner_v1' AS runner,
            'manual' AS mode,
            false AS is_running,
            false AS is_paused,
            NULL::text AS current_task_id,
            NULL::text AS last_task_id,
            (SELECT max(created_at) FROM commander_task_events WHERE actor='local_worker_runner_v1') AS last_run_at,
            NULL::text AS last_error,
            (SELECT count(*) FROM commander_tasks WHERE status='queued') AS queued_tasks,
            (SELECT count(*) FROM commander_tasks WHERE status='running') AS running_tasks,
            (SELECT count(*) FROM commander_tasks WHERE status='waiting_approval') AS waiting_approval_tasks,
            (SELECT count(*) FROM commander_tasks WHERE status='failed') AS failed_tasks,
            (SELECT count(*) FROM commander_task_events WHERE actor='local_worker_runner_v1' AND event_type='task_claimed' AND created_at::date = CURRENT_DATE) AS total_tasks_run_today
        ) data;
        """,
        {
            "runner": RUNNER_NAME,
            "mode": "manual",
            "is_running": False,
            "is_paused": False,
            "current_task_id": None,
            "last_task_id": None,
            "last_run_at": None,
            "last_error": None,
            "total_tasks_run_today": 0,
        },
    )
