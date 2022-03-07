This is a collection of short examples for [PyAMG](https://github.com/pyamg/pyamg).
The source code for these **(and more)** examples is available at
https://github.com/pyamg/pyamg-examples.

### Table of Contents
- **<a href="#blackboxsolver">Blackbox Solver</a>**
- **<a href="#smoothedaggregationamg">Smoothed Aggregation AMG</a>**
- **<a href="#classicalamg">Classical AMG</a>**
- **<a href="#rootnodeamg">Rootnode AMG</a>**
- **<a href="#finiteelements">Finite Elements</a>**
- **<a href="#preconditioning">Preconditioning</a>**
- **<a href="#otherapplications">Other Applications</a>**

<a name="blackboxsolver"></a>
### Blackbox Solver

[demo.py](./blackbox/demo.py)

This demo highlights using PyAMG's `blackbox` module, which attempts to solve
an arbitrary system `A x = b` with minimal input.  The matrix `A` can be
non-Hermitian, indefinite, Hermitian positive-definite, etc...  The method tries
generic and
robust settings for `smoothed_aggregation_solver(..)`.  If
`solve()` fails to effectively solve the system,
then it may be helpful to look at the demo in `solver_diagonstics`
for guidance on automatically finding better parameter settings.

To use `solve()`, only the matrix `A` and a right-hand side `b` are needed:

```python
x = pyamg.solve(A, b, verb=True)
```
The demo produces residual norms that can vary from machine to machine.

```
  Detected a Hermitian matrix
    maxiter = 400
    iteration 1.0
    iteration 2.0
    iteration 3.0
    iteration 4.0
    iteration 5.0
    iteration 6.0
    iteration 7.0
  Residuals ||r_k||_M, ||r_0||_M = 6.45e-01, 8.68e+06
  Residual reduction ||r_k||_M/||r_0||_M = 7.43e-08
```

***

<a name="smoothedaggregationamg"></a>
### Smoothed Aggregation AMG


#### Aggregation

[demo.py](./aggregation/demo.py)

In this example, the first-level aggregates are shown for AMG based on smoothed aggregation.
An example mesh and adjacency matrix is loaded from `square.mat`, followed by a call to
`smoothed_aggregation_solver`.  Then the first-level aggregates are
plotted. From the figure, most aggregates encompass entire groups of
elements in the underlying mesh. Still, there are a many aggregates that yield
"strings" in the aggregation, often impacting performance.

<img src="./aggregation/output/aggregates.png" width="300"/>


#### One Dimensional Problem

[demo.py](./one_dimension/demo.py)

This example illustrates the effect, in 1D, of smoothed aggregation on
tentative prolongation operators.  Each of the aggregates (groups of three in
this case) are plotted with the associated (smoothed) basis functions.

<img src="./one_dimension/output/one_dimension_aggregates.png" width="300"/>


#### Visualizing Aggregation

[demo1.py](./visualizing_aggregation/demo1.py)

[demo2.py](./visualizing_aggregation/demo2.py)

In these two example the `pyamg.vis` module is called to display
aggregation in both two and three dimensions.  `demo1.py` considers the Poisson
problem on an unstructured triangulation of the unit square (from the PyAMG
gallery).  In `demo2.py`, the same Poisson problem is considered on an
unstructured tetrahedral mesh on the unit cube.  Two VTK compliant output files
are generated in each case: `output_mesh.vtu` and `output_aggs.vtu`.
`output_mesh.vtu` provides information on the underlying mesh (straight from
the unit square mesh), while `output_aggs.vtu` holds information on the
aggregates generated from first level of Smoothed Aggregation.  The process of
visulization in paraview is straightforward:

Start [Paraview](http://www.paravieworg/paraview/resources/software.php):

- open file: `output_mesh.vtu`
  - apply
  - under display in the object inspector: select wireframe representation
  - under display in the object inspector: select a better solid color
- open file: `output_aggs.vtu`
  - apply
  - under display in the object inspector: select surface with edges representation
  - under display in the object inspector: select a better solid color
  - under display in the object inspector: increase line width to see line aggregates (if present)
  - under display in the object inspector: increase point size to see point aggregates (if present)

<img src="./visualizing_aggregation/output/vis_aggs3.png" width="300"/>


<img src="./visualizing_aggregation/output/vis_aggs2.png" width="300"/>


#### Solver Diagnostics

[demo.py --matrix 2](./solver_diagnostics/demo.py)

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

```

Searching for optimal smoothed aggregation method for (2500,2500) matrix
    ...
    User specified a symmetric matrix
    User specified definiteness as positive
    ...
    Test 1 out of 18
    Test 2 out of 18
    Test 3 out of 18
    Test 4 out of 18
    Test 5 out of 18
    Test 6 out of 18
    Test 7 out of 18
    Test 8 out of 18
    Test 9 out of 18
    Test 10 out of 18
    Test 11 out of 18
    Test 12 out of 18
    Test 13 out of 18
    Test 14 out of 18
    Test 15 out of 18
    Test 16 out of 18
    Test 17 out of 18
    Test 18 out of 18
    --> Diagnostic Results located in rot_ani_diff_diagnostic.txt
    --> See automatically generated function definition in rot_ani_diff_diagnostic.py
```

#### Complex Arithmetic

[demo.py --solver 1](./complex/demo.py)

The smoothed aggregation solver supports complex arithmetc and
there is no conversion to an equivalent real system.  For example, the
highlighted demo here generates a basic gauge Laplacian from quantum
chromodynamics and solves the system for a random right-hand side and random
initial guess.
   
Using
```
python demo.py --solver 1
```
results in the following.

```
residual at iteration  0: 2.00e+02
residual at iteration  1: 1.21e+02
residual at iteration  2: 2.47e+01
residual at iteration  3: 5.40e+00
residual at iteration  4: 1.46e+00
residual at iteration  5: 4.60e-01
residual at iteration  6: 1.58e-01
residual at iteration  7: 5.77e-02
residual at iteration  8: 2.20e-02
residual at iteration  9: 8.70e-03
residual at iteration 10: 3.53e-03
residual at iteration 11: 1.46e-03
residual at iteration 12: 6.12e-04
residual at iteration 13: 2.59e-04
residual at iteration 14: 1.11e-04
residual at iteration 15: 4.75e-05
residual at iteration 16: 2.04e-05
residual at iteration 17: 8.82e-06
residual at iteration 18: 3.81e-06
residual at iteration 19: 1.65e-06
residual at iteration 20: 7.13e-07
MultilevelSolver
Number of Levels:     5
Operator Complexity:  1.344
Grid Complexity:      1.184
Coarse Solver:        'pinv'
  level   unknowns     nonzeros
     0       10000        50000 [74.43%]
     1        1658        15132 [22.53%]
     2         170         1906 [2.84%]
     3          12          138 [0.21%]
     4           1            1 [0.00%]

```

#### Nonsymmetric example

[demo.py --solver 1](./nonsymmetric/demo.py)

The smoothed aggregation solver supports nonsymmetric (i.e., non-Hermitian) and
indefinite matrices, through recent advances in multigrid research. The
demo highlighted here constructs a solver for a small nonsymmetric
recirculating flow problem.  The out-of-the-box example diverges,
while more advanced options yield a convergent solver.

Using

```python
python demo.py --solver 1
```

we observe the following convergence history.

```

Observe that standard multigrid parameters for Hermitian systems
yield a nonconvergent stand-alone solver.

residual at iteration  0: 8.64e-01
residual at iteration  1: 6.92e-01
residual at iteration  2: 2.02e+01
residual at iteration  3: 5.89e+02
residual at iteration  4: 1.72e+04
residual at iteration  5: 5.02e+05
residual at iteration  6: 1.47e+07
residual at iteration  7: 4.28e+08
residual at iteration  8: 1.25e+10
residual at iteration  9: 3.65e+11
residual at iteration 10: 1.07e+13
residual at iteration 11: 3.12e+14
residual at iteration 12: 9.10e+15
residual at iteration 13: 2.66e+17
residual at iteration 14: 7.76e+18
residual at iteration 15: 2.27e+20
*************************************************************
Now using nonsymmetric parameters for multigrid , we obtain a
convergent stand-alone solver. 

residual at iteration  0: 8.64e-01
residual at iteration  1: 1.14e-01
residual at iteration  2: 3.53e-02
residual at iteration  3: 1.61e-02
residual at iteration  4: 8.68e-03
residual at iteration  5: 5.09e-03
residual at iteration  6: 3.08e-03
residual at iteration  7: 1.89e-03
residual at iteration  8: 1.18e-03
residual at iteration  9: 7.44e-04
residual at iteration 10: 4.78e-04
residual at iteration 11: 3.14e-04
residual at iteration 12: 2.11e-04
residual at iteration 13: 1.46e-04
residual at iteration 14: 1.04e-04
residual at iteration 15: 7.55e-05
*************************************************************
Now, we use the nonsymmetric solver to accelerate GMRES. 

residual at iteration  0: 5.54e+00
residual at iteration  1: 1.47e+00
residual at iteration  2: 5.00e-01
residual at iteration  3: 2.96e-01
residual at iteration  4: 1.62e-01
residual at iteration  5: 5.09e-02
residual at iteration  6: 1.20e-02
residual at iteration  7: 4.86e-03
residual at iteration  8: 1.39e-03
residual at iteration  9: 9.68e-04
residual at iteration 10: 3.05e-04
residual at iteration 11: 1.36e-04
residual at iteration 12: 2.94e-05
residual at iteration 13: 6.66e-06
residual at iteration 14: 1.48e-06
residual at iteration 15: 4.32e-07
```

***

<a name="classicalamg"></a>
### Classical AMG


#### Coarse Fine Splitting

[demo.py](./coarse_fine_splitting/demo.py)

The C/F splitting---i.e. the splitting of indices into strictly coarse nodes
(C-pts) and strictly fine nodes (F-pts)---using Ruge-Stuben coarsening is
illustrated in this example.  An example mesh and adjacency graph is loaded
from `square.mat`, `ruge_stuben_solver()` is initiated, and the first level of
splittings is plotted.  Printing the multilevel object in this case shows that
the coarsening is typical: around 25% reduction in unknowns (or
coarsening-by-four), as shown below. The demo also plots the coarse-fine
splitting, with the orange C-pts and the blue F-pts.

```
MultilevelSolver
Number of Levels:     2
Operator Complexity:  1.327
Grid Complexity:      1.267
Coarse Solver:        'pinv'
  level   unknowns     nonzeros
     0         191         1243 [75.33%]
     1          51          407 [24.67%]

```

<img src="./coarse_fine_splitting/output/splitting.png" width="300"/>


#### Compatible Relaxation

[demo.py](./compatible_relaxation/demo.py)

The C/F splitting---i.e. the splitting of indices into strictly coarse nodes (C-pts)
and strictly fine nodes (F-pts)---using Compatible Relaxation is illustrated in this
example.  A 2d finite-difference matrix of the Poisson problem is used and the
coarse and fine splitting is plotted.  Coarse nodes are
highlighted orange, while fine nodes are highlighted blue.  In this case, the
coarsening is not aggressive, resulting in a coarsening-by-two.

<img src="./compatible_relaxation/output/crsplitting.png" width="300"/>


***

<a name="rootnodeamg"></a>
### Rootnode AMG


#### Rootnode AMG

[demo.py](./rootnode/demo.py)

The `rootnode_solver` is a mixture of both classical and aggregation-based
approaches to AMG, with the intent to combine their strengths, while minimizing
their respective drawbacks.  As a result, this solver is more robust for some
problem types, especially anisotropic diffusion.

In terms of use, the interface to `pyamg.aggregation.rootnode_solver(...)` is
identical to `pyamg.aggregation.smoothed_aggregation_solver(...)`, meaning that
the above aggregation examples can be easily changed by simply replacing calls
to `smoothed_aggregation_solver()` with `rootnode_solver()`.

This example compares the rootnode coarsening to classical AMG's coarsening
(see the Coarse Fine Splitting Example) and to smoothed aggregation's
coarsening (see the Aggregation Example).  The rootnode approach mixes
classical AMG and smoothed aggregation, and hence has an associated C/F
splitting that splits the indices into strictly coarse (C) nodes and strictly
fine (F) nodes, and also has an associated aggregation that disjointly splits
the nodes into strongly connected neighborhoods.  Essentially, each aggregate
has one "root" C-node associated with it, that is injected between the fine and
coarse grids.

An example mesh and adjacency graph is loaded from `square.mat`, and the
`rootnode_solver()` is initiated.  Then, the first-level C/F splitting and the
first-level aggregation are plotted. Coarse nodes are highlighted orange, while
fine nodes are highlighted blue. 

In general (as well as in this example), the C/F splitting for rootnode
contains far fewer coarse nodes than for classical AMG.  In general, this fewer
number of coarse nodes is compensated by having a somewhat denser interpolation
operator than for classical AMG.

<img src="./rootnode/output/rnaggs.png" width="300"/>


<img src="./rootnode/output/rnsplitting.png" width="300"/>


***

<a name="finiteelements"></a>
### Finite Elements


***

<a name="preconditioning"></a>
### Preconditioning


***

<a name="otherapplications"></a>
### Other Applications


***

