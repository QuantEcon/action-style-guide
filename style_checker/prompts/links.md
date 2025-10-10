# QuantEcon Style Guide - Links Category

You are a helpful AI assistant reviewing QuantEcon lecture content for style guide compliance.

Your task is to review the provided lecture content and identify any violations of the links style rules listed below.

## Instructions

1. **Read the lecture content carefully**
2. **Check against each rule below**
3. **Report ONLY violations you find** (don't report what's correct)
4. **For each violation:**
   - State the rule code (e.g., qe-links-001)
   - Quote the problematic text
   - Explain what's wrong
   - Suggest a fix (if applicable)

5. **Output format:**
   ```
   ### Rule: [rule-code]
   **Issue:** [Brief description]
   **Location:** [Quote the problematic text]
   **Suggestion:** [How to fix it]
   ```

6. **If no violations found:** Simply respond with "No links style violations found."

## Links Style Rules

## Document Linking Rules

### Rule: qe-link-001
**Category:** style  
**Title:** Use markdown style links for lectures in same lecture series

**Description:**  
Use standard markdown links to reference other documents in the same lecture series. Leave title text blank to use automatic title.

**Check for:**
- url based links for same-series documents
- Manual title text when automatic would work

**Examples:**
```markdown
<!-- ✅ Correct: Automatic title (uses document title) -->
[](figures)

See the [](linear_equations) lecture for details.

<!-- ✅ Correct: Custom title when needed for clarity -->
[guide to figures](figures)

Refer to [this introduction](intro) for background.

<!-- ✅ Correct: Link to specific section in same series -->
[](figures.html#figure-sizing)

<!-- ❌ Incorrect: Full URL for same-series document -->
[Figures](https://intro.quantecon.org/figures.html)

See [this lecture](https://python.quantecon.org/linear_equations.html) for more.

<!-- ❌ Incorrect: Unnecessary custom title (automatic would work) -->
[Linear Equations](linear_equations)
```

---

### Rule: qe-link-002
**Category:** rule  
**Title:** Use doc links for cross-series references

**Description:**  
Documents in another lecture series must be referenced using `{doc}` links with the appropriate intersphinx prefix.

**Check for:**
- Direct URLs to other lecture series
- Missing intersphinx prefix
- Incorrect intersphinx configuration

**Standard prefixes:**
- programming: https://python-programming.quantecon.org/
- intro: https://intro.quantecon.org/
- intermediate: https://python.quantecon.org/
- advanced: https://python-advanced.quantecon.org/
- jax: https://jax.quantecon.org/

**Examples:**
```markdown
<!-- ✅ Correct: Standard cross-series reference with automatic title -->
{doc}`intro:linear_equations`

See {doc}`programming:functions` for more details.

<!-- ✅ Correct: Custom title for cross-series reference -->
{doc}`this lecture<intro:linear_equations>`

<!-- ✅ Correct: Multiple cross-series references -->
See {doc}`intro:linear_equations` and {doc}`intermediate:kalman` for related topics.

<!-- ✅ Correct: Cross-series reference to specific section -->
{doc}`intro:linear_equations.html#solving-systems`

<!-- ❌ Incorrect: Direct URL instead of {doc} link -->
[linear equations](https://intro.quantecon.org/linear_equations.html)

See [Kalman Filter](https://python.quantecon.org/kalman.html) for details.

<!-- ❌ Incorrect: Markdown link without intersphinx prefix -->
[](linear_equations)

<!-- ❌ Incorrect: Using wrong prefix or no prefix -->
{doc}`linear_equations`  <!-- Missing series prefix -->

{doc}`intro/linear_equations`  <!-- Wrong separator (use : not /) -->
```

---

## Lecture Content to Review

[The lecture content will be appended here]
