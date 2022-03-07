AMG has a range of parameter choices; selecting the optimal combination
can be challenging yet can lead to significant improvements in convergences.
This example highlights a "solver diagnostics" function that makes finding good parameter
choices a bit easier.  A brute force search is applied, and depending on the matrix
characteristics (e.g., symmetry and definiteness), 60-120 different solvers are
constructed and then tested.  As a result, this test is intended for smaller matrix problems.

The function `solver_diagnostics` (`solver_diagnostics.py`) has many
parameters, but the defaults should be sufficient.  For this test,
only the matrix, `A`, is needed, and `A` can be nonsymmetric, indefinite, or
symmetric positive definite.  The function detects symmetry and definiteness,
but it is safest to specify these.

The function outputs two separate files and we briefly examine this output
for the second example of rotated anisotropic diffusion when running the above
`demo.py`. 

Running

```python
python demo.py --matrix 2
```
will run solver diagnostics on the rotated anisotropic diffusion problem.

The first output file is `rot_ani_diff_diagnostic.txt`, which is a sorted table
of solver statistics for all the solvers tried.  This file has detailed output
for the performance of each solver, and the parameter choices used for
each solver.

The second file defines a function `rot_ani_diff_diagnostic.py`, that when
given a matrix, automatically generates and uses the best solver found.
