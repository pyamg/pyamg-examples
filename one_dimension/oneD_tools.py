"""
For use with matplotlib and 1D problems solved with a multilevel method.
Routines here allow you to visualized aggregates, nullspace vectors
and columns of P.  This is possible on any level
"""
__docformat__ = "restructuredtext en"

__all__ = ['oneD_P_vis', 'oneD_coarse_grid_vis', 'oneD_profile']

import matplotlib.pyplot as plt
import numpy as np


def update_rcparams(fig_width_pt=700.0):
    '''
    Updates rcparams for appropriate plotting parameters

    parameters
    ----------
    fig_width_pt : {float}
        sets the size of the figure

    returns
    -------
    nothing, rcparams is updated

    examples
    --------
    >>> from numpy import linspace
    >>> from oneD_tools import update_rcparams
    >>> import matplotlib.pyplot as plt
    >>> update_rcparams(700.0)
    >>> plt.plot(linspace(0,10,10), linspace(0,10,10))
    >>> plt.title(' X = Y' )
    >>> plt.xlabel('X')
    >>> plt.ylabel('Y')
    >>> plt.show()
    '''

    inches_per_pt = 1.0 / 72.27               # Convert pt to inch
    golden_mean = (np.sqrt(5) - 1.0) / 2.0         # Aesthetic ratio
    fig_width = fig_width_pt * inches_per_pt  # width in inches
    fig_height = fig_width * golden_mean      # height in inches
    fig_size = [fig_width, fig_height]

    params = {'backend': 'ps',
              'axes.labelsize': 24,
              'axes.titlesize': 24,
              'legend.fontsize': 22,
              'xtick.labelsize': 22,
              'ytick.labelsize': 22,
              'text.usetex': True,
              'lines.linewidth': 2,
              'figure.figsize': fig_size}

    plt.rcParams.update(params)


def oneD_profile(mg, grid=None, x0=None, b=None, iter=1, cycle='V', fig_num=1):
    '''
    Profile mg on the problem defined by x0 and b.
    Default problem is x0=rand, b = 0.

    Parameters
    ----------
    mg : pyamg multilevel hierarchy
        Hierarchy to profile
    grid : array
        if None, default grid is assumed to be on [0,1]
    x0 : array
        initial guess to linear system, default is a random
    b : array
        right hand side to linear system, default is all zeros
        Note that if b is not all zeros and solution is not provided,
        A must be inverted in order to plot the error
    iter : int
        number of cycle iterations, default is 1
    cycle : {'V', 'W', 'F'}
        solve with a V, W or F cycle
    fig_num : int
        figure number from which to begin plotting

    Returns
    -------
    The residual ratio history are sent to the plotter.
    To see plots, type ">>> import matplotlib.pyplot as plt; plt.show()"

    Notes
    -----

    Examples
    --------
    >>> from pyamg import *
    >>> from oneD_tools import *
    >>> import matplotlib.pyplot as plt
    >>> from numpy import random, zeros
    >>> A = poisson( (128,), format='csr')
    >>> ml=smoothed_aggregation_solver(A, max_coarse=5)
    >>> oneD_profile(ml);                                         plt.show()
    >>> oneD_profile(ml, iter=3);                                 plt.show()
    >>> oneD_profile(ml, iter=3, cycle='W');                      plt.show()
    >>> oneD_profile(ml, b=random.rand(128,), x0=zeros((128,)), iter=5); plt.show()
    '''

    # use good plotting parameters
    update_rcparams()

    A = mg.levels[0].A
    ndof = mg.levels[0].A.shape[0]

    # Default regular grid on 0 to 1
    if grid is None:
        grid = np.linspace(0, 1, ndof)
    elif np.ravel(grid).shape[0] != ndof:
        raise ValueError("Grid must be of size %d" % ndof)

    # Default initial guess is random
    if x0 is None:
        x0 = np.random.rand(ndof,)
        if A.dtype == complex:
            x0 += 1.0j * np.random.rand(ndof,)
    elif np.ravel(x0).shape[0] != ndof:
        raise ValueError("Initial guess must be of size %d" % ndof)
    else:
        x0 = np.ravel(x0)

    # Default RHS is all zero
    if b is None:
        b = np.zeros((ndof,), dtype=A.dtype)
    elif np.ravel(b).shape[0] != ndof:
        raise ValueError("RHS must be of size %d" % ndof)
    else:
        b = np.ravel(b)

    # solve system with mg
    res = []
    guess = mg.solve(
        b,
        x0=x0,
        tol=1e-8,
        maxiter=iter,
        cycle=cycle,
        residuals=res)
    res = np.array(res)
    resratio = res[1:] / res[0:-1]
    r = b - A * guess
    print('Initial residual: ' + str(res[0]))
    print('Final residual: ' + str(np.linalg.norm(r)))

    # plot results
    if iter > 1:
        plt.figure(fig_num)
        plt.plot(np.array(range(1, resratio.shape[0] + 1)), resratio)
        plt.title('Residual Reduction Ratio History')
        plt.xlabel('Iteration')
        plt.ylabel(r'$||r_{i}|| / ||r_{i-1}||$')
        plt.xticks(np.array(range(1, resratio.shape[0] + 1)))


