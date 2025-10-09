# QuantEcon Writing Style Rules

## Version: 2025-Oct-09 (Focused Extract)

This document contains only the **writing-focused rules** for QuantEcon lecture content. Each rule is categorized as either `rule` (clearly actionable) or `style` (advisory guideline requiring judgment).

---

## Writing Rules

### Rule: qe-writing-001
**Category:** rule  
**Title:** Use one sentence per paragraph

**Description:**  
Each paragraph should contain only one sentence. This improves readability and helps readers digest information in clear, focused chunks.

**Check for:**
- Paragraphs containing multiple sentences separated by periods
- Run-on text blocks without paragraph breaks

**Examples:**
```markdown
<!-- ❌ Avoid: Multiple sentences in one paragraph -->
This section introduces the concept of dynamic programming. Dynamic programming is a powerful method for solving optimization problems. We will use it throughout the lecture series.

<!-- ✅ Prefer: One sentence per paragraph -->
This section introduces dynamic programming.

Dynamic programming is a powerful method for solving optimization problems with recursive structure.

We will use it throughout the lecture series.
```

**Implementation note:**  
Can be checked by counting sentences (periods followed by space/newline) within paragraph blocks (text between blank lines).

---

### Rule: qe-writing-002
**Category:** style  
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