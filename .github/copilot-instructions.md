# GitHub Copilot Instructions for action-style-guide

## Project Overview

This is a GitHub Action that performs AI-powered style guide compliance checking for QuantEcon lecture materials using Claude (Anthropic). It reviews MyST Markdown lecture files against defined style rules and can automatically create PRs with fixes.

## Development Phase & Philosophy

### Current Status
- **Active development** - Breaking changes are acceptable
- **Not worried about backward compatibility** - Focus on getting it right, not maintaining legacy behavior
- **Iteration over perfection** - Ship improvements quickly, refine based on real-world usage

### Core Principles

1. **Simplicity above all**
   - Write the simplest code that works
   - Reduce complexity and maintenance burden
   - Prefer clear, obvious solutions over clever ones
   - Less code = less bugs = easier maintenance

2. **Direct over abstract**
   - Don't abstract until you have 3+ use cases
   - Inline is fine if it's clearer
   - Avoid premature optimization

3. **Readable over concise**
   - Explicit is better than implicit
   - Variable names should be self-documenting
   - Comments should explain "why", not "what"

## Repository Structure

```
action-style-guide/
├── action.yml                    # GitHub Action definition
├── style_checker/                # Main action code
│   ├── __init__.py              # Version info (__version__)
│   ├── main.py                  # Entry point, CLI handling
│   ├── reviewer.py              # LLM interaction, response parsing
│   ├── github_handler.py        # GitHub API interactions
│   ├── fix_applier.py           # Apply fixes to markdown files
│   ├── prompt_loader.py         # Load prompts and rules
│   ├── prompts/                 # Category-specific prompts
│   │   ├── writing-prompt.md
│   │   ├── math-prompt.md
│   │   └── ...
│   └── rules/                   # Category-specific rules
│       ├── writing-rules.md
│       ├── math-rules.md
│       └── ...
├── tests/                       # Test files
├── docs/                        # Documentation
└── tool-*/                      # Independent development tools (NOT part of action)
    ├── tool-style-checker/      # Prototype for testing prompts/rules
    └── tool-style-guide-development/  # Rule development utilities
```

### Important: tool-* Folders

**The `tool-*` directories are independent projects for developing and testing prompts and rules.**

- ❌ **NOT part of the GitHub Action** - Not loaded or used by the action
- ✅ **Development utilities** - Used for prototyping and testing rule changes
- ✅ **Standalone tools** - Can be run independently for prompt/rule development
- 📝 **May have different dependencies** - Don't assume they share code with `style_checker/`

**When to use:**
- Testing new prompts before adding to `style_checker/prompts/`
- Developing new rules before adding to `style_checker/rules/`
- Experimenting with rule formatting or LLM behavior
- Quick prototyping without affecting the action

**When NOT to use:**
- Production runs (use the GitHub Action)
- Expecting changes in `tool-*` to affect the action behavior
- Assuming code consistency with `style_checker/`

## Key Technical Decisions

### LLM Architecture
- **Single model**: Claude Sonnet 4.5 only (no model switching complexity)
- **Sequential rule processing**: Process one rule at a time within each category, apply fixes between each
- **Sequential category processing**: Process categories one at a time, feed updated document to next category
- **Prompt-driven**: Instructions in prompts, not hardcoded logic
- **Simple parsing**: Regex-based markdown response parsing

### Rule System
- **Category-based**: 8 categories (writing, math, code, jax, figures, references, links, admonitions)
- **Prompt + Rules**: Each category has a prompt template and rules document
- **One rule per LLM call**: Each rule checked individually, fixes applied before next rule
- **Order matters**: Rules evaluated in specified order (mechanical → structural → stylistic → creative)
- **Single source of truth**: Version in `__init__.py`

### Prompt Files
- **Location**: `style_checker/prompts/*.md`
- **Version tracking**: Each prompt has version comment at top: `<!-- Prompt Version: X.Y.Z | Last Updated: YYYY-MM-DD | Description -->`
- **Update on modification**: Bump version when prompt content changes (usually to match release version)
- **Purpose**: Track which prompt version generated historical LLM responses

### GitHub Integration
- **Programmatic fixes**: Apply fixes via code, don't ask LLM for full corrected content
- **Token efficiency**: ~50% reduction by not requesting corrected content in responses
- **PR creation**: Automatic branch creation and PR submission

## Coding Guidelines

### When Making Changes

1. **Update version in `__init__.py`** for any user-facing change
2. **Update CHANGELOG.md** following Keep a Changelog format
3. **Keep prompts and rules in sync** - but avoid duplication
4. **Test with real lectures** before releasing

### Python Style

```python
# ✅ Good: Simple, clear, explicit
def apply_fix(content: str, violation: dict) -> str:
    """Apply a single fix to content."""
    old_text = violation['current_text']
    new_text = violation['suggested_fix']
    return content.replace(old_text, new_text, 1)

# ❌ Avoid: Clever, complex, requires mental parsing
def apply_fix(c, v):
    return c.replace(v['ct'], v['sf'], 1) if 'ct' in v and 'sf' in v else c
```

### File Organization

- **One clear responsibility per file**
- **Keep files under 500 lines** (split if growing too large)
- **Import only what you need**
- **No circular dependencies**

### Error Handling

```python
# ✅ Good: Explicit, helpful error messages
if not github_token:
    print("❌ GITHUB_TOKEN environment variable not set")
    print("Please set GITHUB_TOKEN to authenticate with GitHub API")
    sys.exit(1)

# ❌ Avoid: Silent failures or cryptic errors
assert github_token
```

### Prompts and Rules

1. **Prompts** (`prompts/*.md`):
   - Instructions for Claude
   - Output format specifications
   - Evaluation order (for writing)
   - Keep focused and concise

