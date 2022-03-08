The C/F splitting---i.e. the splitting of indices into strictly coarse nodes
(C-pts) and strictly fine nodes (F-pts)---using Ruge-Stuben coarsening is
illustrated in this example.  An example mesh and adjacency graph is loaded
from `square.mat`, `ruge_stuben_solver()` is initiated, and the first level of
C/F splitting is plotted.  Printing the multilevel object in this case shows that
the coarsening is typical: around 25% reduction in unknowns (or
coarsening-by-four), as shown below. The demo also plots the coarse-fine
splitting, with the orange C-pts and the blue F-pts.
