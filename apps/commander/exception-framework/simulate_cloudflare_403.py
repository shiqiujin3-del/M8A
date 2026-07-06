#!/usr/bin/env python3
"""Simulate a Cloudflare 403 exception without touching external platforms."""

from __future__ import annotations

import json

from exception_framework import archive_exception, list_exceptions, simulate_cloudflare_403


def main():
    exception = simulate_cloudflare_403()
    exceptions = list_exceptions()
    archived = archive_exception(exception["exception_id"])
    print(json.dumps({
        "created_exception": exception,
        "queue_count_after_create": len(exceptions),
        "archived_exception": archived,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

