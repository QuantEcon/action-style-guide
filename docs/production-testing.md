# Production Testing Guide

> Testing the GitHub Action in real-world scenarios before deploying to production lecture repositories.

## Overview

This guide covers **production testing** - testing the action as it will be used in real repositories. This is different from unit tests (pytest) which test individual components.

| Test Type | Purpose | When to Use |
|-----------|---------|-------------|
| **Unit Tests** (`pytest`) | Test code logic | Every commit, CI |
| **CLI Tool** | Test prompts/rules locally | Developing rules, quick validation |
| **Test Repository** | Test full GitHub Action flow | Before releases, major changes |

## 1. Local Testing with CLI Tool

The `qestyle` CLI provides the fastest way to test prompt and rule changes.

### Setup

```bash
# Install from local clone (editable)
pip install -e .

# Or install from GitHub
pip install git+https://github.com/QuantEcon/action-style-guide.git

# Set API key
export ANTHROPIC_API_KEY='your-key-here'
```

### Basic Usage

```bash
# Test a single category
qestyle lecture.md --categories writing

# Test multiple categories
qestyle lecture.md --categories math,code

# Test all categories (sequential processing)
qestyle lecture.md
```

### Output

By default, `qestyle` prints a Markdown report to stdout. Use `--fix` to apply rule-type fixes in place, or `-o report.md` to save the report to a file.

### What to Check

After running the CLI tool, verify:
1. ✅ Violations detected are accurate (no false positives)
2. ✅ Suggestions are clear and actionable
3. ✅ Corrected content is valid MyST Markdown
4. ✅ Rule types (`rule` vs `style`) are applied correctly
5. ✅ No regressions from previous behavior

## 2. GitHub Test Repository

For full end-to-end testing of the GitHub Action, use a dedicated test repository.

### Recommended Setup: `test-action-style-guide`

Create a test repository that mirrors a real lecture repo structure:

```
test-action-style-guide/
├── .github/
│   └── workflows/
│       └── style-guide.yml      # Action workflow
├── lectures/
│   ├── test-clean.md            # Lecture with no violations
│   ├── test-violations.md       # Lecture with known violations
│   ├── test-math-violations.md  # Math-specific violations
│   ├── test-code-violations.md  # Code-specific violations
│   └── test-edge-cases.md       # Edge cases and tricky content
├── _config.yml                   # Minimal Jupyter Book config
└── README.md
```

### Creating the Test Repository

1. **Create new repo** at `QuantEcon/test-action-style-guide`

2. **Add the workflow file** (`.github/workflows/style-guide.yml`):

```yaml
name: Style Guide Check

on:
  issue_comment:
    types: [created]
  workflow_dispatch:
    inputs:
      lecture:
        description: 'Lecture filename (without .md)'
        required: true
      categories:
        description: 'Categories to check (comma-separated, or "all")'
        required: false
        default: 'all'

jobs:
  style-check:
    if: |
      github.event_name == 'workflow_dispatch' ||
      (github.event_name == 'issue_comment' && 
       contains(github.event.comment.body, '@qe-style-checker'))
    runs-on: ubuntu-latest
    
    steps:
      - name: Run Style Checker
        uses: QuantEcon/action-style-guide@v0.5
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          mode: single
          comment_body: ${{ github.event.comment.body || format('@qe-style-checker {0} {1}', github.event.inputs.lecture, github.event.inputs.categories) }}
```

3. **Add test lectures** with known violations (see examples below)

4. **Configure secrets**:
   - Go to repo Settings → Secrets → Actions
   - Add `ANTHROPIC_API_KEY` with your API key

### Test Lecture Examples

#### `lectures/test-violations.md` (Mixed violations)

```markdown
---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Test Lecture with Violations

This lecture has intentional style violations for testing.

## Math Violations

Display math using $$ (should use {math} directive):

$$
V(x) = \max_{y} u(x,y) + \beta V(y)
$$

Missing superscript on transpose (should be ^\top):

$$
A\top B = B\top A
$$

## Code Violations

Code without language specifier:

```
def example():
    return 42
```

## Writing Violations

This is a very long sentence that goes on and on and contains way too much information in a single sentence making it hard to read and understand what the main point is supposed to be for the reader.

## Reference Violations

See Smith (2020) for more details.

## Exercise Format

**Exercise 1**

Solve the equation.

**Solution**

The answer is 42.
```

#### `lectures/test-clean.md` (No violations)

