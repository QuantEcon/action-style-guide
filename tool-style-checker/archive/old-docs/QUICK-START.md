# QuantEcon Style Checker - Quick Reference

## What You Have

I've created a complete system for using Claude Sonnet 4.5 to check QuantEcon lectures against your style guide:

1. **`claude-style-checker-prompt.md`** - The main prompt that instructs Claude how to perform the review
2. **`usage-guide.md`** - Comprehensive guide on different ways to use the system
3. **`style_checker.py`** - Python script for automated checking via Claude API

## Fastest Way to Get Started

### Option A: Using Claude.ai Web Interface (No coding required)

1. Go to [claude.ai](https://claude.ai)
2. Start a new conversation
3. Upload these three files:
   - `claude-style-checker-prompt.md`
   - `style-guide-database.md`
   - `quantecon-test-lecture.md` (or your own lecture)
4. Send this message:
   ```
   Please follow the instructions in claude-style-checker-prompt.md 
   to review the lecture against the style guide.
   ```

### Option B: Using the Python Script (Requires API key)

```bash
# Install the Claude SDK
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Run the checker
python style_checker.py quantecon-test-lecture.md

# Save output to a file
python style_checker.py quantecon-test-lecture.md --output review.md

# Quick check (only critical violations)
python style_checker.py quantecon-test-lecture.md --quick

# Focus on specific categories
python style_checker.py quantecon-test-lecture.md --focus writing math
```

## What the Output Looks Like

Claude will provide a structured review with:

```markdown
# Style Guide Review for [Lecture Title]

## Summary
- Total violations found: 23
- Critical issues (rule category): 18
- Style suggestions: 5
- Overall assessment: The lecture has several writing and math notation violations...

## Critical Issues (Rule Violations)

### Writing

#### qe-writing-001: Use one sentence per paragraph
**Location**: Lines 42-44
**Current**: "This paragraph has multiple sentences. This is the second one."
**Issue**: Paragraph contains two sentences
**Suggested fix**: 
"This paragraph has one sentence.

This is a separate paragraph with its own sentence."

[... more violations ...]

## Recommendations Summary
1. Fix multiple sentences per paragraph (18 instances)
2. Correct mathematical notation (use \top for transpose)
3. Update figure formatting
[etc.]
```

## Key Features of the Prompt

The prompt I created for you:

✅ **Comprehensive**: Covers all 8 rule categories (Writing, Math, Code, JAX, Figures, References, Links, Admonitions)

✅ **Structured output**: Always returns violations in a consistent, easy-to-parse format

✅ **Prioritized**: Separates critical rule violations from advisory style suggestions

✅ **Specific**: Always quotes exact text and provides exact fixes

✅ **Context-aware**: Understands MyST Markdown, Jupyter Book syntax, and technical content

✅ **Avoids false positives**: Includes guidelines to prevent incorrect flagging

✅ **Actionable**: Provides copy-paste-ready corrections

## Example Use Cases

### 1. Before Publishing a New Lecture
```bash
python style_checker.py new_lecture.md --output review.md
# Review the output, fix violations, then re-check
python style_checker.py new_lecture.md --quick
```

### 2. Quick Math Check
```bash
python style_checker.py lecture.md --focus math --quick
```

### 3. Comprehensive Review for Major Revision
```bash
python style_checker.py lecture.md
# This will check everything thoroughly
```

### 4. Batch Processing Multiple Lectures
```python
# Create a simple script:
import os
from style_checker import check_lecture_style

for lecture in os.listdir('lectures/'):
    if lecture.endswith('.md'):
        review = check_lecture_style(f'lectures/{lecture}')
        with open(f'reviews/{lecture}.review.md', 'w') as f:
            f.write(review)
```

## Customizing for Your Needs

### Modify the Prompt
Edit `claude-style-checker-prompt.md` to:
- Change output format
- Add specific instructions for your use case
- Emphasize certain rule categories
- Add examples of common issues in your lectures

### Focus on Specific Issues
When calling Claude (web or API), you can add:
```
Please focus specifically on mathematical notation rules and 
ignore all other categories for this review.
```

### Adjust Thoroughness
For quick feedback:
```
Please provide only the top 5 most critical violations.
```

For comprehensive review:
```
Please be extremely thorough and include even minor style suggestions.
```

## Tips for Best Results

1. **Review incrementally**: Fix major structural issues first, then re-run for details
2. **Use your judgment**: Claude's suggestions are advisory; you know your content best
3. **Combine automated + manual**: Use Claude for initial scan, then manually review
4. **Test with known violations**: Try it on `quantecon-test-lecture.md` to see how it works
5. **Iterate**: The prompt can be refined based on your experience

## What Makes This Prompt Effective

1. **Clear role definition**: Claude knows it's a technical writing editor
2. **Structured input**: Style guide rules are well-organized with codes
3. **Specific output format**: Consistent structure makes reviews easy to use
4. **Examples included**: Shows Claude what good feedback looks like
5. **Context preservation**: Maintains technical accuracy while fixing style
6. **False positive prevention**: Guidelines to avoid incorrect flagging

## Next Steps

1. **Test it**: Run the checker on `quantecon-test-lecture.md` to see it catch intentional violations
2. **Try on real lecture**: Use it on an actual lecture you're working on
3. **Refine as needed**: Adjust the prompt based on results
4. **Integrate into workflow**: Make it part of your lecture review process

## Questions?

The `usage-guide.md` file has much more detail on:
- Different usage methods
- Advanced options
- Troubleshooting
- Batch processing
- Output interpretation

## Files Created

```
prompt-experiments/
├── claude-style-checker-prompt.md  ← The main prompt
├── usage-guide.md                  ← Detailed usage instructions
├── style_checker.py                ← Automated Python script
└── QUICK-START.md                  ← This file
```

All working with your existing:
- `style-guide-database.md` (the rules)
- `quantecon-test-lecture.md` (test document)
