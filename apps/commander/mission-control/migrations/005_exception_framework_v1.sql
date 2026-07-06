BEGIN;

CREATE TABLE IF NOT EXISTS commander_exceptions (
  exception_id text PRIMARY KEY,
  exception_mission_id text REFERENCES commander_missions(mission_id) ON DELETE SET NULL,
  source_mission_id text REFERENCES commander_missions(mission_id) ON DELETE SET NULL,
  source_task_id text REFERENCES commander_tasks(task_id) ON DELETE SET NULL,
  source_system text NOT NULL,
  exception_type text NOT NULL,
  error_code text,
  error_message text NOT NULL,
  severity text NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
  risk_level text NOT NULL CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
  status text NOT NULL CHECK (status IN ('new', 'investigating', 'waiting_approval', 'resolved', 'ignored', 'archived')),
  assigned_worker_id text REFERENCES commander_workers(worker_id) ON DELETE SET NULL,
  assigned_worker_name text NOT NULL DEFAULT 'Infrastructure Operator',
  requires_ceo_approval boolean NOT NULL DEFAULT false,
  recovery_plan jsonb NOT NULL DEFAULT '{}'::jsonb,
  impact_scope jsonb NOT NULL DEFAULT '{}'::jsonb,
  root_cause_hypothesis jsonb NOT NULL DEFAULT '[]'::jsonb,
  resolution_note text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  resolved_at timestamptz,
  archived_at timestamptz
);

CREATE TABLE IF NOT EXISTS commander_exception_events (
  exception_event_id text PRIMARY KEY,
  exception_id text NOT NULL REFERENCES commander_exceptions(exception_id) ON DELETE CASCADE,
  event_type text NOT NULL,
  from_status text,
  to_status text,
  actor text NOT NULL DEFAULT 'exception_framework',
  event_message text NOT NULL,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_commander_exceptions_status ON commander_exceptions(status, created_at);
CREATE INDEX IF NOT EXISTS idx_commander_exceptions_source_task ON commander_exceptions(source_task_id);
CREATE INDEX IF NOT EXISTS idx_commander_exception_events_exception ON commander_exception_events(exception_id, created_at);

INSERT INTO commander_workers (
  worker_id, name, role, capabilities, allowed_actions, forbidden_actions, approval_policy, status
) VALUES (
  'worker_infrastructure_operator',
  'Infrastructure Operator',
  'Infrastructure, platform, network, security, and API exception investigator',
  '["analyze_cloudflare", "analyze_dns", "analyze_ssl", "analyze_rest_api", "analyze_oauth", "analyze_webhook", "analyze_wordpress", "analyze_network", "analyze_security", "generate_recovery_plan"]'::jsonb,
  '["create_exception_mission", "generate_recovery_plan", "request_ceo_approval", "mark_exception_resolved", "mark_exception_ignored"]'::jsonb,
  '["publish_content", "delete_external_content", "disable_security_controls_without_approval", "store_secrets_in_reports"]'::jsonb,
  '{"requires_ceo_approval_for":["cloudflare_bypass", "security_policy_change", "production_dns_change", "oauth_scope_change"]}'::jsonb,
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

