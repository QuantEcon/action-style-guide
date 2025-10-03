# QuantEcon Style Checker - System Architecture

## File Organization

```
prompt-experiments/
│
├── 📋 CORE SYSTEM FILES
│   ├── claude-style-checker-prompt.md  (5.3K)  ⭐ Main prompt
│   ├── style-guide-database.md         (43K)   📚 Your style guide
│   └── style_checker.py                (6.5K)  🔧 Automation script
│
├── 📖 DOCUMENTATION
│   ├── QUICK-START.md                  (6.2K)  🚀 Start here
│   ├── README.md                       (5.9K)  📝 Project overview
│   ├── usage-guide.md                  (5.8K)  📚 Complete guide
│   ├── example-interactions.md         (10K)   💬 Real examples
│   └── SUMMARY.md                      (8.9K)  📊 This summary
│
├── 🧪 TESTING FILES
│   ├── quantecon-test-lecture.md       (11K)   ✓ Test lecture
│   ├── test_lecture.md                 (870B)  ✓ Original test
│   └── test_prompt.py                  (2.5K)  ✓ Original tester
│
└── 📁 prompts/
    ├── strict.md                                Alternative prompts
    ├── friendly.md                              for comparison
    └── math_only.md
```

## Usage Flow Diagram

### Method 1: Web Interface (Fastest, No Setup)

```
┌─────────────────────────────────────────────────────────┐
│  1. Go to claude.ai                                     │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  2. Upload three files:                                 │
│     • claude-style-checker-prompt.md                    │
│     • style-guide-database.md                           │
│     • your-lecture.md                                   │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  3. Send message:                                       │
│     "Please review the lecture against the style guide" │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  4. Receive structured review with:                     │
│     • Summary (total violations)                        │
│     • Critical issues by category                       │
│     • Specific fixes for each violation                 │
│     • Prioritized recommendations                       │
└─────────────────────────────────────────────────────────┘
```

### Method 2: Python Script (Automated)

```
┌─────────────────────────────────────────────────────────┐
│  Setup (one time):                                      │
│  $ pip install anthropic                                │
│  $ export ANTHROPIC_API_KEY='your-key'                  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Run checker:                                           │
│  $ python style_checker.py lecture.md                   │
│                                                         │
│  Options:                                               │
│  --quick           (critical issues only)               │
│  --focus writing   (specific categories)                │
│  --output file.md  (save to file)                       │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Script automatically:                                  │
│  1. Loads prompt, style guide, and lecture              │
│  2. Sends to Claude API                                 │
│  3. Returns formatted review                            │
│  4. Shows cost and token usage                          │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌──────────────────┐
│  Your Lecture    │
│  (markdown)      │
└────────┬─────────┘
         │
         ├──────────────────┐
         │                  │
         ↓                  ↓
┌──────────────────┐   ┌──────────────────┐
│  Style Guide     │   │  Checker Prompt  │
│  Database        │   │  (instructions)  │
│  (43K rules)     │   │  (5.3K)          │
└────────┬─────────┘   └────────┬─────────┘
         │                      │
         └──────────┬───────────┘
                    │
                    ↓
         ┌────────────────────┐
         │  Claude Sonnet 4.5 │
         │  (LLM Analysis)    │
         └────────┬───────────┘
                  │
                  ↓
         ┌────────────────────┐
         │  Structured Review │
         │                    │
         │  • Violations      │
         │  • Line numbers    │
         │  • Exact fixes     │
         │  • Priorities      │
         └────────────────────┘
```

## Rule Categories Coverage

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
├── Transpose notation
├── Matrix brackets
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
└── Link checking

Admonitions (qe-admonitions-*)    ████ 4 rules
├── Appropriate types
├── Formatting
├── Placement
└── Content guidelines

Total: 42 rules across 8 categories
```

## Output Example Structure

```markdown
# Style Guide Review for [Lecture Title]

