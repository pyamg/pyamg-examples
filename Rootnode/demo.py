# Illustrates the selection of aggregates in AMG based on smoothed aggregation

import numpy as np
from pyamg import rootnode_solver
from pyamg.gallery import load_example
from draw import lineplot
import matplotlib.pyplot as plt

data = load_example('unit_square')

A = data['A'].tocsr()                        # matrix
V = data['vertices'][:A.shape[0]]            # vertices of each variable
E = np.vstack((A.tocoo().row, A.tocoo().col)).T  # edges of the matrix graph

# Use Root-Node Solver
mls = rootnode_solver(A, max_levels=2, max_coarse=1, keep=True)

# AggOp[i,j] is 1 iff node i belongs to aggregate j
AggOp = mls.levels[0].AggOp

# determine which edges lie entirely inside an aggregate
# AggOp.indices[n] is the aggregate to which vertex n belongs
inner_edges = AggOp.indices[E[:, 0]] == AggOp.indices[E[:, 1]]
outer_edges = ~inner_edges

# Grab the root-nodes (i.e., the C/F splitting)
Cpts = mls.levels[0].Cpts
Fpts = mls.levels[0].Fpts


# Plot the aggregation
plt.figure(figsize=(6, 6))
plt.title('Finest-Level Aggregation\nC-pts in Red, F-pts in Blue')
plt.axis('equal')
lineplot(V, E[inner_edges], linewidths=3.0)
lineplot(V, E[outer_edges], linewidths=0.2)
plt.scatter(V[:, 0][Fpts], V[:, 1][Fpts], c='b', s=100.0)  # plot F-nodes in blue
plt.scatter(V[:, 0][Cpts], V[:, 1][Cpts], c='r', s=220.0)  # plot C-nodes in red

# Plot the C/F splitting
plt.figure(figsize=(6, 6))
plt.title('Finest-Level C/F splitting\nC-pts in Red, F-pts in Blue')
plt.axis('equal')
lineplot(V, E)
plt.scatter(V[:, 0][Cpts], V[:, 1][Cpts], c='r', s=100.0)  # plot C-nodes in red
plt.scatter(V[:, 0][Fpts], V[:, 1][Fpts], c='b', s=100.0)  # plot F-nodes in blue

plt.show()
