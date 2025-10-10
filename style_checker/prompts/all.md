# QuantEcon Style Guide - All Categories

You are a helpful AI assistant reviewing QuantEcon lecture content for style guide compliance.

Your task is to review the provided lecture content and identify any violations of the style rules across ALL categories.

## Instructions

1. **Read the lecture content carefully**
2. **Check against all rules below**
3. **Report ONLY violations you find** (don't report what's correct)
4. **For each violation:**
   - State the rule code (e.g., qe-writing-001)
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

6. **Group violations by category** (Writing, Math, Code, etc.)

7. **If no violations found:** Simply respond with "No style violations found."

## Complete Style Guide



## Writing Rules

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

## Math Rules

## Mathematics Rules

### Rule: qe-math-001
**Category:** rule  
**Title:** Prefer UTF-8 unicode for simple parameter mentions, be consistent

**Description:**  
For simple parameter mentions in narrative text, prefer UTF-8 unicode characters (α, β, γ, etc.) over inline math with LaTeX commands (`$\alpha$`, `$\beta$`, etc.). This improves readability and reduces visual clutter.

However, if your text contains mathematical expressions using those parameters (e.g., `$x = \frac{\alpha}{\beta}$`), it's acceptable to use inline math consistently for all parameter mentions in that context.

Always use LaTeX commands inside math environments. Never use unicode characters inside math environments.

**Check for:**
- LaTeX commands in narrative text outside any math delimiters
- Unicode characters inside math environments
- Unnecessary inline math delimiters for isolated parameter mentions when no related mathematical expressions are present

**Examples:**
```markdown
<!-- ✅ Preferred: UTF-8 unicode in simple narrative text -->
The parameter α controls the utility function, and β represents the discount factor.

<!-- ✅ Acceptable: Consistent inline math when mathematical expressions are present -->
The parameter $\alpha$ controls the utility function, where $x = \frac{\alpha}{\beta}$.

<!-- ✅ Correct: LaTeX commands in display math -->
The utility function is $u(c) = \frac{c^{1-\alpha}}{1-\alpha}$ where $\alpha > 0$.

<!-- ❌ Incorrect: LaTeX command without delimiters in narrative text -->
The parameter \alpha controls the utility function.

<!-- ❌ Incorrect: Unicode inside math environment -->
The utility function is $u(c) = \frac{c^{1-α}}{1-α}$ where $α > 0$.
```

---

### Rule: qe-math-002
**Category:** rule  
**Title:** Use \top for transpose notation

**Description:**  
Use `\top` (e.g., $A^\top$) to represent matrix/vector transpose, not superscript T.

**Check for:**
- Use of `^T` for transpose
- Use of `^{\prime}` or `'` for transpose in matrix contexts

**Examples:**
```markdown
<!-- ✅ Correct -->
$$A^\top B$$
$$x^\top y$$

<!-- ❌ Incorrect -->
$$A^T B$$
$$A^{\prime} B$$
```

---

### Rule: qe-math-003
**Category:** rule  
**Title:** Use square brackets for matrix notation

**Description:**  
Matrices must use square brackets with `\begin{bmatrix} ... \end{bmatrix}`. Do not use parentheses, curly brackets, or other delimiters.

**Check for:**
- Use of `\begin{pmatrix}` (parentheses)
- Use of `\begin{vmatrix}` (determinant bars, unless representing determinant)
- Use of `\begin{Bmatrix}` (curly brackets)
- Other matrix bracket types

**Examples:**
```markdown
<!-- ✅ Correct -->
$$
\begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}
$$

<!-- ❌ Incorrect -->
$$
\begin{pmatrix}
1 & 2 \\
3 & 4
\end{pmatrix}
$$
```

---

### Rule: qe-math-004
**Category:** rule  
**Title:** Do not use bold face for matrices or vectors

**Description:**  
Do NOT use bold face formatting (`\mathbf`, `\boldsymbol`, `\bm`) for matrices or vectors. Use plain letters instead.

**Check for:**
- `\mathbf{A}`, `\mathbf{x}` for matrices/vectors
- `\boldsymbol` or `\bm` commands
- Any bold formatting in matrix/vector notation