┌─────────────────────────────────────────┐
│ Summary                                 │
│ • Total violations: 23                  │
│ • Critical issues: 18                   │
│ • Style suggestions: 5                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Critical Issues (Rule Violations)       │
│                                         │
│ ┌─ Writing ─────────────────────────┐  │
│ │                                   │  │
│ │ qe-writing-001                    │  │
│ │ Location: Lines 42-44             │  │
│ │ Current: [quoted text]            │  │
│ │ Issue: [explanation]              │  │
│ │ Fix: [corrected version]          │  │
│ │                                   │  │
│ │ qe-writing-004                    │  │
│ │ ...                               │  │
│ └───────────────────────────────────┘  │
│                                         │
│ ┌─ Mathematics ──────────────────────┐ │
│ │ qe-math-002                        │ │
│ │ ...                                │ │
│ └────────────────────────────────────┘ │
│                                         │
│ [... other categories ...]             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Style Suggestions (Advisory)            │
│ • Suggestion 1                          │
│ • Suggestion 2                          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Recommendations Summary                 │
│ 1. Fix paragraph structure (priority)   │
│ 2. Correct math notation                │
│ 3. Update figure captions               │
└─────────────────────────────────────────┘
```

## Integration Points

```
┌─────────────────────────────────────────────────────┐
│  Existing Workflow                                  │
│                                                     │
│  Write Lecture → Manual Review → Publish            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  Enhanced Workflow with Style Checker               │
│                                                     │
│  Write Lecture                                      │
│       ↓                                             │
│  Automated Style Check ← [New!]                     │
│       ↓                                             │
│  Fix Critical Issues                                │
│       ↓                                             │
│  Quick Re-check ← [New!]                            │
│       ↓                                             │
│  Manual Review (faster!)                            │
│       ↓                                             │
│  Publish                                            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  Advanced: CI/CD Integration                        │
│                                                     │
│  Git Push                                           │
│       ↓                                             │
│  GitHub Action                                      │
│       ↓                                             │
│  Run style_checker.py                               │
│       ↓                                             │
│  Post review as comment                             │
│       ↓                                             │
│  Manual review & merge                              │
└─────────────────────────────────────────────────────┘
```

## Quick Command Reference

```bash
# Basic usage
python style_checker.py lecture.md

# Save output
python style_checker.py lecture.md --output review.md

# Quick check (critical only)
python style_checker.py lecture.md --quick

# Focus on specific categories
python style_checker.py lecture.md --focus writing
python style_checker.py lecture.md --focus writing math
python style_checker.py lecture.md --focus writing math code

# Custom prompt
python style_checker.py lecture.md --prompt custom-prompt.md

# Custom style guide
python style_checker.py lecture.md --style-guide custom-guide.md

# Help
python style_checker.py --help
```

## File Relationships

```
QUICK-START.md ──────────┐
                         ↓
                    (points to)
                         ↓
usage-guide.md ──────→ claude-style-checker-prompt.md ←── (uses)
     ↓                       ↓                              ↓
(explains)              (loads)                         (executes)
     ↓                       ↓                              ↓
example-interactions.md → style_checker.py ──→ style-guide-database.md
     ↑                       ↓
     └─── (demos) ──────────┘

README.md ────────────→ (references all)
SUMMARY.md ───────────→ (summarizes all)
```

## Support Documentation Path

```
┌────────────────────────────────────────────────┐
│  "I want to get started quickly"              │
│  → Read QUICK-START.md                        │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│  "How do I use this in different ways?"       │
│  → Read usage-guide.md                        │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│  "Show me real examples"                      │
│  → Read example-interactions.md               │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│  "What is this project about?"                │
│  → Read README.md                             │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│  "What did I get and how does it all work?"   │
│  → Read SUMMARY.md                            │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│  "How do I customize the prompt?"             │
│  → Edit claude-style-checker-prompt.md        │
└────────────────────────────────────────────────┘
```

## Success Metrics Dashboard

```
┌─────────────────────────────────────────────────┐
│  Coverage                                       │
│  ████████████████████ 100% (8/8 categories)    │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  Rules Checked                                  │
│  ████████████████████ 42 individual rules      │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  Documentation                                  │
│  ████████████████████ 5 guides, 1500+ lines    │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  Usage Methods                                  │
│  ████████████████████ 3 (Web, API, Script)     │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  Cost per Lecture                               │
│  ████░░░░░░░░░░░░░░░░ $0.02-0.20               │
└─────────────────────────────────────────────────┘
```

---

**Status**: ✅ Production Ready
**Version**: 1.0
**Last Updated**: October 3, 2025
**Files Created**: 11
**Total Size**: ~110KB
**Documentation**: Complete
