"""
Compute eigenvectors and eigenvalues using a preconditioned eigensolver

In this example Smoothed Aggregation (SA) is used to precondition
the LOBPCG eigensolver on a two-dimensional Poisson problem with
Dirichlet boundary conditions.
"""

import numpy as np
import scipy.sparse as sparse

import pyamg
import matplotlib.pyplot as plt

N = 100
K = 9
A = pyamg.gallery.poisson((N, N), format='csr')

# create the AMG hierarchy
ml = pyamg.smoothed_aggregation_solver(A)

# initial approximation to the K eigenvectors
X = np.random.rand(A.shape[0], K)

# preconditioner based on ml
M = ml.aspreconditioner()

# compute eigenvalues and eigenvectors with LOBPCG
W, V = sparse.linalg.lobpcg(A, X, M=M, tol=1e-8, largest=False, maxiter=40)

# plot the eigenvectors

fig, axs = plt.subplots(nrows=3, ncols=3)

for i, ax in enumerate(axs.ravel()):
    ax.set_title('Eigenvector %d' % i, fontsize=10)
    ax.pcolor(V[:, i].reshape(N, N), cmap='cool')
    ax.axis('square')
    ax.axis('off')

figname = f'./output/eigenmodes.png'
import sys
if '--savefig' in sys.argv:
    plt.savefig(figname, bbox_inches='tight', dpi=150)
else:
    plt.show()
