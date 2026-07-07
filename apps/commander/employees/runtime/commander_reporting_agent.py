#!/usr/bin/env python3
"""Commander Reporting Agent V1.

Local-only reporting worker for M8A.

Responsibilities:
- validate mission completion report records
- upsert records into docs/M8A_REPORT_INDEX.json
- avoid external APIs, secrets, and platform actions
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
REPORT_INDEX_JSON = ROOT / "docs" / "M8A_REPORT_INDEX.json"

REQUIRED_FIELDS = [
    "mission_id",
    "mission_name",
    "module",
    "branch",
    "commit",
    "report_path",
    "status",
    "tests",
    "ceo_review_status",
    "next_action",
]

FORBIDDEN_VALUE_MARKERS = [
    "sk-",
    "api_key=",
    "token=",
    "password=",
    "app_password=",
    "secret=",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_record(record: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise ValueError(f"Missing report index fields: {', '.join(missing)}")

    serialized = json.dumps(record, ensure_ascii=False).lower()
    blocked = [marker for marker in FORBIDDEN_VALUE_MARKERS if marker in serialized]
    if blocked:
        raise ValueError(f"Sensitive-looking value marker detected: {', '.join(blocked)}")


def upsert_record(index: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    validate_record(record)
    index.setdefault("records", [])
    index["last_updated"] = utc_now()[:10]
    mission_id = record["mission_id"]
    replaced = False
    for offset, existing in enumerate(index["records"]):
        if existing.get("mission_id") == mission_id:
            index["records"][offset] = record
            replaced = True
            break
    if not replaced:
        index["records"].append(record)
    return {
        "mission_id": mission_id,
        "action": "updated" if replaced else "inserted",
        "record_count": len(index["records"]),
    }


def load_record(args: argparse.Namespace) -> dict[str, Any]:
    if args.record_file:
        return read_json(Path(args.record_file))
    if args.record_json:
        return json.loads(args.record_json)
    raise ValueError("Provide --record-file or --record-json.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Upsert one M8A report index record.")
    parser.add_argument("--record-file")
    parser.add_argument("--record-json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    record = load_record(args)
    index = read_json(REPORT_INDEX_JSON)
    result = upsert_record(index, record)
    result["dry_run"] = args.dry_run
    result["external_api_connected"] = False
    result["secrets_written"] = False
    if not args.dry_run:
        write_json(REPORT_INDEX_JSON, index)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
