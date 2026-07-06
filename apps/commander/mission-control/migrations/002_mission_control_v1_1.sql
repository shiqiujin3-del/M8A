BEGIN;

ALTER TABLE commander_missions
  ADD COLUMN IF NOT EXISTS title text,
  ADD COLUMN IF NOT EXISTS objective text,
  ADD COLUMN IF NOT EXISTS product text,
  ADD COLUMN IF NOT EXISTS market text,
  ADD COLUMN IF NOT EXISTS risk_level text NOT NULL DEFAULT 'medium';

ALTER TABLE commander_tasks
  ADD COLUMN IF NOT EXISTS risk_level text NOT NULL DEFAULT 'medium';

ALTER TABLE commander_artifacts
  ADD COLUMN IF NOT EXISTS quality_score numeric;

ALTER TABLE commander_approvals
  ADD COLUMN IF NOT EXISTS platform text NOT NULL DEFAULT 'internal',
  ADD COLUMN IF NOT EXISTS action_type text,
  ADD COLUMN IF NOT EXISTS risk_level text NOT NULL DEFAULT 'high',
  ADD COLUMN IF NOT EXISTS approved_at timestamptz;

UPDATE commander_missions
SET title = COALESCE(title, mission_name),
    objective = COALESCE(objective, command_text),
    product = COALESCE(product, input->>'product'),
    market = COALESCE(market, input->>'market'),
    updated_at = now()
WHERE title IS NULL OR objective IS NULL OR product IS NULL OR market IS NULL;

UPDATE commander_tasks
SET risk_level = CASE WHEN requires_approval THEN 'high' ELSE 'medium' END
WHERE risk_level IS NULL OR risk_level = 'medium';

UPDATE commander_artifacts
SET quality_score = COALESCE(quality_score, 0.8)
WHERE quality_score IS NULL;

UPDATE commander_approvals
SET action_type = COALESCE(action_type, approval_type),
    platform = CASE
      WHEN approval_type LIKE '%wordpress%' THEN 'WordPress'
      WHEN approval_type LIKE '%social%' THEN 'Social'
      WHEN approval_type LIKE '%whatsapp%' THEN 'WhatsApp'
      ELSE platform
    END,
    approved_at = CASE WHEN status = 'approved' THEN COALESCE(approved_at, decided_at) ELSE approved_at END
WHERE action_type IS NULL OR approved_at IS NULL;

COMMIT;
