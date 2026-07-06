#!/usr/bin/env python3
"""M8A Mission Control / Task Dispatcher V1 API.

No external platform access. PostgreSQL is accessed through the running
m8a-postgres container so no Python package installation is required.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from worker_runner import run_mission as runner_run_mission
from worker_runner import run_once as runner_run_once
from worker_runner import runner_status


HOST = "127.0.0.1"
PORT = 8787
DB_CONTAINER = "m8a-postgres"
DB_USER = "m8a"
DB_NAME = "m8a"
ROOT = Path(__file__).resolve().parents[3]
MIGRATION_PATH = Path(__file__).resolve().parent / "migrations" / "001_mission_control_v1.sql"
COMMANDER_ROOT = Path(__file__).resolve().parents[1]
EXCEPTION_ROOT = COMMANDER_ROOT / "exception-framework"
AGENT_DISPATCHER_ROOT = COMMANDER_ROOT / "agent-dispatcher"
sys.path.insert(0, str(EXCEPTION_ROOT))
sys.path.insert(0, str(AGENT_DISPATCHER_ROOT))

from exception_framework import archive_exception
from exception_framework import create_exception_from_failure
from exception_framework import exception_summary
from exception_framework import list_exceptions
from exception_framework import resolve_exception
from dispatcher import dispatch_mission


class RunnerController:
    def __init__(self):
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.thread: threading.Thread | None = None
        self.mode = "manual"
        self.interval_seconds = 5
        self.current_task_id = None
        self.last_task_id = None
        self.last_run_at = None
        self.last_error = None
        self.mission_id = None

    def _latest_mission_id(self):
        return query_json(
            "SELECT to_json(mission_id) FROM commander_missions ORDER BY created_at DESC LIMIT 1;",
            None,
        )

    def _event(self, event_type: str, message: str, metadata=None):
        mission_id = self._latest_mission_id()
        if not mission_id:
            return
        event(mission_id, None, event_type, None, None, message, metadata or {})

    def start(self, interval_seconds: int = 5, mission_id: str | None = None):
        interval_seconds = max(1, min(int(interval_seconds or 5), 60))
        with self.lock:
            self.interval_seconds = interval_seconds
            self.mission_id = mission_id
            self.mode = "loop"
            self.pause_event.clear()
            self.stop_event.clear()
            if self.thread and self.thread.is_alive():
                self._event("runner_start_ignored", "Runner start ignored because loop is already running.", {"interval_seconds": interval_seconds, "mission_id": mission_id})
                return self.status()
            self.thread = threading.Thread(target=self._loop, name="m8a-worker-runner-v1-1", daemon=True)
            self.thread.start()
        self._event("runner_started", "Worker Runner loop started.", {"interval_seconds": interval_seconds, "mission_id": mission_id})
        return self.status()

    def pause(self):
        with self.lock:
            self.pause_event.set()
            self.mode = "paused"
        self._event("runner_paused", "Worker Runner paused. No new queued tasks will be claimed.")
        return self.status()

    def resume(self):
        with self.lock:
            self.pause_event.clear()
            self.mode = "loop"
            should_start = not (self.thread and self.thread.is_alive())
        self._event("runner_resumed", "Worker Runner resumed.", {"started_new_loop": should_start})
        if should_start:
            return self.start(self.interval_seconds, self.mission_id)
        return self.status()

    def stop(self):
        with self.lock:
            self.stop_event.set()
            self.pause_event.clear()
            self.mode = "stopped"
            thread = self.thread
        if thread and thread.is_alive():
            thread.join(timeout=3)
        self._event("runner_stopped", "Worker Runner stop requested and loop exited safely.")
        return self.status()

    def _loop(self):
        while not self.stop_event.is_set():
            if self.pause_event.is_set():
                self.stop_event.wait(self.interval_seconds)
                continue
            try:
                result = runner_run_once(self.mission_id)
                task = result.get("task") or {}
                with self.lock:
                    self.current_task_id = task.get("task_id")
                    if task.get("task_id"):
                        self.last_task_id = task.get("task_id")
                    self.last_run_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    self.last_error = result.get("error")
                if not result.get("ran"):
                    self.stop_event.wait(self.interval_seconds)
                else:
                    with self.lock:
                        self.current_task_id = None
                    self.stop_event.wait(self.interval_seconds)
            except Exception as exc:
                with self.lock:
                    self.last_error = str(exc)
                    self.current_task_id = None
                self._event("runner_error", "Worker Runner caught an exception and kept API alive.", {"error": str(exc)})
                self.stop_event.wait(self.interval_seconds)
        with self.lock:
            self.current_task_id = None

    def status(self):
        db_status = runner_status()
        with self.lock:
            is_alive = bool(self.thread and self.thread.is_alive())
            is_paused = self.pause_event.is_set()
            mode = "paused" if is_paused else ("loop" if is_alive else self.mode)
            return {
                **db_status,
                "mode": mode,
                "is_running": is_alive,
                "is_paused": is_paused,
                "current_task_id": self.current_task_id,
                "last_task_id": self.last_task_id or db_status.get("last_task_id"),
                "last_run_at": self.last_run_at or db_status.get("last_run_at"),
                "last_error": self.last_error,
                "interval_seconds": self.interval_seconds,
                "mission_id": self.mission_id,
            }


RUNNER_CONTROLLER = RunnerController()


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


def route_exception(source_system: str, error_message: str, source_mission_id: str | None = None, source_task_id: str | None = None):
    try:
        return create_exception_from_failure(
            source_mission_id=source_mission_id,
            source_task_id=source_task_id,
            source_system=source_system,
            error_message=error_message,
        )
    except Exception as exc:
        return {"error": f"Exception Framework routing failed: {exc}", "original_error": error_message}


def event(mission_id: str, task_id: str | None, event_type: str, from_status: str | None, to_status: str | None, message: str, metadata=None):
    event_id = new_id("evt")
    run_sql(
        """
        INSERT INTO commander_task_events (
          event_id, mission_id, task_id, event_type, from_status, to_status, event_message, metadata
        ) VALUES (
        """
        + ", ".join([
            sql_str(event_id),
            sql_str(mission_id),
            sql_str(task_id),
            sql_str(event_type),
            sql_str(from_status),
            sql_str(to_status),
            sql_str(message),
            sql_json(metadata or {}),
        ])
        + ");"
    )


def mission_plan(command_text: str):
    normalized = command_text.lower()
    has_plan = all(token in command_text for token in ["HK620", "美国", "市场"]) and "重点做" in command_text
    if not has_plan and not ("hk620" in normalized and "us" in normalized):
        raise ValueError("Mission Planner V1 only supports HK620 美国市场重点做.")

    mission_id = new_id("mission_hk620_us_growth")
    tasks = [
        ("Knowledge Manager", "read_hk620_product_knowledge", "读取 HK620 产品知识", False),
        ("Business Analyst", "generate_us_market_direction", "生成美国市场分析方向", False),
        ("Content Operator", "generate_english_landing_page_structure", "生成英文 Landing Page 草稿结构", False),
        ("Website Operator", "simulate_wordpress_draft", "生成 WordPress draft payload，但不发布", True),
        ("Distribution Operator", "generate_social_distribution_drafts", "生成 Facebook / LinkedIn / TikTok / YouTube 草稿", True),
        ("Sales Assistant", "generate_whatsapp_inquiry_reply", "生成 WhatsApp 询盘回复话术", True),
        ("Business Analyst", "generate_mission_summary", "生成 Mission Summary", False),
    ]
    return {
        "mission_id": mission_id,
        "mission_name": "HK620_US_GROWTH",
        "mission_key": "HK620_US_GROWTH",
        "priority": "P0",
        "command_text": command_text,
        "title": "HK620_US_GROWTH",
        "objective": "今天重点做 HK620，美国市场。",
        "product": "HK620",
        "market": "USA",
        "risk_level": "medium",
        "input": {"product": "HK620", "market": "USA", "source": "rule_planner_v1"},
        "tasks": tasks,
    }


def is_integration_mission(command_text: str) -> bool:
    normalized = command_text.lower()
    triggers = [
        "接 api",
        "接通 api",
        "integration",
        "connector",
        "接软件",
        "接平台",
        "端口接入",
        "workflow 接入",
        "platform adapter",
        "banana api",
        "coze api",
    ]
    return any(trigger in normalized for trigger in triggers) or "Banana API" in command_text or "Coze API" in command_text


def integration_mission_plan(command_text: str):
    mission_id = new_id("mission_integration")
    mission = {
        "mission_id": mission_id,
        "mission_name": "CONNECT_BANANA_API" if "banana" in command_text.lower() else "INTEGRATION_MISSION",
        "mission_key": "CONNECT_BANANA_API" if "banana" in command_text.lower() else "INTEGRATION_MISSION",
        "title": command_text,
        "objective": f"Generate an Agent Dispatcher plan for: {command_text}",
        "command_text": command_text,
        "priority": "P1",
        "risk_level": "medium",
        "product": None,
        "market": None,
        "input": {"mission_type": "integration", "source": "agent_dispatcher_integration_v1", "command_text": command_text},
    }
    dispatch_result = dispatch_mission(mission)
    if dispatch_result.get("status") == "failed":
        raise RuntimeError(dispatch_result.get("error", "Agent Dispatcher failed."))
    return mission, dispatch_result


def create_mission(command_text: str):
    if is_integration_mission(command_text):
        return create_integration_mission(command_text)

    plan = mission_plan(command_text)
    mission_id = plan["mission_id"]
    run_sql(
        """
        INSERT INTO commander_missions (
          mission_id, mission_name, mission_key, title, objective, product, market, risk_level, priority, status, command_text, planner_version, input
        ) VALUES (
        """
        + ", ".join([
            sql_str(mission_id),
            sql_str(plan["mission_name"]),
            sql_str(plan["mission_key"]),
            sql_str(plan["title"]),
            sql_str(plan["objective"]),
            sql_str(plan["product"]),
            sql_str(plan["market"]),
            sql_str(plan["risk_level"]),
            sql_str(plan["priority"]),
            sql_str("queued"),
            sql_str(plan["command_text"]),
            sql_str("rule_planner_v1"),
            sql_json(plan["input"]),
        ])
        + ");"
    )
    event(mission_id, None, "mission_status_changed", "created", "queued", "Mission entered PostgreSQL Mission Queue.")

    for index, (worker_name, action, title, requires_approval) in enumerate(plan["tasks"], start=1):
        worker = query_json(
            "SELECT row_to_json(w) FROM commander_workers w WHERE name = " + sql_str(worker_name) + ";",
            None,
        )
        task_id = f"{mission_id}_task_{index:03d}"
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
                sql_str(worker_name),
                str(index),
                sql_str(title),
                sql_str(action),
                sql_str("queued"),
                sql_str("high" if requires_approval else "medium"),
                sql_json({"command_text": command_text, "product": "HK620", "market": "USA"}),
                "true" if requires_approval else "false",
                sql_str("CEO approval required before external/public action." if requires_approval else None),
            ])
            + ");"
        )
        event(mission_id, task_id, "task_status_changed", "created", "queued", f"{worker_name} task queued.")
    return get_mission(mission_id)


def create_integration_mission(command_text: str):
    mission, dispatch_result = integration_mission_plan(command_text)
    mission_id = mission["mission_id"]
    run_sql(
        """
        INSERT INTO commander_missions (
          mission_id, mission_name, mission_key, title, objective, product, market, risk_level, priority, status, command_text, planner_version, input
        ) VALUES (
        """
        + ", ".join([
            sql_str(mission_id),
            sql_str(mission["mission_name"]),
            sql_str(mission["mission_key"]),
            sql_str(mission["title"]),
            sql_str(mission["objective"]),
            sql_str(mission["product"]),
            sql_str(mission["market"]),
            sql_str(mission["risk_level"]),
            sql_str(mission["priority"]),
            sql_str("waiting_approval"),
            sql_str(mission["command_text"]),
            sql_str("agent_dispatcher_integration_v1"),
            sql_json(mission["input"]),
        ])
        + ");"
    )
    event(mission_id, None, "mission_status_changed", "created", "waiting_approval", "Integration Mission created by Agent Dispatcher planning layer.")

    worker = query_json("SELECT row_to_json(w) FROM commander_workers w WHERE name = 'Business Analyst';", None)
    task_id = f"{mission_id}_task_001"
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
            sql_str("Business Analyst"),
            "1",
            sql_str("Review Agent Dispatcher Plan"),
            sql_str("approve_agent_plan"),
            sql_str("waiting_approval"),
            sql_str("medium"),
            sql_json({"mission_type": "integration", "command_text": command_text}),
            "true",
            sql_str("CEO approval required before real AI, code, credential, deployment, or external platform work."),
        ])
        + ");"
    )
    event(mission_id, task_id, "task_status_changed", "created", "waiting_approval", "Agent Plan review task created.")

    agent_plan = dispatch_result["agent_plan"]
    content_json = {
        "mission_type": "integration",
        "selected_agents": [step["agent_name"] for step in agent_plan["task_sequence"]],
        "task_sequence": agent_plan["task_sequence"],
        "dependencies": agent_plan["dependencies"],
        "expected_outputs": agent_plan["expected_outputs"],
        "approval_points": agent_plan["approval_points"],
        "mock_runtime_result": dispatch_result["mock_runtime_result"],
        "cotas_execution_package": dispatch_result.get("provider_packages", {}).get("cotas"),
        "route_reason": dispatch_result["route"]["route_reason"],
        "real_ai_called": False,
        "external_platform_called": False,
        "real_code_written": False,
    }
    artifact_id = new_id("artifact_agent_plan")
    run_sql(
        """
        INSERT INTO commander_artifacts (
          artifact_id, mission_id, task_id, artifact_type, title, content_json, quality_score, simulation_status, payload_snapshot
        ) VALUES (
        """
        + ", ".join([
            sql_str(artifact_id),
            sql_str(mission_id),
            sql_str(task_id),
            sql_str("agent_plan"),
            sql_str("Agent Dispatcher Plan"),
            sql_json(content_json),
            "0.86",
            sql_str("mock_plan_ready"),
            sql_json(content_json),
        ])
        + ");"
    )
    event(mission_id, task_id, "artifact_created", None, None, "Agent Plan artifact created.", {"artifact_id": artifact_id, "artifact_type": "agent_plan"})

    approval_id = new_id("approval_agent_plan")
    request_payload = {
        "mission_type": "integration",
        "artifact_id": artifact_id,
        "reason": "Approve Agent Plan before any real AI, code, credential, deployment, or external platform work.",
        "selected_agents": content_json["selected_agents"],
        "approval_points": content_json["approval_points"],
        "no_real_execution": True,
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
            sql_str("agent_plan_approval"),
            sql_str("M8A"),
            sql_str("approve_agent_plan"),
            sql_str("medium"),
            sql_str("pending"),
            sql_str("石总"),
            sql_json(request_payload),
            sql_json(request_payload),
        ])
        + ");"
    )
    event(mission_id, task_id, "approval_created", None, "pending", "approve_agent_plan approval created for CEO review.", {"approval_id": approval_id})
    return get_mission(mission_id)


def get_mission(mission_id: str):
    return query_json(
        """
        SELECT row_to_json(data) FROM (
          SELECT m.*,
            COALESCE((
              SELECT json_agg(t ORDER BY task_order)
              FROM commander_tasks t
              WHERE t.mission_id = m.mission_id
            ), '[]'::json) AS tasks,
            COALESCE((
              SELECT json_agg(a ORDER BY created_at)
              FROM commander_artifacts a
              WHERE a.mission_id = m.mission_id
            ), '[]'::json) AS artifacts,
            COALESCE((
              SELECT json_agg(ap ORDER BY created_at)
              FROM commander_approvals ap
              WHERE ap.mission_id = m.mission_id
            ), '[]'::json) AS approvals,
            COALESCE((
              SELECT json_agg(e ORDER BY created_at)
              FROM commander_task_events e
              WHERE e.mission_id = m.mission_id
            ), '[]'::json) AS events
          FROM commander_missions m
          WHERE m.mission_id = """ + sql_str(mission_id) + """
        ) data;
        """,
        None,
    )


def list_missions():
    return query_json(
        """
        SELECT COALESCE(json_agg(m ORDER BY created_at DESC), '[]'::json)
        FROM commander_missions m;
        """,
        [],
    )


def list_tasks():
    return query_json(
        """
        SELECT COALESCE(json_agg(t ORDER BY created_at DESC), '[]'::json)
        FROM commander_tasks t;
        """,
        [],
    )


def list_approvals():
    return query_json(
        """
        SELECT COALESCE(json_agg(data ORDER BY created_at DESC), '[]'::json)
        FROM (
          SELECT ap.*, m.mission_name, t.title AS task_title
          FROM commander_approvals ap
          JOIN commander_missions m ON m.mission_id = ap.mission_id
          JOIN commander_tasks t ON t.task_id = ap.task_id
        ) data;
        """,
        [],
    )


def list_artifacts():
    return query_json(
        """
        SELECT COALESCE(json_agg(data ORDER BY created_at DESC), '[]'::json)
        FROM (
          SELECT a.*, m.mission_name, t.title AS task_title, t.worker_name, t.status AS task_status
          FROM commander_artifacts a
          JOIN commander_missions m ON m.mission_id = a.mission_id
          LEFT JOIN commander_tasks t ON t.task_id = a.task_id
          ORDER BY a.created_at DESC
          LIMIT 50
        ) data;
        """,
        [],
    )


def get_approval(approval_id: str):
    return query_json(
        """
        SELECT row_to_json(data)
        FROM (
          SELECT ap.*, m.mission_name, t.title AS task_title, a.content_json AS artifact_content
          FROM commander_approvals ap
          JOIN commander_missions m ON m.mission_id = ap.mission_id
          JOIN commander_tasks t ON t.task_id = ap.task_id
          LEFT JOIN commander_artifacts a ON a.artifact_id = ap.artifact_id
          WHERE ap.approval_id = """ + sql_str(approval_id) + """
        ) data;
        """,
        None,
    )


def change_mission_status(mission_id: str, to_status: str):
    mission = get_mission(mission_id)
    if not mission:
        raise ValueError("Mission not found.")
    from_status = mission["status"]
    timestamp_column = {
        "running": "started_at",
        "completed": "completed_at",
        "archived": "archived_at",
    }.get(to_status)
    extra = f", {timestamp_column}=now()" if timestamp_column else ""
    run_sql(
        "UPDATE commander_missions SET status="
        + sql_str(to_status)
        + ", updated_at=now()"
        + extra
        + " WHERE mission_id="
        + sql_str(mission_id)
        + ";"
    )
    event(mission_id, None, "mission_status_changed", from_status, to_status, f"Mission changed to {to_status}.")
    return get_mission(mission_id)


def task_transition(task_id: str, to_status: str, actor: str = "mission_control", body=None):
    task = query_json("SELECT row_to_json(t) FROM commander_tasks t WHERE task_id=" + sql_str(task_id) + ";", None)
    if not task:
        raise ValueError("Task not found.")
    from_status = task["status"]
    columns = ["status=" + sql_str(to_status), "updated_at=now()"]
    if to_status == "claimed":
        columns += ["claimed_by=" + sql_str(actor), "claimed_at=now()"]
    if to_status == "running":
        columns.append("started_at=now()")
    if to_status == "completed":
        columns.append("completed_at=now()")
    if to_status == "failed":
        columns.append("failed_at=now()")
        columns.append("error_message=" + sql_str((body or {}).get("error_message", "Task failed.")))
    run_sql("UPDATE commander_tasks SET " + ", ".join(columns) + " WHERE task_id=" + sql_str(task_id) + ";")
    event(task["mission_id"], task_id, "task_status_changed", from_status, to_status, f"Task changed to {to_status}.", {"actor": actor})
    return query_json("SELECT row_to_json(t) FROM commander_tasks t WHERE task_id=" + sql_str(task_id) + ";", None)


def retry_task(task_id: str, actor: str = "mission_control"):
    task = query_json("SELECT row_to_json(t) FROM commander_tasks t WHERE task_id=" + sql_str(task_id) + ";", None)
    if not task:
        raise ValueError("Task not found.")
    if task["status"] != "failed":
        raise ValueError("Only failed tasks can be retried.")
    retry_count = int(task.get("retry_count") or 0)
    if retry_count >= 2:
        event(task["mission_id"], task_id, "task_retry_rejected", task["status"], task["status"], "Retry rejected because retry_count exceeded limit.", {"retry_count": retry_count})
        raise ValueError("Retry limit exceeded. Maximum retry_count is 2.")
    run_sql(
        "UPDATE commander_tasks SET status='queued', retry_count=retry_count+1, error_message=NULL, failed_at=NULL, updated_at=now() WHERE task_id="
        + sql_str(task_id)
        + ";"
    )
    event(task["mission_id"], task_id, "task_retry", "failed", "queued", "Failed task returned to queue.", {"actor": actor, "retry_count": retry_count + 1})
    return query_json("SELECT row_to_json(t) FROM commander_tasks t WHERE task_id=" + sql_str(task_id) + ";", None)


def artifact_payload(task):
    action = task["action"]
    if action == "read_hk620_product_knowledge":
        return "report", {"summary": "HK620 approved_internal knowledge exists; public approval remains 0%."}, None
    if action == "generate_us_market_direction":
        return "report", {"directions": ["skeleton door strip process education", "USA distributor landing page", "technical proof gap"]}, None
    if action == "generate_english_landing_page_structure":
        return "markdown", {"sections": ["Hero", "Problem", "Process", "Applications", "FAQ", "Review notes"]}, None
    if action in ("generate_wordpress_draft_payload", "simulate_wordpress_draft"):
        return "draft_payload", {
            "platform": "wordpress",
            "mock_action": "simulate_wordpress_draft",
            "status": "approval_required",
            "publish": False,
            "title": "HK620 Skeleton Door Strip Processing for the USA Market",
            "slug": "hk620-skeleton-door-strip-processing-usa",
            "meta_title": "HK620 Skeleton Door Strip Processing | Saiyu",
            "meta_description": "Internal draft for HK620 USA market education. Requires CEO approval before any WordPress draft action.",
            "content_preview": "HK620 is positioned as an internal approved knowledge asset for skeleton door strip processing. This WordPress draft payload is simulated and will not be published."
        }, None
    if action == "generate_social_distribution_drafts":
        return "draft_payload", {"platforms": ["Facebook", "LinkedIn", "TikTok", "YouTube"], "publish": False, "draft_only": True}, None
    if action == "generate_whatsapp_inquiry_reply":
        return "draft_payload", {"channel": "WhatsApp", "send": False, "draft_reply": "Thanks for your interest in HK620. Our team will confirm details before providing technical or pricing information."}, None
    return "report", {"summary": "HK620_US_GROWTH mission completed locally."}, None


def approval_platform(action: str) -> str:
    if "wordpress" in action:
        return "WordPress"
    if "social" in action:
        return "Facebook / LinkedIn / TikTok / YouTube"
    if "whatsapp" in action:
        return "WhatsApp"
    return "Internal"


def complete_task(task_id: str, body=None):
    task = query_json("SELECT row_to_json(t) FROM commander_tasks t WHERE task_id=" + sql_str(task_id) + ";", None)
    if not task:
        raise ValueError("Task not found.")
    task_transition(task_id, "running", body.get("actor", "mission_control") if body else "mission_control", body)
    artifact_type, content_json, content_uri = artifact_payload(task)
    artifact_id = new_id("artifact")
    run_sql(
        """
        INSERT INTO commander_artifacts (
          artifact_id, mission_id, task_id, artifact_type, title, content_json, content_uri, quality_score, simulation_status, payload_snapshot
        ) VALUES (
        """
        + ", ".join([
            sql_str(artifact_id),
            sql_str(task["mission_id"]),
            sql_str(task_id),
            sql_str(artifact_type),
            sql_str(task["title"]),
            sql_json(content_json),
            sql_str(content_uri),
            "0.8",
            sql_str("approval_required" if task["action"] == "simulate_wordpress_draft" else "not_applicable"),
            sql_json(content_json),
        ])
        + ");"
    )
    event(task["mission_id"], task_id, "artifact_created", None, None, f"Artifact {artifact_id} created.", {"artifact_type": artifact_type})
    if task["requires_approval"]:
        approval_id = new_id("approval")
        run_sql(
            """
            INSERT INTO commander_approvals (
              approval_id, mission_id, task_id, artifact_id, approval_type, platform, action_type, risk_level, status, approver_name, request_payload, payload_snapshot
            ) VALUES (
            """
            + ", ".join([
                sql_str(approval_id),
                sql_str(task["mission_id"]),
                sql_str(task_id),
                sql_str(artifact_id),
                sql_str(task["action"]),
                sql_str(approval_platform(task["action"])),
                sql_str(task["action"]),
                sql_str("high"),
                sql_str("pending"),
                sql_str("石总"),
                sql_json({"reason": task["approval_reason"], "artifact_id": artifact_id}),
                sql_json({"reason": task["approval_reason"], "artifact_id": artifact_id, "payload": content_json}),
            ])
            + ");"
        )
        task_transition(task_id, "waiting_approval", "mission_control", body)
        event(task["mission_id"], task_id, "approval_created", None, "pending", f"Approval {approval_id} created for 石总.")
    else:
        task_transition(task_id, "completed", "mission_control", body)
    return query_json("SELECT row_to_json(t) FROM commander_tasks t WHERE task_id=" + sql_str(task_id) + ";", None)


def approval_decision(approval_id: str, body):
    decision = body.get("decision")
    if decision not in ("approved", "rejected"):
        raise ValueError("decision must be approved or rejected.")
    approval = query_json("SELECT row_to_json(a) FROM commander_approvals a WHERE approval_id=" + sql_str(approval_id) + ";", None)
    if not approval:
        raise ValueError("Approval not found.")
    run_sql(
        "UPDATE commander_approvals SET status="
        + sql_str(decision)
        + ", decision_payload="
        + sql_json(body)
        + ", decision_note="
        + sql_str(body.get("decision_note") or body.get("decision_reason"))
        + ", decision_reason="
        + sql_str(body.get("decision_reason") or body.get("decision_note"))
        + ", decided_by="
        + sql_str(body.get("decided_by", "石总"))
        + ", decided_at=now()"
        + (", approved_at=now()" if decision == "approved" else "")
        + " WHERE approval_id="
        + sql_str(approval_id)
        + ";"
    )
    event(approval["mission_id"], approval["task_id"], "approval_decision", approval["status"], decision, f"石总 decision: {decision}.", body)
    if decision == "approved":
        task_transition(approval["task_id"], "completed", "石总", body)
        if approval["action_type"] == "simulate_wordpress_draft":
            run_sql("UPDATE commander_artifacts SET simulation_status='simulated_ready' WHERE artifact_id=" + sql_str(approval["artifact_id"]) + ";")
            event(approval["mission_id"], approval["task_id"], "wordpress_draft_simulated_ready", "approval_required", "simulated_ready", "WordPress draft payload marked simulated_ready. No publish executed.", {"artifact_id": approval["artifact_id"]})
    elif decision == "rejected":
        run_sql("UPDATE commander_artifacts SET simulation_status='rejected' WHERE artifact_id=" + sql_str(approval["artifact_id"]) + ";")
    return query_json("SELECT row_to_json(a) FROM commander_approvals a WHERE approval_id=" + sql_str(approval_id) + ";", None)


def dashboard_data():
    return query_json(
        """
        SELECT row_to_json(data) FROM (
          SELECT
            (SELECT row_to_json(m) FROM commander_missions m ORDER BY created_at DESC LIMIT 1) AS current_mission,
            (SELECT COALESCE(json_agg(t ORDER BY task_order), '[]'::json) FROM commander_tasks t WHERE t.mission_id = (SELECT mission_id FROM commander_missions ORDER BY created_at DESC LIMIT 1)) AS tasks,
            (SELECT COALESCE(json_agg(a ORDER BY created_at DESC), '[]'::json) FROM commander_artifacts a WHERE a.mission_id = (SELECT mission_id FROM commander_missions ORDER BY created_at DESC LIMIT 1)) AS artifacts,
            (SELECT COALESCE(json_agg(ap ORDER BY created_at DESC), '[]'::json) FROM commander_approvals ap WHERE ap.mission_id = (SELECT mission_id FROM commander_missions ORDER BY created_at DESC LIMIT 1)) AS approvals,
            (SELECT COALESCE(json_agg(ap ORDER BY created_at DESC), '[]'::json) FROM commander_approvals ap WHERE ap.status = 'pending') AS pending_approvals,
            (SELECT COALESCE(json_agg(e ORDER BY created_at DESC), '[]'::json) FROM commander_task_events e WHERE e.mission_id = (SELECT mission_id FROM commander_missions ORDER BY created_at DESC LIMIT 1)) AS events,
            (SELECT COALESCE(json_agg(t ORDER BY updated_at DESC), '[]'::json) FROM commander_tasks t WHERE t.status = 'failed') AS failed_task_items,
            (SELECT COALESCE(json_agg(a ORDER BY created_at DESC), '[]'::json) FROM commander_artifacts a WHERE a.artifact_type = 'draft_payload' AND a.content_json->>'platform' = 'wordpress') AS wordpress_drafts,
            (SELECT count(*) FROM commander_tasks WHERE mission_id = (SELECT mission_id FROM commander_missions ORDER BY created_at DESC LIMIT 1) AND status IN ('claimed','running')) AS running_tasks,
            (SELECT count(*) FROM commander_tasks WHERE mission_id = (SELECT mission_id FROM commander_missions ORDER BY created_at DESC LIMIT 1) AND status = 'completed') AS completed_tasks,
            (SELECT count(*) FROM commander_tasks WHERE mission_id = (SELECT mission_id FROM commander_missions ORDER BY created_at DESC LIMIT 1) AND status = 'failed') AS failed_tasks,
            (SELECT count(*) FROM commander_tasks WHERE mission_id = (SELECT mission_id FROM commander_missions ORDER BY created_at DESC LIMIT 1)) AS total_tasks
        ) data;
        """,
        {},
    )


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def authorized(self):
        expected = os.environ.get("M8A_COMMANDER_API_TOKEN")
        header = self.headers.get("Authorization", "")
        if not expected:
            exception = route_exception("Mission Control API", "401 unauthorized: M8A_COMMANDER_API_TOKEN is not configured")
            self._send(401, {"error": "M8A_COMMANDER_API_TOKEN is not configured", "exception": exception})
            return False
        if header != f"Bearer {expected}":
            exception = route_exception("Mission Control API", "401 unauthorized: invalid Authorization header")
            self._send(401, {"error": "unauthorized", "exception": exception})
            return False
        return True

    def do_OPTIONS(self):
        self._send(200, {"ok": True})

    def read_body(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self):
        try:
            path = urlparse(self.path).path
            parts = [p for p in path.split("/") if p]
            if path == "/health":
                self._send(200, {"status": "ok", "service": "mission_control_v1_2"})
            elif path.startswith("/api/") and not self.authorized():
                return
            elif path == "/api/missions":
                self._send(200, {"missions": list_missions()})
            elif len(parts) == 3 and parts[:2] == ["api", "missions"]:
                mission = get_mission(parts[2])
                self._send(200 if mission else 404, {"mission": mission})
            elif path == "/api/tasks":
                self._send(200, {"tasks": list_tasks()})
            elif path == "/api/approvals":
                self._send(200, {"approvals": list_approvals()})
            elif len(parts) == 3 and parts[:2] == ["api", "approvals"]:
                approval = get_approval(parts[2])
                self._send(200 if approval else 404, {"approval": approval})
            elif path == "/api/artifacts":
                self._send(200, {"artifacts": list_artifacts()})
            elif path == "/api/exceptions":
                self._send(200, {"exceptions": list_exceptions()})
            elif path == "/api/exceptions/summary":
                self._send(200, {"summary": exception_summary()})
            elif path == "/api/dashboard/commander":
                self._send(200, dashboard_data())
            elif path == "/api/runner/status":
                self._send(200, {"runner": RUNNER_CONTROLLER.status()})
            else:
                self._send(404, {"error": "not_found"})
        except Exception as exc:
            exception = route_exception("Mission Control API", str(exc))
            self._send(500, {"error": str(exc), "exception": exception})

    def do_POST(self):
        try:
            path = urlparse(self.path).path
            parts = [p for p in path.split("/") if p]
            if path.startswith("/api/") and not self.authorized():
                return
            body = self.read_body()
            if path == "/api/missions":
                mission = create_mission(body.get("command_text", ""))
                self._send(201, {"mission": mission})
            elif len(parts) == 4 and parts[:2] == ["api", "missions"] and parts[3] == "start":
                self._send(200, {"mission": change_mission_status(parts[2], "running")})
            elif len(parts) == 4 and parts[:2] == ["api", "missions"] and parts[3] == "archive":
                self._send(200, {"mission": change_mission_status(parts[2], "archived")})
            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "claim":
                self._send(200, {"task": task_transition(parts[2], "claimed", body.get("actor", "mission_control"), body)})
            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "complete":
                self._send(200, {"task": complete_task(parts[2], body)})
            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "fail":
                self._send(200, {"task": task_transition(parts[2], "failed", body.get("actor", "mission_control"), body)})
            elif len(parts) == 4 and parts[:2] == ["api", "tasks"] and parts[3] == "retry":
                self._send(200, {"task": retry_task(parts[2], body.get("actor", "mission_control"))})
            elif len(parts) == 4 and parts[:2] == ["api", "approvals"] and parts[3] == "decision":
                self._send(200, {"approval": approval_decision(parts[2], body)})
            elif path == "/api/runner/run-once":
                self._send(200, runner_run_once())
            elif len(parts) == 4 and parts[:2] == ["api", "runner"] and parts[2] == "run-mission":
                self._send(200, runner_run_mission(parts[3]))
            elif path == "/api/runner/start":
                self._send(200, {"runner": RUNNER_CONTROLLER.start(body.get("interval_seconds", 5), body.get("mission_id"))})
            elif path == "/api/runner/pause":
                self._send(200, {"runner": RUNNER_CONTROLLER.pause()})
            elif path == "/api/runner/resume":
                self._send(200, {"runner": RUNNER_CONTROLLER.resume()})
            elif path == "/api/runner/stop":
                self._send(200, {"runner": RUNNER_CONTROLLER.stop()})
            elif len(parts) == 4 and parts[:2] == ["api", "exceptions"] and parts[3] == "resolve":
                self._send(200, {"exception": resolve_exception(parts[2], body.get("note", "Resolved from Mission Control API."))})
            elif len(parts) == 4 and parts[:2] == ["api", "exceptions"] and parts[3] == "archive":
                self._send(200, {"exception": archive_exception(parts[2])})
            else:
                self._send(404, {"error": "not_found"})
        except Exception as exc:
            exception = route_exception("Mission Control API", str(exc))
            self._send(400, {"error": str(exc), "exception": exception})


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Mission Control V1.2 API running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
