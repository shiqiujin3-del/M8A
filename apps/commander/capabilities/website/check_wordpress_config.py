#!/usr/bin/env python3
"""Check WordPress staging configuration without printing secrets or connecting.

This script only checks whether required environment variables exist.
It does not call WordPress REST API.
"""

from __future__ import annotations

import os
import sys


REQUIRED = [
    ("M8A_WORDPRESS_BASE_URL", "BASE_URL"),
    ("M8A_WORDPRESS_USERNAME", "USERNAME"),
    ("M8A_WORDPRESS_APP_PASSWORD", "APP_PASSWORD"),
]


def configured(value: str | None) -> bool:
    return bool(value and value.strip())


def main() -> int:
    ready = True
    for env_name, label in REQUIRED:
        status = "configured" if configured(os.environ.get(env_name)) else "missing"
        if status == "missing":
            ready = False
        print(f"{label} {status}")
    print("ready" if ready else "not_ready")
    return 0 if ready else 1


if __name__ == "__main__":
    sys.exit(main())

