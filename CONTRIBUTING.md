# Contributing to QuantEcon Style Guide Checker

Thank you for your interest in contributing! 🎉

> **📖 Full developer guide:** The complete, up-to-date guide — development
> setup, adding rules and categories, testing, and the release process — lives
> in [`docs/developer/contributing.md`](docs/developer/contributing.md). This
> page is a quick summary.

## Quick Start

The project uses [uv](https://docs.astral.sh/uv/) to manage Python, the
virtualenv, and dependencies.

```bash
git clone https://github.com/QuantEcon/action-style-guide.git
cd action-style-guide

# uv reads pyproject.toml + uv.lock and creates a .venv automatically.
# --all-extras installs PyGithub (action) + pytest/ruff (dev).
uv sync --all-extras

# Run commands via `uv run` (no need to activate the venv):
uv run qestyle --version
uv run pytest tests/
```

Prefer pip? `pip install -e ".[dev,action]"` uses the same dependency manifest.

To run against real lectures, set your API keys first:

```bash
export ANTHROPIC_API_KEY="your-key"   # Claude (Anthropic)
export GITHUB_TOKEN="your-token"      # GitHub API
```

## Adding Style Rules

Rules live in `style_checker/rules/*.md` and are read directly by the LLM — **no
code change is needed** to add a rule to an existing category. Adding a whole new
category also requires updating `VALID_CATEGORIES`
(`style_checker/categories.py`) and `RULE_EVALUATION_ORDER`
(`style_checker/reviewer.py`); the test suite fails loudly if those drift. See
the [full guide](docs/developer/contributing.md#adding-new-rules) for the rule
format and details.

## Pull Requests

1. Fork the repository and create a feature branch:
   `git checkout -b feature/your-feature-name`
2. Make your changes; add tests where it makes sense.
3. Run the suite: `uv run pytest tests/`
4. Commit using conventional commits (below) and open a PR with a clear
   description that references any related issues.

### Commit Message Format

Use [conventional commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style / formatting
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## Reporting Issues

Include: a description of the problem, steps to reproduce, expected vs. actual
behavior, environment details (OS, Python version), and any relevant logs or
error messages.

## Suggesting Enhancements

Open a GitHub discussion or issue describing the use case, your proposed
solution, and any alternatives you considered.

Thank you for contributing! 🎉
