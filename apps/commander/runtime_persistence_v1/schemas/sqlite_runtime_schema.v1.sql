-- M8A Local Runtime Persistence V1
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS missions (
  mission_id TEXT PRIMARY KEY,
  mission_type TEXT NOT NULL,
  priority TEXT NOT NULL,
  owner_agent TEXT NOT NULL,
  supporting_agents TEXT,
  reviewer TEXT,
  approver TEXT,
  status TEXT NOT NULL,
  knowledge_status TEXT,
  qa_status TEXT,
  approval_status TEXT,
  publish_status TEXT,
  retry_count INTEGER DEFAULT 0,
  created_at TEXT,
  updated_at TEXT,
  payload_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mission_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id TEXT UNIQUE NOT NULL,
  mission_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  source_agent TEXT,
  target_agent TEXT,
  priority TEXT,
  status TEXT,
  timestamp TEXT NOT NULL,
  retry_count INTEGER DEFAULT 0,
  payload_json TEXT NOT NULL,
  event_hash TEXT NOT NULL,
  FOREIGN KEY(mission_id) REFERENCES missions(mission_id)
);

CREATE TABLE IF NOT EXISTS event_history (
  event_id TEXT PRIMARY KEY,
  mission_id TEXT NOT NULL,
  agent_index TEXT,
  event_type TEXT NOT NULL,
  event_date TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  event_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS employee_queues (
  queue_item_id TEXT PRIMARY KEY,
  mission_id TEXT NOT NULL,
  employee_id TEXT NOT NULL,
  status TEXT NOT NULL,
  priority TEXT,
  expected_output TEXT,
  acceptance_criteria TEXT,
  blocks_public_publish INTEGER DEFAULT 0,
  created_at TEXT,
  updated_at TEXT
);

CREATE TABLE IF NOT EXISTS employee_status (
  employee_id TEXT PRIMARY KEY,
  employee_name TEXT,
  current_task TEXT,
  todo_count INTEGER DEFAULT 0,
  today_completed INTEGER DEFAULT 0,
  average_runtime TEXT,
  failed_count INTEGER DEFAULT 0,
  average_qa_score REAL DEFAULT 0,
  blocked_count INTEGER DEFAULT 0,
  updated_at TEXT
);

CREATE TABLE IF NOT EXISTS mission_timeline (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mission_id TEXT NOT NULL,
  event_name TEXT NOT NULL,
  event_time TEXT NOT NULL,
  agent_id TEXT,
  message TEXT,
  payload_json TEXT
);

CREATE TABLE IF NOT EXISTS approvals (
  approval_id TEXT PRIMARY KEY,
  mission_id TEXT NOT NULL,
  approver TEXT NOT NULL,
  approval_status TEXT NOT NULL,
  requested_at TEXT,
  decided_at TEXT,
  payload_json TEXT
);

CREATE TABLE IF NOT EXISTS qa_results (
  qa_result_id TEXT PRIMARY KEY,
  mission_id TEXT NOT NULL,
  reviewer TEXT,
  qa_status TEXT NOT NULL,
  qa_score REAL DEFAULT 0,
  checked_at TEXT,
  payload_json TEXT
);

CREATE TABLE IF NOT EXISTS runtime_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  log_time TEXT NOT NULL,
  level TEXT NOT NULL,
  component TEXT NOT NULL,
  message TEXT NOT NULL,
  payload_json TEXT
);

CREATE TABLE IF NOT EXISTS retry_records (
  retry_id TEXT PRIMARY KEY,
  mission_id TEXT,
  event_id TEXT,
  reason TEXT NOT NULL,
  retry_count INTEGER DEFAULT 0,
  max_retry INTEGER DEFAULT 0,
  status TEXT NOT NULL,
  created_at TEXT,
  updated_at TEXT,
  payload_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_mission_events_mission ON mission_events(mission_id);
CREATE INDEX IF NOT EXISTS idx_mission_events_agent ON mission_events(source_agent, target_agent);
CREATE INDEX IF NOT EXISTS idx_mission_events_type ON mission_events(event_type);
CREATE INDEX IF NOT EXISTS idx_event_history_date ON event_history(event_date);
CREATE INDEX IF NOT EXISTS idx_employee_queues_employee ON employee_queues(employee_id);
CREATE INDEX IF NOT EXISTS idx_timeline_mission ON mission_timeline(mission_id);
