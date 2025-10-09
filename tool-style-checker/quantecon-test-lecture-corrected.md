---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Test Lecture For Style Guide Violations

```{contents} Contents
:depth: 2
```

## Overview

This lecture contains intentional style guide violations for testing purposes.

Each section tests specific rules from the QuantEcon style guide database.

This is a test document and should not be used as a reference for proper formatting.

This lecture demonstrates various common mistakes.

We will cover writing violations, mathematical notation errors, code style issues, JAX conversion patterns, figure formatting problems, and reference citation mistakes.

All of these are intentionally wrong to test the style checker.

Let's start with some imports:

```{code-cell} ipython
import matplotlib.pyplot as plt
import quantecon as qe
import numpy as np
import jax
import jax.numpy as jnp
```

## Writing style violations

This section tests violations of writing rules.

### Multiple sentences per paragraph (qe-writing-001)

This paragraph contains multiple sentences which violates the style guide.

The first sentence introduces a concept.

The second sentence elaborates on it.

The third sentence provides an example.

### Unnecessary capitalization (qe-writing-004)

The bellman equation is a fundamental tool in dynamic programming.

We use the method of lagrange multipliers to solve the optimization problem.

The nash equilibrium is a solution concept in game theory.

### Wrong emphasis formatting (qe-writing-005)

A **closed set** is a set whose complement is open.

All consumers have *identical* endowments in this model.

The *convergence* property is important for our analysis.

### Wrong heading capitalization (qe-writing-006)

## A section about binary packages with python frontends

This section heading violates the capitalization rule by using Title Case.

### Another incorrectly capitalized section heading

This should only have first word capitalized.

## Mathematics violations

This section tests mathematical notation violations.

### LaTeX commands without delimiters (qe-math-001)

The parameter α controls the utility function, and β represents the discount factor.

We set γ = 2 for the risk aversion parameter.

The production function uses parameters θ and σ.

### Unicode in math environments (qe-math-001)

The utility function is given by:

$$
u(c) = \frac{c^{1-\alpha}}{1-\alpha}
$$

where $\alpha > 0$ is the risk aversion parameter.

### Wrong transpose notation (qe-math-002)

The transpose of matrix $A$ is denoted $A^\top$.

The quadratic form is $x^\top A x$ where $x$ is a vector.

We can write this as $y^\top M y$ for the variance.

### Wrong matrix brackets (qe-math-003)

The transition matrix is:

$$
P = \begin{bmatrix}
0.9 & 0.1 \\
0.2 & 0.8
\end{bmatrix}
$$

The identity matrix:

$$
I = \begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}
$$

### Bold face matrices (qe-math-004)

Let $A$ be the coefficient matrix and $x$ be the state vector.

The solution is $y = X \beta$.

We need to solve $A x = b$ for $x$.

### Wrong sequence notation (qe-math-005)

Consider the sequence $\{ x_t \}_{t=0}^{\infty}$ of state variables.

The consumption sequence is denoted $\{ c_t \}_{t=0}^{T}$.

### Nested math environments (qe-math-006)

The system of equations is:

$$
\begin{aligned}
x + y &= 5 \\
2x - y &= 1
\end{aligned}
$$

Another multi-line equation:

$$
\begin{aligned}
\alpha + \beta &= 1 \\
\gamma &= 2
\end{aligned}
$$

### Manual equation tags (qe-math-007)

The Bellman equation is:

$$
V(x) = \max_{y} \{ u(x, y) + \beta V(y) \}
$$ (bellman)

The Euler equation:

$$
u'(c_t) = \beta u'(c_{t+1}) (1 + r)
$$ (euler)

## Code style violations

This section tests code-related violations.

### Spelled-out greek letters (qe-code-002)

```{code-cell} ipython
def utility_function(c, alpha=0.5, beta=0.95, gamma=2.0):
    """Utility function with discount factor."""
    return (c**(1-alpha) - 1) / (1-alpha) * beta

# Production function
def production(k, theta=0.3, sigma=1.0):
    return k**theta * sigma
```

### Missing package installation (qe-code-003)

We will use the `quantecon` package for this analysis without installing it at the top.

```{code-cell} ipython
# Using quantecon without installing it first
mc = qe.MarkovChain([[0.9, 0.1], [0.2, 0.8]])
```

Later in the lecture:

```{code-cell} ipython
# Installing package in middle of lecture
!pip install quantecon
```

### Manual timing instead of qe.Timer (qe-code-004)

```{code-cell} ipython
import time

start_time = time.time()
result = sum([i**2 for i in range(1000000)])
end_time = time.time()
print(f"Elapsed: {end_time - start_time:.4f} seconds")
```

Legacy tic/toc pattern:

```{code-cell} ipython
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

### Using jupyter magic for timing (qe-code-005)

```{code-cell} ipython
%timeit sum([i**2 for i in range(1000000)])
```

```{code-cell} ipython
%%timeit
result = []
for i in range(1000):
    result.append(i**2)
