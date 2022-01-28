# Illustrates the selection of aggregates in AMG based on smoothed aggregation

import numpy as np
from pyamg import rootnode_solver
from pyamg.gallery import load_example
import matplotlib as mplt
import matplotlib.pyplot as plt

data = load_example('unit_square')

A = data['A'].tocsr()                        # matrix
V = data['vertices'][:A.shape[0]]            # vertices of each variable
E = np.vstack((A.tocoo().row, A.tocoo().col)).T  # edges of the matrix graph

# Use Root-Node Solver
mls = rootnode_solver(A, max_levels=2, max_coarse=1, keep=True)

# AggOp[i,j] is 1 iff node i belongs to aggregate j
AggOp = mls.levels[0].AggOp

# Grab the root-nodes (i.e., the C/F splitting)
Cpts = mls.levels[0].Cpts
Fpts = mls.levels[0].Fpts

##
# Plot aggregates
##

# determine which edges lie entirely inside an aggregate
# AggOp.indices[n] is the aggregate to which vertex n belongs
inner_edges = AggOp.indices[E[:,0]] == AggOp.indices[E[:,1]]
outer_edges = ~inner_edges

# set up a figure
fig, ax = plt.subplots(figsize=(6, 6))

# non aggregate edges
nonaggs = V[E[outer_edges].ravel(),:].reshape((-1, 2, 2))
col = mplt.collections.LineCollection(nonaggs,
                                      color=[232.0/255, 74.0/255, 39.0/255],
                                      linewidth=1.0)
ax.add_collection(col, autolim=True)

# aggregate edges
aggs = V[E[inner_edges].ravel(),:].reshape((-1, 2, 2))
col = mplt.collections.LineCollection(aggs,
                                      color=[19.0/255, 41.0/255, 75.0/255],
                                      linewidth=4.0)
ax.add_collection(col, autolim=True)

ax.autoscale_view()
ax.axis('equal')
plt.title("Aggregates", fontsize=16)
plt.savefig('temp.png', dpi=300)

##
# Plot the C/F splitting
##
fig, ax = plt.subplots(figsize=(6, 6))
alledges = V[E.ravel(),:].reshape((-1, 2, 2))
col = mplt.collections.LineCollection(alledges,
                                      color=[0.7, 0.7, 0.7],
                                      linewidth=1.0)
ax.add_collection(col, autolim=True)

ax.autoscale_view()

plt.scatter(V[:,0][Cpts], V[:,1][Cpts],
            color=[232.0/255, 74.0/255, 39.0/255],
            s=100.0, label='C pts', zorder=10)
plt.scatter(V[:,0][Fpts], V[:,1][Fpts],
            color=[19.0/255, 41.0/255, 75.0/255],
            s=100.0, label='F pts', zorder=10)

ax.axis('equal')
l = plt.legend(framealpha=1.0, fontsize=16)
l.set_zorder(20)
plt.xlabel('X', fontsize=16)
plt.ylabel('Y', fontsize=16)
plt.title("C/F Splitting", fontsize=16)
plt.savefig('temp2.png', dpi=300)

plt.show()