**Examples:**
```markdown
<!-- ✅ Correct -->
$$A x = b$$
$$y = X \beta$$

<!-- ❌ Incorrect -->
$$\mathbf{A} \mathbf{x} = \mathbf{b}$$
$$\boldsymbol{y} = \mathbf{X} \boldsymbol{\beta}$$
```

---

### Rule: qe-math-005
**Category:** rule  
**Title:** Use curly brackets for sequences

**Description:**  
Sequences should use curly brackets notation.

**Examples:**
```markdown
<!-- ✅ Correct -->
$$\{ x_t \}_{t=0}^{\infty}$$

<!-- ❌ Incorrect -->
$$[ x_t ]_{t=0}^{\infty}$$
```

---

### Rule: qe-math-006
**Category:** rule  
**Title:** Use aligned environment correctly for PDF compatibility
**Builder:** pdf

**Description:**  
Use `\begin{aligned} ... \end{aligned}` inside math environments (such as `$$`) for multi-line equations. Do NOT use `\begin{align} ... \end{align}` as it creates nested math environments that fail in PDF builds.

**Check for:**
- Use of `align` environment inside `$$`
- Missing `aligned` for multi-line equations

**Examples:**
```markdown
<!-- ✅ Correct -->
$$
\begin{aligned}
x + y &= 5 \\
2x - y &= 1
\end{aligned}
$$

<!-- ❌ Incorrect -->
$$
\begin{align}
x + y &= 5 \\
2x - y &= 1
\end{align}
$$
```

---

### Rule: qe-math-007
**Category:** rule  
**Title:** Use automatic equation numbering, not manual tags

**Description:**  
Do NOT use `\tag` for manual equation numbering inside math environments. Instead, use in-built equation numbering with labels.

**Check for:**
- `\tag` commands in equations
- Manual equation numbers

**Examples:**
```markdown
<!-- ✅ Correct -->
$$
x^2 + y^2 = r^2
$$ (pythagoras)

Reference: {eq}`pythagoras`

<!-- ❌ Incorrect -->
$$
x^2 + y^2 = r^2 \tag{1}
$$
```

---

### Rule: qe-math-008
**Category:** rule  
**Title:** Explain special notation (vectors/matrices)

**Description:**  
Use `\mathbb{1}` ($\mathbb{1}$) to represent vectors or matrices of ones and explain it in the lecture (e.g., "Let $\mathbb{1}$ be an $n \times 1$ vector of ones...").

**Check for:**
- Use of `\mathbb{1}` without explanation
- Inconsistent notation for vectors/matrices of ones

---

### Rule: qe-math-009
**Category:** style  
**Title:** Choose simplicity in mathematical notation

**Description:**  
When you have a choice between two reasonable options, always pick the simpler one. Use simple mathematical notation when possible (e.g., $P$ instead of $\mathcal{P}$ when freely choosing).

**Check for:**
- Overly complex mathematical notation when simpler alternatives exist
- Unnecessary decorative notation (calligraphic, blackboard bold, etc. when basic letters suffice)
- Complex formulations where simpler ones would work equally well

**Guidance:**  
This requires judgment about mathematical context and what "simpler" means in each case.

## Code Rules

## Code Style Rules

### Rule: qe-code-001
**Category:** style  
**Title:** Follow PEP8 unless closer to mathematical notation

**Description:**  
Follow PEP8 conventions unless there is a good reason to do otherwise (e.g., to get closer to mathematical notation). It's fine to use capitals for matrices. Operators are typically surrounded by spaces (`a * b`, `a + b`), but write `a**b` for exponentiation.

**Check for:**
- Spacing violations (except for `**`)
- Naming that violates PEP8 without mathematical justification

---

### Rule: qe-code-002
**Category:** rule  
**Title:** Use Unicode symbols for Greek letters in code

**Description:**  
Unicode symbols for Greek letters commonly used in economics: use `α` instead of `alpha`, `β` instead of `beta`, `γ` instead of `gamma`, etc. This makes code more readable and closer to mathematical notation.

**Check for:**
- Spelled-out Greek letters (alpha, beta, etc.) in variable names
- Inconsistent use of unicode vs spelled-out names

