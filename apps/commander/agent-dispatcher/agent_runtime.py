#!/usr/bin/env python3
"""Mock Agent Runtime.

V1 does not call Claude, Codex, ChatGPT, Gemini, or any external service.
"""

from __future__ import annotations

import time


class MockAgentRuntime:
    def run_plan(self, plan: dict) -> dict:
        results = []
        for step in plan["task_sequence"]:
            results.append({
                "agent_name": step["agent_name"],
                "task_title": step["task_title"],
                "status": "mock_completed",
                "result_summary": f"{step['agent_name']} produced mock plan output for: {step['task_title']}",
                "artifact_type": "agent_plan_fragment",
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            })
        return {
            "runtime": "mock_agent_runtime_v1",
            "external_ai_called": False,
            "external_platform_called": False,
            "results": results,
        }

