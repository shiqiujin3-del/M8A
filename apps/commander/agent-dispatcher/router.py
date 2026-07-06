#!/usr/bin/env python3
"""Router for selecting Agents from a Mission."""

from __future__ import annotations

from registry import AgentRegistry, default_registry


class AgentRouter:
    def __init__(self, registry: AgentRegistry | None = None):
        self.registry = registry or default_registry()

    def route(self, mission: dict) -> dict:
        text = " ".join([
            str(mission.get("mission_name", "")),
            str(mission.get("title", "")),
            str(mission.get("objective", "")),
            str(mission.get("command_text", "")),
        ]).lower()

        integration_markers = [
            "api",
            "connector",
            "integration",
            "adapter",
            "workflow",
            "接",
            "端口",
            "平台",
            "coze",
            "banana",
        ]

        if any(marker in text for marker in integration_markers):
            sequence = [
                "Research Agent",
                "Infrastructure Agent",
                "COTAS Integration Agent",
                "QA Agent",
            ]
            route_reason = "Mission asks for API / connector / adapter / workflow integration, so the safest route is research, infrastructure/auth planning, COTAS/Codex handoff planning, and QA review."
        elif "website" in text or "wordpress" in text:
            sequence = ["Research Agent", "Website Agent", "QA Agent"]
            route_reason = "Mission is website-related, so Website Agent is included before QA."
        elif "content" in text or "文章" in text:
            sequence = ["Research Agent", "Content Agent", "Business Analyst Agent", "QA Agent"]
            route_reason = "Mission is content-related, so Content and Business Analyst agents are included."
        else:
            sequence = ["Research Agent", "Business Analyst Agent", "QA Agent"]
            route_reason = "Generic mission uses research, business analysis, and QA review."

        agents = [self.registry.get(name) for name in sequence]
        return {
            "route_reason": route_reason,
            "selected_agents": agents,
            "agent_sequence": sequence,
        }
