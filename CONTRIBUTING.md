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
   export ANTHROPIC_API_KEY="your-key"  # For Claude
   export OPENAI_API_KEY="your-key"     # For OpenAI
   export GOOGLE_API_KEY="your-key"     # For Gemini
   export GITHUB_TOKEN="your-token"     # For GitHub API
   ```

## Testing Locally

### Test Single Lecture Review

```bash
python -m style_checker.main \
  --mode single \
  --lectures-path lectures/ \
  --style-guide style-guide-database.md \
  --llm-provider claude \
  --repository owner/repo \
  --comment-body "@quantecon-style-guide lecture-name" \
  --create-pr false
```

### Test Bulk Review

```bash
python -m style_checker.main \
  --mode bulk \
  --lectures-path lectures/ \
  --style-guide style-guide-database.md \
  --llm-provider claude \
  --repository owner/repo \
  --create-pr false
```

## Adding New Features

### Adding New Style Rules

1. Edit `style-guide-database.md`
2. Add rule following the existing Markdown format:
   ```markdown
   ### [CODE] Rule Title {#rule-id}
   
   **Category**: rule  
   **Group**: CODE  
   **Priority**: critical
   
   **Rule**: Clear description of the rule
   
   **Correct**:
   ```python
   # Good example
   ```
   
   **Incorrect**:
   ```python
   # Bad example
   ```
   ```

3. Choose appropriate category:
   - `rule` - Actionable, enforced automatically
   - `style` - Style preferences, informational
   - `migrate` - Migration notes for transitions

4. Choose appropriate semantic group:
   - WRITING, MATH, CODE, JAX, FIGURES, REFERENCES, LINKS, ADMONITIONS

5. Test with sample lectures using the semantic grouping system

### Adding New LLM Providers

1. Create new provider class in `style_checker/reviewer.py`
2. Inherit from `LLMProvider` abstract base class
3. Implement `check_style()` method
4. Add to `StyleReviewer.__init__()` provider selection
5. Update documentation and requirements.txt

### Improving Prompts

- Edit system prompts in provider classes
- Test with various lecture types
- Ensure JSON output format is maintained
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
3. **Categorized properly**: Use existing categories when possible
4. **Prioritized correctly**: 
   - `critical`: Breaks builds
   - `mandatory`: Must follow for consistency
   - `best_practice`: Strongly recommended
   - `preference`: Style choice

## Questions?

- Open a discussion on GitHub
- Check existing issues and PRs
- Review the documentation

Thank you for contributing! 🎉