**Examples:**
```python
# ✅ Preferred
def utility_function(c, α=0.5, β=0.95):
    return (c**(1-α) - 1) / (1-α) * β

# ❌ Avoid
def utility_function(c, alpha=0.5, beta=0.95):
    return (c**(1-alpha) - 1) / (1-alpha) * beta
```

---

### Rule: qe-code-003
**Category:** rule  
**Title:** Package installation at lecture top

**Description:**  
Lectures should run in a base installation of Anaconda Python. Any additional packages must be installed at the top of the lecture using `!pip install` with `tags: [hide-output]`.

**Check for:**
- Missing package installations for non-Anaconda packages
- Package installations in the middle of lectures
- Missing hide-output tags

**Examples:**
````markdown
<!-- ✅ Correct -->
In addition to what's in Anaconda, this lecture will need the following libraries:

```{code-cell} ipython
---
tags: [hide-output]
---
!pip install quantecon
!pip install --upgrade yfinance
```

<!-- ❌ Incorrect -->
# (Later in lecture)
!pip install quantecon
````

---

### Rule: qe-code-004
**Category:** migrate  
**Title:** Use quantecon Timer context manager

**Description:**  
Use the modern `qe.Timer()` context manager instead of manual timing patterns or `tic`/`toc` functions.

**Check for:**
- Manual `time.time()` patterns
- Legacy `tic`/`toc`/`tac` usage
- Verbose timing code with print statements

**Examples:**
```python
# ✅ Preferred
import quantecon as qe

with qe.Timer():
    result = expensive_computation()

# ❌ Avoid: Manual time.time() pattern
import time
start_time = time.time()
result = expensive_computation()
end_time = time.time()
print(f"Elapsed: {end_time - start_time}")

# ❌ Avoid: Legacy tic/toc pattern
tic()
result = expensive_computation()
toc()
```

**Reference:**
- Documentation: https://quanteconpy.readthedocs.io/en/latest/tools/timing.html#timer
- API: `quantecon.Timer()`

---

### Rule: qe-code-005
**Category:** migrate  
**Title:** Use quantecon timeit for benchmarking

**Description:**  
Use `qe.timeit()` for statistical performance analysis across multiple runs. Use lambda functions to pass arguments.

**Check for:**
- Custom benchmarking code that could use `qe.timeit()`
- Manual timing with multiple runs
- Jupyter magic commands: `%timeit` or `%%timeit`
- Verbose benchmarking patterns

**Examples:**
```python
# ✅ Preferred
import quantecon as qe

result = qe.timeit(lambda: expensive_function(args), number=100)
result = qe.timeit(matrix_multiplication, number=100)

# ❌ Avoid: Jupyter magic commands
%timeit expensive_function(args)
%%timeit
result = expensive_function(args)
more_code()

# ❌ Avoid: Manual benchmarking with loops
import time
times = []
for _ in range(100):
    start = time.time()
    result = expensive_function()
    times.append(time.time() - start)
print(f"Mean: {sum(times)/len(times)}")
```

**Reference:**
- Documentation: https://quanteconpy.readthedocs.io/en/latest/tools/timing.html#timeit
- API: `quantecon.timeit(func, number=100, repeat=3)`

---

### Rule: qe-code-006
**Category:** rule  
**Title:** Binary packages require installation notes

**Description:**  
If using packages that require binary installations (like `graphviz`), include a warning admonition about local installation requirements at the top of the lecture.

**Check for:**
- Binary package usage without warnings
- Missing installation instructions

**Required pattern:**
````markdown
```{admonition} graphviz
:class: warning
If you are running this lecture locally it requires [graphviz](https://www.graphviz.org)
to be installed on your computer. Installation instructions for graphviz can be found
[here](https://www.graphviz.org/download/) 
```
````

## Jax Rules

## JAX Conversion Rules

### Rule: qe-jax-001
**Category:** style  
**Title:** Use functional programming patterns

**Description:**  
JAX encourages pure functions with no side effects. Functions should not modify inputs, should return new data rather than mutating existing data, and should avoid global state.

**Check for:**
- Functions modifying input arrays
- In-place operations
- Mutable class attributes
- Side effects in functions

