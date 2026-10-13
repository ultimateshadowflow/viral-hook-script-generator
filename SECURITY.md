# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.4.x   | yes       |
| 0.3.x   | security fixes only |
| < 0.3   | no        |

## Reporting a vulnerability

Open a private security advisory on GitHub, or email the maintainer listed
in `pyproject.toml`. Do not open a public issue for anything that leaks
API keys, allows prompt injection to reach the filesystem, or lets a
provider adapter exfiltrate user topics.

## Threat model

This tool talks to third-party LLM APIs and writes generated scripts to
disk. The relevant attack surface:

- **Prompt injection via topic field.** A topic string is untrusted input.
  It is sanitized in `utils/sanitizers.py` before it ever reaches a
  provider. Do not bypass that layer.
- **Provider key leakage.** Keys are loaded from env or `config.local.toml`
  (gitignored). Logs redact anything matching `sk-` / `Bearer`.
- **Path traversal in export.** `services/export_services/` refuses to
  write outside the configured `output_dir`. Report any bypass.
- **Malicious provider response.** Responses are parsed as structured
  data, never `eval`'d. JSON parse failures are caught and surfaced, not
  silently retried into a loop.

## Out of scope

- Content policy of the downstream platforms. That's the operator's job.
- Rate limit bans from providers. Use your own keys, read their ToS.