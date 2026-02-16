# QuantEcon Style Guide Checker

[![Version](https://img.shields.io/badge/version-0.7.2-blue.svg)](https://github.com/QuantEcon/action-style-guide/releases)
[![Status](https://img.shields.io/badge/status-active-green.svg)](https://github.com/QuantEcon/action-style-guide)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A GitHub Action and local CLI for automated style guide compliance checking of [QuantEcon](https://quantecon.org) lecture materials using AI-powered analysis.

Uses Claude Sonnet 4.5 with extended thinking to check **49 style rules** across 8 categories (writing, math, code, JAX, figures, references, links, admonitions) with **zero false positives**.

## Quick Start

### GitHub Action

Comment on any issue in your lecture repository:

```
@qe-style-checker lecture_name
@qe-style-checker lecture_name writing,math
```

### Local CLI

```bash
pip install git+https://github.com/QuantEcon/action-style-guide.git
export ANTHROPIC_API_KEY='your-key-here'

qestyle lecture.md                      # Review all categories, apply fixes
qestyle lecture.md --categories writing  # Specific category
qestyle lecture.md --dry-run             # Report only, no changes
```

## Documentation

Full documentation is available at the [docs site](https://quantecon.github.io/action-style-guide/).

### User Guide

- [Getting Started](docs/user/getting-started.md) — Setup, installation, workflow configuration
- [Configuration](docs/user/configuration.md) — Action inputs, LLM model, rule types
- [Rules Reference](docs/user/rules-reference.md) — All 49 rules by category and type
- [CLI Guide](docs/user/cli.md) — Local `qestyle` command usage
- [GitHub App Setup](docs/user/github-app-setup.md) — Production setup with GitHub Apps

### Developer Guide

- [Architecture](docs/developer/architecture.md) — System design, components, data flow
- [Contributing](docs/developer/contributing.md) — Dev setup, code style, PR process
- [Testing](docs/developer/testing.md) — Unit tests, integration tests, production testing
- [Extended Thinking](docs/developer/extended-thinking.md) — Experiment results and prompt design
- [Roadmap](docs/developer/roadmap.md) — Development plan and future enhancements

## License

MIT License — see [LICENSE](LICENSE) for details.
