
================================================================================
WRITING CATEGORY REVIEW
================================================================================

# Writing Style Review for Test Lecture For Style Guide Violations

## Summary
- Total writing violations: 12 issues found
- Critical issues: 8 issues require attention

## Critical Writing Issues

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 18-19 / Section "Overview"
**Current**: "This lecture contains intentional style guide violations for testing purposes. Each section tests specific rules from the QuantEcon style guide database. This is a test document and should not be used as a reference for proper formatting."
**Issue**: Paragraph contains three sentences instead of one
**Fix**: Split into three separate paragraphs:
```
This lecture contains intentional style guide violations for testing purposes.

Each section tests specific rules from the QuantEcon style guide database.

This is a test document and should not be used as a reference for proper formatting.
```

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 21-22 / Section "Overview"
**Current**: "This lecture demonstrates various common mistakes. We will cover writing violations, mathematical notation errors, code style issues, JAX conversion patterns, figure formatting problems, and reference citation mistakes. All of these are intentionally wrong to test the style checker."
**Issue**: Paragraph contains three sentences instead of one
**Fix**: Split into three separate paragraphs

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 37 / Section "Multiple Sentences Per Paragraph"
**Current**: "This paragraph contains multiple sentences which violates the style guide. The first sentence introduces a concept. The second sentence elaborates on it. The third sentence provides an example."
**Issue**: Paragraph contains four sentences instead of one
**Fix**: Split into four separate paragraphs

### qe-writing-004: Avoid unnecessary capitalization in narrative text
**Location**: Line 41 / Section "Unnecessary Capitalization"
**Current**: "The Bellman Equation is a fundamental tool in Dynamic Programming."
**Issue**: Common nouns capitalized mid-sentence
**Fix**: "The bellman equation is a fundamental tool in dynamic programming."

### qe-writing-004: Avoid unnecessary capitalization in narrative text
**Location**: Line 43 / Section "Unnecessary Capitalization"
**Current**: "We use the Method of Lagrange Multipliers to solve the Optimization Problem."
**Issue**: Common nouns capitalized mid-sentence
**Fix**: "We use the method of lagrange multipliers to solve the optimization problem."

### qe-writing-004: Avoid unnecessary capitalization in narrative text
**Location**: Line 45 / Section "Unnecessary Capitalization"
**Current**: "The Nash Equilibrium is a Solution Concept in Game Theory."
**Issue**: Common nouns capitalized mid-sentence
**Fix**: "The nash equilibrium is a solution concept in game theory."

### qe-writing-005: Use bold for definitions, italic for emphasis
**Location**: Line 49 / Section "Wrong Emphasis Formatting"
**Current**: "A *closed set* is a set whose complement is open."
**Issue**: Definition using italic instead of bold
**Fix**: "A **closed set** is a set whose complement is open."

### qe-writing-005: Use bold for definitions, italic for emphasis
**Location**: Line 51 / Section "Wrong Emphasis Formatting"
**Current**: "All consumers have **identical** endowments in this model."
**Issue**: Emphasis using bold instead of italic
**Fix**: "All consumers have *identical* endowments in this model."

## Writing Style Suggestions

### qe-writing-006: Capitalize lecture titles properly
**Location**: Line 56 / Section heading
**Current**: "## A Section About Binary Packages With Python Frontends"
**Suggestion**: Section headings should only capitalize the first word and proper nouns
**Fix**: "## A section about binary packages with python frontends"

### qe-writing-006: Capitalize lecture titles properly
**Location**: Line 60 / Section heading
**Current**: "### Another Incorrectly Capitalized Section Heading"
**Suggestion**: Section headings should only capitalize the first word and proper nouns
**Fix**: "### Another incorrectly capitalized section heading"

### qe-writing-006: Capitalize lecture titles properly
**Location**: Line 62 / Section heading
**Current**: "This Should Only Have First Word Capitalized."
**Suggestion**: This appears to be explanatory text but follows incorrect capitalization pattern
**Fix**: "This should only have first word capitalized."

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 399 / Section "Exercises"
**Current**: "Calculate The Optimal Value Function. Use Dynamic Programming to solve this Problem."
**Issue**: Exercise contains two sentences in one paragraph
**Fix**: Split into two paragraphs and fix capitalization

