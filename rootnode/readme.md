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
