"""
Illustrates the selection of aggregates in AMG based on smoothed aggregation
"""

import numpy
import scipy.io as sio
import matplotlib as mplt
import matplotlib.pyplot as plt
import pyamg

data = sio.loadmat('square.mat')

A = data['A'].tocsr()                              # matrix
V = data['vertices'][:A.shape[0]]                  # vertices of each variable
E = numpy.vstack((A.tocoo().row,A.tocoo().col)).T  # edges of the matrix graph

# Create a multigrid solver
ml = pyamg.smoothed_aggregation_solver(A, max_levels=2, max_coarse=1, keep=True)

# AggOp[i,j] is 1 iff node i belongs to aggregate j
AggOp = ml.levels[0].AggOp

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
plt.show()
