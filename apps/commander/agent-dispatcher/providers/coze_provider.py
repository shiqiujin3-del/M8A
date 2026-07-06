#!/usr/bin/env python3
"""Coze Provider V1 mock-only adapter.

This module is intentionally local and inert. It does not read environment
files, does not connect to Coze, and does not perform network or external
platform actions.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any


REQUIRED_TASK_FIELDS = {
    "mission_id": str,
    "task_id": str,
    "agent_name": str,
    "objective": str,
    "input_json": dict,
    "expected_output_schema": dict,
}

SENSITIVE_VALUE_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^,\s}]+"),
]


@dataclass(frozen=True)
class CozeProvider:
    provider_name: str = "coze"
    execution_mode: str = "mock_only"
    timeout_seconds: int = 30

    def run(self, task: dict[str, Any]) -> dict[str, Any]:
        try:
            self._validate_task(task)
            return self._mock_result(task)
        except Exception as exc:
            return {
                "provider_name": self.provider_name,
                "execution_mode": self.execution_mode,
                "status": "blocked",
                "summary": str(exc),
                "capabilities": [],
                "limitations": ["Mock-only provider refused the task before any external action."],
                "risks": ["Blocked tasks must be reviewed before any future provider execution."],
                "next_steps": ["Route this blocked result through M8A review before proceeding."],
                "requires_approval": False,
                "external_api_called": False,
                "network_accessed": False,
                "env_read": False,
                "forbidden_actions_executed": False,
            }

    def _validate_task(self, task: dict[str, Any]) -> None:
        for field, expected_type in REQUIRED_TASK_FIELDS.items():
            if field not in task:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(task[field], expected_type):
                raise TypeError(f"Invalid field type for {field}")
            if expected_type is str and not task[field].strip():
                raise ValueError(f"Field cannot be empty: {field}")

        if self.execution_mode != "mock_only":
            raise PermissionError("CozeProvider V1 only allows execution_mode=mock_only.")

        serialized = json.dumps(task, ensure_ascii=False, sort_keys=True)
        if any(pattern.search(serialized) for pattern in SENSITIVE_VALUE_PATTERNS):
            raise PermissionError("Sensitive-looking value detected in task input.")

        requested_action = str(task.get("input_json", {}).get("requested_action", "")).lower()
        if requested_action in {"publish", "send", "deploy", "delete", "live_api_call"}:
            raise PermissionError(f"Forbidden action requested: {requested_action}")

    def _mock_result(self, task: dict[str, Any]) -> dict[str, Any]:
        return {
            "provider_name": self.provider_name,
            "execution_mode": self.execution_mode,
            "status": "completed",
            "summary": "Mock-only Coze Provider Adapter V1 produced a safe integration design without contacting Coze.",
            "capabilities": [
                "Treat Coze Bot / Workflow as an external agent provider.",
                "Convert M8A Agent Task input into a provider request shape.",
                "Return structured provider result for artifact intake.",
                "Mark approval points before any future external provider call.",
                "Expose timeout, auth failure, blocked result, and exception routing requirements.",
            ],
            "limitations": [
                "No real Coze connection in V1.",
                "No credential handling in V1.",
                "No workflow execution in V1.",
                "Candidate endpoint names must be verified in a separate approved staging task.",
            ],
            "risks": [
                "Coze output schema may vary by bot or workflow.",
                "Future credential handling must never log sensitive values.",
                "Future provider timeouts and auth failures must enter Exception Framework.",
                "Coze must not become Commander or Mission Control.",
            ],
            "next_steps": [
                "Run staging credential presence check after CEO approval.",
                "Run real API read-only test after separate approval.",
                "Run one workflow execution test in staging mode after QA approval.",
                "Send successful provider results into Result Intake and QA review.",
            ],
            "requires_approval": True,
            "external_api_called": False,
            "network_accessed": False,
            "env_read": False,
            "forbidden_actions_executed": False,
            "design": {
                "coze_positioning": {
                    "role": "external agent provider",
                    "not_commander": True,
                    "not_mission_control": True,
                },
                "input_schema": {
                    "mission_id": "string",
                    "task_id": "string",
                    "agent_name": "string",
                    "objective": "string",
                    "input_json": "object",
                    "expected_output_schema": "object",
                },
                "output_schema": {
                    "provider_name": "coze",
                    "execution_mode": "mock_only",
                    "status": "completed | failed | blocked",
                    "summary": "string",
                    "capabilities": "array",
                    "limitations": "array",
                    "risks": "array",
                    "next_steps": "array",
                    "requires_approval": True,
                },
                "timeout": {
                    "default_seconds": self.timeout_seconds,
                    "on_timeout": "return failed and route to Exception Framework",
                },
                "auth_failure": {
                    "v1_behavior": "not applicable in mock-only mode",
                    "future_behavior": "return blocked and route to Exception Framework",
                },
                "blocked_result": {
                    "causes": ["missing required fields", "sensitive-looking input", "forbidden action request"],
                    "external_action": False,
                },
                "exception_routing": "All failed future real-provider actions must call Exception Framework.",
                "safety_boundary": {
                    "no_publish": True,
                    "no_sensitive_logging": True,
                    "approval_required": True,
                    "exception_on_failure": True,
                },
            },
        }


def build_mock_task() -> dict[str, Any]:
    return {
        "mission_id": "mission_coze_provider_mock_v1",
        "task_id": "task_coze_provider_mock_v1",
        "agent_name": "COTAS Integration Agent",
        "objective": "研究如何把 Coze Bot / Workflow 作为 M8A 可调度 Agent Provider 接入。",
        "input_json": {
            "target_provider": "Coze",
            "target_mode": "mock_only",
            "requested_action": "research_design",
        },
        "expected_output_schema": {
            "provider_name": "string",
            "execution_mode": "string",
            "status": "string",
            "summary": "string",
            "capabilities": "array",
            "limitations": "array",
            "risks": "array",
            "next_steps": "array",
            "requires_approval": "boolean",
        },
    }


def main() -> None:
    result = CozeProvider().run(build_mock_task())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
