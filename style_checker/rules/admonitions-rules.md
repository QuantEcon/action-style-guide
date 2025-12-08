# QuantEcon Admonitions Style Rules

## Version: 2025-Oct-09 (Focused Extract)

This document contains only the **admonitions-focused rules** for QuantEcon lecture content. Each rule is categorized as either `rule` (clearly actionable) or `style` (advisory guideline requiring judgment).

---

## Admonition and Directive Rules

### Rule: qe-admon-001
**Type:** rule  
**Title:** Use gated syntax for executable code in exercises

**Description:**  
Use gated syntax (`exercise-start`/`exercise-end`) whenever exercises contain executable code cells or nested directives.

**Check for:**
- Code cells inside regular exercise blocks
- Nested directives without gated syntax

---

### Rule: qe-admon-002
**Type:** style  
**Title:** Use dropdown class for solutions

**Description:**  
Use `:class: dropdown` for solutions by default to give readers time to think.

**Check for:**
- Solutions without dropdown class
- Solutions that shouldn't be hidden (consider context)

**Examples:**
````markdown
```{solution-start} my-exercise
:class: dropdown
:label: my-solution
```

Solution content here.

```{solution-end}
```
````

---

### Rule: qe-admon-003
**Type:** rule  
**Title:** Use tick count management for nested directives

**Description:**  
When nesting directives, ensure the outer directive uses more ticks than nested directives. Standard pattern: nested uses 3 ticks, outer uses 4 ticks.

**Check for:**
- Equal tick counts for nested directives
- Missing ticks causing parse errors

---

### Rule: qe-admon-004
**Type:** rule  
**Title:** Use prf prefix for proof directives

**Description:**  
All sphinx-proof directives require `prf:` prefix in both the directive and when referencing (e.g., `{prf:theorem}`, `{prf:ref}`).

**Check for:**
- Missing `prf:` prefix in proof-related directives
- Incorrect reference syntax

**Available directives:**
- prf:proof, prf:theorem, prf:axiom, prf:lemma, prf:definition
- prf:criteria, prf:remark, prf:conjecture, prf:corollary
- prf:algorithm, prf:example, prf:property, prf:observation
- prf:proposition, prf:assumption

---

### Rule: qe-admon-005
**Type:** rule  
**Title:** Link solutions to exercises

**Description:**  
Solution directives must include the label of the corresponding exercise.

**Check for:**
- Solutions without exercise references
- Mismatched exercise-solution pairs