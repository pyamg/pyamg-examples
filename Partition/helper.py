import numpy as np
import scipy.sparse as sparse
import matplotlib.pyplot as plt
import matplotlib as mpl


def trimesh(vertices, indices, labels=False):
    """
    Plot a 2D triangle mesh
    """

    vertices, indices = np.asarray(vertices), np.asarray(indices)

    # 3d tensor [triangle index][vertex index][x/y value]
    triangles = vertices[indices.ravel(), :].reshape((indices.shape[0], 3, 2))

    col = mpl.collections.PolyCollection(triangles)
    col.set_facecolor('black')
    col.set_alpha(0.75)
    col.set_linewidth(1)

    sub = plt.gca()
    sub.add_collection(col, autolim=True)
    plt.axis('off')
    sub.autoscale_view()

    if labels:
        barycenters = np.average(triangles, axis=1)
        for n, bc in enumerate(barycenters):
            plt.text(bc[0], bc[1], str(n), {'color': 'k', 'fontsize': 8,
                                            'horizontalalignment': 'center',
                                            'verticalalignment': 'center'})


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
