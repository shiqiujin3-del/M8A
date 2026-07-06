BEGIN;

ALTER TABLE commander_artifacts
  DROP CONSTRAINT IF EXISTS commander_artifacts_artifact_type_check;

ALTER TABLE commander_artifacts
  ADD CONSTRAINT commander_artifacts_artifact_type_check
  CHECK (artifact_type IN ('markdown', 'html', 'json', 'draft_payload', 'report', 'wordpress_draft'));

COMMIT;

