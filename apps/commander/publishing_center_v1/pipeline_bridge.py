#!/usr/bin/env python3
"""Pipeline Bridge: Content Center V2/V3 → Publishing Center V1 → n8n WordPress Draft

Reads a Content Center pre_publish JSON, converts it to Publishing Center payload,
and optionally calls the n8n Draft-only webhook.

Usage:
  python3 pipeline_bridge.py <pre_publish.json>              # dry-run: print payload
  python3 pipeline_bridge.py <pre_publish.json> --execute    # actually call n8n webhook
  python3 pipeline_bridge.py --latest                        # auto-find latest pre_publish

Safety:
  - Draft-only by default. Publish requires CEO approval via separate step.
  - Never: publish, delete, update published post, Gmail, YouTube.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---- Paths ----
ROOT = Path(os.getenv("M8A_ROOT", str(Path(__file__).resolve().parents[3]))).resolve()
CONTENT_OUTPUTS = ROOT / "apps" / "commander" / "content_center_v1" / "outputs"
PUBLISHING_DIR = ROOT / "apps" / "commander" / "publishing_center_v1"
BRIDGE_RESULT_PATH = PUBLISHING_DIR / "last_bridge_result.v1.json"

# n8n webhooks
DRAFT_WEBHOOK = os.getenv(
    "M8A_WORDPRESS_DRAFT_WEBHOOK",
    "http://localhost:5678/webhook/m8a-hk620-draft-only"
)
PUBLISH_WEBHOOK = os.getenv(
    "M8A_WORDPRESS_PUBLISH_WEBHOOK",
    "http://localhost:5678/webhook/m8a-hk620-publish-approved-v2"
)

# Prohibited workflow ID (old publish workflow, do not call)
PROHIBITED_WORKFLOW = "CWbGujhdNKFpa5JZ"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_latest_pre_publish() -> Path | None:
    """Find the most recent pre_publish JSON in content outputs."""
    if not CONTENT_OUTPUTS.exists():
        return None
    candidates = sorted(
        [p for p in CONTENT_OUTPUTS.glob("*_pre_publish.json")],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def split_markdown_to_sections(md: str) -> list[str]:
    """Split markdown by ## headings into sections for the article_draft payload."""
    sections = []
    current = ""
    for line in md.split("\n"):
        if line.startswith("## "):
            if current.strip():
                sections.append(current.strip())
            current = line + "\n"
        else:
            current += line + "\n"
    if current.strip():
        sections.append(current.strip())
    return sections if sections else [md]


def inline_markdown_to_html(text: str) -> str:
    """Convert a small safe subset of inline markdown to HTML."""
    escaped = html.escape(text.strip())
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped)
    return escaped


def markdown_to_wordpress_html(md: str) -> str:
    """Convert the customer article markdown into WordPress-friendly HTML.

    This intentionally avoids external dependencies so the bridge always sends
    a complete body to n8n even when Python markdown packages are unavailable.
    """
    blocks: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    ordered_items: list[str] = []
    table_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(f"<p>{inline_markdown_to_html(' '.join(paragraph))}</p>")
            paragraph = []

    def flush_lists() -> None:
        nonlocal list_items, ordered_items
        if list_items:
            blocks.append("<ul>" + "".join(f"<li>{inline_markdown_to_html(item)}</li>" for item in list_items) + "</ul>")
            list_items = []
        if ordered_items:
            blocks.append("<ol>" + "".join(f"<li>{inline_markdown_to_html(item)}</li>" for item in ordered_items) + "</ol>")
            ordered_items = []

    def flush_table() -> None:
        nonlocal table_lines
        if not table_lines:
            return
        rows = []
        for line in table_lines:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells and all(set(cell) <= {"-", ":", " "} for cell in cells):
                continue
            rows.append(cells)
        if rows:
            body = []
            for row_index, cells in enumerate(rows):
                tag = "th" if row_index == 0 else "td"
                body.append("<tr>" + "".join(f"<{tag}>{inline_markdown_to_html(cell)}</{tag}>" for cell in cells) + "</tr>")
            blocks.append("<table>" + "".join(body) + "</table>")
        table_lines = []

    for raw_line in md.splitlines():
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            flush_lists()
            flush_table()
            continue
        if line.startswith("|") and line.endswith("|"):
            flush_paragraph()
            flush_lists()
            table_lines.append(line)
            continue
        flush_table()
        if line.startswith("### "):
            flush_paragraph()
            flush_lists()
            blocks.append(f"<h3>{inline_markdown_to_html(line[4:])}</h3>")
        elif line.startswith("## "):
            flush_paragraph()
            flush_lists()
            blocks.append(f"<h2>{inline_markdown_to_html(line[3:])}</h2>")
        elif line.startswith("# "):
            flush_paragraph()
            flush_lists()
            blocks.append(f"<h1>{inline_markdown_to_html(line[2:])}</h1>")
        elif line.startswith("- "):
            flush_paragraph()
            ordered_items = []
            list_items.append(line[2:])
        elif re.match(r"^\d+\.\s+", line):
            flush_paragraph()
            list_items = []
            ordered_items.append(re.sub(r"^\d+\.\s+", "", line))
        else:
            flush_lists()
            paragraph.append(line)

    flush_paragraph()
    flush_lists()
    flush_table()
    return "\n".join(blocks)


