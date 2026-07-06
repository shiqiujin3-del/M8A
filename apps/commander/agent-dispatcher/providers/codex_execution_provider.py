#!/usr/bin/env python3
"""Codex Execution Provider V1.

Runs an existing COTAS_EXECUTION_PACKAGE.md through local `codex exec` in a
read-only, non-interactive mode, then sends the resulting COTAS_RESULT.json
through the existing COTAS Result Intake.

This provider is intentionally narrow:
- no external platform calls
- no git operations
- no write-enabled Codex sandbox
- no Commander Console home changes
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


PROVIDER_DIR = Path(__file__).resolve().parent
PACKAGE_PATH = PROVIDER_DIR / "COTAS_EXECUTION_PACKAGE.md"
RESULT_PATH = PROVIDER_DIR / "COTAS_RESULT.json"
LAST_MESSAGE_PATH = Path(os.environ.get("M8A_CODEX_LAST_MESSAGE_PATH", "/tmp/m8a_codex_last_message.txt"))
PROJECT_ROOT = Path(__file__).resolve().parents[4]
COMMANDER_ROOT = PROJECT_ROOT / "apps" / "commander"
MISSION_CONTROL_ROOT = COMMANDER_ROOT / "mission-control"
EXCEPTION_ROOT = COMMANDER_ROOT / "exception-framework"

sys.path.insert(0, str(PROVIDER_DIR))
sys.path.insert(0, str(MISSION_CONTROL_ROOT))
sys.path.insert(0, str(EXCEPTION_ROOT))

from cotas_result_intake import intake_result
from exception_framework import create_exception_from_failure
from worker_runner import run_once as worker_run_once


PROVIDER_NAME = "Codex Execution Provider V1"
CODEX_RESULT_SCHEMA = {
    "mission_id": "",
    "task_id": "",
    "agent_name": "COTAS Integration Agent",
    "status": "completed | failed | blocked",
    "summary": "",
    "modified_files": [],
    "new_files": [],
    "test_results": [],
    "risks": [],
    "next_steps": [],
    "requires_approval": True,
    "approval_reason": "",
    "artifacts": [],
}


def run_command(args: list[str], cwd: Path | None = None, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=str(cwd or PROJECT_ROOT),
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def route_exception(mission_id: str | None, task_id: str | None, error_message: str) -> dict:
    return create_exception_from_failure(
        source_mission_id=mission_id,
        source_task_id=task_id,
        source_system=PROVIDER_NAME,
        error_message=error_message,
    )


def load_package(path: Path = PACKAGE_PATH) -> str:
    if not path.exists():
        raise FileNotFoundError(f"COTAS execution package not found: {path}")
    return path.read_text(encoding="utf-8")


def detect_auth_configured() -> dict:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    local_auth_present = any(
        (codex_home / candidate).exists()
        for candidate in ("auth.json", "config.toml", "codex.json")
    )
    return {
        "OPENAI_API_KEY_configured": bool(os.environ.get("OPENAI_API_KEY")),
        "CODEX_ACCESS_TOKEN_configured": bool(os.environ.get("CODEX_ACCESS_TOKEN")),
        "local_codex_config_present": local_auth_present,
        "codex_home_checked": str(codex_home),
    }


def check_environment(package_path: Path = PACKAGE_PATH) -> dict:
    codex_path = shutil.which("codex")
    version_result = None
    if codex_path:
        version_result = run_command(["codex", "--version"], timeout=30)
    auth = detect_auth_configured()
    execution_approved = os.environ.get("M8A_CODEX_EXECUTION_APPROVED") == "true"
    ready = bool(
        codex_path
        and version_result
        and version_result.returncode == 0
        and package_path.exists()
        and PROJECT_ROOT.exists()
        and (auth["OPENAI_API_KEY_configured"] or auth["CODEX_ACCESS_TOKEN_configured"] or auth["local_codex_config_present"])
        and execution_approved
    )
    return {
        "ready": ready,
        "codex_cli_installed": bool(codex_path),
        "codex_cli_path": codex_path,
        "codex_version": (version_result.stdout or version_result.stderr).strip() if version_result else None,
        "codex_runnable": bool(version_result and version_result.returncode == 0),
        "auth": auth,
        "project_root": str(PROJECT_ROOT),
        "project_root_exists": PROJECT_ROOT.exists(),
        "package_path": str(package_path),
        "package_exists": package_path.exists(),
        "external_codex_execution_approved": execution_approved,
        "planned_sandbox": "read-only",
        "approval_policy": "never",
        "network_policy": "Default deny. Set M8A_CODEX_EXECUTION_APPROVED=true only after CEO approves sending the execution package to Codex.",
    }


def find_latest_integration_task() -> dict:
    from mission_control_api import query_json

    task = query_json(
        """
        SELECT row_to_json(t)
        FROM commander_tasks t
        JOIN commander_missions m ON m.mission_id = t.mission_id
        WHERE (m.input->>'mission_type' = 'integration' OR m.planner_version='agent_dispatcher_integration_v1')
        ORDER BY t.created_at DESC
        LIMIT 1;
        """,
        None,
    )
    if not task:
        raise ValueError("No integration mission task found for Codex result intake.")
    return task


def build_prompt(package_text: str, mission_id: str, task_id: str) -> str:
    schema_text = json.dumps(CODEX_RESULT_SCHEMA, ensure_ascii=False, indent=2)
    return f"""You are COTAS Integration Agent inside M8A.

