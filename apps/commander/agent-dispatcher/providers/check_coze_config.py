#!/usr/bin/env python3
"""Coze staging credential readiness check.

This script only checks whether required environment variables are present.
It never prints secret values and never calls the Coze API.
"""

from __future__ import annotations

import argparse
import json
import os


REQUIRED_ENV_VARS = [
    "M8A_COZE_BASE_URL",
    "M8A_COZE_API_TOKEN",
    "M8A_COZE_WORKFLOW_ID",
]

OPTIONAL_ENV_VARS = [
    "M8A_COZE_WORKSPACE_ID",
]


def check_env(environ=None) -> dict:
    env = environ if environ is not None else os.environ
    required = {
        name: "configured" if bool(env.get(name)) else "missing"
        for name in REQUIRED_ENV_VARS
    }
    optional = {
        name: "configured" if bool(env.get(name)) else "missing"
        for name in OPTIONAL_ENV_VARS
    }
    ready = all(status == "configured" for status in required.values())
    return {
        "provider": "coze",
        "check_type": "staging_credential_presence",
        "ready": ready,
        "status": "ready" if ready else "not_ready",
        "required": required,
        "optional": optional,
        "safe_to_call_api": False,
        "api_called": False,
        "secrets_printed": False,
        "notes": [
            "This check does not read .env files directly.",
            "This check does not print token values.",
            "This check does not call Coze or any external platform.",
            "A separate CEO approval is required before real API verification.",
        ],
    }


def print_text(result: dict) -> None:
    for name in REQUIRED_ENV_VARS:
        print(f"{name} {result['required'][name]}")
    for name in OPTIONAL_ENV_VARS:
        print(f"{name} {result['optional'][name]}")
    print(result["status"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Coze staging credential environment variables.")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON.")
    args = parser.parse_args()
    result = check_env()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
