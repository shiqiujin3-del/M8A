#!/usr/bin/env python3
"""M8A Exception & Recovery Framework V1.

The framework turns platform/API/worker failures into Exception Missions,
Exception Queue records, recovery plans, and CEO approvals when needed.
"""

from __future__ import annotations

import json
import subprocess
import time


DB_CONTAINER = "m8a-postgres"
DB_USER = "m8a"
DB_NAME = "m8a"
ACTOR = "exception_framework"


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


def event(mission_id: str, task_id: str | None, event_type: str, message: str, metadata=None):
    run_sql(
        """
        INSERT INTO commander_task_events (
          event_id, mission_id, task_id, event_type, actor, event_message, metadata
        ) VALUES (
        """
        + ", ".join([
            sql_str(new_id("evt")),
            sql_str(mission_id),
            sql_str(task_id),
            sql_str(event_type),
            sql_str(ACTOR),
            sql_str(message),
            sql_json(metadata or {}),
        ])
        + ");"
    )


def exception_event(exception_id: str, event_type: str, message: str, from_status=None, to_status=None, metadata=None):
    run_sql(
        """
        INSERT INTO commander_exception_events (
          exception_event_id, exception_id, event_type, from_status, to_status, actor, event_message, metadata
        ) VALUES (
        """
        + ", ".join([
            sql_str(new_id("exevt")),
            sql_str(exception_id),
            sql_str(event_type),
            sql_str(from_status),
            sql_str(to_status),
            sql_str(ACTOR),
            sql_str(message),
            sql_json(metadata or {}),
        ])
        + ");"
    )


def classify_exception(error_message: str, source_system: str):
    text = (error_message or "").lower()
    if "cloudflare" in text or "error 1010" in text or "http 403" in text:
        return {
            "exception_type": "cloudflare_access_denied",
            "error_code": "HTTP_403_CLOUDFLARE_1010",
            "severity": "high",
            "risk_level": "high",
            "requires_ceo_approval": True,
        }
    if "certificate_verify_failed" in text or "ssl" in text:
        return {
            "exception_type": "ssl_certificate",
            "error_code": "SSL_CERTIFICATE_VERIFY_FAILED",
            "severity": "medium",
            "risk_level": "medium",
            "requires_ceo_approval": False,
        }
    if "401" in text or "unauthorized" in text or "oauth" in text:
        return {
            "exception_type": "auth_or_oauth",
            "error_code": "AUTH_OR_OAUTH_FAILURE",
            "severity": "high",
            "risk_level": "high",
            "requires_ceo_approval": True,
        }
    if "timeout" in text:
        return {
            "exception_type": "timeout",
            "error_code": "TIMEOUT",
            "severity": "medium",
            "risk_level": "medium",
            "requires_ceo_approval": False,
        }
    if "500" in text:
        return {
            "exception_type": "server_error",
            "error_code": "HTTP_500",
            "severity": "high",
            "risk_level": "high",
            "requires_ceo_approval": False,
        }
    return {
        "exception_type": f"{source_system}_exception",
        "error_code": "UNCLASSIFIED_EXCEPTION",
        "severity": "medium",
        "risk_level": "medium",
        "requires_ceo_approval": False,
    }


