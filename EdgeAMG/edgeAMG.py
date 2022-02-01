""" Lowest order edge AMG implementing Reitzinger-Schoberl algorithm"""

import numpy as np
import scipy
import scipy.sparse as sparse
import matplotlib.pyplot as plt

import pyamg

__all__ = ['edgeAMG']

make_system = pyamg.relaxation.relaxation.make_system
gauss_seidel = pyamg.relaxation.relaxation.gauss_seidel


def hiptmair_smoother(A, x, b, D, iterations=1, sweep='symmetric'):
    A, x, b = make_system(A, x, b, formats=['csr', 'bsr'])
    gauss_seidel(A, x, b, iterations=1, sweep='forward')

    r = b - A * x
    x_G = np.zeros(D.shape[1])
    A_G, x_G, b_G = make_system(
        D.T * A * D, x_G, D.T * r, formats=['csr', 'bsr'])
    gauss_seidel(A_G, x_G, b_G, iterations=1, sweep='symmetric')
    x[:] += D * x_G
    gauss_seidel(A, x, b, iterations=1, sweep='backward')


def setup_hiptmair(lvl, iterations=1, sweep='symmetric'):
    D = lvl.D

    def smoother(A, x, b):
        hiptmair_smoother(A, x, b, D, iterations=iterations, sweep=sweep)
    return smoother


def edgeAMG(Anode, Acurl, D):
    nodalAMG = pyamg.smoothed_aggregation_solver(Anode, max_coarse=10, keep=True)

    # construct multilevel structure
    levels = []
    levels.append(pyamg.MultilevelSolver.Level())
    levels[-1].A = Acurl
    levels[-1].D = D
    for i in range(1, len(nodalAMG.levels)):
        A = levels[-1].A
        Pnode = nodalAMG.levels[i - 1].AggOp
        P = findPEdge(D, Pnode)
        R = P.T
        levels[-1].P = P
        levels[-1].R = R
        levels.append(pyamg.MultilevelSolver.Level())
        A = R * A * P
        M = sparse.dia_matrix((1.0 / ((P.T * P).diagonal()), 0),
                              shape=(P.shape[1], P.shape[1]))
        D = M * (P.T * D * Pnode)
        D = D.tocsr()
        levels[-1].A = A
        levels[-1].D = D

    edgeML = pyamg.MultilevelSolver(levels)
    for i in range(0, len(edgeML.levels)):
        edgeML.levels[i].presmoother = setup_hiptmair(levels[i])
        edgeML.levels[i].postsmoother = setup_hiptmair(levels[i])
    return edgeML


def findPEdge(D, PNode):
    """
    use D to find edges
    each row has exactly two non zeros, a -1 marking the start node, and 1
    marking the end node
    """
    numEdges = D.shape[0]
    edges = np.zeros((numEdges, 2), dtype=int)
    DRowInd = D.nonzero()[0]
    DColInd = D.nonzero()[1]
    for i in range(0, numEdges):
        if (D[DRowInd[2 * i], DColInd[2 * i]] == -
                1.0):  # first index is start, second is end
            edges[DRowInd[2 * i], 0] = DColInd[2 * i]
            edges[DRowInd[2 * i], 1] = DColInd[2 * i + 1]
        else:  # first index is end, second is start
            edges[DRowInd[2 * i], 0] = DColInd[2 * i + 1]
            edges[DRowInd[2 * i], 1] = DColInd[2 * i]

    # now that we have the edges, we need to find the nodal aggregates
    # the nodal aggregates are the columns

    # each row has 1 nonzero and that column is its aggregate
    aggs = PNode.nonzero()[1]
    numCoarseEdges = 0
    row = []
    col = []
    data = []
    coarseEdges = {}
    for i in range(0, edges.shape[0]):
        coarseV1 = aggs[edges[i, 0]]
        coarseV2 = aggs[edges[i, 1]]
        if (coarseV1 != coarseV2):  # this is a coarse edges
            # check if in dictionary
            if ((coarseV1, coarseV2) in coarseEdges):
                row.append(i)
                col.append(coarseEdges[(coarseV1, coarseV2)])
                data.append(1)
            elif ((coarseV2, coarseV1) in coarseEdges):
                row.append(i)
                col.append(coarseEdges[(coarseV2, coarseV1)])
                data.append(-1)
            else:
                coarseEdges[(coarseV1, coarseV2)] = numCoarseEdges
                numCoarseEdges = numCoarseEdges + 1
                row.append(i)
                col.append(coarseEdges[(coarseV1, coarseV2)])
                data.append(1)

    PEdge = sparse.csr_matrix((data, (row, col)),
                              shape=(numEdges, numCoarseEdges))
    return PEdge


if __name__ == '__main__':

    Acurl = sparse.csr_matrix(scipy.io.mmread("HCurlStiffness.dat"))
    Anode = sparse.csr_matrix(scipy.io.mmread("H1Stiffness.dat"))
    D = sparse.csr_matrix(scipy.io.mmread("D.dat"))

    ml = edgeAMG(Anode, Acurl, D)
    MLOp = ml.aspreconditioner()
    x = np.random.rand(Acurl.shape[1], 1)
    b = Acurl * x
    x0 = np.ones((Acurl.shape[1], 1))

    r_edgeAMG = []
    r_None = []
    r_SA = []

    ml_SA = pyamg.smoothed_aggregation_solver(Acurl)
    ML_SAOP = ml_SA.aspreconditioner()
    x_prec, info = pyamg.krylov.cg(Acurl, b, x0, M=MLOp, tol=1e-8, residuals=r_edgeAMG)
    x_prec, info = pyamg.krylov.cg(Acurl, b, x0, M=None, tol=1e-8, residuals=r_None)
    x_prec, info = pyamg.krylov.cg(Acurl, b, x0, M=ML_SAOP, tol=1e-8, residuals=r_SA)

    plt.semilogy(np.arange(0, len(r_edgeAMG)), r_edgeAMG, label='edge AMG')
    plt.semilogy(np.arange(0, len(r_None)), r_None, label='CG')
    plt.semilogy(np.arange(0, len(r_SA)), r_SA, label='CG + AMG')
    plt.legend()
    plt.show()