```markdown
---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Clean Test Lecture

This lecture follows all style guidelines.

## Mathematics

Here is a properly formatted equation:

```{math}
:label: bellman-equation

V(x) = \max_{y} \{ u(x,y) + \beta V(y) \}
```

Equation {eq}`bellman-equation` shows the Bellman equation.

## Code Example

```{code-cell} ipython3
def bellman_operator(v):
    """Apply the Bellman operator."""
    return max(u + beta * v)
```

## Summary

This lecture demonstrated proper formatting.
```

### Running Tests

#### Via Issue Comment

1. Open any issue in the test repository
2. Comment: `@qe-style-checker test-violations`
3. Wait for the action to run and create a PR

#### Via Workflow Dispatch (Recommended for testing)

1. Go to Actions tab in the test repository
2. Select "Style Guide Check" workflow
3. Click "Run workflow"
4. Enter lecture name: `test-violations`
5. Enter categories: `writing,math` (or `all`)
6. Click "Run workflow"

### What to Verify

After the action runs:

1. **Check the PR created**:
   - Are the right violations detected?
   - Are fixes applied correctly?
   - Is the commit message accurate?

2. **Review the PR body**:
   - Does it list all violations found?
   - Are `rule` vs `style` types separated?
   - Are line numbers/locations accurate?

3. **Test the corrected content**:
   - Does the lecture build correctly?
   - Are fixes semantically correct?

4. **Edge cases**:
   - What happens with a clean file? (Should create no PR)
   - What happens with invalid lecture name? (Should error gracefully)

## 3. Testing Workflow Changes

When making changes to the action itself:

### Before Release Checklist

1. **Run unit tests locally**:
   ```bash
   pytest tests/ -v
   ```

2. **Run LLM integration tests** (optional, costs money):
   ```bash
   export ANTHROPIC_API_KEY='your-key'
   pytest -m integration -v
   ```

3. **Test CLI tool with changes**:
   ```bash
   qestyle lecture.md --categories writing
   ```

4. **Test on GitHub test repository**:
   - Push changes to a branch
   - Update test repo workflow to use branch: `uses: QuantEcon/action-style-guide@your-branch`
   - Run workflow dispatch test
   - Verify results

5. **Test on production repo** (careful!):
   - Use a non-critical lecture
   - Be prepared to close/revert PR

## 4. Version Testing Matrix

Test across different scenarios:

| Scenario | Test Method | Expected Result |
|----------|-------------|-----------------|
| Clean lecture | CLI or GitHub | No violations found |
| Math violations only | `--focus math` | Only math rules trigger |
| Writing violations | `--focus writing` | Writing rules trigger |
| All categories | `--focus all` | All applicable rules trigger |
| Invalid lecture | GitHub comment | Error message posted |
| Large lecture (>5000 lines) | CLI | Completes without timeout |
| Lecture with code cells | GitHub | Code cells preserved |

## 5. Cost Considerations

LLM API calls cost money:

| Test Type | Estimated Cost |
|-----------|---------------|
| CLI tool, single category | ~$0.02 |
| CLI tool, all categories | ~$0.10-0.15 |
| GitHub Action, single lecture | ~$0.10-0.20 |
| Full test suite (multiple lectures) | ~$0.50-1.00 |

**Tips to minimize costs**:
- Use `--focus` to test specific categories
- Use short test lectures for iteration
- Run full tests only before releases

## 6. Debugging Failed Tests

### Action fails to trigger
- Check workflow file syntax
- Verify comment format: `@qe-style-checker lecture_name`
- Check if issue comments trigger is enabled

### No violations detected
- Verify test lecture has actual violations
- Check if category matches the violation type
- Review action logs for parsing errors

### Wrong fixes applied
- Check rule definitions in `style_checker/rules/`
- Verify prompt instructions in `style_checker/prompts/`
- Test with CLI tool first to isolate issue

### PR not created
- Check GitHub token permissions
- Verify branch doesn't already exist
- Review action logs for errors

## Next Steps

1. **Set up test repository**: Create `QuantEcon/test-action-style-guide`
2. **Add test lectures**: Include various violation types
3. **Configure secrets**: Add `ANTHROPIC_API_KEY`
4. **Document results**: Track test outcomes in the test repo

## Related Documentation

- [Testing Quick Reference](testing-quick-reference.md) - Unit test commands
- [LLM Integration Testing](llm-integration-testing.md) - API integration tests
- [CI/CD Setup](ci-cd-setup.md) - GitHub Actions configuration
