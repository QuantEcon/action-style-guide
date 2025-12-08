# QuantEcon References Style Rules

## Version: 2025-Oct-09 (Focused Extract)

This document contains only the **references-focused rules** for QuantEcon lecture content. Each rule is categorized as either `rule` (clearly actionable) or `style` (advisory guideline requiring judgment).

---

## Reference and Citation Rules

### Rule: qe-ref-001
**Type:** rule  
**Title:** Use correct citation style

**Description:**  
Use `{cite}` for standard citations at end of sentences or in lists. Use `{cite:t}` for in-text citations where author names are part of the sentence flow.

**Check for:**
- Incorrect citation style for context
- Manual citation formatting
- Using `{cite}` when author names are part of sentence structure
- Using `{cite:t}` for parenthetical citations

**Examples:**
```markdown
<!-- ✅ Correct: In-text citation (author name is part of sentence) -->
This result was proven by {cite:t}`StokeyLucas1989`.

<!-- ✅ Correct: Standard citation at end of sentence -->
Dynamic programming provides powerful tools for optimization {cite}`Bellman1957`.

<!-- ✅ Correct: In-text citation (author name is part of sentence) -->
The tradition of {cite:t}`Warner1965` surveys are designed to protect privacy.

As discussed in {cite:t}`Sargent1987`, rational expectations have profound implications.

<!-- ✅ Correct: Multiple citations -->
This approach has been widely used {cite}`StokeyLucas1989,Ljungqvist2012`.

Several authors have explored this topic {cite}`Sargent1987,Ljungqvist2012,StokeyLucas1989`.

<!-- ✅ Correct: Citation at beginning of sentence -->
{cite:t}`Bellman1957` introduced the principle of optimality.

<!-- ✅ Correct: Citation in middle of sentence -->
Following {cite:t}`Sargent1987`, we adopt the rational expectations framework.

The model, as shown in {cite:t}`Ljungqvist2012`, exhibits multiple equilibria.

<!-- ❌ Incorrect: Manual formatting instead of citation -->
Warner (1965) surveys are designed to protect privacy. {cite}`Warner1965`

<!-- ❌ Incorrect: Using {cite} when author is part of sentence -->
The work of {cite}`Sargent1987` shows that rational expectations matter.

<!-- ❌ Incorrect: Using {cite:t} for parenthetical citation -->
This result has been proven {cite:t}`StokeyLucas1989`.

<!-- ❌ Incorrect: Manual year in text with citation -->
Bellman (1957) introduced dynamic programming {cite}`Bellman1957`.
```