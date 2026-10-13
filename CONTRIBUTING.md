# Contributing to viral-hook-script-generator

Thanks for wanting to push the hook engine forward. This repo is a Python
desktop tool that turns a topic + platform + tone into a batch of viral
hook candidates and short-form scripts. Contributions are welcome from
prompt engineers, platform-API wranglers, and anyone who has actually
watched a reel die in the first 1.8 seconds.

## Ground rules

- One feature per PR. Keep diffs reviewable.
- Every new provider (LLM backend, platform adapter) ships with a fixture
  under `tests/fixtures/` and at least one assertion in the suite.
- No prompt changes without a before/after sample in the PR description.
- Type hints are required on all public functions. `mypy --strict` is the
  bar; if you can't hit it, say why in the PR.
- Don't hardcode API keys. Everything comes through `config/` or env vars.

## Dev setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
```

## Commit style

Conventional commits: `feat(hooks): add tiktok cold-open template`,
`fix(services): clamp virality score to [0,100]`, `docs(config): explain
provider fallback order`.

## Prompt review

Prompts live in `services/prompt_services/`. They are code. Treat them
like code. If a prompt change alters output distribution meaningfully,
flag it in the PR title with `[PROMPT]`.

## Code of conduct

Be normal. Disagree about architecture, not about people.