Execute the package below in READ-ONLY RESEARCH MODE only.

Hard safety rules:
- Do not edit, create, delete, or move any file.
- Do not connect to Coze or any external platform.
- Do not use web/network access.
- Do not run git commit, git push, pull requests, deploy, publish, or external API calls.
- Do not save or reveal secrets.
- If implementation is needed, describe it only in next_steps.

Return ONLY valid JSON matching this exact COTAS_RESULT.json schema.
Do not wrap it in Markdown.

Required fixed fields:
- mission_id: {mission_id}
- task_id: {task_id}
- agent_name: COTAS Integration Agent
- modified_files: []
- new_files: []
- requires_approval: true

The result must explicitly state in test_results or risks that no external API/platform was called.

Schema:
{schema_text}

COTAS_EXECUTION_PACKAGE.md:
---
{package_text}
---
"""


def parse_codex_result(raw_text: str, mission_id: str, task_id: str) -> dict:
    text = raw_text.strip()
    if not text:
        raise ValueError("Codex returned an empty result.")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        matches = re.findall(r"\{[\s\S]*\}", text)
        if not matches:
            raise ValueError("Codex result did not contain a JSON object.")
        payload = json.loads(matches[-1])

    payload["mission_id"] = mission_id
    payload["task_id"] = task_id
    payload["agent_name"] = "COTAS Integration Agent"
    payload["modified_files"] = []
    payload["new_files"] = []
    payload["requires_approval"] = bool(payload.get("requires_approval", True))
    payload.setdefault("approval_reason", "CEO approval required before implementation or external integration.")
    payload.setdefault("artifacts", [])
    return payload


def execute_codex(package_path: Path, mission_id: str, task_id: str, timeout: int) -> dict:
    package_text = load_package(package_path)
    prompt = build_prompt(package_text, mission_id, task_id)
    if LAST_MESSAGE_PATH.exists():
        LAST_MESSAGE_PATH.unlink()

    command = [
        "codex",
        "exec",
        "--json",
        "--sandbox",
        "read-only",
        "--ignore-rules",
        "--cd",
        str(PROJECT_ROOT),
        "--skip-git-repo-check",
        "--output-last-message",
        str(LAST_MESSAGE_PATH),
        prompt,
    ]
    result = run_command(command, cwd=PROJECT_ROOT, timeout=timeout)
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        stdout_tail = (result.stdout or "").strip()[-2000:]
        raise RuntimeError(f"codex exec failed: {stderr or stdout_tail or 'unknown error'}")

    raw_result = LAST_MESSAGE_PATH.read_text(encoding="utf-8") if LAST_MESSAGE_PATH.exists() else result.stdout
    payload = parse_codex_result(raw_result, mission_id, task_id)
    RESULT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "codex_returncode": result.returncode,
        "jsonl_event_count": len([line for line in (result.stdout or "").splitlines() if line.strip()]),
        "result_path": str(RESULT_PATH),
        "payload": payload,
    }


def run_provider(mission_id: str | None, task_id: str | None, package_path: Path, timeout: int, run_qa: bool) -> dict:
    env = check_environment(package_path)
    if not mission_id or not task_id:
        task = find_latest_integration_task()
        mission_id = mission_id or task["mission_id"]
        task_id = task_id or task["task_id"]

    if not env["ready"]:
        recovery_advice = [
            "Confirm whether CEO approves sending COTAS_EXECUTION_PACKAGE.md to the Codex execution service.",
            "If approved, export M8A_CODEX_EXECUTION_APPROVED=true for this run only.",
            "Keep codex exec sandbox read-only and do not provide external platform credentials.",
            "If not approved, continue using manual COTAS handoff or a local OSS provider.",
        ]
        exception = route_exception(
            mission_id,
            task_id,
            "Codex Execution Provider environment check failed or external execution is not approved: "
            + json.dumps({"environment": env, "recovery_advice": recovery_advice}, ensure_ascii=False),
        )
        return {
            "status": "environment_not_ready",
            "environment": env,
            "recovery_advice": recovery_advice,
            "exception": exception,
        }

    try:
        codex_result = execute_codex(package_path, mission_id, task_id, timeout)
        intake = intake_result(RESULT_PATH)
        qa_run = None
        if run_qa and intake.get("qa_task"):
            qa_run = worker_run_once(mission_id)
        return {
            "status": "completed",
            "environment": env,
            "codex_execution": {
                "result_path": codex_result["result_path"],
                "jsonl_event_count": codex_result["jsonl_event_count"],
                "read_only": True,
                "modified_files": codex_result["payload"].get("modified_files"),
                "new_files": codex_result["payload"].get("new_files"),
            },
            "intake": intake,
            "qa_run": qa_run,
        }
    except Exception as exc:
        exception = route_exception(mission_id, task_id, str(exc))
        return {"status": "failed_exception_created", "environment": env, "error": str(exc), "exception": exception}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run COTAS execution package through read-only codex exec.")
    parser.add_argument("--mission-id", default=None)
    parser.add_argument("--task-id", default=None)
    parser.add_argument("--package", default=str(PACKAGE_PATH))
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--no-run-qa", action="store_true")
    args = parser.parse_args()

    package_path = Path(args.package)
    if args.check_only:
        print(json.dumps(check_environment(package_path), ensure_ascii=False, indent=2))
        return

    result = run_provider(args.mission_id, args.task_id, package_path, args.timeout, not args.no_run_qa)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
