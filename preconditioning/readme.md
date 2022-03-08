This example shows how to effectively use multilevel solvers to
precondition a Krylov method. The first example considers the Poisson problem
from the pyamg gallery and uses a constant near-nullspace vector for SA-AMG.
The second example is 2D linear elasticity also from the pyamg gallery and uses
the typical three rigid body modes (rotation and translation in x and y) to
coach SA-AMG. Since both problems are symmetric and positive definite, CG
acceleration is used. The residual histories show a clear improvement in using
the SA-AMG preconditioners in both cases.

Using

```python
python demo.py --solver 1
```

produces the following.
