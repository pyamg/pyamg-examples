This is a collection of short examples for [PyAMG](https://github.com/pyamg/pyamg).
The source code for these **(and more)** examples is available at
https://github.com/pyamg/pyamg-examples.

### Table of Contents
- **<a href="#introduction">Introduction</a>**
- **<a href="#blackboxsolver">Blackbox Solver</a>**
- **<a href="#smoothedaggregationamg">Smoothed Aggregation AMG</a>**
- **<a href="#classicalamg">Classical AMG</a>**
- **<a href="#rootnodeamg">Rootnode AMG</a>**
- **<a href="#finiteelements">Finite Elements</a>**
- **<a href="#preconditioning">Preconditioning</a>**
- **<a href="#otherapplications">Other Applications</a>**

<a name="introduction"></a>
### Introduction


#### Overview

[demo.py](./0_start_here/demo.py)

As a starting example, this demo considers a rotated anisotropic
diffusion problem from the `pyamg.gallery`.  First, a basic
smoothed aggregation solver is constructed.  Then, many of the
options are modified to yield a more effective solver.

The comments in `demo.py` follow several steps that walk through the demo:

- Step 1: import scipy and pyamg packages
- Step 2: setup up the system using pyamg.gallery
- Step 3: setup of the multigrid hierarchy
- Step 4: solve the system
- Step 5: print details
- Step 6: change the hierarchy
- Step 7: print details
- Step 8: plot convergence history

```


Details: Default AMG
--------------------
MultilevelSolver
Number of Levels:     5
Operator Complexity:  1.125
Grid Complexity:      1.127
Coarse Solver:        'pinv'
  level   unknowns     nonzeros
     0       40000       357604 [88.91%]
     1        4489        39601 [9.85%]
     2         529         4489 [1.12%]
     3          64          484 [0.12%]
     4           9           49 [0.01%]

The residual norm is 0.19228030467508045


The Multigrid Hierarchy
-----------------------
A_0:      40000x40000        P_0:      40000x4489      
A_1:       4489x4489         P_1:       4489x529       
A_2:        529x529          P_2:        529x64        
A_3:         64x64           P_3:         64x9         
A_4:          9x9         


Details: Specialized AMG
------------------------
MultilevelSolver
Number of Levels:     6
Operator Complexity:  2.164
Grid Complexity:      1.202
Coarse Solver:        'pinv'
  level   unknowns     nonzeros
     0       40000       357604 [46.21%]
     1        6700       226352 [29.25%]
     2        1237       177891 [22.99%]
     3         109        11817 [1.53%]
     4          11          121 [0.02%]
     5           4           16 [0.00%]

The residual norm is 1.0844406305459784e-10


```

<img src="./0_start_here/output/amg_convergence.png" width="300"/>


***

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


#### Anisotropic Diffusion

[demo.py](./diffusion/demo.py)

This demo considers different strength measures in the SA-AMG setup phase for
finite element (Q1) discretizations of anisotropic diffusion.  In particular,
the Classic Strength Measure is compared to the Evolution Measure.  For this
example, we see that total work is reduced by using the Evolution Measure and
that a scalable convergence rate is observed with rootnode:

```
Running Grid = (100 x 100)
Running Grid = (200 x 200)
Running Grid = (300 x 300)
Running Grid = (400 x 400)

AMG Scalability Study for Ax = 0, x_init = rand

Emphasis on Robustness of Evolution Strength 
Measure and Root-Node Solver

Rotated Anisotropic Diffusion in 2D
Anisotropic Coefficient = 1.000e-03
Rotation Angle = 0.393
    n     |    nnz    |    rho    |   OpCx    |   Work   
--------------------------------------------------------
 Classic strength 
--------------------------------------------------------
  10000   |   88804   |   0.86    |    1.6    |    24    
  40000   |  357604   |   0.87    |    1.6    |    25    
  90000   |  806404   |   0.87    |    1.6    |    27    
 160000   |  1435204  |   0.87    |    1.6    |    27    
--------------------------------------------------------
 Evolution strength 
--------------------------------------------------------
  10000   |   88804   |   0.56    |    1.8    |     7    
  40000   |  357604   |   0.67    |    1.8    |    10    
  90000   |  806404   |   0.69    |    1.8    |    11    
 160000   |  1435204  |   0.72    |    1.8    |    13    
--------------------------------------------------------
 Evolution strength with Rootnode 
--------------------------------------------------------
  10000   |   88804   |   0.46    |    1.8    |    5.4   
  40000   |  357604   |   0.49    |    1.9    |     6    
  90000   |  806404   |    0.5    |    1.9    |    6.3   
 160000   |  1435204  |    0.5    |    1.9    |    6.5   
```

#### Linear Elasticity

[demo.py --solver 2](./linear_elasticity/demo.py)

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

```
MultilevelSolver
Number of Levels:     5
Operator Complexity:  1.125
Grid Complexity:      1.127
Coarse Solver:        'pinv'
  level   unknowns     nonzeros
     0       80000      1430416 [88.91%]
     1        8978       158404 [9.85%]
     2        1058        17956 [1.12%]
     3         128         1936 [0.12%]
     4          18          196 [0.01%]

Number of iterations:  19d

residual at iteration  0: 1.63e+02
residual at iteration  1: 1.13e+02
residual at iteration  2: 8.19e+00
residual at iteration  3: 1.12e+00
residual at iteration  4: 2.57e-01
residual at iteration  5: 6.80e-02
residual at iteration  6: 1.87e-02
residual at iteration  7: 5.19e-03
residual at iteration  8: 1.46e-03
residual at iteration  9: 4.12e-04
residual at iteration 10: 1.17e-04
residual at iteration 11: 3.34e-05
residual at iteration 12: 9.58e-06
residual at iteration 13: 2.76e-06
residual at iteration 14: 7.99e-07
residual at iteration 15: 2.32e-07
residual at iteration 16: 6.79e-08
residual at iteration 17: 1.99e-08
residual at iteration 18: 5.87e-09
```

***

<a name="preconditioning"></a>
### Preconditioning


#### Krylov Methods

[demo.py --solver 1](./preconditioning/demo.py)

This example shows how to effectively use multilevel solvers to
precondtion a Krylov method. The first example considers the Poisson problem
from the pyamg gallery and uses a constant near-nullspace vector for SA-AMG.
The second example is 2D linear elasticity also from the pyamg gallery and uses
the typical three ridgid body modes (rotation and translation in x and y) to
coach SA-AMG. Since both problems are symmetric and positive definite, CG
acceleration is used. The residual histories show a clear improvement in using
the SA-AMG preconditioners in both cases.

Using

```python
python demo.py --solver 1
```

produces the following.

```
Matrix: Poisson
MultilevelSolver
Number of Levels:     6
Operator Complexity:  1.337
Grid Complexity:      1.188
Coarse Solver:        'pinv'
  level   unknowns     nonzeros
     0      250000      1248000 [74.82%]
     1       41750       373416 [22.39%]
     2        4704        41554 [2.49%]
     3         532         4526 [0.27%]
     4          65          509 [0.03%]
     5           9           65 [0.00%]

Matrix: Elasticity
MultilevelSolver
Number of Levels:     5
Operator Complexity:  1.281
Grid Complexity:      1.191
Coarse Solver:        'pinv'
  level   unknowns     nonzeros
     0       80000      1430416 [78.08%]
     1       13467       356409 [19.45%]
     2        1587        40401 [2.21%]
     3         192         4356 [0.24%]
     4          27          441 [0.02%]

```

<img src="./preconditioning/output/convergence_elasticity.png" width="300"/>


<img src="./preconditioning/output/convergence_poisson.png" width="300"/>


#### Eigenvalue Solvers

[demo.py](./eigensolver/demo.py)

In this this example, smoothed aggregation AMG is used to precondition the
LOBPCG eigensolver to find the lowest nine eigenmodes of a Poisson problem.
With preconditioning (`M=M` in the `loppcg` call), the computation of the
eigensubspace is extremely fast.

<img src="./eigensolver/output/eigenmodes.png" width="300"/>


***

<a name="otherapplications"></a>
### Other Applications


#### Graph Partitioning

[demo.py](./mesh_partition/demo.py)

In this example we computing a partition of a basic crack mesh (`crack_mesh.mat`)
using the Fiedler vector (the second lowest eigenmode of the graph laplacian).
We construct a SA-AMG preconditioner to assist LOBPCG in finding the Fiedler
vector.  Positive/negative values of the Fiedler vector are plotted in
different colors, illustrating the natural splitting this mesh.

<img src="./mesh_partition/output/mesh_partition.png" width="300"/>


#### Indefinite Helmholtz

[demo1d.py](./helmholtz/demo1d.py)

[demo2d.py](./helmholtz/demo2d.py)

The example focusses on the indefinite Helmholtz wave problem.  The first
part highlights the value in using waves to represent the near-null space, `B`.
In addition, we observe the waves to resemble the  (lowest) right singular vectors
of the problem.

In the case of 2D, discontinuous Galerkin is used, yielding multiple
degrees of freedom at each spatial location.  As a result,
the fine level (level-0) aggregates of the discontinuous
elemeents, largely group neigboring vertices.  The wave-like near
null-space is then enforced on the first coarse grid (level-1), resulting
in four modes.

```

Running 2D Helmholtz Example
-- 10.00 Points-per-wavelength
-- 2.73e-01 = h,  2.50 = omega
-- Discretized with a local discontinuous Galerkin method
   on annulus-shaped domain
Using only a constant mode for interpolation yields an inefficient solver.
This is due to aliasing oscillatory, but algebraically smooth, modes on the coarse levels.
residual at iteration  0: 3.14e+01
residual at iteration  1: 4.00e+00
residual at iteration  2: 2.53e+00
residual at iteration  3: 9.74e-01
residual at iteration  4: 2.76e-01
residual at iteration  5: 1.22e-01
residual at iteration  6: 5.91e-02
residual at iteration  7: 2.64e-02
residual at iteration  8: 1.48e-02
residual at iteration  9: 6.75e-03
residual at iteration 10: 3.30e-03
residual at iteration 11: 1.73e-03
residual at iteration 12: 6.48e-04
residual at iteration 13: 3.75e-04
residual at iteration 14: 1.44e-04
residual at iteration 15: 6.55e-05
residual at iteration 16: 3.85e-05
residual at iteration 17: 1.34e-05
residual at iteration 18: 7.11e-06
residual at iteration 19: 3.81e-06
residual at iteration 20: 9.36e-07
Note the improved performance from using planewaves in B.
residual at iteration  0: 3.05e+01
residual at iteration  1: 2.62e-01
residual at iteration  2: 2.42e-03
residual at iteration  3: 2.88e-05
residual at iteration  4: 3.29e-07
residual at iteration  5: 3.87e-09
MultilevelSolver
Number of Levels:     4
Operator Complexity:  1.435
Grid Complexity:      1.411
Coarse Solver:        'pinv2'
  level   unknowns     nonzeros
     0        2880        52016 [69.67%]
     1         880        10480 [14.04%]
     2         256         9856 [13.20%]
     3          48         2304 [3.09%]

```

<img src="./helmholtz/output/1dhelmholtzconv.png" width="300"/>


<img src="./helmholtz/output/2dhelmholtzagg.png" width="300"/>


<img src="./helmholtz/output/1dhelmholtzwaves.png" width="300"/>


<img src="./helmholtz/output/2dhelmholtzB.png" width="300"/>


#### High-Order DG on Poisson

[demo.py](./diffusion_dg/demo.py)

In this example we look at a 2D DG discretization of a Poisson problem.
The mesh consists of 46 elements, with p=5, leading to 21 degrees of freedom
per element.  The first figure shows that aggregation is local, leading to
a continuous first level.  The first coarse level (level1) candidate vector `B` is
also shown.

```

Diffusion problem discretized with p=5 and the local
discontinuous Galerkin method.
Observe that standard SA parameters for this p=5 discontinuous 
Galerkin system yield an inefficient solver.

residual at iteration  0: 2.98e+02
residual at iteration  1: 1.07e+01
residual at iteration  2: 5.17e+00
residual at iteration  3: 2.71e+00
residual at iteration  4: 1.63e+00
residual at iteration  5: 9.92e-01
residual at iteration  6: 5.22e-01
residual at iteration  7: 3.57e-01
residual at iteration  8: 2.27e-01
residual at iteration  9: 1.26e-01
residual at iteration 10: 8.83e-02
residual at iteration 11: 5.53e-02
residual at iteration 12: 3.64e-02
residual at iteration 13: 2.62e-02
residual at iteration 14: 1.78e-02
residual at iteration 15: 1.17e-02
residual at iteration 16: 6.79e-03
residual at iteration 17: 4.44e-03
residual at iteration 18: 2.63e-03
residual at iteration 19: 1.43e-03
residual at iteration 20: 8.59e-04

Now use appropriate parameters, especially 'energy' prolongation
smoothing and a distance based strength measure on level 0.  This
yields a much more efficient solver.

residual at iteration  0: 2.98e+02
residual at iteration  1: 1.32e+00
residual at iteration  2: 8.73e-02
residual at iteration  3: 1.02e-02
residual at iteration  4: 6.41e-04
residual at iteration  5: 6.64e-05
residual at iteration  6: 6.05e-06
residual at iteration  7: 6.16e-07
residual at iteration  8: 4.93e-08
residual at iteration  9: 5.44e-09
MultilevelSolver
Number of Levels:     5
Operator Complexity:  1.622
Grid Complexity:      1.805
Coarse Solver:        'pinv2'
  level   unknowns     nonzeros
     0         966        35338 [61.67%]
     1         652        19602 [34.21%]
     2          94         2006 [3.50%]
     3          26          322 [0.56%]
     4           6           36 [0.06%]

```

<img src="./diffusion_dg/output/dgaggs.png" width="300"/>


<img src="./diffusion_dg/output/dgmodes.png" width="300"/>


***