def recovery_plan_for(classification: dict, error_message: str, source_system: str):
    exception_type = classification["exception_type"]
    if exception_type == "cloudflare_access_denied":
        return {
            "summary": "Cloudflare blocked the platform/API request before the action could reach WordPress.",
            "possible_causes": [
                "Cloudflare WAF or bot rule blocked the local API request.",
                "REST API authenticated request pattern is not allowlisted.",
                "Source IP, user agent, or security score triggered Error 1010."
            ],
            "recommended_actions": [
                "Review Cloudflare Security Events for the blocked request.",
                "Create a narrow allow rule for trusted M8A source and WordPress REST draft endpoint.",
                "Avoid disabling global security rules.",
                "Retry draft-only verification after allowlist is confirmed."
            ],
            "impact_scope": ["Website Capability", "WordPress Draft Creation", "Publishing Center MVP"],
            "risk_level": "high",
            "needs_ceo": True,
            "ceo_decision_required": "Approve Cloudflare/WAF allowlist or staging bypass for controlled M8A draft creation.",
        }
    if exception_type == "ssl_certificate":
        return {
            "summary": "Local runtime certificate verification failed.",
            "possible_causes": ["Python CA bundle missing or not configured."],
            "recommended_actions": ["Use system CA path such as SSL_CERT_FILE=/etc/ssl/cert.pem.", "Do not disable TLS verification."],
            "impact_scope": ["Local Mission Control runtime"],
            "risk_level": "medium",
            "needs_ceo": False,
        }
    return {
        "summary": f"{source_system} exception requires Infrastructure Operator review.",
        "possible_causes": ["Unknown or unclassified platform/API error."],
        "recommended_actions": ["Inspect task_events and platform response.", "Classify error and define a targeted recovery path."],
        "impact_scope": [source_system],
        "risk_level": classification["risk_level"],
        "needs_ceo": classification["requires_ceo_approval"],
    }


def existing_exception(source_task_id: str | None, error_code: str):
    if not source_task_id:
        return None
    return query_json(
        """
        SELECT row_to_json(e)
        FROM commander_exceptions e
        WHERE e.source_task_id = """ + sql_str(source_task_id) + """
          AND e.error_code = """ + sql_str(error_code) + """
          AND e.status IN ('new','investigating','waiting_approval')
        ORDER BY e.created_at DESC
        LIMIT 1;
        """,
        None,
    )


