# How to Use the QuantEcon Style Checker with Claude

## Quick Start

To check a lecture document against the QuantEcon style guide using Claude Sonnet 4.5, provide three things in your conversation:

1. **The prompt** (`claude-style-checker-prompt.md`)
2. **The style guide** (`style-guide-database.md`)
3. **The lecture to review** (e.g., `quantecon-test-lecture.md`)

## Option 1: Using Claude.ai Web Interface

### Step 1: Start a new conversation
Go to claude.ai and start a new chat.

### Step 2: Upload files
Attach these files to your message:
- `claude-style-checker-prompt.md`
- `style-guide-database.md`
- `your-lecture.md` (the lecture you want to review)

### Step 3: Send your request
```
Please follow the instructions in claude-style-checker-prompt.md to review 
the lecture file against the style guide database. Be thorough but focus 
on the most impactful issues.
```

## Option 2: Using Claude API

If you're using the Claude API programmatically:

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Read the files
with open('claude-style-checker-prompt.md', 'r') as f:
    prompt = f.read()

with open('style-guide-database.md', 'r') as f:
    style_guide = f.read()

with open('your-lecture.md', 'r') as f:
    lecture = f.read()

# Create the message
message = client.messages.create(
    model="claude-sonnet-4-20250514",  # or latest version
    max_tokens=8000,
    messages=[
        {
            "role": "user",
            "content": f"""
{prompt}

## Style Guide Database

{style_guide}

## Lecture to Review

{lecture}
"""
        }
    ]
)

print(message.content[0].text)
```

## Option 3: Copy-Paste Method

If you prefer not to upload files:

1. Copy the entire content of `claude-style-checker-prompt.md`
2. Paste it into Claude
3. Add: "## Style Guide Database" and paste `style-guide-database.md` content
4. Add: "## Lecture to Review" and paste your lecture content
5. Send the message

## Tips for Best Results

### Be Specific About Focus Areas
If you want Claude to focus on certain rule categories:

```
Please review this lecture focusing specifically on:
- Writing rules (qe-writing-*)
- Mathematics rules (qe-math-*)

You can skip JAX and code-related rules for now.
```

### Adjust Thoroughness
For a quick review:
```
Please provide a high-level review focusing only on the most critical 
violations (rule category). Skip minor style suggestions.
```

For comprehensive review:
```
Please provide a thorough review including all rule violations and 
style suggestions, even minor ones.
```

### Request Specific Output
If you want the fixes in a different format:
```
Please provide your review, and then create a corrected version of 
the full document with all violations fixed.
```

Or for a diff-style output:
```
Please provide specific line-by-line changes in a format I can 
easily apply (show before/after for each change).
```

## Example Workflow

1. **Initial comprehensive review**
   - Upload all three files
   - Get full analysis with all violations

2. **Prioritize fixes**
   - Review Claude's recommendations
   - Decide which violations to fix first

3. **Apply fixes manually**
   - Make changes to your lecture file
   - Save the updated version

4. **Second-pass review** (optional)
   - Upload the corrected version
   - Ask Claude: "Please review this updated lecture and confirm the previous violations have been addressed"

## Understanding the Output

Claude will structure the response with:

- **Summary**: Quick overview of issues found
- **Critical Issues**: Rule violations (most important)
- **Style Suggestions**: Advisory improvements
- **Positive Observations**: What the lecture does well
- **Recommendations Summary**: Prioritized action items

### How to Read a Violation Report

```markdown
#### qe-writing-001: Use one sentence per paragraph
**Location**: Lines 42-44, Section "Introduction"
**Current**: [exact text from your lecture]
**Issue**: [what's wrong]
**Suggested fix**: [corrected version]
```

You can directly copy the "Suggested fix" text to replace the "Current" text in your document.

## Common Issues and Solutions

### Claude misses some violations
- The lecture might be very long; try breaking it into sections
- Some rules require deep context; ask Claude to re-check specific sections

### Claude reports false positives
- Review the style guide rule yourself
- Context might justify the exception; use your judgment

### Too many violations to handle
- Ask Claude to prioritize: "Which 5 violations would have the biggest impact?"
- Fix in batches by category (all writing issues first, then math, etc.)

## Customizing the Prompt

You can modify `claude-style-checker-prompt.md` to:

1. **Change output format**: Edit the "Output Format" section
2. **Add domain-specific rules**: If your lecture series has additional conventions
3. **Adjust priorities**: Emphasize certain rule categories over others
4. **Add examples**: Include sample violations specific to your common issues

## Advanced: Batch Processing

To check multiple lectures:

```python
import os
import anthropic

lectures_dir = "path/to/lectures"
output_dir = "path/to/reviews"

for lecture_file in os.listdir(lectures_dir):
    if lecture_file.endswith('.md'):
        # Review each lecture
        # Save results to output_dir
```

(See `test_prompt.py` for a starting point)

## Getting Help

If Claude's analysis seems off:
1. Check that all three files were properly provided
2. Verify the lecture uses MyST Markdown format
3. Try being more specific in your request
4. Ask Claude to explain why it flagged something specific

## Version Tracking

The style guide includes a version number (currently 2025-Oct-02). When the style guide is updated:
1. Make sure to use the latest version
2. Note that older reviews may be based on previous rules
3. Consider re-reviewing important lectures with the updated guide
