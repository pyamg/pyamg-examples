This demo shows the performance of finite element assembly (by way of scikit-fem)
and multigrid setup/solve (within PCG).  The solver is run to a tolerance of `1e-8`.
The figure shows:

- `DoFs`: the total number of degrees of freedom in the system
- `Assembly`: the total time to assemble the FE matrix (scikit-fem)
- `Solve prep`: the total time to condense the system to non-Dirichlet nodes (scikit-fem)
- `Solve setup`: the total time for the AMG setup phase (pyamg)
- `Solve`: the total time for the AMG solve phase (pyamg) withing PCG (scikit-fem)
