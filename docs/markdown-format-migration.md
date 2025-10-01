# Migration from JSON to Markdown Response Format

**Date:** October 1, 2025  
**Issue:** JSON parsing errors with unterminated strings  
**Solution:** Migrate to structured Markdown format

## Problem

The action was experiencing consistent JSON parsing failures across all LLM chunks:

```
⚠️ JSON parsing error: Unterminated string starting at: line 275 column 24 (char 26118)
Response length: 70689 characters
❌ Error in chunk 1: JSON parsing failed: Unterminated string starting at...
```

### Root Cause

**JSON is fragile for LLM-generated content:**
- LLMs must properly escape quotes, newlines, backslashes in JSON strings
- Lecture content contains code blocks, LaTeX math, markdown that needs escaping
- Long responses (50K-70K characters) increase failure probability
- The `corrected_content` field containing full lecture markup is especially problematic
- Even with explicit instructions, LLMs frequently produce malformed JSON

## Solution

**Switch to Markdown-based structured format:**

### Why Markdown?

✅ **Native LLM format** - LLMs generate markdown naturally without escaping issues  
✅ **Structured yet flexible** - Clear section delimiters using headings  
✅ **Better for content** - No need to escape code, quotes, special characters  
✅ **More reliable** - Parsing is more forgiving and robust  
✅ **Human-readable** - Easy to debug when issues occur  
✅ **Handles long content** - No string length or escaping limits  

### New Format Specification

```markdown
# Review Results

## Summary
<Brief summary of all changes made by category>

## Issues Found
<number>

## Violations

### Violation 1: <rule_id> - <rule_title>
- **Severity:** <critical|mandatory|best_practice|preference>
- **Location:** <Line X or section name>
- **Description:** <Clear description of the violation>
- **Current text:**
```
<Exact text that violates the rule>
```
- **Suggested fix:**
```
<Exact corrected text>
```
- **Explanation:** <Why this change is needed per the rule>

[Repeat for each violation...]

## Corrected Content

```markdown
<Complete lecture content with ALL fixes applied>
```
```

## Changes Made

### 1. Created Markdown Parser (`parse_markdown_response()`)
- Location: `style_checker/reviewer.py`
- Extracts structured data from Markdown response using regex
- Handles sections: Summary, Issues Found, Violations, Corrected Content
- Robust error handling with fallbacks

### 2. Updated All LLM Providers
- **OpenAI Provider**: Updated system prompt to request Markdown format
- **Anthropic Provider**: Replaced JSON parsing with Markdown parser, removed JSON error recovery code
- **Gemini Provider**: Updated prompts and removed `response_mime_type: application/json`

### 3. Removed JSON Dependencies
- Removed `import json` from reviewer.py
- Removed all `json.loads()` calls
- Removed JSON-specific error handling
- Removed JSON escaping warnings from prompts

### 4. Added Test Suite
- Created `tests/test_markdown_parser.py` to validate parsing
- Tests all key parsing features with realistic sample responses
- Verified extraction of violations, summary, and corrected content

## Benefits

1. **Eliminates JSON parsing errors** - No more "Unterminated string" failures
2. **More reliable reviews** - LLMs can focus on content, not JSON escaping
3. **Better error handling** - Partial responses can still be parsed
4. **Easier debugging** - Markdown responses are human-readable
5. **Supports longer responses** - No JSON string length concerns

## Testing

Run the test suite to verify the parser:

```bash
python tests/test_markdown_parser.py
```

Expected output:
```
✅ All tests passed!

The Markdown parser successfully:
  - Extracted summary
  - Parsed issues count
  - Extracted all violations with full details
  - Extracted corrected content
```

## Compatibility

- ✅ All existing functionality preserved
- ✅ Same output structure (dict with violations, corrected_content, etc.)
- ✅ Works with all three LLM providers (OpenAI, Anthropic, Gemini)
- ✅ No changes required to calling code in `main.py` or `github_handler.py`

## Next Steps

1. **Test with real lecture content** - Run the action on actual lecture files
2. **Monitor for parsing issues** - Check logs for any Markdown parsing errors
3. **Refine regex patterns** - Adjust if LLMs use slightly different formatting
4. **Consider fallbacks** - Add alternate parsing strategies if needed

## Notes

- The structured Markdown format is documented in system prompts for each provider
- LLMs are instructed to use "EXACT Markdown format" for consistency
- The parser is robust to minor variations in formatting (case-insensitive, flexible whitespace)
- Triple backtick code blocks preserve content exactly without escaping