2. **Rules** (`rules/*.md`):
   - Rule definitions only
   - Examples of violations and fixes
   - No duplication with prompts
   - Each rule has: Category, Title, Description, Check for, Examples

### Version Management

```python
# In __init__.py
__version__ = "0.3.7"  # Bump for every release

# In main.py - print version at startup
print(f"📋 QuantEcon Style Guide Checker v{__version__}")
```

### Release Process

**CRITICAL: Always run tests before any release!**

1. Make changes
2. **Run full test suite**: `pytest tests/ -v`
3. **Verify all tests pass** (except LLM integration tests which require API keys)
4. Update `__version__` in `style_checker/__init__.py`
5. **Update prompt versions** if any prompts were modified:
   - Update version comment at top of each modified prompt file
   - Format: `<!-- Prompt Version: X.Y.Z | Last Updated: YYYY-MM-DD | Description -->`
   - Version should match the release version
6. Update `CHANGELOG.md` (move Unreleased to new version)
7. Commit: "Release vX.Y.Z - Description"
8. Create GitHub release: `gh release create vX.Y.Z --title "..." --notes "..."`
9. Update floating tag: `git tag -f v0.3 && git push origin v0.3 --force`
10. Push main branch: `git push origin main`

**Never skip testing** - it catches regressions and ensures quality.

**Prompt Version Tracking**: Prompt versions should stay in sync with releases when prompts are modified. This helps track which prompt version was used in historical runs.

## Common Tasks

### Adding a New Rule

1. Add rule definition to appropriate `rules/*.md` file
2. Update corresponding `prompts/*.md` if needed (e.g., add to checklist)
3. Update `CHANGELOG.md`
4. Test with real lecture files
5. No code changes needed (LLM reads the rules)

### Adding a New Category

1. Create `prompts/category-prompt.md`
2. Create `rules/category-rules.md`
3. Add category to `CATEGORIES` list in `reviewer.py`
4. Update action workflow examples
5. Test end-to-end

### Debugging LLM Issues

1. Check the prompt - is it clear and explicit?
2. Add more examples to rules
3. Strengthen language (e.g., "do NOT" instead of "don't")
4. Add "Important:" or "Critical:" sections
5. Test with isolated examples first

## Performance Considerations

### Token Optimization
- Don't request full corrected content from LLM (~50% token savings)
- Apply fixes programmatically using `fix_applier.py`
- Process categories sequentially (not all at once)

### Cost Management
- Single LLM call per category
- Reuse parsed content across categories
- Batch fixes when possible

## Testing Philosophy

- **Test with real lectures** - synthetic examples miss edge cases
- **Manual testing is OK** - we're iterating quickly
- **Integration tests > unit tests** - test the full flow
- **Document test cases** in `tests/README.md`

## Documentation

### Keep Updated
- `README.md` - User-facing overview
- `CHANGELOG.md` - All changes (follow Keep a Changelog)
- `docs/` - Setup guides, architecture docs
- `.github/copilot-instructions.md` - This file!

### Writing Style
- Clear and concise
- Examples over explanations
- Assume reader is technical
- Link to relevant docs/code

## What NOT to Do

❌ **Don't** add abstraction layers without proven need  
❌ **Don't** optimize prematurely  
❌ **Don't** maintain backward compatibility at the cost of simplicity  
❌ **Don't** add configuration options "just in case"  
❌ **Don't** duplicate information across files  
❌ **Don't** use complex regex when simple string operations work  
❌ **Don't** add dependencies without strong justification  

## Questions to Ask Before Adding Code

1. Is this the simplest solution?
2. Can I delete code instead of adding it?
3. Does this add maintenance burden?
4. Is this actually needed now, or might be needed later?
5. Can someone else understand this in 6 months?

## Useful Commands

```bash
# Test locally
python style_checker/main.py --mode single --repository owner/repo --comment-body "..."

# Run tests
pytest tests/

# Run tests with nox (when available)
nox -s tests

# Check version
python -c "from style_checker import __version__; print(__version__)"

# Create release
gh release create v0.3.7 --title "..." --notes "..."
git tag -f v0.3 && git push origin v0.3 --force
```

## GitHub CLI Note

**Important:** When using `gh` CLI commands that produce large output (e.g., `gh pr view`, `gh api`), redirect output to a `/tmp` file to see complete results:

```bash
# Write gh output to temp file for inspection
gh pr view 123 --json body > /tmp/pr-body.json
cat /tmp/pr-body.json

# For API calls with large responses
gh api repos/QuantEcon/lecture-python.myst/pulls/123 > /tmp/pr-details.json
```

This is particularly useful when debugging GitHub integration issues or inspecting PR/issue content.

## Terminal Multi-line Content Note

**Important:** When writing multi-line content (PR descriptions, issue bodies, commit messages with special characters), **always use `create_file` to write content to a `/tmp` file first**, then reference that file in the CLI command. Do NOT use heredocs (`cat << EOF`), escaped strings, or inline multi-line content in terminal commands — these frequently fail due to escaping issues.

```bash
# ✅ Good: Write content to file, then reference it
# (use create_file tool to write /tmp/pr-body.md)
gh pr edit 9 --body-file /tmp/pr-body.md

# ❌ Bad: Heredocs and escaped strings break often
cat << 'EOF' > /tmp/file.md
content with $special chars...
EOF
```

## Remember

- **Development phase** = freedom to improve without legacy concerns
- **Simple > clever** = maintainable code that anyone can understand
- **Ship and iterate** = get it working, then refine based on real usage
- **Less is more** = every line of code is a liability

When in doubt, choose the simpler solution. Future maintainers (including yourself) will thank you!