## Positive Observations
The lecture structure is well-organized with clear sections for testing different rule categories. The use of code examples and mathematical notation provides good context for testing various style rules.

## Writing Summary
The document contains systematic violations across all major writing style categories, which is appropriate for its purpose as a test document. The main areas requiring attention are paragraph structure (multiple sentences per paragraph), unnecessary capitalization of common nouns, incorrect emphasis formatting, and improper heading capitalization. Once corrected, the document would serve as a good example of proper QuantEcon writing style.


================================================================================
MATH CATEGORY REVIEW
================================================================================

# Mathematical Notation Review for Test Lecture For Style Guide Violations

## Summary
- Total math violations: 23 issues found
- Critical issues: 21 issues require attention

## Critical Math Issues

### qe-math-001: Prefer UTF-8 unicode for simple parameter mentions, be consistent
**Location**: Line 67 / Section "LaTeX commands without delimiters"
**Current**: `The parameter \alpha controls the utility function, and \beta represents the discount factor.`
**Issue**: LaTeX commands used in narrative text without math delimiters
**Fix**: `The parameter α controls the utility function, and β represents the discount factor.`

**Location**: Line 69 / Section "LaTeX commands without delimiters"
**Current**: `We set \gamma = 2 for the risk aversion parameter.`
**Issue**: LaTeX commands used in narrative text without math delimiters
**Fix**: `We set γ = 2 for the risk aversion parameter.`

**Location**: Line 71 / Section "LaTeX commands without delimiters"
**Current**: `The production function uses parameters \theta and \sigma.`
**Issue**: LaTeX commands used in narrative text without math delimiters
**Fix**: `The production function uses parameters θ and σ.`

### qe-math-001: Prefer UTF-8 unicode for simple parameter mentions, be consistent
**Location**: Lines 77-81 / Section "Unicode in math environments"
**Current**: 
```
$$
u(c) = \frac{c^{1-α}}{1-α}
$$

where α > 0 is the risk aversion parameter.
```
**Issue**: Unicode character α used inside math environment
**Fix**: 
```
$$
u(c) = \frac{c^{1-\alpha}}{1-\alpha}
$$

where α > 0 is the risk aversion parameter.
```

### qe-math-002: Use \top for transpose notation
**Location**: Line 85 / Section "Wrong transpose notation"
**Current**: `The transpose of matrix $A$ is denoted $A^T$.`
**Issue**: Using ^T instead of ^\top for transpose
**Fix**: `The transpose of matrix $A$ is denoted $A^\top$.`

**Location**: Line 87 / Section "Wrong transpose notation"
**Current**: `The quadratic form is $x^T A x$ where $x$ is a vector.`
**Issue**: Using ^T instead of ^\top for transpose
**Fix**: `The quadratic form is $x^\top A x$ where $x$ is a vector.`

**Location**: Line 89 / Section "Wrong transpose notation"
**Current**: `We can write this as $y^{\prime} M y$ for the variance.`
**Issue**: Using ^{\prime} instead of ^\top for transpose
**Fix**: `We can write this as $y^\top M y$ for the variance.`

### qe-math-003: Use square brackets for matrix notation
**Location**: Lines 93-98 / Section "Wrong matrix brackets"
**Current**: 
```
$$
P = \begin{pmatrix}
0.9 & 0.1 \\
0.2 & 0.8
\end{pmatrix}
$$
```
**Issue**: Using pmatrix (parentheses) instead of bmatrix (square brackets)
**Fix**: 
```
$$
P = \begin{bmatrix}
0.9 & 0.1 \\
0.2 & 0.8
\end{bmatrix}
$$
```

