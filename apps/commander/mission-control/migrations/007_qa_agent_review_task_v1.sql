BEGIN;

ALTER TABLE commander_artifacts
  DROP CONSTRAINT IF EXISTS commander_artifacts_artifact_type_check;

ALTER TABLE commander_artifacts
  ADD CONSTRAINT commander_artifacts_artifact_type_check
  CHECK (artifact_type IN ('markdown', 'html', 'json', 'draft_payload', 'report', 'wordpress_draft', 'agent_plan', 'qa_review_result'));

INSERT INTO commander_workers (
  worker_id, name, role, capabilities, allowed_actions, forbidden_actions, approval_policy, status
) VALUES (
  'worker_qa_agent',
  'QA Agent',
  'Quality assurance review agent for COTAS/Codex results and implementation plans',
  '["qa_review_cotas_result", "validate_result_schema", "check_forbidden_actions", "check_secret_leakage", "check_external_platform_safety", "generate_qa_result"]'::jsonb,
  '["qa_review_cotas_result"]'::jsonb,
  '["call_external_platform", "publish_content", "store_secrets", "approve_without_ceo", "modify_production_system"]'::jsonb,
  '{"requires_ceo_approval_for":["qa_result_acceptance", "implementation_go_ahead"]}'::jsonb,
  'active'
)
ON CONFLICT (worker_id) DO UPDATE SET
  name = EXCLUDED.name,
  role = EXCLUDED.role,
  capabilities = EXCLUDED.capabilities,
  allowed_actions = EXCLUDED.allowed_actions,
  forbidden_actions = EXCLUDED.forbidden_actions,
  approval_policy = EXCLUDED.approval_policy,
  status = EXCLUDED.status,
  updated_at = now();

COMMIT;

