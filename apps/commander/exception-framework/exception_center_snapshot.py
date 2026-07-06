#!/usr/bin/env python3
"""Generate a local Exception Center snapshot for review.

This does not require Mission Control API and does not modify Commander Home.
"""

from __future__ import annotations

import json
from pathlib import Path

from exception_framework import exception_summary, list_exceptions


OUT = Path(__file__).resolve().parent / "exception_center_snapshot.json"


def main():
    payload = {
        "summary": exception_summary(),
        "exceptions": list_exceptions(),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(OUT))


if __name__ == "__main__":
    main()