**Location**: Lines 102-107 / Section "Wrong matrix brackets"
**Current**: 
```
$$
I = \begin{Bmatrix}
1 & 0 \\
0 & 1
\end{Bmatrix}
$$
```
**Issue**: Using Bmatrix (curly brackets) instead of bmatrix (square brackets)
**Fix**: 
```
$$
I = \begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}
$$
```

### qe-math-004: Do not use bold face for matrices or vectors
**Location**: Line 111 / Section "Bold face matrices"
**Current**: `Let $\mathbf{A}$ be the coefficient matrix and $\mathbf{x}$ be the state vector.`
**Issue**: Using \mathbf for matrices and vectors
**Fix**: `Let $A$ be the coefficient matrix and $x$ be the state vector.`

**Location**: Line 113 / Section "Bold face matrices"
**Current**: `The solution is $\mathbf{y} = \mathbf{X} \boldsymbol{\beta}$.`
**Issue**: Using \mathbf and \boldsymbol for matrices and vectors
**Fix**: `The solution is $y = X \beta$.`

**Location**: Line 115 / Section "Bold face matrices"
**Current**: `We need to solve $\mathbf{A} \mathbf{x} = \mathbf{b}$ for $\mathbf{x}$.`
**Issue**: Using \mathbf for matrices and vectors
**Fix**: `We need to solve $A x = b$ for $x$.`

### qe-math-005: Use curly brackets for sequences
**Location**: Line 119 / Section "Wrong sequence notation"
**Current**: `Consider the sequence $[ x_t ]_{t=0}^{\infty}$ of state variables.`
**Issue**: Using square brackets instead of curly brackets for sequences
**Fix**: `Consider the sequence $\{ x_t \}_{t=0}^{\infty}$ of state variables.`

**Location**: Line 121 / Section "Wrong sequence notation"
**Current**: `The consumption sequence is denoted $[ c_t ]_{t=0}^{T}$.`
**Issue**: Using square brackets instead of curly brackets for sequences
**Fix**: `The consumption sequence is denoted $\{ c_t \}_{t=0}^{T}$.`

### qe-math-006: Use aligned environment correctly for PDF compatibility
**Location**: Lines 125-130 / Section "Nested math environments"
**Current**: 
```
$$
\begin{align}
x + y &= 5 \\
2x - y &= 1
\end{align}
$$
```
**Issue**: Using align environment inside $$ creates nested math environments
**Fix**: 
```
$$
\begin{aligned}
x + y &= 5 \\
2x - y &= 1
\end{aligned}
$$
```

**Location**: Lines 134-139 / Section "Nested math environments"
**Current**: 
```
$$
\begin{align}
\alpha + \beta &= 1 \\
\gamma &= 2
\end{align}
$$
```
**Issue**: Using align environment inside $$ creates nested math environments
**Fix**: 
```
$$
\begin{aligned}
\alpha + \beta &= 1 \\
\gamma &= 2
\end{aligned}
$$
```

### qe-math-007: Use automatic equation numbering, not manual tags
**Location**: Lines 145-147 / Section "Manual equation tags"
**Current**: 
```
$$
V(x) = \max_{y} \{ u(x, y) + \beta V(y) \} \tag{1}
$$
```
**Issue**: Using manual \tag for equation numbering
**Fix**: 
```
$$
V(x) = \max_{y} \{ u(x, y) + \beta V(y) \}
$$ (bellman)
```

**Location**: Lines 151-153 / Section "Manual equation tags"
**Current**: 
```
$$
u'(c_t) = \beta u'(c_{t+1}) (1 + r) \tag{2}
$$
```
**Issue**: Using manual \tag for equation numbering
**Fix**: 
```
$$
u'(c_t) = \beta u'(c_{t+1}) (1 + r)
$$ (euler)
```

### qe-math-001: Prefer UTF-8 unicode for simple parameter mentions, be consistent
**Location**: Line 350 / Section "Additional mixed violations"
**Current**: `The production function uses parameters \alpha and \beta.`
**Issue**: LaTeX commands used in narrative text without math delimiters
**Fix**: `The production function uses parameters α and β.`

