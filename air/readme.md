We demonstrate the use of AMG based on Approximate Ideal Restriction
(AIR) to solve upwind discretiazations of advection. Here we consider
a simple 2d first-order upwind finite difference discretization of
the steady advection problem
    (cos(theta),sin(theta)) cdot nabla u = 0,
with Dirichlet inflow BCs on the left and bottom of the domain
enforced strongly.

AIR is ideal for upwind discretizations of advection-dominated problems.
For pure advection, often AIR does not need Krylov acceleration; we see
this by converging to 1e-10 residual tolerance in as little as 7
iterations. AIR operator complexity tends to be large; here we comparse
using AIR with distance-1 and distance-2 restriction, and with and
without second pass coarsening. Distance-2 restriction and second-pass
coarsening will both increase operator complexity but also a improve
convergence.
```python
python demo
```
