# QuantEcon Figures Style Rules

## Version: 2025-Oct-09 (Focused Extract)

This document contains only the **figures-focused rules** for QuantEcon lecture content. Each rule is categorized as either `rule` (clearly actionable) or `style` (advisory guideline requiring judgment).

---

## Figure Rules

### Rule: qe-fig-001
**Type:** style  
**Title:** Do not set figure size unless necessary

**Description:**  
Do not set figure size and style unless there is a good reason. QuantEcon lecture series set defaults in `_config.yml`.

**Check for:**
- Explicit `figsize` settings without justification
- Custom style settings overriding defaults

---

### Rule: qe-fig-002
**Type:** style  
**Title:** Prefer code-generated figures

**Description:**  
Use code-generated figures whenever possible rather than static image files.

**Check for:**
- Static images where code could generate equivalent output
- PNG/PDF files for simple plots

---

### Rule: qe-fig-003
**Type:** rule  
**Title:** No matplotlib embedded titles

**Description:**  
Do not use `ax.set_title()` to embed titles in matplotlib figures. Titles should be added using `mystnb` metadata or `figure` directive instead

**Check for:**
- `ax.set_title()` usage
- `fig.suptitle()` usage
- Any embedded title in matplotlib code

**Exceptions:** 
- `ax.set_title()` may be used to embed titles in matplotlib figures when inside `exercise` or `solution` directives or between (`exercise-start`, `exercise-end`) and (`solution-start`, `solution-end`) directives.

---

### Rule: qe-fig-004
**Type:** rule  
**Title:** Caption formatting conventions

**Description:**  
Figure captions must follow proper formatting:
- Use lowercase except for first letter and proper nouns
- Keep captions concise (5-6 words maximum)

**Check for:**
- Incorrect capitalization in captions (Title Case)
- Long captions (>6 words)
- Verbose or wordy captions

---

### Rule: qe-fig-005
**Type:** rule  
**Title:** Descriptive figure names for cross-referencing

**Description:**  
Every figure must have a descriptive `name` field for cross-referencing with `numref`. Names should follow the pattern `fig-description` using lowercase with hyphens.

**Check for:**
- Missing `name` field in figure metadata
- Generic names (e.g., `fig1`, `figure1`)
- Non-descriptive names
- Names not following `fig-` prefix convention

---

### Rule: qe-fig-006
**Type:** rule  
**Title:** Lowercase axis labels

**Description:**  
Axis labels in matplotlib figures should be lowercase (except for proper nouns).

**Check for:**
- Uppercase axis labels (e.g., `ax.set_xlabel("Time")`)
- Title Case in axis labels
- Inconsistent capitalization

---

### Rule: qe-fig-007
**Type:** rule  
**Title:** Keep figure box and spines

**Description:**  
Keep the default box around matplotlib figures. Do not remove spines unless there is a specific reason to do so.

**Check for:**
- Removed spines using `ax.spines['top'].set_visible(False)`
- Removed spines using `ax.spines['right'].set_visible(False)`
- Any spine removal code

---

### Rule: qe-fig-008
**Type:** rule  
**Title:** Use lw=2 for line charts

**Description:**  
Line charts should use `lw=2` (line width of 2) for better visibility and consistency across lectures.

**Check for:**
- Missing `lw` parameter in `ax.plot()`
- Line width values other than 2
- Thin lines that are hard to see

---

### Rule: qe-fig-009
**Type:** rule  
**Title:** Figure sizing

**Description:**  
Figures should be 80-100% of text width for optimal readability and layout.

**Check for:**
- Figures that are too small (<80% text width)
- Figures that are too large (>100% text width)
- Explicit width settings that don't fall in this range

---

### Rule: qe-fig-010
**Type:** rule  
**Title:** Plotly figures require latex directive

**Description:**  
Plotly figures must include a `{only} latex` directive after the figure with a link back to the website for PDF compatibility.

**Check for:**
- Plotly figures without latex directive
- Incorrect link format

---

### Rule: qe-fig-011
**Type:** rule  
**Title:** Use image directive when nested in other directives

**Description:**  
For PDF compatibility, use the `image` directive (rather than `figure`) when inside other directives such as `exercise` or `solution`.

**Check for:**
- `figure` directive nested inside other directives
- Missing PDF compatibility consideration