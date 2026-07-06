# M8A AI Change Control Policy

Date: 2026-07-06

## Purpose

This policy defines how AI-assisted code changes are controlled inside M8A.

The goal is to let AI move fast without bypassing Git, QA, CEO Approval, or M8A safety boundaries.

## Rules

1. AI may create local branches for scoped work.

2. AI may create commits on a local feature branch after tests and safety checks pass.

3. AI may not merge into `main` by itself.

4. AI may not push.

5. AI may not create or configure a Git remote.

6. AI may not use `git add -f` unless CEO explicitly approves it for a specific file.

7. Files blocked by `.gitignore` should be renamed, moved out of commit scope, or excluded by default. Force-adding ignored files is not the default path.

8. The following must never be committed:

- `.env`
- real tokens
- real passwords
- real credentials
- real secrets
- WordPress Application Passwords
- API keys
- private keys
- database dumps
- raw logs containing secrets

9. Runtime result files are not committed by default unless they are approved example files, fixture files, or audit reports.

10. Merging into `main` requires CEO Approval.

11. Every workspace-write task must start with `git status`.

12. Every workspace-write task must end with:

- tests
- sensitive value scan
- `git status`
- `git diff --stat`
- human-readable summary

13. AI may not modify Commander Console Home, Mission Control lifecycle, Worker Runner architecture, Exception Framework core, or Approval lifecycle unless the CEO explicitly authorizes that scope.

14. AI may not connect external platforms, publish content, deploy code, create pull requests, or run production actions without explicit CEO approval.

15. AI must not output secret values in reports, logs, chat, or artifacts.

## Required Review Before Main Merge

Before a branch is merged into `main`, the CEO should review:

- branch name
- changed file list
- test output
- sensitive scan result
- `git diff --stat`
- whether any ignored file was force-added
- whether any V1 frozen module was touched
- whether any external platform was called
- whether any real credential was used

## Default Decision

If there is uncertainty about secrets, external actions, or frozen architecture boundaries, the default decision is:

Do not merge.

Create an Exception or review task instead.
