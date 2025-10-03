# Style Checker Modes Guide

The style checker now supports three output modes to suit different workflows.

## Three Modes

### 1. **Suggestions Mode** (Default)
Get detailed review with violations and suggested fixes.

**Use when:**
- Learning what's wrong and why
- Want to review changes before applying
- Need to selectively apply fixes
- First time using the checker

**Example:**
```bash
python style_checker.py lecture.md
# or explicitly:
python style_checker.py lecture.md --mode suggestions
```

**Output:** Detailed review with violations, issues, and recommendations

---

### 2. **Corrected Mode**
Get the fully corrected lecture file ready to use.

**Use when:**
- You trust the style guide rules completely
- Want fast automatic fixes
- Batch processing many lectures
- Second pass after reviewing suggestions

**Example:**
```bash
# Get corrected file
python style_checker.py lecture.md --mode corrected --output lecture-fixed.md

# Review the changes
diff lecture.md lecture-fixed.md

# If satisfied, replace original
mv lecture-fixed.md lecture.md
```

**Output:** Only the corrected lecture file (no review)

---

### 3. **Both Mode**
Get review AND corrected file in one run.

**Use when:**
- Want to see what changed and get the fixed file
- Need to verify fixes before using them
- Want complete documentation of changes
- Teaching/learning purposes

**Example:**
```bash
python style_checker.py lecture.md --mode both --output combined.md
```

**Output:** 
1. Complete style review
2. Separator line
3. Fully corrected lecture file

The script will also extract the corrected portion to a separate file:
- `combined.md` - Full output (review + corrected)
- `combined-corrected.md` - Just the corrected lecture

---

## Recommended Workflows

### Workflow 1: Learning (First Time)
```bash
# Step 1: Get suggestions to understand issues
python style_checker.py lecture.md --mode suggestions --output review.md

# Step 2: Read review.md and learn what needs fixing

# Step 3: Get corrected version to see how fixes look
python style_checker.py lecture.md --mode corrected --output lecture-fixed.md

# Step 4: Compare and learn
diff lecture.md lecture-fixed.md

# Step 5: Apply what you learned
mv lecture-fixed.md lecture.md
```

### Workflow 2: Quick Fix (Trusted Rules)
```bash
# One command to fix everything
python style_checker.py lecture.md --mode corrected --output lecture-fixed.md

# Quick verify (optional)
diff lecture.md lecture-fixed.md | head -50

# Apply
mv lecture-fixed.md lecture.md
```

### Workflow 3: Careful Review (Both)
```bash
# Get everything
python style_checker.py lecture.md --mode both --output analysis.md

# Review the suggestions section in analysis.md
# Then use the corrected file: analysis-corrected.md

# Verify changes
diff lecture.md analysis-corrected.md

# Apply if satisfied
mv analysis-corrected.md lecture.md
```

### Workflow 4: Batch Processing
```bash
# Process all lectures in a folder
for lecture in lectures/*.md; do
    echo "Processing $lecture..."
    python style_checker.py "$lecture" --mode corrected \
        --output "${lecture%.md}-fixed.md"
done

# Review all changes
for lecture in lectures/*-fixed.md; do
    original="${lecture%-fixed.md}.md"
    echo "=== Changes in $lecture ==="
    diff "$original" "$lecture" | head -20
    echo ""
done

# Apply all (if satisfied)
for lecture in lectures/*-fixed.md; do
    mv "$lecture" "${lecture%-fixed.md}.md"
done
```

---

## Mode Comparison

| Feature | Suggestions | Corrected | Both |
|---------|-------------|-----------|------|
| **Get review** | ✅ | ❌ | ✅ |
| **Get fixed file** | ❌ | ✅ | ✅ |
| **Speed** | Fast | Fast | Slower (2x output) |
| **File size** | Small | Medium | Large |
| **Learning** | ✅✅✅ | ❌ | ✅✅ |
| **Automation** | ❌ | ✅✅✅ | ✅ |
| **Safety** | ✅✅✅ | ⚠️ | ✅✅ |

---

## Combining with Other Options

All modes work with other options:

```bash
# Quick mode + corrected output
python style_checker.py lecture.md --quick --mode corrected --output fixed.md

# Focus on specific categories + both mode
python style_checker.py lecture.md --focus writing math --mode both --output analysis.md

# Custom prompt + corrected mode
python style_checker.py lecture.md --prompt custom.md --mode corrected --output fixed.md
```

---

## Tips

### For Suggestions Mode
- Save output to review later: `--output review.md`
- Use `--quick` for high-level overview first
- Use `--focus` to check specific categories

### For Corrected Mode
- **Always save to a new file** (don't overwrite original immediately)
- Use `diff` to review changes before applying
- Consider version control (git) before applying changes
- Test the corrected file builds correctly

### For Both Mode
- Best for documentation and learning
- Larger output, use `--output` to save to file
- Script automatically extracts corrected portion
- Good for archiving the full analysis

### Safety First
```bash
# Always backup before replacing
cp lecture.md lecture.md.backup
python style_checker.py lecture.md --mode corrected --output lecture-fixed.md
diff lecture.md lecture-fixed.md  # Review!
mv lecture-fixed.md lecture.md
# If issues: mv lecture.md.backup lecture.md
```

---

## Examples

### Example 1: First time checking a lecture
```bash
$ python style_checker.py intro.md --mode suggestions

================================================================================
STYLE REVIEW
================================================================================

# Style Guide Review for intro.md

## Summary
- Total violations: 12
- Critical issues: 8
- Style suggestions: 4

[... detailed review ...]
```

### Example 2: Get corrected file
```bash
$ python style_checker.py intro.md --mode corrected --output intro-fixed.md

Loading lecture: intro.md
Loading prompt: claude-style-checker-prompt.md
Loading style guide: style-guide-database.md

Sending request to Claude Sonnet 4.5...
Message size: 58,432 characters

✓ Corrected lecture saved to: intro-fixed.md

✓ Style check complete!
```

### Example 3: Get both
```bash
$ python style_checker.py intro.md --mode both --output full-analysis.md

Loading lecture: intro.md
Loading prompt: claude-style-checker-prompt.md
Loading style guide: style-guide-database.md

Sending request to Claude Sonnet 4.5...
Message size: 58,556 characters

✓ Review and corrected file saved to: full-analysis.md
✓ Corrected lecture also saved to: full-analysis-corrected.md

✓ Style check complete!
```

---

## When to Use Which Mode

**Use Suggestions when:**
- 📚 Learning the style guide
- 🔍 Reviewing before changes
- 🎯 Selective fixes needed
- 👥 Collaborative review

**Use Corrected when:**
- ⚡ Speed is priority
- ✅ Trust the rules completely
- 🔄 Batch processing
- 🤖 Automation/CI-CD

**Use Both when:**
- 📖 Documentation needed
- 🔬 Verification required
- 🎓 Teaching/training
- 📝 Archive full analysis

---

## See Also

- Run `python style_checker.py --help` for all options
- See `DOCUMENTATION.md` for complete guide
- Test with `quantecon-test-lecture.md` to see all modes in action
