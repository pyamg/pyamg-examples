We consider the 2D linear elasticity problem from the pyamg gallery in this
example (corresponding to a simple finite element discretization on a regular
grid).  Three near null space modes are fed to the
`smoothed_aggregation_solver()` (relating to rotation and two types of
translation).  Smoothed aggregation and root node are ideal for this problem
and the results are apparent.  Very low operator complexities and the
convergence is quick, whether you choose the root node or smoothed aggregation
solver.

Using

```python
python demo --solver 2
```

results in the following.