```

## JAX violations

This section tests JAX-specific violations.

### In-place array modifications (qe-jax-004)

```{code-cell} ipython
def bad_update(state, shock):
    """Violates functional programming - modifies input."""
    state[0] = state[0] + shock
    return state

# Another violation
def increment_array(arr):
    arr += 1
    return arr
```

### NumPy random instead of JAX random (qe-jax-006)

```{code-cell} ipython
# Using NumPy random instead of JAX
np.random.seed(42)
shocks = np.random.normal(0, 1, 100)
random_draws = np.random.uniform(0, 1, 50)

# Another violation
np.random.seed(123)
data = np.random.randn(1000)
```

## Figure violations

This section tests figure formatting violations.

### Embedded titles in figures (qe-fig-003)

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "GDP per capita vs life expectancy"
    name: fig-gdp-life-expectancy
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9], lw=2)
ax.set_xlabel("time")
ax.set_ylabel("value")
plt.show()
```

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "model comparison"
    name: fig-model-comparison
---
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot([1, 2, 3], [1, 4, 9], lw=2)
ax2.plot([1, 2, 3], [9, 4, 1], lw=2)
plt.show()
```

### Wrong caption formatting (qe-fig-004)

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "detailed figure description"
    name: fig-detailed-description
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16], lw=2)
ax.set_xlabel("time")
plt.show()
```

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "GDP trends"
    name: fig-gdp-trends
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 2, 3, 4], lw=2)
ax.set_xlabel("year")
plt.show()
```

### Missing or generic figure names (qe-fig-005)

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "convergence path"
    name: fig-convergence-path
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [10, 5, 2.5, 1.25], lw=2)
ax.set_xlabel("iteration")
plt.show()
```

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "simulation results"
    name: fig-simulation-results
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16], lw=2)
ax.set_xlabel("time")
plt.show()
```

### Uppercase axis labels (qe-fig-006)

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "time series data"
    name: fig-time-series
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16], lw=2)
ax.set_xlabel("time period")
ax.set_ylabel("GDP per capita")
plt.show()
```

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "annual values"
    name: fig-annual-values
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 2, 3, 4], lw=2)
ax.set_xlabel("year")
ax.set_ylabel("value")
plt.show()
```

### Removed spines (qe-fig-007)

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "quadratic growth"
    name: fig-quadratic-growth
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16], lw=2)
ax.set_xlabel("time")
plt.show()
```

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "linear trend"
    name: fig-linear-trend
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 2, 3, 4], lw=2)
ax.set_xlabel("time")
plt.show()
```

### Missing line width (qe-fig-008)

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "growth pattern"
    name: fig-growth-pattern
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16], lw=2)
ax.set_xlabel("time")
ax.set_ylabel("value")
plt.show()
```

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "value progression"
    name: fig-value-progression
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16], lw=2)
ax.set_xlabel("time")
ax.set_ylabel("value")
plt.show()
```

## Citation violations

This section tests citation and reference violations.

### Wrong citation style (qe-ref-001)

This result was proven by {cite:t}`StokeyLucas1989`.

The work of {cite:t}`Sargent1987` shows that rational expectations matter.

Dynamic programming was introduced by {cite:t}`Bellman1957`.

As shown in the literature {cite}`Ljungqvist2012`, this approach is standard.

## Additional mixed violations

### Combining multiple violations

The production function uses parameters α and β.

This is based on work by {cite}`Solow1956`.

The parameter values are typically set with α = 0.3 representing capital share.

$$
Y = K^\alpha L^{\beta}
$$ (production)

Where $K$ is the capital stock and $L$ is labor.

```{code-cell} ipython
def production_calc(K, L, alpha=0.3, beta=0.7):
    """Calculate output using Cobb-Douglas Production Function."""
    start_time = time.time()
    Y = K**alpha * L**beta
    end_time = time.time()
    print(f"Calculation Time: {end_time - start_time}")
    return Y
```

### Figure with multiple violations

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "production possibilities frontier"
    name: fig-production-frontier
---
fig, ax = plt.subplots()
ax.plot([0, 1, 2, 3, 4], [4, 3, 2, 1, 0], lw=2)
ax.set_xlabel("good X")
ax.set_ylabel("good Y")
plt.show()
```

## Exercises

```{exercise}
:label: test-ex-1

Calculate the optimal value function.

Use dynamic programming to solve this problem.
```

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

## Summary

This test lecture contains violations of the following rule categories:

1. **Writing rules**: Multiple sentences per paragraph, unnecessary capitalization, wrong emphasis formatting, incorrect heading capitalization
2. **Mathematics rules**: LaTeX without delimiters, unicode in math, wrong transpose notation, wrong matrix brackets, bold matrices, wrong sequence notation, nested math environments, manual tags
3. **Code rules**: Spelled-out Greek letters, missing package installation, manual timing, Jupyter magic timing
4. **JAX rules**: In-place modifications, NumPy random instead of JAX random
5. **Figure rules**: Embedded titles, wrong captions, missing names, uppercase labels, removed spines, missing line width
6. **Citation rules**: Wrong citation style for context

This document should be used as input for automated style guide checking tools.