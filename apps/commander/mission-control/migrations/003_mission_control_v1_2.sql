BEGIN;

ALTER TABLE commander_tasks
  ADD COLUMN IF NOT EXISTS retry_count integer NOT NULL DEFAULT 0;

ALTER TABLE commander_artifacts
  ADD COLUMN IF NOT EXISTS simulation_status text NOT NULL DEFAULT 'not_applicable',
  ADD COLUMN IF NOT EXISTS payload_snapshot jsonb NOT NULL DEFAULT '{}'::jsonb;

ALTER TABLE commander_approvals
  ADD COLUMN IF NOT EXISTS decision_reason text,
  ADD COLUMN IF NOT EXISTS decided_by text,
  ADD COLUMN IF NOT EXISTS payload_snapshot jsonb NOT NULL DEFAULT '{}'::jsonb;

UPDATE commander_artifacts
SET payload_snapshot = COALESCE(content_json, '{}'::jsonb),
    simulation_status = CASE
      WHEN artifact_type = 'draft_payload' AND content_json->>'platform' = 'wordpress' THEN 'approval_required'
      ELSE simulation_status
    END
WHERE payload_snapshot = '{}'::jsonb;

UPDATE commander_approvals
SET payload_snapshot = COALESCE(request_payload, '{}'::jsonb),
    decision_reason = COALESCE(decision_reason, decision_note),
    decided_by = CASE WHEN decided_at IS NOT NULL THEN COALESCE(decided_by, approver_name) ELSE decided_by END
WHERE payload_snapshot = '{}'::jsonb OR decision_reason IS NULL OR decided_by IS NULL;

COMMIT;