**Location**: Line 354 / Section "Additional mixed violations"
**Current**: `The parameter values are typically set with alpha = 0.3 representing capital share.`
**Issue**: Should use consistent unicode notation
**Fix**: `The parameter values are typically set with α = 0.3 representing capital share.`

### qe-math-002: Use \top for transpose notation
**Location**: Lines 356-358 / Section "Additional mixed violations"
**Current**: 
```
$$
Y = K^\alpha L^{\beta} \tag{3}
$$
```
**Issue**: Manual \tag usage (also violates qe-math-007)
**Fix**: 
```
$$
Y = K^\alpha L^{\beta}
$$ (production)
```

### qe-math-004: Do not use bold face for matrices or vectors
**Location**: Line 360 / Section "Additional mixed violations"
**Current**: `Where $\mathbf{K}$ is the capital stock and $\mathbf{L}$ is labor.`
**Issue**: Using \mathbf for variables
**Fix**: `Where $K$ is the capital stock and $L$ is labor.`

### qe-math-007: Use automatic equation numbering, not manual tags
**Location**: Lines 395-397 / Exercise solution
**Current**: 
```
$$
V(k) = \max_{c} \{ u(c) + \beta V(k') \} \tag{4}
$$
```
**Issue**: Using manual \tag for equation numbering
**Fix**: 
```
$$
V(k) = \max_{c} \{ u(c) + \beta V(k') \}
$$ (value-function)
```

### qe-math-004: Do not use bold face for matrices or vectors
**Location**: Line 399 / Exercise solution
**Current**: `Where $\mathbf{k}$ is capital and $\mathbf{c}$ is consumption.`
**Issue**: Using \mathbf for variables
**Fix**: `Where $k$ is capital and $c$ is consumption.`

## Math Style Suggestions

### qe-math-009: Choose simplicity in mathematical notation
The mathematical notation throughout the document is generally appropriate in complexity level. The use of standard variable names like $K$, $L$, $c$, $k$ for economic variables is good practice and maintains simplicity.

## Positive Observations
The document demonstrates good understanding of mathematical typesetting concepts, even though it contains intentional violations. The mathematical expressions are generally well-structured and readable once the notation issues are corrected.

## Mathematical Notation Summary
The document contains systematic violations across all major mathematical notation rules, which is expected given its purpose as a test document. The main areas requiring correction are: consistent parameter notation (unicode vs LaTeX), proper transpose notation, correct matrix brackets, removal of bold formatting, proper sequence notation, aligned environments instead of nested align, and automatic equation numbering. Once corrected, the mathematical content will be properly formatted according to QuantEcon standards.


================================================================================
FIGURES CATEGORY REVIEW
================================================================================

# Figure Style Review for Test Lecture

## Summary
- Total figure violations: 23 issues found
- Critical issues: 23 issues require attention

## Critical Figure Issues

### qe-fig-003: No matplotlib embedded titles
**Location**: Line 175-182 / First figure with embedded title
**Current**: 
```python
fig, ax = plt.subplots()
ax.set_title("GDP Per Capita Vs Life Expectancy")
ax.plot([1, 2, 3], [1, 4, 9], lw=2)
```
**Issue**: Using `ax.set_title()` to embed titles in matplotlib figures
**Fix**: Remove `ax.set_title()` and add title using mystnb metadata:
```python
---
mystnb:
  figure:
    caption: "GDP per capita vs life expectancy"
    name: fig-gdp-life-expectancy
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9], lw=2)
```

### qe-fig-003: No matplotlib embedded titles
**Location**: Line 185-190 / Second figure with suptitle
**Current**: 
```python
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle("Comparison of Models")
```
**Issue**: Using `fig.suptitle()` to embed titles in matplotlib figures
**Fix**: Remove `fig.suptitle()` and add title using mystnb metadata:
```python
---
mystnb:
  figure:
    caption: "comparison of models"
    name: fig-model-comparison
---
fig, (ax1, ax2) = plt.subplots(1, 2)
```

