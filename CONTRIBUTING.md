# Contributing to QuantEcon Style Guide Checker

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- GitHub account

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/QuantEcon/action-style-guide.git
   cd action-style-guide
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

4. **Set up API keys**
   ```bash
   export ANTHROPIC_API_KEY="your-key"  # For Claude Sonnet 4.5
   export GITHUB_TOKEN="your-token"     # For GitHub API
   ```

## Testing Locally

### Test Single Lecture Review

```bash
python -m style_checker.main \
  --mode single \
  --lectures-path lectures/ \
  --repository owner/repo \
  --comment-body "@qe-style-checker lecture-name" \
  --create-pr false
```

### Test Bulk Review

```bash
python -m style_checker.main \
  --mode bulk \
  --lectures-path lectures/ \
  --repository owner/repo \
  --create-pr false
```

## Adding New Features

### Adding New Style Rules

Rules are now organized in category-specific files in `style_checker/rules/`:

1. Edit the appropriate rules file (e.g., `style_checker/rules/writing-rules.md`)
2. Add rule following the existing Markdown format:
   ```markdown
   ## Rule Title
   
   **Description**: Clear explanation of what the rule checks
   
   **Why**: Rationale for this rule
   
   **Good**:
   ```python
   # Good example
   ```
   
   **Bad**:
   ```python
   # Bad example
   ```
   ```

3. Rules are grouped into 8 categories:
   - writing, math, code, jax, figures, references, links, admonitions

4. If needed, update corresponding prompt file in `style_checker/prompts/`

5. Test with sample lectures

### Adding New LLM Providers

The action currently uses Claude Sonnet 4.5 via the Anthropic API. The provider logic is in `style_checker/reviewer.py`.

To switch or add a provider:
1. Update the API client setup in `AnthropicProvider.__init__()`
2. Adjust model name and parameters as needed
3. Update `requirements.txt` with new dependencies
4. Test with real lecture files

### Improving Prompts

The action uses a focused prompts architecture:
- **Prompts** (`style_checker/prompts/*.md`): Concise instructions for the LLM
- **Rules** (`style_checker/rules/*.md`): Detailed specifications with examples

To improve:
- Edit the appropriate prompt or rules file
- Test with various lecture types
- Ensure Markdown output format is maintained
- Validate against all rule categories

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to all functions/classes
- Keep functions focused and small
- Comment complex logic

## Pull Request Process

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make changes**
   - Write clean, documented code
   - Add tests if applicable
   - Update documentation

4. **Test thoroughly**
   - Test locally with real lectures
   - Verify PR creation works
   - Check all output formats

5. **Commit with clear messages**
   ```bash
   git commit -m "feat: add feature description"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **PR Requirements**
   - Clear description of changes
   - Reference any related issues
   - Include test results
   - Update README if needed

## Commit Message Format

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## Reporting Issues

When reporting issues, include:

1. **Description** of the problem
2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **Environment details** (OS, Python version, etc.)
6. **Relevant logs** or error messages

## Suggesting Enhancements

For feature requests:

1. **Use case**: Why is this needed?
2. **Proposed solution**: How should it work?
3. **Alternatives considered**: Other approaches?
4. **Implementation ideas**: Technical approach?

## Style Guide Rules

When adding or modifying style guide rules:

1. **Clear and specific**: Rules should be unambiguous
2. **Actionable**: Include examples of correct/incorrect usage
3. **Categorized properly**: Use one of the 8 categories (writing, math, code, jax, figures, references, links, admonitions)
4. **Typed correctly**: 
   - `rule`: Actionable, automatically applied
   - `style`: Advisory, requires human judgment
   - `migrate`: Legacy pattern modernization

## Questions?

- Open a discussion on GitHub
- Check existing issues and PRs
- Review the documentation

Thank you for contributing! 🎉
