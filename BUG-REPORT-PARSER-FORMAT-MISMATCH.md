# CRITICAL BUG REPORT - v0.3.x

**Date:** October 10, 2025  
**Severity:** CRITICAL - Core functionality broken  
**Affects:** v0.3.0, v0.3.1

---

## Problem

The GitHub Action reports "No issues found" for lectures that clearly have style violations.

**Test Case:**
- File: `additive_functionals.md` (41,882 chars)
- Expected: 15 writing violations (verified with `tool-style-checker`)
- Actual (v0.3.1): "✓ No issues found"

---

## Root Cause

**MISMATCH between prompt output format and parser expectations:**

### What the Parser Expects (`parse_markdown_response()`)

```markdown
# Review Results

## Summary
<summary text>

## Issues Found
12

## Violations

### Violation 1: qe-writing-001 - Use one sentence per paragraph
- **Severity:** error
- **Location:** Line 45-47
- **Description:** ...
- **Current text:**
```
<text>
```
- **Suggested fix:**
```
<fix>
```
- **Explanation:** ...

## Corrected Content

```markdown
<corrected_content>
```
```

### What the Prompts Actually Request

The prompts (`style_checker/prompts/*.md`) request:

```markdown
# Writing Style Review for [filename]

## Summary
- Total writing violations: [number] issues found
- Critical issues: [number] issues require attention

## Critical Writing Issues

### [Rule Code]: [Rule Title]
**Location**: Line [X]
**Current**: "..."
**Issue**: ...
**Fix**: ...
```

**These formats are COMPLETELY DIFFERENT!**

---

## Why This Wasn't Caught

1. **No integration tests** with real API calls in CI/CD
2. **Parser tests** use mock data that matches expected format
3. **tool-style-checker** doesn't use a parser (saves raw output)
4. **Different workflows**: 
   - tool-style-checker: Direct API call → Save response
   - GitHub Action: API call → Parse → Extract violations → Apply fixes

---

## Impact

**COMPLETE FAILURE** of core functionality:
- ❌ No violations detected (parser can't find them)
- ❌ No fixes applied
- ❌ PRs show "No issues found" when issues exist
- ❌ Users get false confidence in lecture quality

**Why "No issues" is returned:**
```python
# parse_markdown_response() in reviewer.py
issues_match = re.search(r'## Issues Found\s*\n(\d+)', response)
if issues_match:
    result['issues_found'] = int(issues_match.group(1))
# If no match, issues_found stays 0
```

---

## Solution Options

### Option 1: Update Prompts (RECOMMENDED)

Update all 8 prompts in `style_checker/prompts/` to request the exact format the parser expects.

**Pros:**
- Parser is well-tested
- Structured format is easier to work with programmatically
- Consistent with existing architecture

**Cons:**
- Need to update 8 prompt files
- Claude might not always follow the format perfectly

### Option 2: Update Parser

Rewrite `parse_markdown_response()` to handle the free-form format.

**Pros:**
- Works with current prompts
- More flexible

**Cons:**
- Complex regex parsing
- Error-prone
- Harder to test

### Option 3: Hybrid Approach

Add format specification to prompts AND make parser more tolerant.

---

## Recommended Fix

**Update all prompt files to specify the required output format.**

Add this section to each prompt file (after the existing content):

```markdown
## CRITICAL: Required Output Format

You MUST structure your response EXACTLY as follows:

```markdown
# Review Results

## Summary
[Brief 1-2 sentence summary of findings]

## Issues Found
[NUMBER - just the number, e.g., 15]

## Violations

### Violation 1: [rule-id] - [Rule Title]
- **Severity:** [error|warning|info]
- **Location:** Line [X] or Section "[Section Name]"
- **Description:** [Brief explanation]
- **Current text:**
```
[Exact quote of problematic text]
```
- **Suggested fix:**
```
[Corrected version]
```
- **Explanation:** [Why this fix is recommended]

[Repeat for each violation...]

## Corrected Content

```markdown
[Complete corrected lecture content with all fixes applied]
```
```

**IMPORTANT:** 
- The `## Issues Found` section must contain ONLY a number
- Each violation must follow the exact format above
- The corrected content must be in a markdown code block
- Do not deviate from this structure
```

---

## Testing Required

After fix:

1. **Unit Tests**: Update mocks to use actual Claude responses
2. **Integration Tests**: Run with real API on sample lectures
3. **Regression Tests**: Test against known-good lectures
4. **Format Validation**: Ensure parser handles Claude's actual output

---

## Timeline

**Priority:** CRITICAL  
**Urgency:** IMMEDIATE  

This is a showstopper bug that breaks the core value proposition of the action.

---

## Related Files

- `style_checker/prompts/*.md` (8 files) - Need format specification
- `style_checker/reviewer.py` - Parser implementation
- `tests/test_markdown_parser.py` - Parser tests (need real examples)

---

## Additional Notes

The `tool-style-checker` works because it:
1. Uses a different prompt that requests "both analysis and corrected file"
2. Doesn't parse the response - just saves it raw
3. Splits on a simple separator: `"="*80 + "\nCORRECTED LECTURE FILE\n" + "="*80`

This is much simpler and more reliable than the GitHub Action's approach.

**Consider:** Should we simplify the GitHub Action to match tool-style-checker's approach?