### qe-fig-004: Caption formatting conventions
**Location**: Line 196-205 / Long verbose caption
**Current**: `caption: "A Very Long And Verbose Caption That Describes The Entire Figure In Great Detail"`
**Issue**: Caption is too long (>6 words) and uses Title Case
**Fix**: `caption: "figure description"`

### qe-fig-004: Caption formatting conventions
**Location**: Line 213-222 / Title case caption
**Current**: `caption: "Title Case Caption For GDP"`
**Issue**: Caption uses Title Case instead of lowercase
**Fix**: `caption: "GDP trends"`

### qe-fig-005: Descriptive figure names for cross-referencing
**Location**: Line 227-235 / Missing figure name
**Current**: Figure has caption but no `name` field
**Issue**: Missing `name` field for cross-referencing
**Fix**: Add `name: fig-convergence-path`

### qe-fig-005: Descriptive figure names for cross-referencing
**Location**: Line 238-247 / Generic figure name
**Current**: `name: fig1`
**Issue**: Generic, non-descriptive name
**Fix**: `name: fig-simulation-results`

### qe-fig-006: Lowercase axis labels
**Location**: Line 252-257 / Uppercase axis labels
**Current**: 
```python
ax.set_xlabel("Time Period")
ax.set_ylabel("GDP Per Capita")
```
**Issue**: Axis labels use Title Case
**Fix**: 
```python
ax.set_xlabel("time period")
ax.set_ylabel("GDP per capita")
```

### qe-fig-006: Lowercase axis labels
**Location**: Line 261-266 / More uppercase labels
**Current**: 
```python
ax.set_xlabel("Year")
ax.set_ylabel("Value")
```
**Issue**: Axis labels use Title Case
**Fix**: 
```python
ax.set_xlabel("year")
ax.set_ylabel("value")
```

### qe-fig-007: Keep figure box and spines
**Location**: Line 271-277 / Removed spines
**Current**: 
```python
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```
**Issue**: Removing spines without justification
**Fix**: Remove these lines to keep default spines

### qe-fig-007: Keep figure box and spines
**Location**: Line 281-287 / All spines removed
**Current**: 
```python
for spine in ax.spines.values():
    spine.set_visible(False)
```
**Issue**: Removing all spines
**Fix**: Remove this loop to keep default spines

### qe-fig-008: Use lw=2 for line charts
**Location**: Line 292-297 / Missing line width
**Current**: `ax.plot([1, 2, 3, 4], [1, 4, 9, 16])`
**Issue**: Missing `lw` parameter
**Fix**: `ax.plot([1, 2, 3, 4], [1, 4, 9, 16], lw=2)`

### qe-fig-008: Use lw=2 for line charts
**Location**: Line 301-306 / Wrong line width
**Current**: `ax.plot([1, 2, 3, 4], [1, 4, 9, 16], lw=1)`
**Issue**: Line width is 1 instead of 2
**Fix**: `ax.plot([1, 2, 3, 4], [1, 4, 9, 16], lw=2)`

### qe-fig-008: Use lw=2 for line charts
**Location**: Line 355-363 / Multiple missing line widths in final figure
**Current**: `ax.plot([0, 1, 2, 3, 4], [4, 3, 2, 1, 0])`
**Issue**: Missing `lw` parameter
**Fix**: `ax.plot([0, 1, 2, 3, 4], [4, 3, 2, 1, 0], lw=2)`

This pattern of missing `lw=2` occurs throughout the document in multiple figures.

## Figure Style Suggestions

### qe-fig-001: Do not set figure size unless necessary
**Location**: Line 355 / Final figure with explicit figsize
**Current**: `fig, ax = plt.subplots(figsize=(10, 6))`
**Suggestion**: Remove explicit figsize unless there's a specific layout requirement: `fig, ax = plt.subplots()`

## Positive Observations
Several figures correctly use `lw=2` parameter and proper lowercase axis labels in some instances.

## Figure Presentation Summary
The document contains systematic violations across all major figure formatting rules. The most critical issues are embedded titles (violating qe-fig-003), inconsistent line widths, and improper caption formatting. All figures need proper mystnb metadata with descriptive names for cross-referencing. The document would benefit from consistent application of figure formatting standards throughout.


