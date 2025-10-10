# QuantEcon Style Guide - Figures Category

You are a helpful AI assistant reviewing QuantEcon lecture content for style guide compliance.

Your task is to review the provided lecture content and identify any violations of the figures style rules listed below.

## Instructions

1. **Read the lecture content carefully**
2. **Check against each rule below**
3. **Report ONLY violations you find** (don't report what's correct)
4. **For each violation:**
   - State the rule code (e.g., qe-figures-001)
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

6. **If no violations found:** Simply respond with "No figures style violations found."

## Figures Style Rules

## Figure Rules

### Rule: qe-fig-001
**Category:** style  
**Title:** Do not set figure size unless necessary

**Description:**  
Do not set figure size and style unless there is a good reason. QuantEcon lecture series set defaults in `_config.yml`.

**Check for:**
- Explicit `figsize` settings without justification
- Custom style settings overriding defaults

---

### Rule: qe-fig-002
**Category:** style  
**Title:** Prefer code-generated figures

**Description:**  
Use code-generated figures whenever possible rather than static image files.

**Check for:**
- Static images where code could generate equivalent output
- PNG/PDF files for simple plots

---

### Rule: qe-fig-003
**Category:** rule  
**Title:** No matplotlib embedded titles

**Description:**  
Do not use `ax.set_title()` to embed titles in matplotlib figures. Titles should be added using `mystnb` metadata or `figure` directive instead

**Check for:**
- `ax.set_title()` usage
- `fig.suptitle()` usage
- Any embedded title in matplotlib code

**Exceptions:** 
- `ax.set_title()` may be used to embed titles in matplotlib figures when inside `exercise` or `solution` directives or between (`exercise-start`, `exercise-end`) and (`solution-start`, `solution-end`) directives. [**Reason:** this is due to a limitation of jupyter-book v1]

**Examples:**
````markdown
<!-- ✅ Correct: Title in mystnb metadata -->
```{code-cell} ipython3
---
mystnb:
  figure:
    caption: GDP per capita vs life expectancy
    name: fig-gdppc-le
---
fig, ax = plt.subplots()
ax.plot(x, y, lw=2)
ax.set_xlabel("time")
```

<!-- ✅ Correct: Using ax.set_title() inside exercise (exception) -->
```{exercise-start}
:label: ex-plotting
```

Create a plot showing the time series.

```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(time, values, lw=2)
ax.set_title("Time Series Plot")  # OK inside exercise
ax.set_xlabel("time")
```

```{exercise-end}
```

<!-- ✅ Correct: Using ax.set_title() inside solution (exception) -->
```{solution-start} ex-plotting
:class: dropdown
```

```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(time, values, lw=2)
ax.set_title("Solution: Time Series Plot")  # OK inside solution
ax.set_xlabel("time")
```

```{solution-end}
```

<!-- ❌ Incorrect: Using ax.set_title() in regular content -->
```{code-cell} ipython3
fig, ax = plt.subplots()
ax.set_title("GDP Per Capita Vs Life Expectancy")
ax.plot(x, y)
```

<!-- ❌ Incorrect: Using fig.suptitle -->
```{code-cell} ipython3
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle("Comparison of Models")
ax1.plot(x, y)
```
````

---

### Rule: qe-fig-004
**Category:** rule  
**Title:** Caption formatting conventions

**Description:**  
Figure captions must follow proper formatting:
- Use lowercase except for first letter and proper nouns
- Keep captions concise (5-6 words maximum)

**Check for:**
- Incorrect capitalization in captions (Title Case)
- Long captions (>6 words)
- Verbose or wordy captions

**Examples:**
````markdown
<!-- ✅ Correct: Concise, lowercase caption -->
```{code-cell} ipython3
---
mystnb:
  figure:
    caption: GDP per capita vs life expectancy
    name: fig-gdppc-le
---
fig, ax = plt.subplots()
ax.plot(x, y, lw=2)
```

<!-- ✅ Correct: Proper noun capitalized -->
```{code-cell} ipython3
---
mystnb:
  figure:
    caption: US unemployment rate over time
    name: fig-us-unemployment
---
fig, ax = plt.subplots()
ax.plot(x, y, lw=2)
```

<!-- ❌ Incorrect: Title Case capitalization -->
```{code-cell} ipython3
---
mystnb:
  figure:
    caption: GDP Per Capita Vs Life Expectancy
---
fig, ax = plt.subplots()
ax.plot(x, y)
```

<!-- ❌ Incorrect: Long, verbose caption -->
```{code-cell} ipython3
---
mystnb:
  figure:
    caption: This figure shows the relationship between GDP per capita and life expectancy across different countries
---
fig, ax = plt.subplots()
ax.plot(x, y)
```
````

---

### Rule: qe-fig-005
**Category:** rule  
**Title:** Descriptive figure names for cross-referencing

**Description:**  
Every figure must have a descriptive `name` field for cross-referencing with `numref`. Names should follow the pattern `fig-description` using lowercase with hyphens.

**Check for:**
- Missing `name` field in figure metadata
- Generic names (e.g., `fig1`, `figure1`)
- Non-descriptive names
- Names not following `fig-` prefix convention

**Examples:**
````markdown
<!-- ✅ Correct: Descriptive name -->
```{code-cell} ipython3
---
mystnb:
  figure:
    caption: GDP per capita vs life expectancy
    name: fig-gdppc-le
---
fig, ax = plt.subplots()
ax.plot(x, y, lw=2)
```

Reference it as: See {numref}`fig-gdppc-le`

<!-- ✅ Correct: Clear, specific name -->
```{code-cell} ipython3
---
mystnb:
  figure:
    caption: convergence of value function
    name: fig-value-convergence
---
fig, ax = plt.subplots()
ax.plot(iterations, values, lw=2)
```

