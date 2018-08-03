import numpy as np
import scipy.sparse as sparse
import matplotlib.pyplot as plt
import pyamg

from helper import trimesh, graph_laplacian

meshnum = 2

if meshnum == 1:
    from pyamg.gallery import mesh
    V, E = mesh.regular_triangle_mesh(20, 6)
if meshnum == 2:
    from scipy.io import loadmat
    mesh = loadmat('crack_mesh.mat')
    V = mesh['V']
    E = mesh['E']

A = graph_laplacian(V, E)

# construct preconditioner
ml = pyamg.smoothed_aggregation_solver(A, coarse_solver='pinv2', max_coarse=10)
M = ml.aspreconditioner()

# solve for lowest two modes: constant vector and Fiedler vector
X = np.random.rand(A.shape[0], 2)
(eval, evec, res) = sparse.linalg.lobpcg(A, X, M=None, tol=1e-12, largest=False,
                                         verbosityLevel=0,
                                         retResidualNormsHistory=True)

fiedler = evec[:, 1]

# use the median of the Fiedler vector as the separator
vmed = np.median(fiedler)
v = np.zeros((A.shape[0],))
K = np.where(fiedler <= vmed)[0]
v[K] = -1
K = np.where(fiedler > vmed)[0]
v[K] = 1

# plot the mesh and partition
trimesh(V, E)
sub = plt.gca()
sub.scatter(V[:, 0], V[:, 1], marker='o', s=50, c=v)
# sub.scatter(V[:,0],V[:,1],marker='o',s=50,c=fiedler)
plt.show()
