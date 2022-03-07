"""
Illustrates the selection of Coarse-Fine (CF) splittings in Classical AMG.
"""

import numpy as np
import scipy.io as sio
import pyamg
import matplotlib as mplt
import matplotlib.pyplot as plt

data = sio.loadmat('square.mat') #load_example('airfoil')

A = data['A'].tocsr()                           # matrix
V = data['vertices'][:A.shape[0]]               # vertices of each variable
E = np.vstack((A.tocoo().row,A.tocoo().col)).T  # edges of the matrix graph

# Use Ruge-Stuben Splitting Algorithm (use 'keep' in order to retain the splitting)
ml = pyamg.ruge_stuben_solver(A, max_levels=2, max_coarse=1, CF='RS',keep=True)
print(ml)

# The CF splitting, 1 == C-node and 0 == F-node
splitting = ml.levels[0].splitting
C_nodes = splitting == 1
F_nodes = splitting == 0

fig, ax = plt.subplots()
alledges = V[E.ravel(),:].reshape((-1, 2, 2))
col = mplt.collections.LineCollection(alledges,
                                      color=[0.7, 0.7, 0.7],
                                      linewidth=1.0)
ax.add_collection(col, autolim=True)
ax.autoscale_view()

ax.scatter(V[:,0][C_nodes], V[:,1][C_nodes],
           color=[232.0/255, 74.0/255, 39.0/255],
           s=100.0, label='C-pts', zorder=10)
ax.scatter(V[:,0][F_nodes], V[:,1][F_nodes],
           color=[19.0/255, 41.0/255, 75.0/255],
           s=100.0, label='F-pts', zorder=10)

ax.axis('square')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')

plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",
           borderaxespad=0, ncol=2)

figname = './output/splitting.png'
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == '--savefig':
        plt.savefig(figname, bbox_inches='tight', dpi=150)
else:
    plt.show()
