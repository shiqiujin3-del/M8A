#!/usr/bin/env python3
"""Banana API demo mission for Agent Dispatcher V1."""

from __future__ import annotations

import json

from dispatcher import dispatch_mission


def banana_api_mission() -> dict:
    return {
        "mission_name": "CONNECT_BANANA_API",
        "title": "帮我接 Banana API",
        "objective": "Plan how M8A should connect Banana API without executing real integration.",
        "command_text": "帮我接 Banana API",
        "priority": "P1",
        "risk_level": "medium",
        "product": None,
        "market": None,
        "source": "agent_dispatcher_v1_demo",
    }


def main():
    result = dispatch_mission(banana_api_mission())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