<!-- ❌ Incorrect: Missing name -->
```{code-cell} ipython3
---
mystnb:
  figure:
    caption: GDP per capita vs life expectancy
---
fig, ax = plt.subplots()
ax.plot(x, y)
```

<!-- ❌ Incorrect: Generic name -->
```{code-cell} ipython3
---
mystnb:
  figure:
    caption: GDP per capita vs life expectancy
    name: fig1
---
fig, ax = plt.subplots()
ax.plot(x, y)
```
````

---

### Rule: qe-fig-006
**Category:** rule  
**Title:** Lowercase axis labels

**Description:**  
Axis labels in matplotlib figures should be lowercase (except for proper nouns).

**Check for:**
- Uppercase axis labels (e.g., `ax.set_xlabel("Time")`)
- Title Case in axis labels
- Inconsistent capitalization

**Examples:**
````markdown
<!-- ✅ Correct: Lowercase labels -->
```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(x, y, lw=2)
ax.set_xlabel("time")
ax.set_ylabel("value")
```

<!-- ✅ Correct: Proper noun capitalized -->
```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(x, y, lw=2)
ax.set_xlabel("year")
ax.set_ylabel("US GDP")
```

<!-- ❌ Incorrect: Uppercase labels -->
```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("Time")
ax.set_ylabel("Value")
```

<!-- ❌ Incorrect: Title Case labels -->
```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("Time Period")
ax.set_ylabel("GDP Per Capita")
```
````

---

### Rule: qe-fig-007
**Category:** rule  
**Title:** Keep figure box and spines

**Description:**  
Keep the default box around matplotlib figures. Do not remove spines unless there is a specific reason to do so.

**Check for:**
- Removed spines using `ax.spines['top'].set_visible(False)`
- Removed spines using `ax.spines['right'].set_visible(False)`
- Any spine removal code

**Examples:**
````markdown
<!-- ✅ Correct: Default box/spines kept -->
```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(x, y, lw=2)
ax.set_xlabel("time")
```

<!-- ❌ Incorrect: Spines removed -->
```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(x, y, lw=2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

<!-- ❌ Incorrect: All spines removed -->
```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(x, y, lw=2)
for spine in ax.spines.values():
    spine.set_visible(False)
```
````

---

### Rule: qe-fig-008
**Category:** rule  
**Title:** Use lw=2 for line charts

**Description:**  
Line charts should use `lw=2` (line width of 2) for better visibility and consistency across lectures.

**Check for:**
- Missing `lw` parameter in `ax.plot()`
- Line width values other than 2
- Thin lines that are hard to see

**Examples:**
````markdown
<!-- ✅ Correct: Using lw=2 -->
```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(x, y, lw=2)
ax.set_xlabel("time")
```

<!-- ✅ Correct: Multiple lines with lw=2 -->
```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(x, y1, label='series 1', lw=2)
ax.plot(x, y2, label='series 2', lw=2)
ax.legend()
```

<!-- ❌ Incorrect: Missing lw parameter -->
```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("time")
```

<!-- ❌ Incorrect: Wrong line width -->
```{code-cell} ipython3
fig, ax = plt.subplots()
ax.plot(x, y, lw=1)  # Too thin
ax.set_xlabel("time")
```
````

---

### Rule: qe-fig-009
**Category:** rule  
**Title:** Figure sizing

**Description:**  
Figures should be 80-100% of text width for optimal readability and layout.

**Check for:**
- Figures that are too small (<80% text width)
- Figures that are too large (>100% text width)
- Explicit width settings that don't fall in this range

**Examples:**
````markdown
<!-- ✅ Correct: Default or appropriate width -->
```{code-cell} ipython3
---
mystnb:
  figure:
    caption: time series plot
    name: fig-timeseries
---
fig, ax = plt.subplots()
ax.plot(x, y, lw=2)
```

<!-- ✅ Correct: Explicit width in acceptable range -->
```{code-cell} ipython3
---
mystnb:
  figure:
    caption: comparison plot
    name: fig-compare
    width: 90%
---
fig, ax = plt.subplots()
ax.plot(x, y, lw=2)
```
````

---

### Rule: qe-fig-010
**Category:** rule  
**Title:** Plotly figures require latex directive

**Description:**  
Plotly figures must include a `{only} latex` directive after the figure with a link back to the website for PDF compatibility.

**Check for:**
- Plotly figures without latex directive
- Incorrect link format

**Required pattern:**
````markdown
(fig-label)=
```{code-cell} python
import plotly.express as px
fig = px.scatter(x=[0, 1, 2], y=[0, 1, 4])
fig.show()
```

```{only} latex
This figure is interactive you may [click here to see this figure on the website](https://intro.quantecon.org/filename.html#fig-label)
```
````

---

### Rule: qe-fig-011
**Category:** rule  
**Title:** Use image directive when nested in other directives

**Description:**  
For PDF compatibility, use the `image` directive (rather than `figure`) when inside other directives such as `exercise` or `solution`.

**Check for:**
- `figure` directive nested inside other directives
- Missing PDF compatibility consideration

**Examples:**
`````markdown
<!-- ✅ Correct: Using image directive inside exercise -->
````{exercise}
:label: ex-plot

Create a time series plot.

```{image} path/to/figure.png
:width: 80%
:align: center
```
````

<!-- ❌ Incorrect: Using figure directive inside exercise -->
````{exercise}
:label: ex-plot

Create a time series plot.

```{figure} path/to/figure.png
:width: 80%
GDP growth over time
```
````
`````

---

## Lecture Content to Review

[The lecture content will be appended here]