def create_exception_from_failure(source_mission_id: str | None, source_task_id: str | None, source_system: str, error_message: str):
    classification = classify_exception(error_message, source_system)
    existing = existing_exception(source_task_id, classification["error_code"])
    if existing:
        exception_event(existing["exception_id"], "exception_idempotent_skip", "Existing active exception reused; duplicate exception was not created.", metadata={"source_task_id": source_task_id})
        return existing

    worker = query_json("SELECT row_to_json(w) FROM commander_workers w WHERE name='Infrastructure Operator';", None)
    worker_id = worker["worker_id"] if worker else "worker_infrastructure_operator"
    plan = recovery_plan_for(classification, error_message, source_system)
    exception_id = new_id("exception")
    exception_mission_id = new_id("mission_exception")
    task_id = f"{exception_mission_id}_task_001"
    artifact_id = new_id("artifact_exception")
    requires_ceo = bool(plan.get("needs_ceo") or classification["requires_ceo_approval"])
    queue_status = "waiting_approval" if requires_ceo else "investigating"

    title = f"Exception: {classification['error_code']}"
    objective = f"Infrastructure Operator investigates {source_system} exception and prepares recovery plan."
    run_sql(
        """
        INSERT INTO commander_missions (
          mission_id, mission_name, mission_key, title, objective, product, market, risk_level, priority, status, command_text, planner_version, input
        ) VALUES (
        """
        + ", ".join([
            sql_str(exception_mission_id),
            sql_str("EXCEPTION_MISSION"),
            sql_str(classification["error_code"]),
            sql_str(title),
            sql_str(objective),
            sql_str(None),
            sql_str(None),
            sql_str(classification["risk_level"]),
            sql_str("P0" if classification["severity"] in ("high", "critical") else "P1"),
            sql_str("waiting_approval" if requires_ceo else "running"),
            sql_str(objective),
            sql_str("exception_framework_v1"),
            sql_json({"source_mission_id": source_mission_id, "source_task_id": source_task_id, "source_system": source_system, "error_code": classification["error_code"]}),
        ])
        + ");"
    )
    run_sql(
        """
        INSERT INTO commander_tasks (
          task_id, mission_id, worker_id, worker_name, task_order, title, action, status, risk_level, input, requires_approval, approval_reason
        ) VALUES (
        """
        + ", ".join([
            sql_str(task_id),
            sql_str(exception_mission_id),
            sql_str(worker_id),
            sql_str("Infrastructure Operator"),
            "1",
            sql_str("Analyze exception and generate recovery plan"),
            sql_str("analyze_exception_recovery"),
            sql_str("waiting_approval" if requires_ceo else "running"),
            sql_str(classification["risk_level"]),
            sql_json({"exception_id": exception_id, "error_message": error_message}),
            "true" if requires_ceo else "false",
            sql_str(plan.get("ceo_decision_required")),
        ])
        + ");"
    )
    run_sql(
        """
        INSERT INTO commander_artifacts (
          artifact_id, mission_id, task_id, artifact_type, title, content_json, quality_score, simulation_status, payload_snapshot
        ) VALUES (
        """
        + ", ".join([
            sql_str(artifact_id),
            sql_str(exception_mission_id),
            sql_str(task_id),
            sql_str("report"),
            sql_str("Recovery Plan"),
            sql_json(plan),
            "0.9",
            sql_str("recovery_plan"),
            sql_json(plan),
        ])
        + ");"
    )
    approval_id = None
    if requires_ceo:
        approval_id = new_id("approval_exception")
        request_payload = {
            "exception_id": exception_id,
            "source_system": source_system,
            "error_code": classification["error_code"],
            "recovery_plan": plan,
            "no_external_action": True,
        }
        run_sql(
            """
            INSERT INTO commander_approvals (
              approval_id, mission_id, task_id, artifact_id, approval_type, platform, action_type, risk_level, status, approver_name, request_payload, payload_snapshot
            ) VALUES (
            """
            + ", ".join([
                sql_str(approval_id),
                sql_str(exception_mission_id),
                sql_str(task_id),
                sql_str(artifact_id),
                sql_str("exception_recovery_approval"),
                sql_str("Infrastructure"),
                sql_str("approve_recovery_plan"),
                sql_str(classification["risk_level"]),
                sql_str("pending"),
                sql_str("石总"),
                sql_json(request_payload),
                sql_json(request_payload),
            ])
            + ");"
        )

    run_sql(
        """
        INSERT INTO commander_exceptions (
          exception_id, exception_mission_id, source_mission_id, source_task_id, source_system, exception_type, error_code, error_message,
          severity, risk_level, status, assigned_worker_id, assigned_worker_name, requires_ceo_approval, recovery_plan, impact_scope, root_cause_hypothesis
        ) VALUES (
        """
        + ", ".join([
            sql_str(exception_id),
            sql_str(exception_mission_id),
            sql_str(source_mission_id),
            sql_str(source_task_id),
            sql_str(source_system),
            sql_str(classification["exception_type"]),
            sql_str(classification["error_code"]),
            sql_str(error_message),
            sql_str(classification["severity"]),
            sql_str(classification["risk_level"]),
            sql_str(queue_status),
            sql_str(worker_id),
            sql_str("Infrastructure Operator"),
            "true" if requires_ceo else "false",
            sql_json(plan),
            sql_json(plan.get("impact_scope", [])),
            sql_json(plan.get("possible_causes", [])),
        ])
        + ");"
    )
    event(exception_mission_id, task_id, "exception_mission_created", "Exception Mission created and assigned to Infrastructure Operator.", {"exception_id": exception_id, "source_task_id": source_task_id})
    if source_mission_id:
        event(source_mission_id, source_task_id, "exception_created", "Failure was routed into Exception Framework.", {"exception_id": exception_id, "exception_mission_id": exception_mission_id})
    exception_event(exception_id, "exception_created", "Exception entered Exception Queue.", None, queue_status, {"exception_mission_id": exception_mission_id, "approval_id": approval_id})
    return query_json("SELECT row_to_json(e) FROM commander_exceptions e WHERE exception_id=" + sql_str(exception_id) + ";", None)


