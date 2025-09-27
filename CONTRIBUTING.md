# Contributing

Thanks for helping improve the Playwright AI Browser Use showcase! This document explains how to propose changes while keeping the repository healthy and deterministic.

## Development Workflow

1. **Create a feature branch** using the agreed naming scheme: `feat/*`, `fix/*`, `test/*`, `ci/*`, or `docs/*`.
2. **Install tooling**: `pip install -r requirements-dev.txt` and run `pre-commit install`.
3. **Write code & tests**:
   - Follow the existing Page Object + Flow structure.
   - Use deterministic data factories from `utils/data.py`.
   - Keep selectors resilient and avoid `time.sleep`; leverage Playwright expectations.
4. **Run local checks** before committing:
   ```bash
   pre-commit run --all-files
   pytest -m "regression" --browser chromium -n auto
   ```
5. **Use Conventional Commits** for every commit message:
   - `feat: add parabank negative transfer coverage`
   - `fix: stabilize demoblaze cart flow`
   - `docs: update README for AI usage`

## Pull Request Checklist

- [ ] Tests added/updated and `pytest -m "regression"` passes locally in stub mode
- [ ] Linting (`ruff`, `black`, `isort`) and typing (`mypy --strict`) succeed
- [ ] Security scan (`bandit -c pyproject.toml -r .`) passes
- [ ] Documentation / baselines updated if behavior changed
- [ ] No secrets or credentials committed
- [ ] Relevant artifacts (screenshots, transcripts) reviewed and attached if necessary

## Handling Flaky Tests

- Flaky tests **must** be marked with `@pytest.mark.flaky` and optionally configured with `pytest-retry` parameters.
- Document the instability in the test docstring and open an issue for remediation.
- Flaky tests remain part of CI results; they cannot silently pass.

## Adding AI Agent Scenarios

- Define prompts in natural language referencing allow-listed domains only.
- Update or add playbooks under `agents/playbooks/` for reusable instruction sets.
- Ensure transcripts are saved via `agent_runner` fixture to `reports/ai_transcripts/<TC-ID>.jsonl`.
- Provide stub expectations so CI remains deterministic without API keys.

## Reporting Issues

When filing bugs or feature requests, include:

- Scenario / TC identifier
- Environment (OS, browser, agent mode)
- Steps to reproduce and expected vs actual results
- Relevant artifacts (trace, screenshot, transcript, logs)

Happy testing! 🚀
