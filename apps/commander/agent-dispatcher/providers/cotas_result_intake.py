#!/usr/bin/env python3
"""COTAS / Codex Result Intake V1.

Reads a local COTAS_RESULT.json file and writes the result back to M8A as
artifacts, task events, approvals, and exceptions when needed.
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
ACTOR = "cotas_result_intake_v1"
PROVIDER_DIR = Path(__file__).resolve().parent
DEFAULT_RESULT_PATH = PROVIDER_DIR / "COTAS_RESULT.json"
COMMANDER_ROOT = Path(__file__).resolve().parents[2]
EXCEPTION_ROOT = COMMANDER_ROOT / "exception-framework"
sys.path.insert(0, str(EXCEPTION_ROOT))

from exception_framework import create_exception_from_failure


REQUIRED_FIELDS = {
    "mission_id": str,
    "task_id": str,
    "agent_name": str,
    "status": str,
    "summary": str,
    "modified_files": list,
    "new_files": list,
    "test_results": list,
    "risks": list,
    "next_steps": list,
    "requires_approval": bool,
    "approval_reason": str,
    "artifacts": list,
}

VALID_STATUSES = {"completed", "failed", "blocked"}


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


def load_result(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_result(payload: dict) -> None:
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in payload:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(payload[field], expected_type):
            raise ValueError(f"Invalid field type: {field}")
    if payload["agent_name"] != "COTAS Integration Agent":
        raise ValueError("agent_name must be COTAS Integration Agent")
    if payload["status"] not in VALID_STATUSES:
        raise ValueError("status must be completed, failed, or blocked")
    if not payload["mission_id"] or not payload["task_id"]:
        raise ValueError("mission_id and task_id are required for result intake")


def ensure_task_exists(mission_id: str, task_id: str) -> dict:
    task = query_json(
        "SELECT row_to_json(t) FROM commander_tasks t WHERE t.mission_id="
        + sql_str(mission_id)
        + " AND t.task_id="
        + sql_str(task_id)
        + ";",
        None,
    )
    if not task:
        raise ValueError("Referenced mission/task was not found in Mission Control")
    return task


def write_event(mission_id: str, task_id: str, event_type: str, message: str, metadata=None, from_status=None, to_status=None):
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
            sql_str(ACTOR),
            sql_str(message),
            sql_json(metadata or {}),
        ])
        + ");"
    )


def create_artifact(mission_id: str, task_id: str, artifact_type: str, title: str, content_json: dict, simulation_status: str) -> dict:
    artifact_id = new_id("artifact_cotas")
    run_sql(
        """
        INSERT INTO commander_artifacts (
          artifact_id, mission_id, task_id, artifact_type, title, content_json, quality_score, simulation_status, payload_snapshot, created_by
        ) VALUES (
        """
        + ", ".join([
            sql_str(artifact_id),
            sql_str(mission_id),
            sql_str(task_id),
            sql_str(artifact_type),
            sql_str(title),
            sql_json(content_json),
            "0.84",
            sql_str(simulation_status),
            sql_json(content_json),
            sql_str(ACTOR),
        ])
        + ");"
    )
    return query_json("SELECT row_to_json(a) FROM commander_artifacts a WHERE artifact_id=" + sql_str(artifact_id) + ";", {})


def create_approval(mission_id: str, task_id: str, artifact_id: str, payload: dict) -> dict:
    approval_id = new_id("approval_cotas")
    request_payload = {
        "reason": payload["approval_reason"],
        "agent_name": payload["agent_name"],
        "status": payload["status"],
        "summary": payload["summary"],
        "artifact_id": artifact_id,
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
            sql_str(mission_id),
            sql_str(task_id),
            sql_str(artifact_id),
            sql_str("cotas_result_approval"),
            sql_str("M8A"),
            sql_str("approve_cotas_result"),
            sql_str("medium"),
            sql_str("pending"),
            sql_str("石总"),
            sql_json(request_payload),
            sql_json(request_payload),
        ])
        + ");"
    )
    return query_json("SELECT row_to_json(a) FROM commander_approvals a WHERE approval_id=" + sql_str(approval_id) + ";", {})


def update_task_status(task: dict, payload: dict):
    if payload["status"] != "completed":
        return task
    run_sql(
        "UPDATE commander_tasks SET status='completed', completed_at=COALESCE(completed_at, now()), updated_at=now() WHERE task_id="
        + sql_str(task["task_id"])
        + ";"
    )
    write_event(
        task["mission_id"],
        task["task_id"],
        "task_status_changed",
        "COTAS result marked task completed.",
        {"agent_name": payload["agent_name"]},
        from_status=task["status"],
        to_status="completed",
    )
    return query_json("SELECT row_to_json(t) FROM commander_tasks t WHERE task_id=" + sql_str(task["task_id"]) + ";", task)


def create_qa_review_artifact(mission_id: str, task_id: str, payload: dict) -> dict:
    qa_payload = {
        "title": "QA Agent Review Required",
        "source_agent": payload["agent_name"],
        "cotas_status": payload["status"],
        "summary": payload["summary"],
        "modified_files": payload["modified_files"],
        "new_files": payload["new_files"],
        "test_results": payload["test_results"],
        "risks": payload["risks"],
        "next_steps": payload["next_steps"],
        "qa_question": "Should this COTAS/Codex result proceed to the next controlled implementation step?",
        "recommendation_required": True,
    }
    return create_artifact(mission_id, task_id, "report", "QA Agent Review Required", qa_payload, "qa_review_required")


def create_qa_review_task(mission_id: str, original_task_id: str, result_artifact_id: str, payload: dict) -> dict | None:
    if payload["status"] != "completed":
        return None
    worker = query_json("SELECT row_to_json(w) FROM commander_workers w WHERE name='QA Agent';", None)
    if not worker:
        raise ValueError("QA Agent worker is not registered. Apply migration 007_qa_agent_review_task_v1.sql first.")
    next_order = query_json(
        "SELECT COALESCE(max(task_order), 0) + 1 FROM commander_tasks WHERE mission_id=" + sql_str(mission_id) + ";",
        1,
    )
    task_id = f"{mission_id}_qa_{int(next_order):03d}_{time.time_ns()}"
    input_json = {
        "mission_id": mission_id,
        "original_cotas_task_id": original_task_id,
        "cotas_result_artifact_id": result_artifact_id,
        "modified_files": payload["modified_files"],
        "new_files": payload["new_files"],
        "test_results": payload["test_results"],
        "risks": payload["risks"],
        "next_steps": payload["next_steps"],
        "summary": payload["summary"],
        "artifacts": payload["artifacts"],
    }
    run_sql(
        """
        INSERT INTO commander_tasks (
          task_id, mission_id, worker_id, worker_name, task_order, title, action, status, risk_level, input, requires_approval, approval_reason
        ) VALUES (
        """
        + ", ".join([
            sql_str(task_id),
            sql_str(mission_id),
            sql_str(worker["worker_id"]),
            sql_str("QA Agent"),
            str(int(next_order)),
            sql_str("QA Review COTAS Result"),
            sql_str("qa_review_cotas_result"),
            sql_str("queued"),
            sql_str("medium"),
            sql_json(input_json),
            "true",
            sql_str("CEO approval required after QA result before implementation proceeds."),
        ])
        + ");"
    )
    write_event(
        mission_id,
        task_id,
        "task_status_changed",
        "QA Agent review task queued from COTAS result intake.",
        {"original_cotas_task_id": original_task_id, "cotas_result_artifact_id": result_artifact_id},
        from_status="created",
        to_status="queued",
    )
    return query_json("SELECT row_to_json(t) FROM commander_tasks t WHERE task_id=" + sql_str(task_id) + ";", {})


def intake_result(path: Path = DEFAULT_RESULT_PATH) -> dict:
    payload = load_result(path)
    validate_result(payload)
    task = ensure_task_exists(payload["mission_id"], payload["task_id"])
    result_artifact = create_artifact(
        payload["mission_id"],
        payload["task_id"],
        "json",
        "COTAS Result",
        payload,
        f"cotas_{payload['status']}",
    )
    write_event(
        payload["mission_id"],
        payload["task_id"],
        "cotas_result_received",
        "COTAS/Codex result received and saved as artifact.",
        {"artifact_id": result_artifact["artifact_id"], "status": payload["status"]},
    )

    updated_task = update_task_status(task, payload)
    exception = None
    if payload["status"] in {"failed", "blocked"}:
        exception = create_exception_from_failure(
            source_mission_id=payload["mission_id"],
            source_task_id=payload["task_id"],
            source_system="COTAS Integration Agent",
            error_message=f"COTAS result status={payload['status']}: {payload['summary']}",
        )
        write_event(
            payload["mission_id"],
            payload["task_id"],
            "cotas_result_exception_routed",
            "COTAS/Codex failed or blocked result routed to Exception Framework.",
            {"exception_id": exception.get("exception_id")},
        )

    approval = None
    if payload["requires_approval"]:
        approval = create_approval(payload["mission_id"], payload["task_id"], result_artifact["artifact_id"], payload)
        write_event(
            payload["mission_id"],
            payload["task_id"],
            "approval_created",
            "COTAS/Codex result approval created.",
            {"approval_id": approval["approval_id"], "action_type": "approve_cotas_result"},
        )

    qa_artifact = create_qa_review_artifact(payload["mission_id"], payload["task_id"], payload)
    write_event(
        payload["mission_id"],
        payload["task_id"],
        "qa_review_required",
        "QA Agent Review Required artifact created.",
        {"artifact_id": qa_artifact["artifact_id"]},
    )
    qa_task = create_qa_review_task(payload["mission_id"], payload["task_id"], result_artifact["artifact_id"], payload)

    return {
        "status": "intake_completed",
        "result_path": str(path),
        "result_artifact": result_artifact,
        "qa_review_artifact": qa_artifact,
        "approval": approval,
        "exception": exception,
        "qa_task": qa_task,
        "task": updated_task,
    }


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RESULT_PATH
    result = intake_result(path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