def list_exceptions():
    return query_json(
        """
        SELECT COALESCE(json_agg(data ORDER BY created_at DESC), '[]'::json)
        FROM (
          SELECT e.*,
            m.mission_name AS exception_mission_name,
            t.title AS source_task_title,
            ap.approval_id,
            ap.status AS approval_status
          FROM commander_exceptions e
          LEFT JOIN commander_missions m ON m.mission_id = e.exception_mission_id
          LEFT JOIN commander_tasks t ON t.task_id = e.source_task_id
          LEFT JOIN commander_approvals ap ON ap.mission_id = e.exception_mission_id AND ap.status = 'pending'
          ORDER BY e.created_at DESC
          LIMIT 50
        ) data;
        """,
        [],
    )


def exception_summary():
    return query_json(
        """
        SELECT row_to_json(data) FROM (
          SELECT
            (SELECT count(*) FROM commander_exceptions WHERE created_at::date = CURRENT_DATE) AS today_count,
            (SELECT count(*) FROM commander_exceptions WHERE status IN ('new','investigating')) AS investigating,
            (SELECT count(*) FROM commander_exceptions WHERE status = 'waiting_approval') AS waiting_ceo,
            (SELECT count(*) FROM commander_exceptions WHERE status = 'resolved') AS resolved,
            (SELECT COALESCE(round(avg(EXTRACT(EPOCH FROM (resolved_at - created_at)) / 60)::numeric, 1), 0) FROM commander_exceptions WHERE resolved_at IS NOT NULL) AS avg_recovery_minutes
        ) data;
        """,
        {"today_count": 0, "investigating": 0, "waiting_ceo": 0, "resolved": 0, "avg_recovery_minutes": 0},
    )


def resolve_exception(exception_id: str, note: str):
    exception = query_json("SELECT row_to_json(e) FROM commander_exceptions e WHERE exception_id=" + sql_str(exception_id) + ";", None)
    if not exception:
        raise ValueError("Exception not found.")
    run_sql(
        "UPDATE commander_exceptions SET status='resolved', resolution_note="
        + sql_str(note)
        + ", resolved_at=now(), updated_at=now() WHERE exception_id="
        + sql_str(exception_id)
        + ";"
    )
    run_sql(
        "UPDATE commander_missions SET status='completed', completed_at=now(), updated_at=now() WHERE mission_id="
        + sql_str(exception["exception_mission_id"])
        + ";"
    )
    exception_event(exception_id, "exception_resolved", "Exception marked resolved.", exception["status"], "resolved", {"note": note})
    return query_json("SELECT row_to_json(e) FROM commander_exceptions e WHERE exception_id=" + sql_str(exception_id) + ";", None)


def archive_exception(exception_id: str):
    exception = query_json("SELECT row_to_json(e) FROM commander_exceptions e WHERE exception_id=" + sql_str(exception_id) + ";", None)
    if not exception:
        raise ValueError("Exception not found.")
    run_sql(
        "UPDATE commander_exceptions SET status='archived', archived_at=now(), updated_at=now() WHERE exception_id="
        + sql_str(exception_id)
        + ";"
    )
    run_sql(
        "UPDATE commander_missions SET status='archived', archived_at=now(), updated_at=now() WHERE mission_id="
        + sql_str(exception["exception_mission_id"])
        + ";"
    )
    exception_event(exception_id, "exception_archived", "Exception archived.", exception["status"], "archived")
    return query_json("SELECT row_to_json(e) FROM commander_exceptions e WHERE exception_id=" + sql_str(exception_id) + ";", None)


def simulate_cloudflare_403():
    return create_exception_from_failure(
        source_mission_id=None,
        source_task_id=None,
        source_system="WordPress",
        error_message="WordPress draft creation failed with HTTP 403: Cloudflare Error 1010 Access denied.",
    )

