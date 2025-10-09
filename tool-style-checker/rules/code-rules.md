# QuantEcon Code Style Rules

## Version: 2025-Oct-09 (Focused Extract)

This document contains only the **code-focused rules** for QuantEcon lecture content. Each rule is categorized as either `rule` (clearly actionable), `style` (advisory guideline requiring judgment), or `migrate` (legacy patterns to update).

---

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