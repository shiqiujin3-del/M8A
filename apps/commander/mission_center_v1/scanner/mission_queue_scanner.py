#!/usr/bin/env python3
"""
M8A Mission Queue Scanner v1
自动扫描、分类、处理 Mission Queue。

用法:
  python3 mission_queue_scanner.py scan          # 只扫描，不修改
  python3 mission_queue_scanner.py scan --fix     # 扫描并自动修复
  python3 mission_queue_scanner.py report         # 生成队列健康报告
"""

import json
import sys
import os
from datetime import datetime, timezone, timedelta
from collections import Counter
from copy import deepcopy

# ============================================================
# Config
# ============================================================

QUEUE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "runtime", "global_mission_queue.v1.json"
)

RULES = {
    # Completed missions older than N days → auto-archive
    "auto_archive_after_days": 7,

    # Dispatched missions with no update in N days → flag as stale
    "stale_dispatch_days": 3,

    # Blocked missions where ALL deps are closed → auto-unblock to Waiting
    "auto_unblock_when_deps_closed": True,

    # Waiting CEO missions older than N days → escalate
    "escalate_waiting_ceo_days": 7,

    # Any active mission not updated in N days → stale warning
    "stale_warning_days": 7,
}

# ============================================================
# Helpers
# ============================================================

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def parse_ts(ts_str):
    """Parse various timestamp formats to datetime."""
    if not ts_str:
        return None
    try:
        # Handle +01:00 and Z suffixes
        ts_str = ts_str.replace("Z", "+00:00")
        return datetime.fromisoformat(ts_str)
    except (ValueError, TypeError):
        return None

def days_since(ts_str):
    """Days since a timestamp. Returns None if unparseable."""
    dt = parse_ts(ts_str)
    if not dt:
        return None
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (now - dt).days