================================================================================
REFERENCES CATEGORY REVIEW
================================================================================

# Reference Style Review for Test Lecture

## Summary
- Total reference violations: 4 issues found
- Critical issues: 4 issues require attention

## Critical Reference Issues

### qe-ref-001: Use correct citation style
**Location**: Line 346 (Citation violations section)
**Current**: `This result was proven by {cite}`StokeyLucas1989`.`
**Issue**: Using `{cite}` when author name is part of sentence structure - should use `{cite:t}` for in-text citations
**Fix**: `This result was proven by {cite:t}`StokeyLucas1989`.`

### qe-ref-001: Use correct citation style
**Location**: Line 348 (Citation violations section)
**Current**: `The work of {cite}`Sargent1987` shows that rational expectations matter.`
**Issue**: Using `{cite}` when author name is part of sentence structure - should use `{cite:t}` for in-text citations
**Fix**: `The work of {cite:t}`Sargent1987` shows that rational expectations matter.`

### qe-ref-001: Use correct citation style
**Location**: Line 350 (Citation violations section)
**Current**: `Dynamic programming was introduced by Bellman (1957) {cite}`Bellman1957`.`
**Issue**: Manual year formatting in text combined with citation - should use only `{cite:t}` for in-text citations
**Fix**: `Dynamic programming was introduced by {cite:t}`Bellman1957`.`

### qe-ref-001: Use correct citation style
**Location**: Line 352 (Citation violations section)
**Current**: `As shown in the literature {cite:t}`Ljungqvist2012`, this approach is standard.`
**Issue**: Using `{cite:t}` for parenthetical citation at end of clause - should use `{cite}` for standard citations
**Fix**: `As shown in the literature {cite}`Ljungqvist2012`, this approach is standard.`

## Reference Style Suggestions

### qe-ref-001: Use correct citation style
**Location**: Line 358 (Additional mixed violations section)
**Current**: `This is based on work by {cite}`Solow1956`.`
**Suggestion**: Consider using `{cite:t}` if the author name should be part of the sentence flow, or restructure to use standard citation format. Current usage is acceptable but could be improved for clarity.

## Positive Observations
The lecture demonstrates awareness of MyST citation syntax and uses proper citation keys that follow academic conventions.

## Bibliography Summary
The lecture uses proper MyST citation syntax but contains several context-inappropriate citation styles. The main issue is confusion between when to use `{cite}` (for parenthetical citations) versus `{cite:t}` (for in-text citations where author names are part of sentence structure). All citations need bibliography entries to be complete, but the focus here is on citation syntax within the text.


================================================================================
LINKS CATEGORY REVIEW
================================================================================

# Link Style Review for test_lecture.md

## Summary
- Total link violations: 0 issues found
- Critical issues: 0 issues require attention

## Critical Link Issues

None found.

## Link Style Suggestions

None found.

## Positive Observations

This document contains no hyperlinks, cross-references to other lectures, or external web links, so there are no link-related style violations to report. All content is self-contained within this single test document.

## Link Usage Summary

The document does not utilize any linking patterns covered by the QuantEcon link style rules (qe-link-001 and qe-link-002). There are no:
- Markdown links to other lectures in the same series
- Cross-series references using {doc} links
- External URLs or web references
- Intersphinx references

This is appropriate for a self-contained test document, though in a real lecture series, you would typically expect to see some cross-references to related lectures or external resources.


================================================================================
ADMONITIONS CATEGORY REVIEW
================================================================================

# Admonition Style Review for test_lecture.md

## Summary
- Total admonition violations: 4 issues found
- Critical issues: 3 issues require attention

## Critical Admonition Issues

### qe-admon-001: Use gated syntax for executable code in exercises
**Location**: Line 456-477
**Current**: 
```markdown
```{solution} test-ex-1
:class: dropdown

The bellman equation gives us:

