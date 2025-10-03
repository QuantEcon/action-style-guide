# Example Claude Interaction

This file shows exactly what a conversation with Claude would look like when using the style checker prompt.

## Example 1: Basic Usage

### Your Message to Claude:

```
[Attach three files: claude-style-checker-prompt.md, style-guide-database.md, quantecon-test-lecture.md]

Please follow the instructions in claude-style-checker-prompt.md to review 
the quantecon-test-lecture.md file against the style guide database.
```

### Claude's Expected Response:

```markdown
# Style Guide Review for Test Lecture For Style Guide Violations

## Summary
- Total violations found: 47
- Critical issues (rule category): 38
- Style suggestions: 9
- Overall assessment: This test lecture contains numerous intentional violations across all categories, serving as a good test case for the style checker.

## Critical Issues (Rule Violations)

### Writing

#### qe-writing-001: Use one sentence per paragraph
**Location**: Lines 22-23, Section "Overview"
**Current**:
```
This lecture contains intentional style guide violations for testing purposes. Each section tests specific rules from the QuantEcon style guide database. This is a test document and should not be used as a reference for proper formatting.
```
**Issue**: Paragraph contains three sentences instead of one.
**Suggested fix**:
```
This lecture contains intentional style guide violations for testing purposes.

Each section tests specific rules from the QuantEcon style guide database.

This is a test document and should not be used as a reference for proper formatting.
```

#### qe-writing-001: Use one sentence per paragraph
**Location**: Lines 24-25, Section "Overview"
**Current**:
```
This lecture demonstrates various common mistakes. We will cover writing violations, mathematical notation errors, code style issues, JAX conversion patterns, figure formatting problems, and reference citation mistakes. All of these are intentionally wrong to test the style checker.
```
**Issue**: Paragraph contains three sentences.
**Suggested fix**:
```
This lecture demonstrates various common mistakes.

We will cover writing violations, mathematical notation errors, code style issues, JAX conversion patterns, figure formatting problems, and reference citation mistakes.

All of these are intentionally wrong to test the style checker.
```

**Pattern note**: This violation occurs throughout the document in sections: "Multiple Sentences Per Paragraph", "Overview", and others.

#### qe-writing-004: Avoid unnecessary capitalization in narrative text
**Location**: Lines 43-47, Section "Unnecessary Capitalization"
**Current**:
```
The Bellman Equation is a fundamental tool in Dynamic Programming.

We use the Method of Lagrange Multipliers to solve the Optimization Problem.

The Nash Equilibrium is a Solution Concept in Game Theory.
```
**Issue**: Common nouns are incorrectly capitalized mid-sentence.
**Suggested fix**:
```
The bellman equation is a fundamental tool in dynamic programming.

We use the method of Lagrange multipliers to solve the optimization problem.

The Nash equilibrium is a solution concept in game theory.
```

[... many more violations ...]

### Mathematics

#### qe-math-002: Use \top for transpose notation
**Location**: Line 156 (approximate)
**Current**: `$$A^T B$$`
**Issue**: Using `^T` instead of `^\top` for transpose.
**Suggested fix**: `$$A^\top B$$`

[... more violations ...]

## Recommendations Summary

1. **Fix paragraph structure** (18 instances): Split multi-sentence paragraphs
2. **Correct capitalization** (8 instances): Remove unnecessary caps from common nouns
3. **Update transpose notation** (5 instances): Replace `^T` with `^\top`
4. **Fix figure formatting**: Add proper captions and alt text
5. **Update code documentation**: Add docstrings to functions

## Positive Observations

1. The lecture uses proper MyST Markdown syntax for code cells
2. Import statements are clearly organized
3. The overall structure with sections is logical
```

---

## Example 2: Focused Review

### Your Message to Claude:

```
[Attach the same three files]

Please review this lecture but ONLY check for:
1. Writing rules (qe-writing-*)
2. Mathematics rules (qe-math-*)

Skip all code, JAX, figures, and reference checks. I want to focus on 
improving the prose and mathematical notation first.
```

### Claude's Response:

```markdown
# Style Guide Review - Writing & Mathematics Focus

## Summary
- Writing violations: 26
- Mathematics violations: 12
- Total reviewed: 38 issues

## Writing Issues

[Same detailed format as above, but only writing-related violations]

## Mathematics Issues

[Only math-related violations]

## Next Steps

After addressing these writing and mathematics issues, consider running 
a second review focusing on code and figure formatting rules.
```

---

## Example 3: Quick Mode

### Your Message:

```
[Attach files]

I need a quick review. Please only report the TOP 5 most critical 
violations that would have the biggest impact on readability and 
professional appearance.
```

### Claude's Response:

