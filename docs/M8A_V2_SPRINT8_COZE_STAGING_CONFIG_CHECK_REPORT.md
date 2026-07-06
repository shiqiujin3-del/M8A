# M8A V2 Sprint 8: Coze Staging Credential Check V1 Report

Date: 2026-07-06

## Objective

Prepare the next step before real Coze API verification by checking whether Coze staging credentials are configured.

This sprint does not call Coze.

This sprint does not read `.env` directly.

This sprint does not print token values.

## Branch

`sprint/coze-staging-credential-check-v1`

## New Files

- `/Users/shiqiujing/Documents/M8A/apps/commander/agent-dispatcher/providers/check_coze_config.py`
- `/Users/shiqiujing/Documents/M8A/apps/commander/agent-dispatcher/providers/test_check_coze_config.py`
- `/Users/shiqiujing/Documents/M8A/docs/M8A_V2_SPRINT8_COZE_STAGING_CONFIG_CHECK_REPORT.md`

## Modified Files

- `/Users/shiqiujing/Documents/M8A/.env.example`

Added placeholder fields only:

```text
M8A_COZE_BASE_URL=
M8A_COZE_API_TOKEN=
M8A_COZE_WORKFLOW_ID=
M8A_COZE_WORKSPACE_ID=
```

No real credential was written.

## Check Command

```bash
python3 apps/commander/agent-dispatcher/providers/check_coze_config.py
```

## Check Result

```text
M8A_COZE_BASE_URL missing
M8A_COZE_API_TOKEN missing
M8A_COZE_WORKFLOW_ID missing
M8A_COZE_WORKSPACE_ID missing
not_ready
```

Current Coze staging readiness:

`not_ready`

Required missing fields:

- `M8A_COZE_BASE_URL`
- `M8A_COZE_API_TOKEN`
- `M8A_COZE_WORKFLOW_ID`

Optional missing field:

- `M8A_COZE_WORKSPACE_ID`

## Test Command

```bash
python3 apps/commander/agent-dispatcher/providers/test_check_coze_config.py
```

## Test Result

PASS

3 tests passed.

Validated:

- Missing required values return `not_ready`.
- Required values return `ready` without exposing token value.
- Optional workspace ID does not block readiness.
- API call flag remains false.
- Secret printing flag remains false.

## Safety Confirmation

- Coze API called: NO
- External platform called: NO
- `.env` file read: NO
- Token value printed: NO
- Real credential written: NO
- Commander Console modified: NO
- Mission Control lifecycle modified: NO
- Worker Runner modified: NO
- Exception Framework modified: NO

## Next Step

Fill local environment variables only after CEO approves Coze staging verification:

```bash
export M8A_COZE_BASE_URL="..."
export M8A_COZE_API_TOKEN="..."
export M8A_COZE_WORKFLOW_ID="..."
```

Then rerun:

```bash
python3 apps/commander/agent-dispatcher/providers/check_coze_config.py
```

Only when the script returns `ready` should M8A proceed to a separate real read-only Coze API verification mission.

## Recommendation

Do not call Coze API yet.

Recommendation: wait until staging variables are configured and then run a credential presence check again.
