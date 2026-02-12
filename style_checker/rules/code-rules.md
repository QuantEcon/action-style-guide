# QuantEcon Code Style Rules

## Version: 2025-Oct-09 (Focused Extract)

This document contains only the **code-focused rules** for QuantEcon lecture content. Each rule is categorized as either `rule` (clearly actionable), `style` (advisory guideline requiring judgment), or `migrate` (legacy patterns to update).

---

## Code Style Rules

### Rule: qe-code-001
**Type:** style  
**Title:** Follow PEP8 unless closer to mathematical notation

**Description:**  
Follow PEP8 conventions unless there is a good reason to do otherwise (e.g., to get closer to mathematical notation). It's fine to use capitals for matrices. Operators are typically surrounded by spaces (`a * b`, `a + b`), but write `a**b` for exponentiation.

**Check for:**
- Spacing violations (except for `**`)
- Naming that violates PEP8 without mathematical justification

---

### Rule: qe-code-002
**Type:** rule  
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
**Type:** rule  
**Title:** Package installation at lecture top

**Description:**  
Lectures should run in a base installation of Anaconda Python. Any additional packages not included in Anaconda must be installed near the top of the lecture, in one of the first code cells (after the title and any introductory text). The installation cell should use `!pip install` commands with `tags: [hide-output]` to suppress verbose installation output. A brief introductory sentence should precede the installation cell explaining what additional libraries are needed.

**Important:** This rule only applies when the lecture imports packages that are NOT part of the standard Anaconda distribution (e.g., `quantecon`, `yfinance`). Common packages like `numpy`, `matplotlib`, `scipy`, and `pandas` are included in Anaconda and do NOT require installation cells.

**Check for:**
- Non-Anaconda packages imported but not installed at the top of the lecture
- Package installation commands (`!pip install`) appearing in the middle or end of the lecture instead of near the top
- Missing `hide-output` tags on installation code cells
- Do NOT flag lectures that only use standard Anaconda packages (numpy, matplotlib, scipy, pandas, sympy, etc.)

**Examples:**
````markdown
<!-- ✅ Correct: Installation cell near the top, after title/intro -->
# Lecture Title

Introduction paragraph explaining the lecture topic.

In addition to what's in Anaconda, this lecture will need the following libraries:

```{code-cell} ipython3
---
tags: [hide-output]
---
!pip install quantecon
!pip install --upgrade yfinance
```

<!-- ❌ Incorrect: Installation buried in the middle of the lecture -->
## Some Later Section

```{code-cell} ipython3
!pip install quantecon
```

<!-- ❌ Incorrect: Missing hide-output tag -->
```{code-cell} ipython3
!pip install quantecon
```
````

---

### Rule: qe-code-004
**Type:** migrate  
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
**Type:** migrate  
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
**Type:** rule  
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