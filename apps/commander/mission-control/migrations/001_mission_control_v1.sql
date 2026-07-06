BEGIN;

CREATE TABLE IF NOT EXISTS commander_missions (
  mission_id text PRIMARY KEY,
  mission_name text NOT NULL,
  mission_key text NOT NULL,
  priority text NOT NULL CHECK (priority IN ('P0', 'P1', 'P2', 'P3')),
  status text NOT NULL CHECK (status IN ('created', 'queued', 'claimed', 'running', 'completed', 'failed', 'waiting_approval', 'archived')),
  command_text text NOT NULL,
  planner_version text NOT NULL,
  input jsonb NOT NULL DEFAULT '{}'::jsonb,
  output jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_by text NOT NULL DEFAULT '石总',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  started_at timestamptz,
  completed_at timestamptz,
  archived_at timestamptz
);

CREATE TABLE IF NOT EXISTS commander_workers (
  worker_id text PRIMARY KEY,
  name text NOT NULL UNIQUE,
  role text NOT NULL,
  capabilities jsonb NOT NULL DEFAULT '[]'::jsonb,
  allowed_actions jsonb NOT NULL DEFAULT '[]'::jsonb,
  forbidden_actions jsonb NOT NULL DEFAULT '[]'::jsonb,
  approval_policy jsonb NOT NULL DEFAULT '{}'::jsonb,
  status text NOT NULL CHECK (status IN ('active', 'paused', 'retired')),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS commander_tasks (
  task_id text PRIMARY KEY,
  mission_id text NOT NULL REFERENCES commander_missions(mission_id) ON DELETE CASCADE,
  parent_task_id text REFERENCES commander_tasks(task_id),
  worker_id text NOT NULL REFERENCES commander_workers(worker_id),
  worker_name text NOT NULL,
  task_order integer NOT NULL,
  title text NOT NULL,
  action text NOT NULL,
  status text NOT NULL CHECK (status IN ('created', 'queued', 'claimed', 'running', 'completed', 'failed', 'waiting_approval', 'archived')),
  input jsonb NOT NULL DEFAULT '{}'::jsonb,
  output jsonb NOT NULL DEFAULT '{}'::jsonb,
  requires_approval boolean NOT NULL DEFAULT false,
  approval_reason text,
  claimed_by text,
  error_message text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  claimed_at timestamptz,
  started_at timestamptz,
  completed_at timestamptz,
  failed_at timestamptz,
  archived_at timestamptz,
  UNIQUE (mission_id, task_order)
);

CREATE TABLE IF NOT EXISTS commander_task_events (
  event_id text PRIMARY KEY,
  mission_id text NOT NULL REFERENCES commander_missions(mission_id) ON DELETE CASCADE,
  task_id text REFERENCES commander_tasks(task_id) ON DELETE CASCADE,
  event_type text NOT NULL,
  from_status text,
  to_status text,
  actor text NOT NULL DEFAULT 'mission_control',
  event_message text NOT NULL,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS commander_artifacts (
  artifact_id text PRIMARY KEY,
  mission_id text NOT NULL REFERENCES commander_missions(mission_id) ON DELETE CASCADE,
  task_id text REFERENCES commander_tasks(task_id) ON DELETE SET NULL,
  artifact_type text NOT NULL CHECK (artifact_type IN ('markdown', 'html', 'json', 'draft_payload', 'report')),
  title text NOT NULL,
  content_json jsonb,
  content_uri text,
  created_by text NOT NULL DEFAULT 'mission_control',
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS commander_approvals (
  approval_id text PRIMARY KEY,
  mission_id text NOT NULL REFERENCES commander_missions(mission_id) ON DELETE CASCADE,
  task_id text NOT NULL REFERENCES commander_tasks(task_id) ON DELETE CASCADE,
  artifact_id text REFERENCES commander_artifacts(artifact_id) ON DELETE SET NULL,
  approval_type text NOT NULL,
  status text NOT NULL CHECK (status IN ('pending', 'approved', 'rejected', 'cancelled')),
  approver_name text NOT NULL DEFAULT '石总',
  request_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  decision_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  decision_note text,
  created_at timestamptz NOT NULL DEFAULT now(),
  decided_at timestamptz
);

CREATE TABLE IF NOT EXISTS commander_locks (
  lock_id text PRIMARY KEY,
  resource_type text NOT NULL,
  resource_id text NOT NULL,
  locked_by text NOT NULL,
  lock_status text NOT NULL CHECK (lock_status IN ('active', 'released', 'expired')),
  locked_at timestamptz NOT NULL DEFAULT now(),
  expires_at timestamptz,
  released_at timestamptz,
  UNIQUE (resource_type, resource_id, lock_status)
);

CREATE INDEX IF NOT EXISTS idx_commander_missions_status ON commander_missions(status);
CREATE INDEX IF NOT EXISTS idx_commander_tasks_mission_status ON commander_tasks(mission_id, status);
CREATE INDEX IF NOT EXISTS idx_commander_task_events_mission ON commander_task_events(mission_id, created_at);
CREATE INDEX IF NOT EXISTS idx_commander_artifacts_mission ON commander_artifacts(mission_id, created_at);
CREATE INDEX IF NOT EXISTS idx_commander_approvals_status ON commander_approvals(status, created_at);

INSERT INTO commander_workers (
  worker_id, name, role, capabilities, allowed_actions, forbidden_actions, approval_policy, status
) VALUES
('worker_knowledge_manager', 'Knowledge Manager', 'Product knowledge checker',
 '["read_product_knowledge", "check_coverage", "summarize_gaps"]'::jsonb,
 '["read_hk620_product_knowledge"]'::jsonb,
 '["approve_public_claims", "publish_content", "connect_external_platforms"]'::jsonb,
 '{"requires_ceo_approval_for":["public_knowledge_approval"]}'::jsonb, 'active'),
('worker_content_operator', 'Content Operator', 'Content draft producer',
 '["generate_content_structure", "prepare_landing_page_outline", "prepare_faq"]'::jsonb,
 '["generate_english_landing_page_structure"]'::jsonb,
 '["auto_publish", "invent_product_facts", "bypass_review"]'::jsonb,
 '{"requires_ceo_approval_for":["public_content_use"]}'::jsonb, 'active'),
('worker_website_operator', 'Website Operator', 'Website draft preparer',
 '["prepare_wordpress_draft_payload", "validate_publish_payload"]'::jsonb,
 '["generate_wordpress_draft_payload"]'::jsonb,
 '["publish_wordpress", "connect_wordpress_without_approval"]'::jsonb,
 '{"requires_ceo_approval_for":["wordpress_draft", "wordpress_publish"]}'::jsonb, 'active'),
('worker_distribution_operator', 'Distribution Operator', 'Social distribution draft preparer',
 '["prepare_social_drafts", "prepare_video_distribution_checklist"]'::jsonb,
 '["generate_social_distribution_drafts"]'::jsonb,
 '["publish_social", "connect_social_platforms"]'::jsonb,
 '{"requires_ceo_approval_for":["social_distribution"]}'::jsonb, 'active'),
('worker_sales_assistant', 'Sales Assistant', 'Sales and customer reply drafter',
 '["generate_whatsapp_reply_draft", "retrieve_product_context"]'::jsonb,
 '["generate_whatsapp_inquiry_reply"]'::jsonb,
 '["send_customer_reply", "quote_price_without_approval"]'::jsonb,
 '{"requires_ceo_approval_for":["customer_reply"]}'::jsonb, 'active'),
('worker_business_analyst', 'Business Analyst', 'Market and mission analysis',
 '["market_direction_summary", "mission_summary", "priority_analysis"]'::jsonb,
 '["generate_us_market_direction", "generate_mission_summary"]'::jsonb,
 '["claim_external_data_without_source", "connect_analytics_platforms"]'::jsonb,
 '{"requires_ceo_approval_for":[]}'::jsonb, 'active')
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
