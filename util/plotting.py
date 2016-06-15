"""
Random plotting routines
"""

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.patches import Polygon


def plotmeshelements(V, E, ax=None, *args, **kwargs):
    """
    input
    -----
        V : rank 2 array
            list of verties
        E : rank 2 array
            list of triangle elements
        ax : current axes

    return
    ------
        pc : the patch collection

    notes
    -----
        args, kwargs are passed to matplotlib.pyplot.PatchCollection
    """

    if ax is None:
        ax = plt.gca()

    x = V[:, 0]
    y = V[:, 1]
    ax.set_xlim((x.min(), x.max()))
    ax.set_ylim((y.min(), y.max()))

    nel = E.shape[0]
    ps = [Polygon(V[E[i, :], :], *args, **kwargs) for i in range(nel)]

    if 'clip_on' not in kwargs:
        kwargs['clip_on'] = False

    ps = PatchCollection(ps, match_original=True, clip_on=False)
    pc = ax.add_collection(ps)
    ax.set_aspect('equal', adjustable='box')

    return pc


def plotmeshedges(V, E, ax=None, *args, **kwargs):
    """
    input
    -----
        V : rank 2 array
            list of verties
        E : rank 2 array
            list of edges
        ax : current axes

    return
    ------
        lc : the line collection

    notes
    -----
        args, kwargs are passed to matplotlib.pyplot.LineCollection
    """

    if ax is None:
        ax = plt.gca()

    x = V[:, 0]
    y = V[:, 1]
    ax.set_xlim((x.min(), x.max()))
    ax.set_ylim((y.min(), y.max()))

    xstart = x[E[:, 0]]
    ystart = y[E[:, 0]]
    xend = x[E[:, 1]]
    yend = y[E[:, 1]]
    ls = []

    for i in range(len(xstart)):
        ls.append([(xstart[i], ystart[i]), (xend[i], yend[i])])

    if 'clip_on' not in kwargs:
        kwargs['clip_on'] = False

    ls = LineCollection(ls, *args, **kwargs)
    lc = ax.add_collection(ls)
    ax.set_aspect('equal', adjustable='box')

    return lc

if __name__ == '__main__':
    from scipy.io import loadmat
    import numpy as np
    d = loadmat('square.mat')
    A = d['A'].tocoo()
    V = d['vertices']
    Elmts = d['elements']
    Edges = np.vstack((A.row, A.col)).T

    f, ax = plt.subplots(1)
    lc = plotmeshedges(V, Edges, ax=ax, colors=('r'), linewidth=2)
    ax.set_title('test')

    f, ax2 = plt.subplots(1)
    lc = plotmeshelements(V, Elmts, ax=ax2, linewidth=2, ec='g', fc='w')
    ax.set_title('test')

    plt.show()
