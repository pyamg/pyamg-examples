import numpy as np
import scipy.sparse as sparse
import matplotlib.pyplot as plt
import pyamg

def graph_laplacian(V, E):
    # build graph Laplacian
    Nel = E.shape[0]
    Npts = E.max() + 1
    row = np.kron(list(range(0, Nel)), [1, 1, 1])
    col = E.ravel()
    data = np.ones((col.size,), dtype=float)
    A = sparse.coo_matrix((data, (row, col)), shape=(Nel, Npts)).tocsr()
    A = A.T * A
    A.data = -1 * np.ones((A.nnz,), dtype=float)
    A.setdiag(np.zeros((Npts,), dtype=float))
    A.setdiag(-1 * np.array(A.sum(axis=1)).ravel())
    return A.tocsr()

meshnum = 2

if meshnum == 1:
    from pyamg.gallery import mesh
    V, E = mesh.regular_triangle_mesh(20, 6)
if meshnum == 2:
    from scipy.io import loadmat
    mesh = loadmat('crack_mesh.mat')
    V = mesh['V']
    E = mesh['E']

    # order ccw
    E[:,[0,1]] = E[:,[1,0]]
    from pyamg.gallery.fem import Mesh
    m = Mesh(V, E)
    m.refine(1)
    V = m.V
    E = m.E

A = graph_laplacian(V, E)

# construct preconditioner
np.random.seed(8923)
ml = pyamg.smoothed_aggregation_solver(A, coarse_solver='pinv2', max_coarse=20)
M = ml.aspreconditioner()

# solve for lowest two modes: constant vector and Fiedler vector
X = np.random.randn(A.shape[0], 2)
(eigval, eigvec, res) = sparse.linalg.lobpcg(A, X, M=M, tol=1e-8, largest=False,
                                         verbosityLevel=0,
                                         maxiter=200,
                                         retResidualNormsHistory=True)

#print([r[0] for r in res])
fiedler = eigvec[:, 1]

# use the median of the Fiedler vector as the separator
vmed = np.median(fiedler)
v = np.zeros((A.shape[0],))
K = np.where(fiedler <= vmed)[0]
v[K] = -1
K = np.where(fiedler > vmed)[0]
v[K] = 1

# plot the mesh and partition
fig, ax = plt.subplots()
ax.triplot(V[:,0], V[:,1], E)
ax.scatter(V[:, 0], V[:, 1], marker='o', s=50, c=v, cmap='PiYG', facecolor='w')
# sub.scatter(V[:,0],V[:,1],marker='o',s=50,c=fiedler)

figname = f'./output/mesh_partition.png'
import sys
if '--savefig' in sys.argv:
    plt.savefig(figname, bbox_inches='tight', dpi=150)
else:
    plt.show()