def load_queue():
    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_queue(data):
    # Backup first
    backup_path = QUEUE_PATH + f".backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        with open(backup_path, "w", encoding="utf-8") as bf:
            bf.write(f.read())

    with open(QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  [backup] {backup_path}")

# ============================================================
# Scan Logic
# ============================================================

def classify_mission(mission):
    """Classify a single mission and determine recommended actions."""
    rt = mission.get("runtime", {})
    status = rt.get("status", "Unknown")
    updated = rt.get("updated_at")
    stale_days = days_since(updated)

    deps = mission.get("dependencies", [])
    deps_open = [d for d in deps if d.get("status") == "open"]
    deps_closed = [d for d in deps if d.get("status") == "closed"]

    result = {
        "mission_id": mission["mission_id"],
        "title": mission.get("title", "")[:60],
        "priority": mission.get("priority", "?"),
        "status": status,
        "stale_days": stale_days,
        "deps_open": len(deps_open),
        "deps_closed": len(deps_closed),
        "actions": [],
        "classification": "healthy",
    }

    # Rule 1: Completed → auto-archive after N days
    if status == "Completed":
        if stale_days is not None and stale_days >= RULES["auto_archive_after_days"]:
            result["classification"] = "auto_archive"
            result["actions"].append(f"Auto-archive (completed {stale_days}d ago)")
        else:
            result["classification"] = "completed_recent"
        return result

    # Already archived — skip
    if status == "Archived":
        result["classification"] = "archived"
        return result

    # Rule 2: Blocked with all deps closed → auto-unblock
    if status == "Blocked" and RULES["auto_unblock_when_deps_closed"]:
        if len(deps_open) == 0 and len(deps_closed) > 0:
            result["classification"] = "auto_unblock"
            result["actions"].append("Auto-unblock (all dependencies closed)")
            return result

    # Rule 3: Blocked with open deps, stale
    if status == "Blocked":
        if stale_days is not None and stale_days >= RULES["stale_warning_days"]:
            result["classification"] = "blocked_stale"
            result["actions"].append(f"Escalate to CEO (blocked {stale_days}d, deps still open)")
        else:
            result["classification"] = "blocked_active"
            result["actions"].append("Monitor (blocked, deps open)")
        return result

    # Rule 4: Waiting CEO, stale → escalate
    if status == "Waiting CEO":
        if stale_days is not None and stale_days >= RULES["escalate_waiting_ceo_days"]:
            result["classification"] = "escalate_ceo"
            result["actions"].append(f"ESCALATE: Waiting CEO for {stale_days} days")
        else:
            result["classification"] = "waiting_ceo"
        return result

    # Rule 5: Dispatched but stale → flag for re-dispatch
    if status == "dispatched":
        if stale_days is not None and stale_days >= RULES["stale_dispatch_days"]:
            result["classification"] = "stale_dispatch"
            result["actions"].append(f"Re-dispatch or close (dispatched {stale_days}d ago, no completion)")
        else:
            result["classification"] = "dispatched_recent"
        return result

    # Rule 6: Any other active status, stale
    if stale_days is not None and stale_days >= RULES["stale_warning_days"]:
        result["classification"] = "stale"
        result["actions"].append(f"Stale warning ({stale_days}d since update)")

    return result


def scan(fix=False):
    """Scan the mission queue and optionally apply fixes."""
    data = load_queue()
    missions = data["missions"]

    print("=" * 70)
    print("  M8A Mission Queue Scanner v1")
    print(f"  Scan time: {now_iso()}")
    print(f"  Queue file: {QUEUE_PATH}")
    print(f"  Mode: {'SCAN + FIX' if fix else 'SCAN ONLY'}")
    print("=" * 70)
    print()

    # Classify all missions
    results = []
    for m in missions:
        r = classify_mission(m)
        results.append((m, r))

    # Summary
    classifications = Counter(r["classification"] for _, r in results)
    status_counts = Counter(m["runtime"]["status"] for m in missions)

    print("--- Queue Overview ---")
    print(f"  Total missions: {len(missions)}")
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        print(f"    {status:20s}: {count}")
    print()

    print("--- Classification ---")
    for cls, count in sorted(classifications.items(), key=lambda x: -x[1]):
        print(f"    {cls:25s}: {count}")
    print()

    # Active missions detail
    active = [(m, r) for m, r in results if r["classification"] not in ("archived", "completed_recent", "auto_archive")]
    if active:
        print(f"--- Active Missions ({len(active)}) ---")
        for m, r in active:
            icon = {
                "healthy": "[OK]",
                "stale": "[STALE]",
                "stale_dispatch": "[STALE-D]",
                "blocked_active": "[BLOCKED]",
                "blocked_stale": "[BLOCKED!]",
                "waiting_ceo": "[CEO]",
                "escalate_ceo": "[CEO!!!]",
                "auto_unblock": "[UNBLOCK]",
                "dispatched_recent": "[DISP]",
            }.get(r["classification"], "[?]")

            stale_str = f"{r['stale_days']}d" if r["stale_days"] is not None else "?"
            print(f"  {icon:12s} [{r['priority']}] {r['title']}")
            print(f"               status={r['status']} | stale={stale_str} | deps: {r['deps_open']}o/{r['deps_closed']}c")
            for action in r["actions"]:
                print(f"               -> {action}")
            print()

    # Auto-archive candidates
    archive_candidates = [(m, r) for m, r in results if r["classification"] == "auto_archive"]
    if archive_candidates:
        print(f"--- Auto-Archive Candidates ({len(archive_candidates)}) ---")
        for m, r in archive_candidates:
            print(f"  {m['mission_id'][:50]} (completed {r['stale_days']}d ago)")
        print()

    # Apply fixes
    if fix:
        print("--- Applying Fixes ---")
        fixed = 0

        for m, r in results:
            if r["classification"] == "auto_archive":
                m["runtime"]["status"] = "Archived"
                m["runtime"]["updated_at"] = now_iso()
                m.setdefault("log", []).append({
                    "at": now_iso(),
                    "event": "Auto-archived by Mission Queue Scanner",
                    "message": f"Mission was Completed, auto-archived after {r['stale_days']} days."
                })
                print(f"  [ARCHIVED] {m['mission_id'][:50]}")
                fixed += 1

            elif r["classification"] == "auto_unblock":
                m["runtime"]["status"] = "Waiting"
                m["runtime"]["updated_at"] = now_iso()
                m.setdefault("log", []).append({
                    "at": now_iso(),
                    "event": "Auto-unblocked by Mission Queue Scanner",
                    "message": "All dependencies closed, status changed from Blocked to Waiting."
                })
                print(f"  [UNBLOCKED] {m['mission_id'][:50]}")
                fixed += 1

            elif r["classification"] == "escalate_ceo":
                m.setdefault("log", []).append({
                    "at": now_iso(),
                    "event": "Escalated by Mission Queue Scanner",
                    "message": f"Waiting CEO for {r['stale_days']} days. Escalation flag added."
                })
                # Don't change status, just add escalation flag
                m["escalated"] = True
                m["escalated_at"] = now_iso()
                print(f"  [ESCALATED] {m['mission_id'][:50]}")
                fixed += 1

        if fixed > 0:
            save_queue(data)
            print(f"\n  Total fixes applied: {fixed}")
        else:
            print("  No fixes needed.")

    print()
    print("=" * 70)
    return results


def report():
    """Generate a health report."""
    data = load_queue()
    missions = data["missions"]

    active = [m for m in missions if m["runtime"]["status"] not in ("Archived", "Completed")]
    archived = [m for m in missions if m["runtime"]["status"] == "Archived"]
    completed = [m for m in missions if m["runtime"]["status"] == "Completed"]

    print("=" * 50)
    print("  Mission Queue Health Report")
    print(f"  {now_iso()}")
    print("=" * 50)
    print()
    print(f"  Total:     {len(missions)}")
    print(f"  Active:    {len(active)}")
    print(f"  Completed: {len(completed)}")
    print(f"  Archived:  {len(archived)}")
    print()

    if active:
        print("  Active Breakdown:")
        by_status = Counter(m["runtime"]["status"] for m in active)
        for s, c in sorted(by_status.items()):
            print(f"    {s:20s}: {c}")

        by_priority = Counter(m["priority"] for m in active)
        print()
        print("  By Priority:")
        for p in ["P0", "P1", "P2", "P3"]:
            if p in by_priority:
                print(f"    {p}: {by_priority[p]}")

        blocked = [m for m in active if m["runtime"]["status"] == "Blocked"]
        if blocked:
            print()
            print(f"  Blocked ({len(blocked)}):")
            for m in blocked:
                print(f"    - {m['title'][:50]}")

        ceo = [m for m in active if m["runtime"]["status"] == "Waiting CEO"]
        if ceo:
            print()
            print(f"  Waiting CEO ({len(ceo)}):")
            for m in ceo:
                stale = days_since(m["runtime"].get("updated_at"))
                print(f"    - {m['title'][:50]} ({stale}d)")

    print()
    print("=" * 50)


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "scan":
        fix = "--fix" in sys.argv
        scan(fix=fix)
    elif cmd == "report":
        report()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
