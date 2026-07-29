#!/usr/bin/env python3
"""M8A local Commander Mission API.

Purpose: keep the CEO Commander Console mission entry working even when the
PostgreSQL-backed Mission Control API is not running.

Safety boundaries:
- Local JSON only.
- No external API calls.
- No WordPress publish.
- No Gmail send.
- No YouTube upload.
- No merge or push.
"""

from __future__ import annotations

import hashlib
import json
import os
import socket
import sqlite3
import time
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(os.getenv("M8A_ROOT", str(Path(__file__).resolve().parents[3]))).resolve()
HOST = os.getenv("M8A_MISSION_API_HOST", "127.0.0.1")
PORT = int(os.getenv("M8A_MISSION_API_PORT", "8787"))
MISSION_DIR = ROOT / "apps" / "commander" / "missions" / "local_queue"
QUEUE_PATH = MISSION_DIR / "commander_mission_queue.json"
RUNTIME_DB_PATH = ROOT / "apps" / "commander" / "runtime_persistence_v1" / "db" / "m8a_runtime_v1.sqlite"
AUDIT_PATH = ROOT / "apps" / "commander" / "external_executor_v1" / "audit" / "external_executor_real_execution_audit_log.v1.json"
LOG_DIR = Path(os.getenv("M8A_LOG_DIR", str(ROOT / "logs" / "production"))).resolve()
N8N_HEALTH_URL = os.getenv("M8A_N8N_HEALTH_URL", "http://127.0.0.1:5678/")
POSTGRES_HOST = os.getenv("M8A_POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = int(os.getenv("M8A_POSTGRES_PORT", "5432"))
REDIS_HOST = os.getenv("M8A_REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("M8A_REDIS_PORT", "6379"))
QDRANT_URL = os.getenv("M8A_QDRANT_URL", "http://127.0.0.1:6333/")

TEST_CHAIN_ACTIONS = [
    ("Website Agent", "generate_customer_article", "Website Agent 生成客户可看的文章", False),
    ("n8n Execution Layer", "create_wordpress_draft", "n8n 创建 WordPress Draft，不发布", True),
    ("QA Agent", "qa_review_wordpress_draft", "QA Agent 检查 Draft", False),
    ("Commander", "return_acceptance_result", "Commander 返回验收结果", False),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def append_production_log(component: str, payload: dict) -> None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        entry = {"timestamp": now_iso(), "component": component, **payload}
        with (LOG_DIR / f"{component}.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
    except Exception as exc:
        print(json.dumps({"level": "WARN", "message": "production_log_write_failed", "error": str(exc)}, ensure_ascii=False))


def tcp_health(name: str, host: str, port: int, timeout: float = 2.0) -> dict:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return {"name": name, "status": "ok", "host": host, "port": port}
    except Exception as exc:
        return {"name": name, "status": "fail", "host": host, "port": port, "error": str(exc)}


def http_health(name: str, url: str, timeout: float = 3.0) -> dict:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "M8A-HealthCheck/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"name": name, "status": "ok", "url": url, "http_status": resp.status}
    except Exception as exc:
        return {"name": name, "status": "fail", "url": url, "error": str(exc)}


def runtime_db_health() -> dict:
    try:
        RUNTIME_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(RUNTIME_DB_PATH) as conn:
            conn.execute("SELECT 1")
        return {"name": "runtime_db", "status": "ok", "path": str(RUNTIME_DB_PATH)}
    except Exception as exc:
        return {"name": "runtime_db", "status": "fail", "path": str(RUNTIME_DB_PATH), "error": str(exc)}


def log_dir_health() -> dict:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        probe = LOG_DIR / ".healthcheck"
        probe.write_text(now_iso() + "\n", encoding="utf-8")
        return {"name": "log_dir", "status": "ok", "path": str(LOG_DIR)}
    except Exception as exc:
        return {"name": "log_dir", "status": "fail", "path": str(LOG_DIR), "error": str(exc)}


def health_payload() -> dict:
    checks = [
        {"name": "commander", "status": "ok"},
        {"name": "mission_api", "status": "ok", "host": HOST, "port": PORT},
        http_health("n8n", N8N_HEALTH_URL),
        tcp_health("database", POSTGRES_HOST, POSTGRES_PORT),
        tcp_health("redis", REDIS_HOST, REDIS_PORT),
        http_health("qdrant", QDRANT_URL),
        runtime_db_health(),
        log_dir_health(),
    ]
    overall = "ok" if all(c.get("status") == "ok" for c in checks) else "degraded"
    return {
        "status": overall,
        "mode": "production_infrastructure_v1",
        "service": "m8a_commander_mission_api",
        "queue_path": str(QUEUE_PATH),
        "checks": checks,
    }


def ensure_queue() -> dict:
    MISSION_DIR.mkdir(parents=True, exist_ok=True)
    if not QUEUE_PATH.exists():
        data = {
            "queue_version": "1.0",
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "missions": [],
            "tasks": [],
            "approvals": [],
            "artifacts": [],
            "events": [],
            "safety": {
                "external_api_calls": False,
                "wordpress_publish": False,
                "gmail_send": False,
                "youtube_upload": False,
                "git_merge": False,
                "git_push": False,
            },
        }
        write_json(QUEUE_PATH, data)
    return read_json(QUEUE_PATH)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = now_iso()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def new_id(prefix: str) -> str:
    return f"{prefix}_{int(time.time() * 1000)}"


def add_event(queue: dict, mission_id: str, task_id: str | None, event_type: str, message: str, metadata: dict | None = None) -> None:
    queue["events"].append({
        "event_id": new_id("evt"),
        "mission_id": mission_id,
        "task_id": task_id,
        "event_type": event_type,
        "event_message": message,
        "created_at": now_iso(),
        "metadata": metadata or {},
    })


def mission_file_path(mission_id: str) -> Path:
    return MISSION_DIR / f"{mission_id}.json"


def clean_text(value: object, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text or default


def bool_value(value: object, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on", "需要", "是"}


def normalize_contact_payload(payload: dict) -> dict:
    submission_id = clean_text(payload.get("submission_id") or payload.get("Submission ID") or payload.get("id"))
    submitted_time = clean_text(payload.get("submitted_time") or payload.get("Submitted Time") or payload.get("created_at"), now_iso())
    name = clean_text(payload.get("name") or payload.get("Name"), "Unknown Contact")
    company = clean_text(payload.get("company") or payload.get("Company"))
    country = clean_text(payload.get("country") or payload.get("Country"))
    email = clean_text(payload.get("email") or payload.get("Email"))
    whatsapp = clean_text(payload.get("whatsapp") or payload.get("WhatsApp"))
    interested_machine = clean_text(payload.get("interested_machine") or payload.get("Interested Machine") or payload.get("machine") or payload.get("Machine"))
    message = clean_text(payload.get("message") or payload.get("Message"))
    inquiry_id = clean_text(payload.get("inquiry_id") or payload.get("Inquiry ID"))
    if not inquiry_id:
        suffix = submission_id or str(int(time.time() * 1000))
        inquiry_id = f"WMN-INQ-{suffix}"
    return {
        "inquiry_id": inquiry_id,
        "submission_id": submission_id,
        "submitted_time": submitted_time,
        "name": name,
        "company": company,
        "country": country,
        "email": email,
        "whatsapp": whatsapp,
        "interested_machine": interested_machine,
        "message": message,
        "source": "Website Contact Form",
    }


def build_contact_mission(payload: dict) -> tuple[dict, list[dict], list[dict], list[dict], list[dict]]:
    contact = normalize_contact_payload(payload)
    mission_id = new_id("mission_website_contact")
    created_at = now_iso()
    title_bits = [contact["name"]]
    if contact["interested_machine"]:
        title_bits.append(contact["interested_machine"])
    mission = {
        "mission_id": mission_id,
        "mission_name": "WEBSITE_CONTACT_SALES_INQUIRY",
        "mission_key": "CONTACT_WEBHOOK_BRIDGE_V1",
        "title": "Website Contact Form 销售询盘 - " + " / ".join(title_bits),
        "objective": "Create sales_inquiry Mission from Website Contact Form submission. Do not auto reply, quote, or call Gmail Draft.",
        "command_text": contact["message"],
        "mission_type": "sales_inquiry",
        "task_type": "sales_inquiry",
        "source": "website_contact",
        "product": contact["interested_machine"],
        "market": contact["country"],
        "priority": clean_text(payload.get("priority"), "normal"),
        "risk_level": "low",
        "status": "created",
        "created_at": created_at,
        "updated_at": created_at,
        "planner_version": "contact_webhook_bridge_v1_existing_commander_api",
        "input": {
            **contact,
            "source": "website_contact",
            "external_actions_executed": False,
            "auto_reply_executed": False,
            "quotation_generated": False,
            "gmail_draft_created": False,
        },
    }
    tasks: list[dict] = []
    approvals: list[dict] = []
    artifacts = [{
        "artifact_id": new_id("artifact_contact_payload"),
        "mission_id": mission_id,
        "task_id": None,
        "artifact_type": "website_contact_payload",
        "title": "Website Contact Form Payload",
        "content_json": contact,
        "quality_score": 1.0,
        "simulation_status": "real_contact_submission_received",
        "created_at": created_at,
    }]
    events = [{
        "event_id": new_id("evt"),
        "mission_id": mission_id,
        "task_id": None,
        "event_type": "mission_created_from_website_contact",
        "event_message": "Website Contact Form submission created sales_inquiry Mission. No downstream workflow executed.",
        "created_at": created_at,
        "metadata": {
            "inquiry_id": contact["inquiry_id"],
            "submission_id": contact["submission_id"],
            "source": "website_contact",
            "auto_reply_executed": False,
            "gmail_draft_created": False,
        },
    }]
    return mission, tasks, approvals, artifacts, events


def write_runtime_and_audit(mission: dict, event_payload: dict) -> dict:
    result = {"runtime_db": "skipped", "audit": "skipped"}
    payload_json = json.dumps(mission.get("input", {}), ensure_ascii=False)
    event_id = event_payload.get("event_id") or new_id("evt")
    event_hash = hashlib.sha256(json.dumps(event_payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    if RUNTIME_DB_PATH.exists():
        with sqlite3.connect(RUNTIME_DB_PATH) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO missions (
                  mission_id, mission_type, priority, owner_agent, supporting_agents, reviewer, approver,
                  status, knowledge_status, qa_status, approval_status, publish_status, retry_count,
                  created_at, updated_at, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    mission["mission_id"],
                    mission.get("mission_type", "sales_inquiry"),
                    mission.get("priority", "normal"),
                    "Commander",
                    "Sales Agent, Customer Intelligence",
                    "CEO",
                    "CEO",
                    mission.get("status", "created"),
                    "not_required_for_intake",
                    "not_started",
                    "not_required_for_intake",
                    "not_started",
                    0,
                    mission.get("created_at"),
                    mission.get("updated_at"),
                    payload_json,
                ),
            )
            conn.execute(
                "INSERT INTO runtime_logs (log_time, level, component, message, payload_json) VALUES (?, ?, ?, ?, ?)",
                (now_iso(), "INFO", "contact_webhook_bridge_v1", "Website Contact Form created sales_inquiry Mission", json.dumps({"mission_id": mission["mission_id"], **mission.get("input", {})}, ensure_ascii=False)),
            )
            conn.execute(
                """
                INSERT OR REPLACE INTO mission_events (
                  event_id, mission_id, event_type, source_agent, target_agent, priority, status, timestamp, retry_count, payload_json, event_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (event_id, mission["mission_id"], "mission_created", "Website Contact Form", "Commander", mission.get("priority", "normal"), mission.get("status", "created"), now_iso(), 0, json.dumps(event_payload, ensure_ascii=False), event_hash),
            )
            conn.execute(
                "INSERT OR REPLACE INTO event_history (event_id, mission_id, agent_index, event_type, event_date, payload_json, event_hash) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (event_id, mission["mission_id"], "Website Contact Form -> Commander", "mission_created", now_iso(), json.dumps(event_payload, ensure_ascii=False), event_hash),
            )
        result["runtime_db"] = "written"
    if AUDIT_PATH.exists():
        audit = read_json(AUDIT_PATH)
        audit.setdefault("entries", []).append({
            "audit_log_id": new_id("audit_contact_bridge"),
            "timestamp": now_iso(),
            "mission_id": mission["mission_id"],
            "event": "website_contact_webhook_created_mission",
            "result": {
                "success": True,
                "source": "website_contact",
                "mission_id": mission["mission_id"],
                "payload": mission.get("input", {}),
                "safety": {
                    "auto_reply": False,
                    "quotation": False,
                    "gmail_draft": False,
                    "wordpress_change": False,
                    "m8a_downstream_workflow": False,
                },
            },
        })
        audit["updated_at"] = now_iso()
        write_json(AUDIT_PATH, audit)
        result["audit"] = "written"
    append_production_log("contact_webhook_bridge", {
        "event": "website_contact_webhook_created_mission",
        "mission_id": mission["mission_id"],
        "source": "website_contact",
        "runtime_result": result,
        "external_actions_executed": False,
    })
    return result


def build_mission(payload: dict) -> tuple[dict, list[dict], list[dict], list[dict], list[dict]]:
    command_text = clean_text(payload.get("command_text") or payload.get("command"))
    task_type = clean_text(payload.get("task_type"), "general")
    target_employee = clean_text(payload.get("target_employee"), "General Manager")
    priority = clean_text(payload.get("priority"), "P1")
    input_materials = clean_text(payload.get("input_materials"))
    output_requirements = clean_text(payload.get("output_requirements"))
    safety_boundaries = clean_text(
        payload.get("safety_boundaries"),
        "不执行 n8n；不发布 WordPress；不修改已发布文章；不连接外部平台；如需外部动作必须先进入 CEO 审批。",
    )
    requires_ceo_approval = bool_value(payload.get("requires_ceo_approval"), True)
    mission_id = new_id("mission_standard_input")
    created_at = now_iso()
    mission_input = {
        "source": clean_text(payload.get("source"), "mission_standard_input_window_v1"),
        "task_type": task_type,
        "target_employee": target_employee,
        "input_materials": input_materials,
        "output_requirements": output_requirements,
        "safety_boundaries": safety_boundaries,
        "requires_ceo_approval": requires_ceo_approval,
        "external_api_calls_allowed": False,
        "n8n_execution_allowed": False,
        "wordpress_publish_allowed": False,
        "wordpress_published_article_edit_allowed": False,
        "gmail_send_allowed": False,
        "youtube_upload_allowed": False,
    }
    mission = {
        "mission_id": mission_id,
        "mission_name": f"MISSION_STANDARD_INPUT_V1_{task_type.upper()}",
        "mission_key": "MISSION_STANDARD_INPUT_WINDOW_V1",
        "title": command_text[:80] or "Mission 标准输入窗口 V1",
        "objective": command_text,
        "command_text": command_text,
        "task_type": task_type,
        "target_employee": target_employee,
        "assigned_employee": target_employee,
        "input_materials": input_materials,
        "output_requirements": output_requirements,
        "safety_boundaries": safety_boundaries,
        "requires_ceo_approval": requires_ceo_approval,
        "product": clean_text(payload.get("product"), ""),
        "market": clean_text(payload.get("market"), ""),
        "priority": priority,
        "risk_level": "medium" if requires_ceo_approval else "low",
        "status": "ready",
        "created_at": created_at,
        "updated_at": created_at,
        "planner_version": "mission_standard_input_window_v1_local_json",
        "input": mission_input,
    }
    task_specs = [
        (target_employee, "accept_mission_standard_input", "接收 Mission 标准输入", False),
        (target_employee, "prepare_employee_execution_plan", "准备员工执行计划", False),
    ]
    if requires_ceo_approval:
        task_specs.append(("CEO", "wait_for_ceo_execution_approval", "等待 CEO 审批后再进入执行动作", True))
    tasks = []
    approvals = []
    artifacts = []
    events = []
    for index, (worker_name, action, title, approval_required) in enumerate(task_specs, start=1):
        task_id = f"{mission_id}_task_{index:03d}"
        task = {
            "task_id": task_id,
            "mission_id": mission_id,
            "task_order": index,
            "worker_name": worker_name,
            "title": title,
            "action": action,
            "status": "queued",
            "risk_level": "medium" if approval_required else "low",
            "requires_approval": approval_required,
            "approval_required": approval_required,
            "approval_reason": "CEO approval required before any execution action. No n8n, WordPress publish, or published article edit is allowed." if approval_required else None,
            "retry_count": 0,
            "created_at": created_at,
            "updated_at": created_at,
            "input": mission_input,
        }
        tasks.append(task)
        events.append({
            "event_id": new_id("evt"),
            "mission_id": mission_id,
            "task_id": task_id,
            "event_type": "task_status_changed",
            "event_message": f"{worker_name} task queued locally from Mission Standard Input Window V1.",
            "created_at": created_at,
            "metadata": {"from_status": "created", "to_status": "queued", "action": action},
        })
        if approval_required:
            approval_id = new_id("approval")
            approvals.append({
                "approval_id": approval_id,
                "mission_id": mission_id,
                "task_id": task_id,
                "artifact_id": None,
                "approval_type": "mission_execution_approval",
                "platform": "M8A Local Commander",
                "action_type": "approve_mission_execution_scope",
                "risk_level": "medium",
                "status": "pending",
                "approver_name": "石总",
                "request_payload": {
                    "title": command_text,
                    "task_type": task_type,
                    "target_employee": target_employee,
                    "priority": priority,
                    "input_materials": input_materials,
                    "output_requirements": output_requirements,
                    "safety_boundaries": safety_boundaries,
                    "n8n_execution_allowed": False,
                    "wordpress_publish_allowed": False,
                    "wordpress_published_article_edit_allowed": False,
                },
                "payload_snapshot": {
                    "reason": "CEO approval gate for Mission scope only. No external action is executed by this local queue write.",
                    "task_id": task_id,
                },
                "created_at": created_at,
            })
    artifacts.append({
        "artifact_id": new_id("artifact"),
        "mission_id": mission_id,
        "task_id": None,
        "artifact_type": "mission_standard_input",
        "title": "Mission 标准输入已写入本地任务队列",
        "content_json": {
            "summary": "总控台 Mission 标准输入窗口 V1 已生成 Mission ID，并写入本地 Commander queue。",
            "queue_path": str(QUEUE_PATH),
            "mission_file": str(mission_file_path(mission_id)),
            "n8n_executed": False,
            "wordpress_published": False,
            "published_article_modified": False,
        },
        "quality_score": 1.0,
        "simulation_status": "queued_local_only",
        "created_at": created_at,
    })
    events.insert(0, {
        "event_id": new_id("evt"),
        "mission_id": mission_id,
        "task_id": None,
        "event_type": "mission_status_changed",
        "event_message": "Mission Standard Input Window V1 wrote mission to local JSON queue only.",
        "created_at": created_at,
        "metadata": {"from_status": "created", "to_status": "ready", "external_actions_executed": False},
    })
    return mission, tasks, approvals, artifacts, events


def create_mission(payload: dict) -> dict:
    queue = ensure_queue()
    is_contact = clean_text(payload.get("source")).lower() == "website_contact" or clean_text(payload.get("Source")).lower() == "website contact form"
    mission, tasks, approvals, artifacts, events = build_contact_mission(payload) if is_contact else build_mission(payload)
    queue["missions"].insert(0, mission)
    queue["tasks"].extend(tasks)
    queue["approvals"].extend(approvals)
    queue["artifacts"].extend(artifacts)
    queue["events"].extend(events)
    write_json(QUEUE_PATH, queue)
    write_json(mission_file_path(mission["mission_id"]), {
        "mission": mission,
        "tasks": tasks,
        "approvals": approvals,
        "artifacts": artifacts,
        "events": events,
    })
    if is_contact:
        runtime_result = write_runtime_and_audit(mission, events[0] if events else {"mission_id": mission["mission_id"]})
        mission_detail = get_mission(mission["mission_id"])
        mission_detail["runtime_result"] = runtime_result
        mission_detail["execution_response"] = {
            "success": True,
            "mission_id": mission["mission_id"],
            "source": "website_contact",
            "requires_execution_lookup": False,
            "status": "created",
            "error": None,
        }
        return mission_detail
    return get_mission(mission["mission_id"])


def get_mission(mission_id: str) -> dict | None:
    queue = ensure_queue()
    mission = next((m for m in queue["missions"] if m.get("mission_id") == mission_id), None)
    if not mission:
        return None
    return {
        **mission,
        "tasks": [t for t in queue["tasks"] if t.get("mission_id") == mission_id],
        "approvals": [a for a in queue["approvals"] if a.get("mission_id") == mission_id],
        "artifacts": [a for a in queue["artifacts"] if a.get("mission_id") == mission_id],
        "events": [e for e in queue["events"] if e.get("mission_id") == mission_id],
    }


def dashboard_payload() -> dict:
    queue = ensure_queue()
    missions = queue["missions"]
    current = missions[0] if missions else {}
    tasks = [t for t in queue["tasks"] if not current or t.get("mission_id") == current.get("mission_id")]
    approvals = [a for a in queue["approvals"] if not current or a.get("mission_id") == current.get("mission_id")]
    artifacts = [a for a in queue["artifacts"] if not current or a.get("mission_id") == current.get("mission_id")]
    events = [e for e in queue["events"] if not current or e.get("mission_id") == current.get("mission_id")]
    return {
        "api_mode": "local_json_commander_entry_v1",
        "current_mission": current,
        "tasks": tasks,
        "approvals": approvals,
        "pending_approvals": [a for a in approvals if a.get("status") == "pending"],
        "artifacts": artifacts,
        "events": events,
        "total_tasks": len(tasks),
        "running_tasks": len([t for t in tasks if t.get("status") == "running"]),
        "completed_tasks": len([t for t in tasks if t.get("status") == "completed"]),
        "failed_tasks": len([t for t in tasks if t.get("status") == "failed"]),
        "failed_task_items": [t for t in tasks if t.get("status") == "failed"],
        "wordpress_drafts": [a for a in artifacts if a.get("artifact_type") in {"wordpress_draft", "draft_payload"}],
        "queue_path": str(QUEUE_PATH),
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "M8ALocalCommanderAPI/1.0"

    def _send(self, code: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(200, {"ok": True})

    def do_GET(self):
        path = urlparse(self.path).path
        queue = ensure_queue()
        if path == "/health":
            payload = health_payload()
            return self._send(200 if payload["status"] == "ok" else 503, payload)
        if path == "/api/missions":
            return self._send(200, {"missions": queue["missions"]})
        if path.startswith("/api/missions/"):
            mission_id = path.rsplit("/", 1)[-1]
            mission = get_mission(mission_id)
            if not mission:
                return self._send(404, {"error": "mission_not_found"})
            return self._send(200, {"mission": mission})
        if path == "/api/tasks":
            return self._send(200, {"tasks": queue["tasks"]})
        if path == "/api/approvals":
            return self._send(200, {"approvals": queue["approvals"]})
        if path == "/api/artifacts":
            return self._send(200, {"artifacts": queue["artifacts"]})
        if path == "/api/dashboard/commander":
            return self._send(200, dashboard_payload())
        if path == "/api/runner/status":
            return self._send(200, {"runner": {"mode": "manual", "is_running": False, "is_paused": False, "current_task_id": None, "last_error": None, "total_tasks_run_today": 0}})
        return self._send(404, {"error": "not_found", "path": path})

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            length = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(length).decode("utf-8") or "{}") if length else {}
        except Exception:
            body = {}
        if path == "/api/missions":
            is_contact = clean_text(body.get("source")).lower() == "website_contact" or clean_text(body.get("Source")).lower() == "website contact form"
            command_text = clean_text(body.get("command_text") or body.get("command"))
            if not command_text and not is_contact:
                return self._send(400, {"error": "command_text_required"})
            mission = create_mission(body)
            if is_contact:
                return self._send(201, {
                    "success": True,
                    "mission_id": mission.get("mission_id"),
                    "source": "website_contact",
                    "requires_execution_lookup": False,
                    "mission": mission,
                    "runtime_result": mission.get("runtime_result"),
                    "error": None,
                })
            return self._send(201, {"mission": mission, "queue_path": str(QUEUE_PATH)})
        return self._send(404, {"error": "not_found", "path": path})

    def log_message(self, fmt, *args):
        print(f"[{now_iso()}] {self.address_string()} {fmt % args}")


def main():
    ensure_queue()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    print(json.dumps({"status": "started", "url": f"http://{HOST}:{PORT}", "queue_path": str(QUEUE_PATH), "log_dir": str(LOG_DIR)}, ensure_ascii=False))
    server.serve_forever()


if __name__ == "__main__":
    main()