def oneD_coarse_grid_vis(mg, fig_num=1, level=0):
    '''
    Visualize the aggregates on level=level in terms of
    the aggregates' fine grid representation

    Parameters
    ----------
    mg : pyamg multilevel hierarchy
         visualize the components of mg
    fig_num : int
        figure number from which to begin plotting
    level : int
        level on which to visualize

    Returns
    -------
    A plot of the aggregates on level=level is sent to the plotter
    The aggregates are always interpolated to the finest level
    To see plots, type ">>> import matplotlib.pyplot as plt; plt.show()"

    Notes
    -----

    Examples
    --------
    >>>from pyamg import *
    >>>from oneD_tools import *
    >>>import matplotlib.pyplot as plt
    >>>A = poisson( (64,), format='csr')
    >>>ml=smoothed_aggregation_solver(A, max_coarse=5)
    >>>oneD_coarse_grid_vis(ml, level=0)
    >>>plt.show()
    >>>oneD_coarse_grid_vis(ml, level=1)
    >>>plt.show()

    '''

    update_rcparams()
    colors = ['b', 'r', 'g', 'k', 'c', 'm', 'y']

    if level > (len(mg.levels) - 2):
        raise ValueError("Level %d has no AggOp" % level)

    # Retrieve and map Aggregate to finest level
    ndof = mg.levels[0].A.shape[0]

    if not hasattr(mg.levels[level], 'AggOp'):
        raise ValueError(
            'AggOp needed in hierarchy.  Run the setup with the \'keep\' flag')

    AggOp = mg.levels[level].AggOp
    for i in range(level - 1, -1, -1):
        AggOp = mg.levels[i].AggOp * AggOp

    AggOp = AggOp.tocsc()

    # Default grid
    x = np.array(range(ndof))

    # Plot each aggregate
    plt.figure(fig_num)
    for i in range(AggOp.shape[1]):
        aggi = AggOp[:, i].indices
        plt.plot(x[aggi], i * np.ones((aggi.shape[0],)),
                 colors[np.mod(i, len(colors))],
                 marker='o', linewidth=2, markersize=12)

    title_string = 'Level ' + str(level) + ' Aggregates'
    if level != 0:
        title_string += '\nMapped to Finest Level'
    plt.title(title_string)
    plt.xlabel('DOF')
    plt.ylabel('Aggregate Number')
    plt.axis([min(x) - .05, max(x) + .05, -1, AggOp.shape[1]])


def oneD_P_vis(mg, fig_num=1, level=0, interp=False):
    '''
    Visualize the basis functions of P (i.e. columns) from level=level

    Parameters
    ----------
    mg : pyamg multilevel hierarchy
        visualize the components of mg
    fig_num : int
        figure number from which to begin plotting
    level : int
        level on which to visualize
    interp : {True, False}
        Should the columns of P be interpolated to the finest
        level before plotting? i.e., plot the columns of
        (P_1*P_2*...*P_level) or just columns of P_level

    Returns
    -------
    A plot of the columns of P on level=level is sent to the plotter
    To see plots, type ">>> import matplotlib.pyplot as plt; plt.show()"

    Notes
    -----
    These plots are only useful for small grids as all columns
    of P are actually printed

    Examples
    --------
    >>>from pyamg import *
    >>>from oneD_tools import *
    >>>import matplotlib.pyplot as plt
    >>>A = poisson( (32,), format='csr')
    >>>ml=smoothed_aggregation_solver(A, max_coarse=5)
    >>>oneD_P_vis(ml, level=0, interp=False)
    >>>plt.show()
    >>>oneD_P_vis(ml, level=1, interp=False)
    >>>plt.show()
    >>>oneD_P_vis(ml, level=1, interp=True)
    >>>plt.show()
    '''

    update_rcparams()
    colors = ['b', 'r', 'g', 'k', 'c', 'm', 'y']

    if level > (len(mg.levels) - 2):
        raise ValueError("Level %d has no P" % level)

    # Retrieve P from appropriate level
    if not interp:
        ndof = mg.levels[level].A.shape[0]
        P = mg.levels[level].P
    else:
        # Interpolate P to the finest level
        ndof = mg.levels[0].A.shape[0]
        P = mg.levels[level].P
        for i in range(level - 1, -1, -1):
            P = mg.levels[i].P * P

    blocks = P.blocksize[1]
    P = P.tocsc()

    # Default grid
    x = np.array(range(ndof))

    # Grab and plot each aggregate's part of a basis function together
    for i in range(0, P.shape[1], blocks):
        # extract aggregate i's basis functions
        p = P[:, i:(i + blocks)].todense()
        for j in range(blocks):
            plt.figure(fig_num + j)
            p2 = np.ravel(p[:, j])
            plt.plot(x[p2 != 0], p2[p2 != 0.0],
                     colors[np.mod(i, len(colors))],
                     marker='o', linewidth=2, markersize=12)
            title_string = (
                'Level ' +
                str(level) +
                '\nLocal Interp Fcn %d' %
                (j+1))
            if interp and (level != 0):
                title_string += '\nInterpolated to Finest Level'
            plt.title(title_string)
            plt.xlabel('DOF')
            plt.ylabel('Local Interp Fcn')
