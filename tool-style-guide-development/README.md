# Style Guide Development Tools

This directory contains tools for managing the QuantEcon style guide rules database.

## Purpose

This is the **development workspace** for maintaining style guide rules. The actual GitHub Action reads rules from `../style_checker/rules/`, making that the single source of truth for the action.

## Workflow

### 1. Edit the Master Database

Edit `style-guide-database.md` to add, modify, or remove rules. This is the central source for all rules.

### 2. Generate Category-Specific Rule Files

Run the build script to generate individual rule files by category:

```bash
python build_rules.py
```

This creates/updates files in `tool-style-guide-development/rules/`:
- `writing-rules.md`
- `math-rules.md`
- `code-rules.md`
- `jax-rules.md`
- `figures-rules.md`
- `references-rules.md`
- `links-rules.md`
- `admonitions-rules.md`

### 3. Review Generated Files

Check the generated files in `rules/` to ensure they look correct.

### 4. Copy to Action

Copy the updated rule files to the action's rules directory:

```bash
cp rules/*.md ../style_checker/rules/
```

Or copy individual categories:

```bash
cp rules/writing-rules.md ../style_checker/rules/
```

### 5. Test

Run the action's test suite to ensure nothing broke:

```bash
cd ..
pytest tests/
```

## File Structure

```
tool-style-guide-development/
├── README.md                    # This file
├── build_rules.py              # Script to generate rule files
├── style-guide-database.md     # Master rule database
└── rules/                      # Generated rule files (git-ignored)
    ├── writing-rules.md
    ├── math-rules.md
    ├── code-rules.md
    ├── jax-rules.md
    ├── figures-rules.md
    ├── references-rules.md
    ├── links-rules.md
    └── admonitions-rules.md
```

## Important Notes

### Single Source of Truth

- **For Development**: `style-guide-database.md` (this directory)
- **For GitHub Action**: `style_checker/rules/*.md` (parent directory)

The action does NOT read `style-guide-database.md` - it only uses the files in `style_checker/rules/`.

### Version Control

- `style-guide-database.md` is tracked in git
- `rules/` folder is git-ignored (generated files)
- `../style_checker/rules/*.md` is tracked in git (used by action)

### Rule Format in Database

Rules in `style-guide-database.md` are organized by group sections:

```markdown
<!-- GROUP:WRITING-START -->
## Writing Rules

### Rule: qe-writing-001
**Category:** rule  
**Title:** Use one sentence per paragraph

**Description:**  
Each paragraph should contain only one sentence...

---

### Rule: qe-writing-002
...
<!-- GROUP:WRITING-END -->
```

The `build_rules.py` script parses these GROUP markers to extract rules.

## Adding New Rules

1. Edit `style-guide-database.md`
2. Add rule in appropriate GROUP section
3. Follow the existing format
4. Run `python build_rules.py`
5. Copy to `../style_checker/rules/`
6. Test with `pytest tests/`
7. Commit changes to both files

## Modifying Existing Rules

1. Edit `style-guide-database.md`
2. Find and update the rule
3. Run `python build_rules.py`
4. Copy updated file(s) to `../style_checker/rules/`
5. Test and commit

## Troubleshooting

### Script fails to parse database

- Check that GROUP markers are present: `<!-- GROUP:WRITING-START -->` and `<!-- GROUP:WRITING-END -->`
- Ensure rule format is correct: `### Rule: qe-category-NNN`

### Generated files look wrong

- Check the `generate_rule_file_header()` function in `build_rules.py`
- Verify rule extraction regex patterns

### Action fails after updating rules

- Ensure rule IDs are unique
- Check that rule format matches what LLM expects
- Run tests: `pytest tests/test_parser_md.py -v`

## Related Directories

- `../style_checker/rules/` - Rules used by GitHub Action (source of truth for action)
- `../tool-style-checker/` - Standalone CLI tool (different codebase, separate rules)