def extract_summary(md: str) -> str:
    """Extract the first meaningful paragraph after any heading as summary."""
    lines = md.strip().split("\n")
    i = 0
    # Skip past all heading lines (#, ##) and blank lines
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#") or not line:
            i += 1
        else:
            break
    # Take first non-empty paragraph (up to 300 chars)
    summary = ""
    while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith("#"):
        summary += lines[i].strip() + " "
        i += 1
        if len(summary) > 300:
            break
    return summary.strip()[:300]


def build_publishing_payload(content: dict[str, Any]) -> dict[str, Any]:
    """Convert Content Center pre_publish JSON to Publishing Center V1 payload."""
    stamp = int(time.time() * 1000)
    ids = {
        "mission_id": content.get("mission_id", f"mission_bridge_{stamp}"),
        "publishing_mission_id": f"pub_bridge_{stamp}",
        "trace_id": f"trace_bridge_{stamp}",
    }

    title = content.get("title", "HK620 Article")
    md = content.get("draft_markdown", "")
    seo = content.get("seo", {})
    qa = content.get("qa", {})
    safety = content.get("safety", {})

    summary = extract_summary(md)
    sections = split_markdown_to_sections(md)
    content_html = markdown_to_wordpress_html(md)

    return {
        "mission_id": ids["mission_id"],
        "publishing_mission_id": ids["publishing_mission_id"],
        "trace_id": ids["trace_id"],
        "source": "pipeline_bridge_v1",
        "employee": "Publishing Agent",
        "priority": "P1",
        "provider": "wordpress_provider",
        "product": content.get("product", "HK620"),
        "market": content.get("target_market", "US"),
        "language": content.get("language", "en-US"),
        "title": title,
        "content_markdown": md,
        "content_html": content_html,
        "content": content_html,
        "article_draft": {
            "title": title,
            "slug": content.get("slug", ""),
            "meta_title": content.get("meta_title", seo.get("meta_title", title)),
            "meta_description": content.get("meta_description", seo.get("meta_description", "")),
            "primary_keyword": seo.get("primary_keyword", ""),
            "secondary_keywords": seo.get("secondary_keywords", []),
            "summary": summary,
            "sections": sections,
            "content_markdown": md,
            "content_html": content_html,
            "content": content_html,
            "content_html_length": len(content_html),
            "cta": seo.get("cta", "Contact SYUTECH for quotation and sample review."),
            "source_note": f"Generated by Content Center V3. Bridge at {now_iso()}.",
        },
        "qa_report": {
            "qa_standard": "Website Agent QA V2",
            "qa_score": qa.get("score", 0),
            "qa_status": "passed" if qa.get("score", 0) >= 90 else "failed",
            "reason": qa.get("gate", "QA completed"),
            "publish_allowed": False,  # Always requires CEO approval
        },
        "qa_score": qa.get("score", 0),
        "action": "create_wordpress_draft_only",
        "dry_run": False,
        "publish": False,
        "update_published_post": False,
        "delete_post": False,
        "send_gmail": False,
        "upload_youtube": False,
        "workflow_path": "m8a-hk620-draft-only",
        "prohibited_workflow": PROHIBITED_WORKFLOW,
        "safety": {
            "draft_only": True,
            "publish": False,
            "delete_post": False,
            "update_published_post": False,
            "send_gmail": False,
            "upload_youtube": False,
            "prohibited_workflow": PROHIBITED_WORKFLOW,
        },
        "content_source": {
            "file": content.get("_source_file", "unknown"),
            "content_package_id": content.get("content_package_id", ""),
            "agent": content.get("agent", ""),
            "created_at": content.get("created_at", ""),
        },
        "open_gaps": content.get("open_gaps_before_publish", []),
    }


