# 06 Security Plan

## Secrets Policy
- Never commit real API keys or passwords.
- Use `.env.example` only for placeholders.
- Store real local secrets in ignored files under `env/`.

## Access Control
- Separate local test, staging, and production credentials.
- Use least privilege for all API accounts.
- Avoid sharing admin credentials between services.

## External Connections
- OpenAI, Anthropic, Google, WordPress, GitHub, and social platforms require explicit approval before connection.

## Logging Rules
- Do not log secrets.
- Mask tokens, passwords, and personally identifiable data.

## Review Checklist
To be completed before production deployment.
