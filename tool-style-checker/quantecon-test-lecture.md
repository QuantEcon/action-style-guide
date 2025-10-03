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

This lecture contains intentional style guide violations for testing purposes. Each section tests specific rules from the QuantEcon style guide database. This is a test document and should not be used as a reference for proper formatting.

This lecture demonstrates various common mistakes. We will cover writing violations, mathematical notation errors, code style issues, JAX conversion patterns, figure formatting problems, and reference citation mistakes. All of these are intentionally wrong to test the style checker.

Let's start with some imports:

```{code-cell} ipython
import matplotlib.pyplot as plt
import quantecon as qe
import numpy as np
import jax
import jax.numpy as jnp
```

## Writing Style Violations

This section tests violations of writing rules.

### Multiple Sentences Per Paragraph (qe-writing-001)

This paragraph contains multiple sentences which violates the style guide. The first sentence introduces a concept. The second sentence elaborates on it. The third sentence provides an example.

### Unnecessary Capitalization (qe-writing-004)

The Bellman Equation is a fundamental tool in Dynamic Programming.

We use the Method of Lagrange Multipliers to solve the Optimization Problem.

The Nash Equilibrium is a Solution Concept in Game Theory.

### Wrong Emphasis Formatting (qe-writing-005)

A *closed set* is a set whose complement is open.

All consumers have **identical** endowments in this model.

The **convergence** property is important for our analysis.

### Wrong Heading Capitalization (qe-writing-006)

## A Section About Binary Packages With Python Frontends

This section heading violates the capitalization rule by using Title Case.

### Another Incorrectly Capitalized Section Heading

This Should Only Have First Word Capitalized.

## Mathematics Violations

This section tests mathematical notation violations.

### LaTeX Commands Without Delimiters (qe-math-001)

The parameter \alpha controls the utility function, and \beta represents the discount factor.

We set \gamma = 2 for the risk aversion parameter.

The production function uses parameters \theta and \sigma.

### Unicode in Math Environments (qe-math-001)

The utility function is given by:

$$
u(c) = \frac{c^{1-α}}{1-α}
$$

where α > 0 is the risk aversion parameter.

### Wrong Transpose Notation (qe-math-002)

The transpose of matrix $A$ is denoted $A^T$.

The quadratic form is $x^T A x$ where $x$ is a vector.

We can write this as $y^{\prime} M y$ for the variance.

### Wrong Matrix Brackets (qe-math-003)

The transition matrix is:

$$
P = \begin{pmatrix}
0.9 & 0.1 \\
0.2 & 0.8
\end{pmatrix}
$$

The identity matrix:

$$
I = \begin{Bmatrix}
1 & 0 \\
0 & 1
\end{Bmatrix}
$$

### Bold Face Matrices (qe-math-004)

Let $\mathbf{A}$ be the coefficient matrix and $\mathbf{x}$ be the state vector.

The solution is $\mathbf{y} = \mathbf{X} \boldsymbol{\beta}$.

We need to solve $\mathbf{A} \mathbf{x} = \mathbf{b}$ for $\mathbf{x}$.

### Wrong Sequence Notation (qe-math-005)

Consider the sequence $[ x_t ]_{t=0}^{\infty}$ of state variables.

The consumption sequence is denoted $[ c_t ]_{t=0}^{T}$.

### Nested Math Environments (qe-math-006)

The system of equations is:

$$
\begin{align}
x + y &= 5 \\
2x - y &= 1
\end{align}
$$

Another multi-line equation:

$$
\begin{align}
\alpha + \beta &= 1 \\
\gamma &= 2
\end{align}
$$

### Manual Equation Tags (qe-math-007)

The Bellman equation is:

$$
V(x) = \max_{y} \{ u(x, y) + \beta V(y) \} \tag{1}
$$

The Euler equation:

$$
u'(c_t) = \beta u'(c_{t+1}) (1 + r) \tag{2}
$$

## Code Style Violations

This section tests code-related violations.

### Spelled-Out Greek Letters (qe-code-002)

```{code-cell} ipython
def utility_function(c, alpha=0.5, beta=0.95, gamma=2.0):
    """Utility function with discount factor."""
    return (c**(1-alpha) - 1) / (1-alpha) * beta

# Production function
def production(k, theta=0.3, sigma=1.0):
    return k**theta * sigma
```

### Missing Package Installation (qe-code-003)

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

### Manual Timing Instead of qe.Timer (qe-code-004)

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

### Using Jupyter Magic for Timing (qe-code-005)

```{code-cell} ipython
%timeit sum([i**2 for i in range(1000000)])
```

```{code-cell} ipython
%%timeit
result = []
for i in range(1000):
    result.append(i**2)
```

## JAX Violations

This section tests JAX-specific violations.

### In-Place Array Modifications (qe-jax-004)

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

### NumPy Random Instead of JAX Random (qe-jax-006)

