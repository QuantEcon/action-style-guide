# QuantEcon Writing Style Rules

## Version: 2025-Oct-09 (Focused Extract)

This document contains only the **writing-focused rules** for QuantEcon lecture content. Each rule is categorized as either `rule` (clearly actionable) or `style` (advisory guideline requiring judgment).

---

## Writing Rules

### Rule: qe-writing-001
**Category:** rule  
**Title:** Use one sentence per paragraph

**Description:**  
Each paragraph block (text separated by blank lines) must contain exactly one sentence. This improves readability and helps readers digest information in clear, focused chunks.

**Important:** A paragraph is defined as text between blank lines in the markdown source. Line breaks within text (without blank lines) do NOT create new paragraphs. A single sentence may span multiple lines.

**Check for:**
- Paragraph blocks containing multiple sentences (identified by multiple periods)
- Multiple complete sentences within the same block of text (between blank lines)

**Associated rules:**  
This rule focuses on sentence structure and paragraph organization. For whitespace formatting issues (multiple spaces between words), see qe-writing-008.

**Examples:**

```markdown
<!-- ❌ VIOLATION: Multiple sentences in one paragraph block -->
This section introduces the concept of dynamic programming. Dynamic programming is a powerful method for solving optimization problems. We will use it throughout the lecture series.

<!-- ❌ VIOLATION: Multiple sentences even with line breaks (no blank lines between) -->
This section introduces the concept of dynamic programming. Dynamic programming 
is a powerful method for solving optimization problems. We will use it throughout 
the lecture series.

<!-- ✅ CORRECT: Each sentence in its own paragraph block (separated by blank lines) -->
This section introduces dynamic programming.

Dynamic programming is a powerful method for solving optimization problems with recursive structure.

We will use it throughout the lecture series.

<!-- ✅ CORRECT: Single sentence spanning multiple lines (no blank lines within) -->
Dynamic programming is a powerful method for solving optimization problems 
with recursive structure.

<!-- ✅ CORRECT: Already following the rule (each block has one sentence) -->
Many economic time series display persistent growth that prevents them from being asymptotically stationary and ergodic.

For example, outputs, prices, and dividends typically display irregular but persistent growth.

Asymptotic stationarity and ergodicity are key assumptions needed to make it possible to learn by applying statistical methods.
```

**Implementation note:**  
Check by counting sentences (periods followed by space/capital or newline) within each paragraph block. Paragraph blocks are defined by blank lines—text separated by blank lines forms distinct paragraphs. Line breaks (without blank lines) within a paragraph do not create new paragraphs. Whitespace formatting between words is handled by qe-writing-008.

**Key distinction:**  
- **Blank line** = Creates new paragraph (required between sentences)
- **Line break** = Does not create new paragraph (allowed within sentences)

---



### Rule: qe-writing-002
**Category:** rule  
**Title:** Keep writing clear, concise, and valuable

**Description:**  
Keep sentences short and clear. Minimize unnecessary words. The value of a lecture equals the importance and clarity of information divided by word count.

**Check for:**
- Overly long sentences that reduce clarity (>30-40 words as a rough guideline)
- Unnecessary verbosity that doesn't add value
- Complex sentence structures where simpler ones would work
- Redundant phrases or explanations

**Guidance:**  
This is a judgment call that requires understanding context and content value. Focus on whether every word serves a purpose.

---



### Rule: qe-writing-003
**Category:** style  
**Title:** Maintain logical flow

**Description:**  
Ensure lectures have good logical flow with no jumps. Choose carefully what you pay attention to and minimize distractions.

**Check for:**
- Abrupt topic changes without transitions
- Introducing concepts before prerequisites are established
- Tangential content that distracts from the main narrative
- Missing connections between sections

**Guidance:**  
Each new paragraph or section should build naturally from the previous one.

---



### Rule: qe-writing-004
**Category:** rule  
**Title:** Avoid unnecessary capitalization in narrative text

**Description:**  
Don't capitalize words in narrative text unless grammatically required (proper nouns, start of sentences). This keeps writing simple and consistent.

**Check for:**
- Mid-sentence capitalization of common nouns
- Capitalized technical terms that aren't proper nouns
- Inconsistent capitalization patterns

**Examples:**
```markdown
<!-- ✅ Correct -->
The bellman equation is a fundamental tool.

We use dynamic programming to solve the model.

<!-- ❌ Incorrect -->
The Bellman Equation is a fundamental tool.

We use Dynamic Programming to solve the Model.
```

**Implementation note:**  
Can detect capitalized words mid-sentence that aren't proper nouns or at the start of sentences.

---



### Rule: qe-writing-005
**Category:** rule  
**Title:** Use bold for definitions, italic for emphasis

**Description:**  
Use **bold** for definitions and *italic* for emphasis only.

**Check for:**
- Definitions not in bold
- Emphasis using bold instead of italic
- Overuse of emphasis formatting

**Examples:**
```markdown
<!-- ✅ Correct -->
A **closed set** is a set whose complement is open.

All consumers have *identical* endowments.

<!-- ❌ Incorrect -->
A *closed set* is a set whose complement is open.

All consumers have **identical** endowments.
```

---



### Rule: qe-writing-006
**Category:** rule  
**Title:** Capitalize lecture titles properly

**Description:**  
Use capitalization of all words only for lecture titles. For all other headings (sections, subsections, etc.), capitalize only the first word and proper nouns.

**Check for:**
- Section headings with all words capitalized
- Lecture titles with only first word capitalized

**Examples:**
```markdown
<!-- ✅ Lecture title -->
# How It Works: Data, Variables and Names

<!-- ✅ Section heading -->
## Binary packages with Python frontends

<!-- ❌ Section heading - wrong capitalization -->
## Binary Packages With Python Frontends
```

---



### Rule: qe-writing-007
**Category:** style  
**Title:** Use visual elements to enhance understanding

**Description:**  
Good lectures use colors, layout, figures, and diagrams to emphasize ideas and make content more engaging. Consider opportunities to visualize concepts.

**Check for:**
- Sections describing visual concepts without accompanying figures
- Opportunities to use admonitions for important notes
- Mathematical relationships that could be illustrated with diagrams

**Guidance:**  
This requires understanding the content and judging where visualization adds value.

**Reference example:**  
https://continuous-time-mcs.quantecon.org/kolmogorov_fwd.html

---


### Rule: qe-writing-008
**Category:** rule  
**Title:** Remove excessive whitespace between words

**Description:**  
MyST Markdown source files should contain only single spaces between words. Multiple consecutive spaces between words should be reduced to a single space for clean, consistent formatting.

**Check for:**
- Two or more consecutive spaces between words in narrative text
- Extra spacing in headings, list items, or inline text
- Inconsistent spacing patterns

**Examples:**
```markdown
<!-- ❌ Incorrect: Multiple spaces between words -->
This is  an  example with    excessive spacing.

The bellman equation  is a fundamental  tool.

## Section  Heading  With  Extra  Spaces

<!-- ✅ Correct: Single space between words -->
This is an example with excessive spacing.

The bellman equation is a fundamental tool.

## Section Heading With Extra Spaces
```

**Important exceptions:**
- Code blocks (indented or fenced) - preserve all spacing
- Inline code spans - preserve all spacing
- Math blocks and inline math - preserve all spacing
- Intentional formatting like tables or aligned content
