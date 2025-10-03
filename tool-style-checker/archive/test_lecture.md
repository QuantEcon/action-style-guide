# Dynamic Programming

This lecture introduces dynamic programming.

## The bellman Equation

The bellman equation is fundamental. It relates the value of a state to future states.

Consider a simple problem. The value function satisfies:

$$v(x) = max_{a} [r(x,a) + beta * v(x')]$$

Where beta is the discount factor and x' is the next state.

## Example

Let's solve a simple consumption-savings problem. The agent maximizes utility over time. They choose consumption c and savings.

The value function is v(w) = max_{c} [u(c) + beta * v(w')]. Here w is wealth and w' = R(w-c) where R is the return.

We can solve this using iteration. Start with an initial guess. Then update using the bellman equation. Continue until convergence.

## Summary

Dynamic programming is powerful. It breaks problems into subproblems. The bellman equation provides the key relationship.
