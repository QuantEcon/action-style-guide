# QuantEcon JAX Code Style Rules

## Version: 2025-Oct-09 (Focused Extract)

This document contains only the **JAX-focused rules** for QuantEcon lecture content. Each rule is categorized as either `rule` (clearly actionable), `style` (advisory guideline requiring judgment), or `migrate` (legacy patterns to update).

---

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