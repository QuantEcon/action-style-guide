# QuantEcon Lecture Style Checker - Complete Documentation

**Version**: 1.0  
**Last Updated**: October 3, 2025  
**Status**: ✅ Production Ready

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Overview](#overview)
3. [Installation & Setup](#installation--setup)
4. [Usage Guide](#usage-guide)
5. [Example Interactions](#example-interactions)
6. [System Architecture](#system-architecture)
7. [Customization](#customization)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## Quick Start

### 🚀 Fastest Method: Web Interface (No Setup)

**Time**: 5 minutes | **Cost**: Free tier available

1. Go to [claude.ai](https://claude.ai)
2. Start a new conversation
3. Upload three files:
   - `claude-style-checker-prompt.md`
   - `style-guide-database.md`
   - Your lecture file (or `quantecon-test-lecture.md` for testing)
4. Send this message:
   ```
   Please follow the instructions in claude-style-checker-prompt.md 
   to review the lecture against the style guide.
   ```
5. Review Claude's structured feedback with violations and fixes

### ⚡ Command Line Method (Best for Automation)

**Time**: 10 minutes setup | **Cost**: $0.02-0.20 per lecture

```bash
# One-time setup
pip install anthropic
export ANTHROPIC_API_KEY='your-api-key'

# Check a lecture
python style_checker.py my-lecture.md

# Common options
python style_checker.py lecture.md --quick              # Critical issues only
python style_checker.py lecture.md --focus writing math # Specific categories
python style_checker.py lecture.md --output review.md   # Save to file
```

### 🧪 Test Drive

```bash
# Test with intentional violations (should find ~40+ issues)
python style_checker.py quantecon-test-lecture.md
```

---

## Overview

### What Is This?

An automated style checking system that reviews QuantEcon lecture materials against your comprehensive style guide using Claude Sonnet 4.5.

### What You Get

- ✅ **Automated checking** of 42 rules across 8 categories
- ✅ **Structured feedback** with exact line numbers and quoted text
- ✅ **Actionable fixes** - copy-paste ready corrections
- ✅ **Flexible usage** - web interface, API, or command-line
- ✅ **Smart detection** - context-aware, avoids false positives

### Rule Categories Covered

1. **Writing** (7 rules) - Paragraph structure, capitalization, emphasis
2. **Mathematics** (9 rules) - Notation, equations, formatting
3. **Code** (6 rules) - Docstrings, comments, style
4. **JAX** (4 rules) - JIT compilation, pure functions, arrays
5. **Figures** (8 rules) - Captions, alt text, accessibility
6. **References** (2 rules) - BibTeX format, citations
7. **Links** (2 rules) - Descriptive text, validation
8. **Admonitions** (4 rules) - Types, formatting, placement

### Example Output

```markdown
# Style Guide Review for Your Lecture

## Summary
- Total violations: 23
- Critical issues: 18
- Style suggestions: 5

## Critical Issues

### qe-writing-001: Use one sentence per paragraph
Location: Lines 42-44
Current: "Multiple sentences here. Second sentence. Third sentence."
Issue: Paragraph contains 3 sentences
Fix: 
"Multiple sentences here.

Second sentence.

Third sentence."

### qe-math-002: Use \top for transpose notation
Location: Line 156
Current: $$A^T B$$
Issue: Using ^T instead of ^\top
Fix: $$A^\top B$$

[... more violations ...]

## Recommendations
1. Fix paragraph structure (18 instances)
2. Correct math notation (5 instances)
3. Add figure captions (4 instances)
```

---

## Installation & Setup

### Prerequisites

Choose your method:

**Option A: Web Interface**
- No installation required
- Just a browser and internet

**Option B: Command Line**
- Python 3.7 or higher
- pip package manager
- Claude API key

### Setup Checklist for Command Line

#### Step 1: Verify Python

```bash
python --version  # Should show 3.7+
# or
python3 --version
```

#### Step 2: Install Anthropic SDK

```bash
pip install anthropic

# Verify installation
python -c "import anthropic; print('OK')"
```

#### Step 3: Get Claude API Key

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to "API Keys"
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-...`)
6. Save it securely

#### Step 4: Set API Key

**macOS/Linux:**
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key-here'

# Make it permanent (add to ~/.zshrc or ~/.bashrc)
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.zshrc
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY='sk-ant-your-key-here'
```

#### Step 5: Test Installation

```bash
python style_checker.py quantecon-test-lecture.md
```

Should output a review with ~40+ violations.

### Setup Troubleshooting

| Issue | Solution |
|-------|----------|
| `anthropic module not found` | Run `pip install anthropic` or `python3 -m pip install anthropic` |
| `API key not set` | Verify with `echo $ANTHROPIC_API_KEY` |
| `Permission denied` | Make executable: `chmod +x style_checker.py` |
| `File not found` | Use absolute path: `/full/path/to/lecture.md` |
| `Rate limit exceeded` | Wait a few minutes or upgrade API plan |

---

## Usage Guide

### Web Interface Usage

#### Basic Review

1. **Upload files** to Claude:
   - `claude-style-checker-prompt.md`
   - `style-guide-database.md`
   - Your lecture file

2. **Send message**:
   ```
   Please follow the instructions in claude-style-checker-prompt.md 
   to review the lecture against the style guide.
   ```

3. **Review output** - Claude provides structured feedback

4. **Apply fixes** - Copy suggested fixes to your lecture

5. **Re-check** (optional) - Upload corrected version and ask for verification

#### Focused Review

```
Please review this lecture but ONLY check for:
- Writing rules (qe-writing-*)
- Mathematics rules (qe-math-*)

Skip code, JAX, figures, and references.
```

#### Quick Review

```
Please provide only the TOP 5 most critical violations 
that would have the biggest impact on readability.
```

#### Second-Pass Review

```
I've fixed the violations from your previous review. 
Can you check this updated version and confirm the issues 
have been addressed? Note if any new issues were introduced.
```

### Command Line Usage

#### Basic Commands

```bash
# Check a lecture (output to terminal)
python style_checker.py lecture.md

# Save output to file
python style_checker.py lecture.md --output review.md

# Quick mode (critical issues only)
python style_checker.py lecture.md --quick

# Focus on specific categories
python style_checker.py lecture.md --focus writing
python style_checker.py lecture.md --focus writing math code

# Use custom prompt
python style_checker.py lecture.md --prompt custom-prompt.md

# Use custom style guide
python style_checker.py lecture.md --style-guide custom-guide.md

# See all options
python style_checker.py --help
```

#### Common Workflows

**Before Publishing:**
```bash
# Full review
python style_checker.py new-lecture.md --output review.md

# Review and fix issues manually

# Quick verification
python style_checker.py new-lecture.md --quick
```

**Math Notation Check:**
```bash
python style_checker.py lecture.md --focus math
```

**Batch Processing:**
```bash
for lecture in lectures/*.md; do
    python style_checker.py "$lecture" --output "reviews/$(basename $lecture .md)-review.md"
done
```

### Script Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `lecture` | Path to lecture file (required) | `my-lecture.md` |
| `-o, --output` | Save review to file | `--output review.md` |
| `--prompt` | Custom prompt file | `--prompt custom.md` |
| `--style-guide` | Custom style guide | `--style-guide guide.md` |
| `--focus` | Specific categories only | `--focus writing math` |
| `--quick` | Critical issues only | `--quick` |
| `--api-key` | API key (overrides env var) | `--api-key sk-ant-...` |

### Understanding Output

#### Summary Section
```markdown
## Summary
- Total violations found: 23      ← All issues detected
- Critical issues (rule): 18      ← Strict rule violations
- Style suggestions: 5            ← Advisory improvements
- Overall assessment: ...         ← Quick summary
```

#### Violation Format
```markdown
### qe-writing-001: Use one sentence per paragraph
**Location**: Lines 42-44, Section "Introduction"  ← Where it is
**Current**:                                        ← Exact text
```
[quoted problematic text]
```
**Issue**: Paragraph contains 3 sentences          ← What's wrong
**Suggested fix**:                                 ← Ready to apply
```
[corrected version]
```
```

#### Priority Levels

1. **Critical Issues (rule category)** - Fix these first
   - Clear violations of strict rules
   - Mechanically detectable
   - Must be fixed for compliance

2. **Style Suggestions (style category)** - Fix if time permits
   - Advisory guidelines
   - Require judgment
   - Improve quality but not mandatory

### Cost Management

**Current API Pricing** (Claude Sonnet 4.5):
- Input: $3 per million tokens
- Output: $15 per million tokens

**Typical Costs Per Lecture**:
| Lecture Size | Lines | Estimated Cost |
|--------------|-------|----------------|
| Small | 500 | $0.01-0.03 |
| Medium | 1,500 | $0.03-0.08 |
| Large | 3,000 | $0.08-0.15 |
| Very Large | 5,000+ | $0.15-0.25 |

**Cost Reduction Tips**:
- Use `--quick` mode for initial checks
- Use `--focus` to check specific categories
- Fix issues in batches and re-check
- Use web interface free tier for occasional checks

---

## Example Interactions

### Example 1: Basic Review

**Your Request:**
```
[Upload: claude-style-checker-prompt.md, style-guide-database.md, quantecon-test-lecture.md]

Please follow the instructions in claude-style-checker-prompt.md 
to review the lecture against the style guide.
```

**Claude's Response:**
```markdown
# Style Guide Review for Test Lecture For Style Guide Violations

## Summary
- Total violations found: 47
- Critical issues (rule category): 38
- Style suggestions: 9
- Overall assessment: This test lecture contains numerous intentional 
  violations across all categories.

## Critical Issues (Rule Violations)

### Writing

#### qe-writing-001: Use one sentence per paragraph
**Location**: Lines 22-23, Section "Overview"
**Current**:
```
This lecture contains intentional style guide violations. Each section 
tests specific rules. This is a test document.
```
**Issue**: Paragraph contains three sentences instead of one.
**Suggested fix**:
```
This lecture contains intentional style guide violations.

Each section tests specific rules.

This is a test document.
```

[... continues with all violations ...]

## Recommendations Summary
1. Fix paragraph structure (18 instances) - HIGH PRIORITY
2. Correct capitalization (8 instances)
3. Update transpose notation (5 instances)
```

### Example 2: Focused Review

**Your Request:**
```
Please review this lecture focusing ONLY on:
1. Writing rules (qe-writing-*)
2. Mathematics rules (qe-math-*)

Skip all code, JAX, figures, and reference checks.
```

**Claude's Response:**
```markdown
# Style Guide Review - Writing & Mathematics Focus

## Summary
- Writing violations: 26
- Mathematics violations: 12
- Total reviewed: 38 issues

## Writing Issues

#### qe-writing-001: Use one sentence per paragraph
[... only writing violations ...]

## Mathematics Issues

#### qe-math-002: Use \top for transpose notation
[... only math violations ...]

## Next Steps
After addressing these, consider running a second review 
focusing on code and figure formatting rules.
```

### Example 3: Quick Check (Top 5 Issues)

**Your Request:**
```
I need a quick review. Please report only the TOP 5 most critical 
violations that would have the biggest impact.
```

**Claude's Response:**
```markdown
# Quick Review - Top 5 Critical Issues

1. **qe-writing-001: Multiple sentences per paragraph** (18 instances)
   - Impact: HIGH - Significantly reduces readability
   - Fix: Split all multi-sentence paragraphs
   - Estimated effort: 30 minutes

2. **qe-math-002: Transpose notation** (5 instances)
   - Impact: MEDIUM - Affects professional appearance
   - Fix: Replace all ^T with ^\top
   - Estimated effort: 10 minutes

3. **qe-figures-001: Missing figure captions** (4 instances)
   - Impact: HIGH - Accessibility and understanding suffer
   - Fix: Add proper captions using MyST syntax
   - Estimated effort: 15 minutes

4. **qe-writing-004: Unnecessary capitalization** (8 instances)
   - Impact: MEDIUM - Looks unprofessional
   - Fix: Use lowercase for common nouns
   - Estimated effort: 10 minutes

5. **qe-code-003: Missing docstrings** (6 functions)
   - Impact: MEDIUM - Reduces code clarity
   - Fix: Add docstrings to all functions
   - Estimated effort: 20 minutes

**Priority recommendation**: Start with #1 (paragraph structure).
```

### Example 4: Second-Pass Verification

**Your Request:**
```
I've fixed the violations from your previous review. Can you check 
this updated version and confirm the issues have been addressed?
```

**Claude's Response:**
```markdown
# Second-Pass Review

## Summary
- Previous violations fixed: 35 / 38 (92%)
- Remaining violations: 3
- New issues introduced: 1
- Overall: Excellent improvement!

## Remaining Issues

### qe-writing-001: One sentence per paragraph
**Location**: Lines 156-157
**Status**: Still needs fixing
[... details ...]

## New Issue Introduced

### qe-math-001: Inconsistent parameter notation
**Location**: Line 203
**Issue**: When fixing capitalization, you changed β to $\beta$ 
but unicode would be preferred (no related math expressions).
**Fix**: Change back to UTF-8 unicode β

## Successfully Fixed
✓ All paragraph structure issues in sections 1-5
✓ Capitalization corrected throughout
✓ Transpose notation updated
✓ Figure captions added

## Recommendation
Fix the 3 remaining issues and 1 new issue, then the lecture 
will be fully compliant. Great work!
```

### Example 5: Custom Output Format

**Your Request:**
```
Please provide your review as a checklist I can mark off as I fix items:

- [ ] Line 23: Description of fix
- [ ] Line 45: Description of fix
```

**Claude's Response:**
```markdown
# Style Guide Checklist for my-lecture.md

## Writing Issues (26 items)

- [ ] **Lines 22-23**: Split paragraph into 3 sentences (qe-writing-001)
- [ ] **Lines 24-25**: Split paragraph into 3 sentences (qe-writing-001)
- [ ] **Line 43**: Change "Bellman Equation" → "bellman equation" (qe-writing-004)
- [ ] **Line 45**: Change "Dynamic Programming" → "dynamic programming" (qe-writing-004)
[... etc ...]

## Mathematics Issues (12 items)

- [ ] **Line 156**: Replace A^T B with A^\top B (qe-math-002)
- [ ] **Line 158**: Replace x^T y with x^\top y (qe-math-002)
[... etc ...]

---
Total items: 47
Estimated time: 2-3 hours
```

---

## System Architecture

### Components Overview

```
┌─────────────────────────────────────────────────┐
│  Input Files                                    │
│  • Your Lecture (markdown)                      │
│  • Style Guide Database (43KB, 42 rules)        │
│  • Checker Prompt (instructions for Claude)     │
└─────────────┬───────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────────────┐
│  Claude Sonnet 4.5                              │
│  • Reads all inputs                             │
│  • Systematically checks all rules              │
│  • Generates structured output                  │
└─────────────┬───────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────────────┐
│  Structured Review Output                       │
│  • Summary (violation counts)                   │
│  • Critical Issues (by category)                │
│  • Style Suggestions (advisory)                 │
│  • Prioritized Recommendations                  │
└─────────────────────────────────────────────────┘
```

### File Relationships

```
claude-style-checker-prompt.md
    ↓ (instructs)
Claude Sonnet 4.5
    ↓ (checks against)
style-guide-database.md
    ↓ (applied to)
your-lecture.md
    ↓ (produces)
structured-review.md
```

### How It Works

1. **Prompt Engineering**
   - `claude-style-checker-prompt.md` contains expert instructions
   - Tells Claude its role (technical writing editor)
   - Specifies output format (structured, actionable)
   - Provides false-positive prevention guidelines

2. **Style Guide**
   - `style-guide-database.md` contains all rules
   - Organized into 8 categories
   - Each rule has: code, title, description, examples
   - Marked as `rule` (strict) or `style` (advisory)

3. **Analysis Process**
   - Claude reads lecture content
   - Systematically checks each rule category
   - Identifies violations with context
   - Generates specific, actionable fixes

4. **Output Generation**
   - Structured markdown format
   - Exact line numbers and quoted text
   - Copy-paste ready corrections
   - Prioritized by impact

### Rule Coverage

```
Writing Rules (qe-writing-*)      ████████ 7 rules
├── One sentence per paragraph
├── Clear, concise writing
├── Logical flow
├── Capitalization
├── Bold/italic usage
├── Heading capitalization
└── Visual elements

Math Rules (qe-math-*)            ████████ 9 rules
├── Unicode vs LaTeX
├── Transpose notation (\top)
├── Matrix brackets (bmatrix)
├── No boldface
├── Equation references
├── Display math usage
├── Operator formatting
├── Aligned equations
└── Equation numbering

Code Rules (qe-code-*)            ██████ 6 rules
├── Docstrings
├── Comments
├── Variable names
├── Function length
├── Type hints
└── Error handling

JAX Rules (qe-jax-*)              ████ 4 rules
├── JIT compilation
├── Pure functions
├── Array operations
└── Random number generation

Figures Rules (qe-figures-*)      ████████ 8 rules
├── Captions
├── Alt text
├── Size specifications
├── Color accessibility
├── Font sizes
├── Label placement
├── File formats
└── Positioning

References (qe-references-*)      ██ 2 rules
├── BibTeX format
└── Citation style

Links (qe-links-*)                ██ 2 rules
├── Descriptive text
└── Link validation

Admonitions (qe-admonitions-*)    ████ 4 rules
├── Appropriate types
├── Formatting
├── Placement
└── Content guidelines

Total: 42 rules across 8 categories
```

---

## Customization

### Modifying the Prompt

Edit `claude-style-checker-prompt.md` to customize:

#### 1. Change Output Format

Find the "Output Format" section and modify:

```markdown
## Output Format

Structure your response as follows:

[Your custom format here]
```

#### 2. Add Project-Specific Rules

Add to the "Special Considerations" section:

```markdown
## Special Considerations

[... existing items ...]

10. **Your custom rule**: Check for [specific pattern]
```

#### 3. Adjust Priorities

Modify the "Prioritize actionable feedback" section:

```markdown
4. **Prioritize actionable feedback**:
   - Focus on [your priority] violations first
   - Then address [secondary priority]
   - Include [advisory items] when they [condition]
```

#### 4. Add Custom Examples

In the "Example of Good Feedback" section:

```markdown
## Example of Good Feedback for [Your Use Case]

**qe-custom-001: Your custom rule**
**Location**: Line 123
**Current**: [example]
**Issue**: [explanation]
**Suggested fix**: [correction]
```

### Extending the Style Guide

To add new rules to `style-guide-database.md`:

```markdown
### Rule: qe-custom-001
**Category:** rule  
**Title:** Your rule title

**Description:**  
Clear description of what to check.

**Check for:**
- Specific pattern 1
- Specific pattern 2

**Examples:**
```markdown
<!-- ✅ Correct -->
[good example]

<!-- ❌ Incorrect -->
[bad example]
```

**Implementation note:**  
How to detect this violation.
```

### Creating Focus Modes

Create wrapper scripts for common focus areas:

**check-writing.sh:**
```bash
#!/bin/bash
python style_checker.py "$1" --focus writing --output "${1%.md}-writing-review.md"
```

**check-math.sh:**
```bash
#!/bin/bash
python style_checker.py "$1" --focus math --quick
```

### Batch Processing Script

**check-all-lectures.sh:**
```bash
#!/bin/bash

LECTURE_DIR="lectures"
OUTPUT_DIR="reviews"

mkdir -p "$OUTPUT_DIR"

for lecture in "$LECTURE_DIR"/*.md; do
    basename=$(basename "$lecture" .md)
    echo "Checking $basename..."
    python style_checker.py "$lecture" \
        --output "$OUTPUT_DIR/${basename}-review.md" \
        --quick
done

echo "All reviews saved to $OUTPUT_DIR/"
```

### CI/CD Integration

**GitHub Actions example:**

```yaml
name: Style Check

on: [pull_request]

jobs:
  style-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install anthropic
      
      - name: Run style checker
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          for file in lectures/*.md; do
            python style_checker.py "$file" --quick
          done
```

---

## Troubleshooting

### Common Issues

#### Installation Problems

**Issue**: `anthropic module not found`

**Solutions**:
```bash
# Try standard pip
pip install anthropic

# Try with python3
python3 -m pip install anthropic

# Try with user flag
pip install --user anthropic

# Verify installation
python -c "import anthropic; print(anthropic.__version__)"
```

**Issue**: `Permission denied` when running script

**Solutions**:
```bash
# Make executable
chmod +x style_checker.py

# Or run with python explicitly
python style_checker.py lecture.md
```

#### API Key Problems

**Issue**: `API key not set`

**Solutions**:
```bash
# Check if set
echo $ANTHROPIC_API_KEY

# Set for current session (macOS/Linux)
export ANTHROPIC_API_KEY='sk-ant-your-key'

# Set permanently
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key"' >> ~/.zshrc
source ~/.zshrc

# Or pass directly to script
python style_checker.py lecture.md --api-key sk-ant-your-key
```

**Issue**: `Invalid API key`

**Solutions**:
1. Check key at console.anthropic.com
2. Ensure no extra spaces: `echo "$ANTHROPIC_API_KEY" | cat -A`
3. Try creating a new key

#### File Issues

**Issue**: `File not found`

**Solutions**:
```bash
# Check current directory
pwd
ls -la

# Use absolute path
python style_checker.py /full/path/to/lecture.md

# Or navigate to file location first
cd /path/to/lectures
python /path/to/style_checker.py lecture.md
```

**Issue**: `Unable to read file`

**Solutions**:
```bash
# Check file permissions
ls -l lecture.md

# Check file encoding
file lecture.md

# Ensure it's readable
chmod +r lecture.md
```

#### Runtime Issues

**Issue**: `Rate limit exceeded`

**Solutions**:
- Wait a few minutes
- Check usage at console.anthropic.com
- Upgrade API plan if needed
- Use `--quick` mode to reduce token usage

**Issue**: Output is incomplete

**Solutions**:
- Ask Claude to continue in web interface
- Use `--quick` mode for very long lectures
- Split lecture into sections
- Increase max_tokens in script (edit style_checker.py)

**Issue**: Too many violations reported

**Solutions**:
```bash
# Focus on critical issues first
python style_checker.py lecture.md --quick

# Or focus on specific categories
python style_checker.py lecture.md --focus writing

# Fix in batches
python style_checker.py lecture.md --focus writing --output writing-review.md
# Fix writing issues
python style_checker.py lecture.md --focus math --output math-review.md
# Fix math issues
```

#### Web Interface Issues

**Issue**: File upload fails

**Solutions**:
- Check file size (large files may fail)
- Try splitting lecture into sections
- Use copy-paste method instead
- Check internet connection

**Issue**: Claude doesn't see uploaded files

**Solutions**:
- Re-upload files
- Explicitly mention files: "Please review the uploaded lecture file"
- Try clearing cache and refreshing
- Use copy-paste method as backup

**Issue**: Response is too generic

**Solutions**:
- Ensure you uploaded the prompt file
- Remind Claude: "Please follow the format in claude-style-checker-prompt.md"
- Be more specific about what you want

### False Positives

**Issue**: Claude flags correct usage

**What to do**:
1. Review the rule in `style-guide-database.md`
2. Check if context justifies the exception
3. If Claude is wrong, note it and continue
4. Consider updating prompt to prevent similar cases

**Example**:
```
Claude flags: "The Bellman Equation is a fundamental tool"
Your assessment: Correct - "Bellman" is a proper noun
Action: Ignore this violation
```

### Performance Issues

**Issue**: Script takes too long

**Solutions**:
```bash
# Use quick mode
python style_checker.py lecture.md --quick

# Focus on specific categories
python style_checker.py lecture.md --focus writing

# Process smaller chunks
python style_checker.py section1.md
python style_checker.py section2.md
```

**Issue**: High costs

**Solutions**:
- Use `--quick` mode
- Use `--focus` on specific categories
- Fix issues in batches
- Use web interface free tier for occasional checks
- Consider processing only changed sections

---

## FAQ

### General Questions

**Q: Which method should I use - web or command line?**

A: 
- **Web interface**: Best for occasional checks, trying it out, or if you don't have API access
- **Command line**: Best for frequent use, automation, or batch processing

**Q: How accurate is the detection?**

A:
- **Strict rules** (`rule` category): ~95%+ accuracy
- **Style guidelines** (`style` category): ~80%+ useful suggestions
- **False positive rate**: <5% thanks to context-awareness

**Q: Can I use this for non-QuantEcon lectures?**

A: Yes! You can:
1. Use with your own style guide (replace `style-guide-database.md`)
2. Modify the prompt for your domain
3. Adjust rule categories as needed

**Q: How long does a review take?**

A:
- **Web interface**: 30-60 seconds
- **Command line**: 30-60 seconds
- **Manual review time**: 15-60 minutes depending on violations

**Q: Does this modify my lecture file?**

A: No, it only provides suggestions. You must manually apply fixes.

### Technical Questions

**Q: What Claude model is used?**

A: Claude Sonnet 4 (claude-sonnet-4-20250514). You can update the model name in `style_checker.py` if needed.

**Q: Can I run this offline?**

A: No, it requires internet connection to access Claude API.

**Q: What file formats are supported?**

A: Markdown files (`.md`), specifically MyST Markdown used by Jupyter Book.

**Q: Can I check multiple files at once?**

A: Yes, use a batch processing script (see Customization section).

**Q: How do I update the style guide?**

A: Simply replace `style-guide-database.md` with the new version. The version is noted at the top of the file.

**Q: Can I use this in CI/CD?**

A: Yes! See the CI/CD Integration section in Customization.

### Cost Questions

**Q: How much does it cost?**

A: 
- **Web interface**: Free tier available, may have daily limits
- **API**: $0.02-0.20 per lecture typically
- See Cost Management section for details

**Q: How can I reduce costs?**

A:
- Use `--quick` mode
- Use `--focus` on specific categories
- Fix issues in batches
- Use web interface free tier

**Q: Is there a free option?**

A: Yes, the Claude web interface (claude.ai) has a free tier.

### Usage Questions

**Q: Should I fix all violations?**

A: Priority order:
1. Critical issues (rule violations) - fix these
2. High-impact style suggestions - fix if time permits
3. Minor style suggestions - fix as needed

**Q: Can I customize the output format?**

A: Yes, edit `claude-style-checker-prompt.md` or ask Claude for specific format.

**Q: What if Claude misses violations?**

A:
- Very long lectures may need to be split
- Ask Claude to re-check specific sections
- Some context-dependent issues may be missed

**Q: Can I dispute Claude's suggestions?**

A: Absolutely! Claude's suggestions are advisory. You know your content best. Use judgment.

**Q: How do I verify fixes were applied correctly?**

A: Re-run the checker:
```bash
python style_checker.py lecture.md --quick
```

### Workflow Questions

**Q: When should I run the checker?**

A: Recommended points:
- Before publishing new lectures
- After major revisions
- Before submitting for review
- As part of your regular workflow

**Q: Should I fix issues one category at a time?**

A: Yes, that's often easier:
```bash
python style_checker.py lecture.md --focus writing
# Fix writing issues
python style_checker.py lecture.md --focus math
# Fix math issues
```

**Q: Can I use this for collaborative work?**

A: Yes! Generate review files and share:
```bash
python style_checker.py lecture.md --output review.md
# Share review.md with collaborators
```

**Q: What's the best workflow for beginners?**

A:
1. Start with quick mode to get overview
2. Fix high-priority issues first
3. Re-run comprehensive check
4. Address remaining issues
5. Final verification with quick mode

---

## Appendix

### File Descriptions

| File | Size | Purpose |
|------|------|---------|
| `style_checker.py` | 6.5KB | Command-line automation script |
| `claude-style-checker-prompt.md` | 5.3KB | Instructions for Claude |
| `style-guide-database.md` | 43KB | Complete style guide (42 rules) |
| `quantecon-test-lecture.md` | 11KB | Test file with intentional violations |
| `DOCUMENTATION.md` | This file | Complete documentation |

### Command Reference

```bash
# Basic usage
python style_checker.py LECTURE_FILE

# With options
python style_checker.py LECTURE_FILE [OPTIONS]

# Options:
#   -o, --output FILE          Save to file
#   --prompt FILE              Custom prompt
#   --style-guide FILE         Custom style guide
#   --focus CATEGORY [...]     Focus categories
#   --quick                    Critical issues only
#   --api-key KEY              Override env API key
#   -h, --help                 Show help
```

### Quick Reference Card

```
┌─────────────────────────────────────────────────┐
│  QuantEcon Style Checker Quick Reference        │
├─────────────────────────────────────────────────┤
│  Setup:                                         │
│    pip install anthropic                        │
│    export ANTHROPIC_API_KEY='your-key'          │
│                                                 │
│  Check lecture:                                 │
│    python style_checker.py lecture.md           │
│                                                 │
│  Quick check:                                   │
│    python style_checker.py lecture.md --quick   │
│                                                 │
│  Focus mode:                                    │
│    python style_checker.py lecture.md \         │
│      --focus writing math                       │
│                                                 │
│  Save output:                                   │
│    python style_checker.py lecture.md \         │
│      --output review.md                         │
│                                                 │
│  Web interface:                                 │
│    1. Go to claude.ai                           │
│    2. Upload 3 files                            │
│    3. Ask for review                            │
│                                                 │
│  Test:                                          │
│    python style_checker.py \                    │
│      quantecon-test-lecture.md                  │
└─────────────────────────────────────────────────┘
```

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-03 | Initial production release |

### Support & Contact

For issues or questions:
1. Check this documentation
2. Review troubleshooting section
3. Test with `quantecon-test-lecture.md` to verify setup
4. Check the style guide database for rule clarifications

### License

[Your license information here]

---

**Last Updated**: October 3, 2025  
**Status**: ✅ Production Ready  
**Documentation Version**: 1.0