**Examples:**
```python
# ❌ Avoid: Mutating input
def bad_update(state, shock):
    state[0] += shock
    return state

# ✅ Prefer: Pure function
def good_update(state, shock):
    return state.at[0].add(shock)
```

---

### Rule: qe-jax-002
**Category:** rule  
**Title:** Use NamedTuple for model parameters

**Description:**  
Replace classes with NamedTuple for storing model parameters. Create factory functions for instantiation with validation.

**Check for:**
- Large classes for simple parameter storage
- Mutable model parameters
- Missing factory functions

**Examples:**
```python
# ✅ Preferred pattern
from typing import NamedTuple

class EconomicModel(NamedTuple):
    α: float
    β: float
    γ: float
    grid_size: int = 100

def create_model_instance(α=0.5, β=0.95, γ=2.0, grid_size=100):
    if not 0 < α < 1:
        raise ValueError("α must be between 0 and 1")
    return EconomicModel(α=α, β=β, γ=γ, grid_size=grid_size)

# ❌ Avoid: Large mutable classes
class EconomicModel:
    def __init__(self, α, β, γ):
        self.α = α
        self.β = β
        self.γ = γ
```

---

### Rule: qe-jax-003
**Category:** style  
**Title:** Use generate_path for sequence generation

**Description:**  
Use the standardized `generate_path` function pattern for iterative sequence generation with JAX.

**Check for:**
- Imperative loops for sequence generation
- Custom scan implementations that duplicate generate_path
- Non-functional iteration patterns

**Standard pattern:**
```python
@partial(jax.jit, static_argnames=['f', 'num_steps'])
def generate_path(f, initial_state, num_steps, **kwargs):
    def update_wrapper(state, t):
        next_state = f(state, t, **kwargs)
        return next_state, state
    _, path = jax.lax.scan(update_wrapper, initial_state, jnp.arange(num_steps))
    return path.T
```

---

### Rule: qe-jax-004
**Category:** migrate  
**Title:** Use functional update patterns

**Description:**  
Use JAX functional update patterns (`.at[].set()`, `.at[].add()`) instead of NumPy in-place operations.

**Check for:**
- In-place array modifications (`arr[i] = x`, `arr += x`)
- Direct array mutations

**Examples:**
```python
# ❌ Avoid
arr[0] = 5
arr += 1

# ✅ Prefer
arr = arr.at[0].set(5)
arr = arr + 1
```

---

### Rule: qe-jax-005
**Category:** style  
**Title:** Use jax.lax for control flow

**Description:**  
Replace Python loops with JAX control flow: `jax.lax.scan` for iterations with accumulation, `jax.lax.fori_loop` for fixed iterations, `jax.lax.while_loop` for conditional loops.

**Check for:**
- Python for/while loops in JIT-compiled functions
- Imperative iteration patterns

**Examples:**
```python
# ❌ Avoid
result = []
for i in range(n):
    result.append(f(i))

# ✅ Prefer
def step(state, i):
    return state, f(i)
_, result = jax.lax.scan(step, None, jnp.arange(n))
```

---

### Rule: qe-jax-006
**Category:** migrate  
**Title:** Explicit PRNG key management

**Description:**  
Use explicit JAX PRNG key management instead of NumPy's implicit random state.

**Check for:**
- `np.random.seed()` usage
- NumPy random functions in JAX code

**Examples:**
```python
# ❌ Avoid
import numpy as np
np.random.seed(42)
shocks = np.random.normal(0, 1, 100)

# ✅ Prefer
import jax.random as jr
key = jr.PRNGKey(42)
shocks = jr.normal(key, (100,))
```

---

### Rule: qe-jax-007
**Category:** style  
**Title:** Use consistent function naming for updates

**Description:**  
Use descriptive names following the pattern `[quantity]_update` for update functions. Include time step parameter even if unused for consistency.

**Examples:**
```python
# ✅ Preferred
@jax.jit
def stock_update(current_stocks, time_step, model):
    return A @ current_stocks

@jax.jit  
def rate_update(current_rates, time_step, model):
    return A_hat @ current_rates

# ❌ Avoid
def update(x, t, m):
    return A @ x
```

## Figures Rules

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

## References Rules

## Reference and Citation Rules

### Rule: qe-ref-001
**Category:** rule  
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