```{code-cell} ipython
# Using NumPy random instead of JAX
np.random.seed(42)
shocks = np.random.normal(0, 1, 100)
random_draws = np.random.uniform(0, 1, 50)

# Another violation
np.random.seed(123)
data = np.random.randn(1000)
```

## Figure Violations

This section tests figure formatting violations.

### Embedded Titles in Figures (qe-fig-003)

```{code-cell} ipython
fig, ax = plt.subplots()
ax.set_title("GDP Per Capita Vs Life Expectancy")
ax.plot([1, 2, 3], [1, 4, 9], lw=2)
ax.set_xlabel("time")
ax.set_ylabel("value")
plt.show()
```

```{code-cell} ipython
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle("Comparison of Models")
ax1.plot([1, 2, 3], [1, 4, 9], lw=2)
ax2.plot([1, 2, 3], [9, 4, 1], lw=2)
plt.show()
```

### Wrong Caption Formatting (qe-fig-004)

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "A Very Long And Verbose Caption That Describes The Entire Figure In Great Detail"
    name: fig-long-caption
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
    caption: "Title Case Caption For GDP"
    name: fig-title-case
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 2, 3, 4], lw=2)
ax.set_xlabel("year")
plt.show()
```

### Missing or Generic Figure Names (qe-fig-005)

```{code-cell} ipython
---
mystnb:
  figure:
    caption: "convergence path"
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
    name: fig1
---
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16], lw=2)
ax.set_xlabel("time")
plt.show()
```

### Uppercase Axis Labels (qe-fig-006)

```{code-cell} ipython
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16], lw=2)
ax.set_xlabel("Time Period")
ax.set_ylabel("GDP Per Capita")
plt.show()
```

```{code-cell} ipython
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 2, 3, 4], lw=2)
ax.set_xlabel("Year")
ax.set_ylabel("Value")
plt.show()
```

### Removed Spines (qe-fig-007)

```{code-cell} ipython
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16], lw=2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel("time")
plt.show()
```

```{code-cell} ipython
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 2, 3, 4], lw=2)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_xlabel("time")
plt.show()
```

### Missing Line Width (qe-fig-008)

```{code-cell} ipython
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16])
ax.set_xlabel("time")
ax.set_ylabel("value")
plt.show()
```

```{code-cell} ipython
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16], lw=1)
ax.set_xlabel("time")
ax.set_ylabel("value")
plt.show()
```

## Citation Violations

This section tests citation and reference violations.

### Wrong Citation Style (qe-ref-001)

This result was proven by {cite}`StokeyLucas1989`.

The work of {cite}`Sargent1987` shows that rational expectations matter.

Dynamic programming was introduced by Bellman (1957) {cite}`Bellman1957`.

As shown in the literature {cite:t}`Ljungqvist2012`, this approach is standard.

## Additional Mixed Violations

### Combining Multiple Violations

The Production Function uses parameters \alpha and \beta. This is based on work by {cite}`Solow1956`. The parameter values are typically set with alpha = 0.3 representing capital share.

$$
Y = K^\alpha L^{\beta} \tag{3}
$$

Where $\mathbf{K}$ is the Capital Stock and $\mathbf{L}$ is Labor.

```{code-cell} ipython
def production_calc(K, L, alpha=0.3, beta=0.7):
    """Calculate output using Cobb-Douglas Production Function."""
    start_time = time.time()
    Y = K**alpha * L**beta
    end_time = time.time()
    print(f"Calculation Time: {end_time - start_time}")
    return Y
```

### Figure with Multiple Violations

```{code-cell} ipython
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title("Production Possibilities Frontier")
ax.plot([0, 1, 2, 3, 4], [4, 3, 2, 1, 0])
ax.set_xlabel("Good X")
ax.set_ylabel("Good Y")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()
```

## Exercises

```{exercise}
:label: test-ex-1

Calculate The Optimal Value Function. Use Dynamic Programming to solve this Problem.
```

```{solution} test-ex-1
:class: dropdown

The Bellman Equation gives us:

$$
V(k) = \max_{c} \{ u(c) + \beta V(k') \} \tag{4}
$$

Where $\mathbf{k}$ is Capital and $\mathbf{c}$ is Consumption.

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

## Summary

This test lecture contains violations of the following rule categories:

1. **Writing Rules**: Multiple sentences per paragraph, unnecessary capitalization, wrong emphasis formatting, incorrect heading capitalization
2. **Mathematics Rules**: LaTeX without delimiters, unicode in math, wrong transpose notation, wrong matrix brackets, bold matrices, wrong sequence notation, nested math environments, manual tags
3. **Code Rules**: Spelled-out Greek letters, missing package installation, manual timing, Jupyter magic timing
4. **JAX Rules**: In-place modifications, NumPy random instead of JAX random
5. **Figure Rules**: Embedded titles, wrong captions, missing names, uppercase labels, removed spines, missing line width
6. **Citation Rules**: Wrong citation style for context

This document should be used as input for automated style guide checking tools.