```markdown
# Quick Review - Top 5 Critical Issues

1. **qe-writing-001: Multiple sentences per paragraph** (18 instances)
   - Impact: HIGH - Significantly reduces readability
   - Fix: Split all multi-sentence paragraphs into single-sentence paragraphs
   - Estimated effort: 30 minutes

2. **qe-math-002: Transpose notation** (5 instances)  
   - Impact: MEDIUM - Affects professional appearance
   - Fix: Replace all `^T` with `^\top` in mathematical expressions
   - Estimated effort: 10 minutes

3. **qe-figures-001: Missing figure captions** (4 instances)
   - Impact: HIGH - Accessibility and understanding suffer
   - Fix: Add proper captions to all figures using MyST syntax
   - Estimated effort: 15 minutes

4. **qe-writing-004: Unnecessary capitalization** (8 instances)
   - Impact: MEDIUM - Looks unprofessional
   - Fix: Use lowercase for common nouns
   - Estimated effort: 10 minutes

5. **qe-code-003: Missing docstrings** (6 functions)
   - Impact: MEDIUM - Reduces code clarity
   - Fix: Add docstrings to all functions
   - Estimated effort: 20 minutes

**Priority recommendation**: Start with fixing paragraph structure (#1) 
as it has the highest impact on readability.
```

---

## Example 4: Second-Pass Review

### Your Message:

```
[Attach: claude-style-checker-prompt.md, style-guide-database.md, and 
your CORRECTED lecture file]

I've fixed the violations from your previous review. Can you please 
check this updated version and confirm the issues have been properly 
addressed? Also note if any new issues were introduced.
```

### Claude's Response:

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
**Current**: [shows the text]
**Fix**: [provides correction]

[... 2 more remaining issues ...]

## New Issue Introduced

### qe-math-001: Inconsistent parameter notation
**Location**: Line 203
**Issue**: When you fixed the capitalization, you also changed `β` to `$\beta$` 
but this introduces inline math where unicode would be preferred (no related 
mathematical expressions in that paragraph).
**Fix**: Change back to UTF-8 unicode `β`

## Successfully Fixed

✓ All paragraph structure issues in sections 1-5
✓ Capitalization corrected throughout
✓ Transpose notation updated
✓ Figure captions added
✓ Code docstrings added

## Recommendation

Fix the 3 remaining issues and the 1 new issue, then the lecture will be 
fully compliant with the style guide. Great work on the improvements!
```

---

## Example 5: Requesting Different Output Format

### Your Message:

```
[Attach files]

Please review the lecture, but instead of the standard format, provide 
your output as a markdown file with inline comments that I can use as 
a checklist. Format like:

- [ ] Line 23: Fix paragraph - split into 3 separate paragraphs
- [ ] Line 45: Change "Dynamic Programming" to "dynamic programming"

This way I can check off items as I fix them.
```

### Claude's Response:

```markdown
# Style Guide Checklist for quantecon-test-lecture.md

## Writing Issues (26 items)

- [ ] **Lines 22-23**: Split paragraph into 3 sentences (qe-writing-001)
- [ ] **Lines 24-25**: Split paragraph into 3 sentences (qe-writing-001)  
- [ ] **Line 43**: Change "The Bellman Equation" to "The bellman equation" (qe-writing-004)
- [ ] **Line 45**: Change "Dynamic Programming" to "dynamic programming" (qe-writing-004)
- [ ] **Line 47**: Change "Method of Lagrange Multipliers" to "method of Lagrange multipliers" (qe-writing-004)
[... etc ...]

## Mathematics Issues (12 items)

- [ ] **Line 156**: Replace `A^T B` with `A^\top B` (qe-math-002)
- [ ] **Line 158**: Replace `x^T y` with `x^\top y` (qe-math-002)
[... etc ...]

## Code Issues (8 items)

[... etc ...]

---
Total items: 47
Estimated time to fix all: 2-3 hours
```

---

## Tips for Using These Examples

1. **Copy the message format**: Use the example messages as templates
2. **Adjust specificity**: Add more context if you want Claude to focus on specific aspects
3. **Iterate**: You can have a back-and-forth conversation with Claude about specific violations
4. **Ask for explanations**: If a violation isn't clear, ask "Why is this flagged as qe-writing-004?"
5. **Request examples**: Ask "Can you show me 2-3 more examples of correct usage for qe-math-001?"

## Advanced Techniques

### Ask Claude to explain a specific rule
```
Looking at qe-math-001, I'm confused about when to use unicode vs inline math.
Can you provide 5 examples showing the difference between correct and 
incorrect usage?
```

### Request a corrected version
```
After showing me the violations, please also provide a fully corrected 
version of the "Mathematics" section with all fixes applied.
```

### Get help prioritizing
```
I only have 30 minutes to improve this lecture. Which violations should 
I fix first to get the biggest improvement in quality?
```

### Domain-specific focus
```
This lecture is about dynamic programming. Please pay extra attention to 
mathematical notation and ensure the Bellman equation formatting follows 
the style guide precisely.
```