def call_n8n_webhook(payload: dict[str, Any], webhook_url: str) -> tuple[int | None, dict[str, Any], str | None]:
    """Call n8n webhook with the publishing payload."""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        webhook_url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "application/json",
            "Cache-Control": "no-cache",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw or "{}"), None
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"raw": raw}
        return exc.code, parsed, str(exc)
    except Exception as exc:
        return None, {}, str(exc)


def run(source_path: str | None, execute: bool = False, publish: bool = False) -> dict[str, Any]:
    """Main bridge execution."""
    # Find source file
    if source_path:
        src = Path(source_path)
    else:
        src = find_latest_pre_publish()
        if src is None:
            return {
                "success": False,
                "error": "No pre_publish JSON found. Provide a file path or generate content first.",
                "searched_dir": str(CONTENT_OUTPUTS),
            }

    if not src.exists():
        return {"success": False, "error": f"File not found: {src}"}

    # Read and validate
    content = read_json(src)
    content["_source_file"] = str(src)

    # Check QA gate
    qa = content.get("qa", {})
    qa_score = qa.get("score", 0)
    qa_gate = qa.get("gate", "")
    if qa_score < 90:
        return {
            "success": False,
            "error": f"QA score {qa_score} < 90. Content not ready for publishing.",
            "qa_gate": qa_gate,
            "source_file": str(src),
        }

    # Build payload
    payload = build_publishing_payload(content)

    # Dry-run mode
    if not execute:
        result = {
            "success": True,
            "mode": "dry_run",
            "source_file": str(src),
            "content_package_id": content.get("content_package_id", ""),
            "title": payload["title"],
            "qa_score": qa_score,
            "payload": payload,
            "next_step": "Run with --execute to create WordPress Draft. Then use --publish for CEO-approved publishing.",
        }
        write_json(BRIDGE_RESULT_PATH, result)
        return result

    # Execute: call n8n Draft webhook
    started_at = now_iso()
    http_status, response, error = call_n8n_webhook(payload, DRAFT_WEBHOOK)
    finished_at = now_iso()

    # Parse n8n response
    result_block = response.get("result", {}) if isinstance(response.get("result"), dict) else {}
    post_id = result_block.get("post_id") or response.get("post_id")
    draft_url = result_block.get("draft_url") or response.get("draft_url")
    edit_url = result_block.get("edit_url") or response.get("edit_url")
    success = bool(response.get("success")) and bool(post_id) and bool(draft_url)

    result = {
        "success": success,
        "mode": "executed",
        "source_file": str(src),
        "content_package_id": content.get("content_package_id", ""),
        "title": payload["title"],
        "qa_score": qa_score,
        "publishing_mission_id": payload["publishing_mission_id"],
        "mission_id": payload["mission_id"],
        "execution_id": str(response.get("execution_id", "")),
        "provider": "wordpress",
        "resource_type": "wordpress_draft",
        "status": "completed" if success else "failed",
        "post_id": post_id,
        "draft_url": draft_url,
        "edit_url": edit_url,
        "started_at": started_at,
        "finished_at": finished_at,
        "http_status": http_status,
        "error": None if success else {
            "error_code": response.get("error_code", "WORDPRESS_DRAFT_FAILED"),
            "error_message": error or response.get("error_message", "Webhook call failed."),
        },
        "raw_response": response,
        "safety": payload["safety"],
        "ceo_approval_required": True,
        "ceo_action": f"Draft created. Review at {edit_url or draft_url}. Approve to publish.",
    }

    write_json(BRIDGE_RESULT_PATH, result)

    # Also write to external executor's result path for Commander to read
    ext_path = ROOT / "apps" / "commander" / "external_executor_v1" / "real_execution" / "last_bridge_result.v1.json"
    write_json(ext_path, result)

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Content Center → Publishing Center Bridge"
    )
    parser.add_argument(
        "source",
        nargs="?",
        help="Path to pre_publish.json. Omit with --latest to auto-find.",
    )
    parser.add_argument(
        "--execute", action="store_true",
        help="Actually call the n8n Draft webhook (default: dry-run)."
    )
    parser.add_argument(
        "--latest", action="store_true",
        help="Auto-find the most recent pre_publish.json."
    )
    parser.add_argument(
        "--publish", action="store_true",
        help="Publish the draft after creation (requires CEO approval)."
    )
    args = parser.parse_args()

    source_path = None if args.latest else args.source
    result = run(source_path, execute=args.execute, publish=args.publish)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