$$
V(k) = \max_{c} \{ u(c) + \beta V(k') \}
$$ (value-function)

Where $k$ is capital and $c$ is consumption.

```{code-cell} ipython
def solve_bellman(k, beta=0.95, alpha=0.3):
    """Solve the Bellman equation."""
    import time
    start = time.time()
    # Solution code here
    result = k**alpha * beta
    end = time.time()
    print(f"Time: {end-start}")
    return result
```
```
```
**Issue**: Solution contains executable code cell but uses regular solution syntax instead of gated syntax
**Fix**: 
````markdown
```{solution-start} test-ex-1
:class: dropdown
:label: test-ex-1-solution
```

The bellman equation gives us:

$$
V(k) = \max_{c} \{ u(c) + \beta V(k') \}
$$ (value-function)

Where $k$ is capital and $c$ is consumption.

```{code-cell} ipython
def solve_bellman(k, beta=0.95, alpha=0.3):
    """Solve the Bellman equation."""
    import time
    start = time.time()
    # Solution code here
    result = k**alpha * beta
    end = time.time()
    print(f"Time: {end-start}")
    return result
```

```{solution-end}
```
````

### qe-admon-005: Link solutions to exercises
**Location**: Line 456
**Current**: 
```markdown
```{solution} test-ex-1
:class: dropdown
```
**Issue**: Solution directive correctly references the exercise label, but when converted to gated syntax, needs proper label
**Fix**: Already addressed in the gated syntax fix above with `:label: test-ex-1-solution`

## Admonition Style Suggestions

### qe-admon-002: Use dropdown class for solutions
**Location**: Line 456
**Current**: Solution already uses `:class: dropdown`
**Suggestion**: This is correctly implemented - good practice for giving readers time to think before revealing the solution.

## Positive Observations
The exercise and solution structure follows good pedagogical practices with proper labeling and the solution appropriately uses the dropdown class to encourage student engagement before revealing answers.

## Admonition Usage Summary
The document has minimal admonition usage with only one exercise-solution pair. The main issue is the use of regular solution syntax when executable code is present, which should use gated syntax for proper MyST parsing. The exercise labeling and solution referencing are handled correctly, and the dropdown class usage follows best practices.


================================================================================
CODE CATEGORY REVIEW
================================================================================

# Style Guide Review

## Summary
- Total code violations: 15 issues found
- Critical issues: 8 issues require attention

## Critical Code Issues

### qe-code-002: Use Unicode symbols for Greek letters in code
**Location**: Code Block 2
**Current**: ```python
def utility_function(c, alpha=0.5, beta=0.95, gamma=2.0):
    """Utility function with discount factor."""
    return (c**(1-alpha) - 1) / (1-alpha) * beta

# Production function
def production(k, theta=0.3, sigma=1.0):
    return k**theta * sigma
```
**Issue**: Using spelled-out Greek letters instead of Unicode symbols
**Fix**: ```python
def utility_function(c, α=0.5, β=0.95, γ=2.0):
    """Utility function with discount factor."""
    return (c**(1-α) - 1) / (1-α) * β

# Production function
def production(k, θ=0.3, σ=1.0):
    return k**θ * σ
```

### qe-code-003: Package installation at lecture top
**Location**: Code Block 4 and 5
**Current**: ```python
# Using quantecon without installing it first
mc = qe.MarkovChain([[0.9, 0.1], [0.2, 0.8]])

# Later in the lecture:
!pip install quantecon
```
**Issue**: Package installation missing at top and appearing in middle of lecture
**Fix**: Add at the beginning of the lecture after imports:
```python
# At the top of the lecture
!pip install quantecon
```

### qe-code-002: Use Unicode symbols for Greek letters in code
**Location**: Code Block 12 (production_calc function)
**Current**: ```python
def production_calc(K, L, alpha=0.3, beta=0.7):
    """Calculate output using Cobb-Douglas Production Function."""
    start_time = time.time()
    Y = K**alpha * L**beta
    end_time = time.time()
    print(f"Calculation Time: {end_time - start_time}")
    return Y
```
**Issue**: Using spelled-out Greek letters instead of Unicode symbols
**Fix**: ```python
def production_calc(K, L, α=0.3, β=0.7):
    """Calculate output using Cobb-Douglas Production Function."""
    start_time = time.time()
    Y = K**α * L**β
    end_time = time.time()
    print(f"Calculation Time: {end_time - start_time}")
    return Y
```

### qe-code-002: Use Unicode symbols for Greek letters in code
**Location**: Code Block 14 (solve_bellman function)
**Current**: ```python
def solve_bellman(k, beta=0.95, alpha=0.3):
    """Solve the Bellman equation."""
    import time
    start = time.time()
    # Solution code here
    result = k**alpha * beta
    end = time.time()
    print(f"Time: {end-start}")
    return result
```
**Issue**: Using spelled-out Greek letters instead of Unicode symbols
**Fix**: ```python
def solve_bellman(k, β=0.95, α=0.3):
    """Solve the Bellman equation."""
    import time
    start = time.time()
    # Solution code here
    result = k**α * β
    end = time.time()
    print(f"Time: {end-start}")
    return result
```

## Code Style Suggestions

### qe-code-004: Use quantecon Timer context manager
**Location**: Code Block 6
**Current**: ```python
import time

start_time = time.time()
result = sum([i**2 for i in range(1000000)])
end_time = time.time()
print(f"Elapsed: {end_time - start_time:.4f} seconds")
```
**Suggestion**: Replace manual timing with qe.Timer() context manager for cleaner, more consistent timing code.

### qe-code-004: Use quantecon Timer context manager
**Location**: Code Block 7
**Current**: ```python
def tic():
    global start_time
    start_time = time.time()

def toc():
    end_time = time.time()
    print(f"Elapsed: {end_time - start_time:.4f} seconds")

tic()
result = sum([i**2 for i in range(1000000)])
toc()
```
**Suggestion**: Replace legacy tic/toc pattern with modern qe.Timer() context manager.

### qe-code-005: Use quantecon timeit for benchmarking
**Location**: Code Block 8
**Current**: ```python
%timeit sum([i**2 for i in range(1000000)])
```
**Suggestion**: Replace Jupyter magic commands with qe.timeit() for consistent benchmarking across different environments.

### qe-code-005: Use quantecon timeit for benchmarking
**Location**: Code Block 9
**Current**: ```python
%%timeit
result = []
for i in range(1000):
    result.append(i**2)
```
**Suggestion**: Replace Jupyter cell magic with qe.timeit() using lambda function for multi-line benchmarking.

## Migration Opportunities

### qe-code-004: Use quantecon Timer context manager
**Location**: Multiple timing patterns throughout
**Current**: Manual time.time() patterns and tic/toc functions
**Modern Alternative**: 
```python
import quantecon as qe

with qe.Timer():
    result = sum([i**2 for i in range(1000000)])
```

### qe-code-005: Use quantecon timeit for benchmarking
**Location**: Code blocks with %timeit magic
**Current**: Jupyter magic commands for timing
**Modern Alternative**: 
```python
import quantecon as qe

# For simple function calls
result = qe.timeit(lambda: sum([i**2 for i in range(1000000)]), number=100)

# For more complex benchmarking
def benchmark_function():
    result = []
    for i in range(1000):
        result.append(i**2)
    return result

result = qe.timeit(benchmark_function, number=100)
```

## Positive Observations
The lecture properly imports quantecon as qe and uses consistent import patterns. The code structure is generally well-organized with clear function definitions.

## Code Style Summary
The main areas for improvement are:
1. **Greek letter consistency**: Replace all spelled-out Greek letters (alpha, beta, gamma, theta, sigma) with Unicode symbols (α, β, γ, θ, σ)
2. **Modern timing patterns**: Migrate from manual timing and Jupyter magic to quantecon Timer and timeit functions
3. **Package installation structure**: Ensure all required packages are installed at the top of the lecture

These changes will improve code readability, maintain consistency with mathematical notation, and follow modern QuantEcon best practices.