## Links Rules

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

## Admonitions Rules

## Admonition and Directive Rules

### Rule: qe-admon-001
**Category:** rule  
**Title:** Use gated syntax for executable code in exercises

**Description:**  
Use gated syntax (`exercise-start`/`exercise-end`) whenever exercises contain executable code cells or nested directives.

**Check for:**
- Code cells inside regular exercise blocks
- Nested directives without gated syntax

**Examples:**
`````markdown
<!-- ✅ Correct: Gated syntax with code cell -->
```{exercise-start}
:label: my-exercise
```

Calculate factorial of 5.

```{code-cell} python
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)
factorial(5)
```

```{exercise-end}
```

<!-- ✅ Correct: Gated syntax with nested directive -->
```{exercise-start}
:label: nested-exercise
```

Prove the following theorem.

```{prf:theorem}
For all n > 0, n! > 0.
```

```{exercise-end}
```

<!-- ❌ Incorrect: Code cell without gated syntax -->
````{exercise}
:label: bad-exercise

Calculate factorial of 5.

```{code-cell} python
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)
```
````

<!-- ❌ Incorrect: Nested directive without gated syntax -->
````{exercise}
:label: bad-nested

Prove this result.

```{prf:theorem}
The result holds.
```
````
`````

---

### Rule: qe-admon-002
**Category:** style  
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
**Category:** rule  
**Title:** Use tick count management for nested directives

**Description:**  
When nesting directives, ensure the outer directive uses more ticks than nested directives. Standard pattern: nested uses 3 ticks, outer uses 4 ticks.

**Check for:**
- Equal tick counts for nested directives
- Missing ticks causing parse errors

**Examples:**
`````markdown
<!-- ✅ Correct -->
````{prf:theorem}
:label: my-theorem

```{math}
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
```

````

<!-- ❌ Incorrect - same tick count -->
```{prf:theorem}
```{math}
x = y
```
```
`````

---

### Rule: qe-admon-004
**Category:** rule  
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

**Examples:**
````markdown
<!-- ✅ Correct: Using prf: prefix in directive -->
```{prf:theorem} Bellman Principle
:label: bellman-thm

The value function satisfies the Bellman equation.
```

<!-- ✅ Correct: Using prf:ref for referencing -->
See {prf:ref}`bellman-thm` for details.

The result follows from {prf:ref}`Bellman Principle <bellman-thm>`.

<!-- ✅ Correct: Multiple prf directives -->
```{prf:lemma}
:label: helper-lemma

This intermediate result is useful.
```

```{prf:proof}
The proof follows from {prf:ref}`helper-lemma`.
```

<!-- ❌ Incorrect: Missing prf: prefix in directive -->
```{theorem} Bellman Principle
:label: bellman-thm

The value function satisfies the Bellman equation.
```

<!-- ❌ Incorrect: Using wrong reference syntax -->
See {ref}`bellman-thm` for details.

See [](#bellman-thm) for the theorem.
````

---

### Rule: qe-admon-005
**Category:** rule  
**Title:** Link solutions to exercises

**Description:**  
Solution directives must include the label of the corresponding exercise.

**Check for:**
- Solutions without exercise references
- Mismatched exercise-solution pairs

**Examples:**
`````markdown
<!-- ✅ Correct: Solution references exercise label -->
````{exercise}
:label: factorial-exercise

Write a function to calculate factorial.
````

````{solution} factorial-exercise
:class: dropdown

```python
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)
```
````

<!-- ✅ Correct: Gated solution references exercise -->
```{exercise-start}
:label: convergence-ex
```

Prove that the sequence converges.

```{exercise-end}
```

```{solution-start} convergence-ex
:class: dropdown
```

The sequence is monotonic and bounded, therefore it converges.

```{solution-end}
```

<!-- ❌ Incorrect: Solution without exercise reference -->
````{solution}
:class: dropdown

```python
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)
```
````

<!-- ❌ Incorrect: Mismatched labels -->
````{exercise}
:label: exercise-1

Calculate the sum.
````

````{solution} exercise-2
:class: dropdown

The sum is 15.
````
`````

---

## Lecture Content to Review

[The lecture content will be appended here]
