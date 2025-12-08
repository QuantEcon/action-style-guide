# Documentation

This directory contains documentation for the QuantEcon Style Guide Checker.

## Quick Links

### For Users

| Document | Description |
|----------|-------------|
| [GitHub App Setup](github-app-setup.md) | Configure GitHub App for production use |
| [CI/CD Setup](ci-cd-setup.md) | Set up automated testing with pytest and GitHub Actions |

### For Developers

| Document | Description |
|----------|-------------|
| [Architecture](ARCHITECTURE.md) | System architecture, data flow, and component design |
| [Testing Quick Reference](testing-quick-reference.md) | Quick commands for running tests |
| [LLM Integration Testing](llm-integration-testing.md) | Testing with real LLM API calls |
| [Future Enhancements](FUTURE-ENHANCEMENTS.md) | Roadmap and planned features |

## Getting Started

1. **New users**: Start with the main [README.md](../README.md) for quick start
2. **Setting up CI**: See [CI/CD Setup](ci-cd-setup.md)
3. **Contributing**: See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines
4. **Understanding the code**: See [Architecture](ARCHITECTURE.md)

## Testing

```bash
# Run all tests (excludes integration tests)
pytest

# Run integration tests (requires API key)
export ANTHROPIC_API_KEY="your-key"
pytest -m integration

# Run with coverage
pytest --cov=style_checker
```

See [Testing Quick Reference](testing-quick-reference.md) for more commands.
