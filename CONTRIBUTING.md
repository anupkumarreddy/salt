# Contributing

Thanks for taking the time to improve SALT.

## Development Setup

SALT requires Python 3.11 or newer.

```bash
python3 -m venv .venv
./.venv/bin/pip install -e ".[dev]"
```

## Run Checks

```bash
./.venv/bin/python -m pytest
./.venv/bin/python -m salt check examples/demo --config examples/salt.yaml
```

## Pull Requests

- Keep changes focused on one bug, rule, reporter, or documentation topic.
- Add or update tests when changing behavior.
- Update `docs/rules.md` when adding or changing lint rules.
- Include sample input for new SystemVerilog or UVM checks when practical.
- Make sure generated reports, virtual environments, caches, and IDE files stay out of commits.

## Adding Rules

Rules live under `salt/rules/` and should follow the existing `Rule` classes. Prefer small, explicit checks that report a clear message and severity. SALT is a lightweight scanner, so rules should avoid implying full parser accuracy.
