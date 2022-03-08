"""
Simple example of one dimensional diffusion that makes use of
the included one dimensional visualization tools for a
stand-along SA solver.
"""
import numpy as np
import pyamg
import matplotlib.pyplot as plt
from oneD_tools import oneD_profile, oneD_P_vis, oneD_coarse_grid_vis
import sys

# Ensure repeatability of tests
np.random.seed(625)

n = 10

# setup 1D Poisson problem
A = pyamg.gallery.poisson((n,), format='csr')
ml = pyamg.smoothed_aggregation_solver(
    A, max_coarse=5, coarse_solver='pinv2', keep=True)

fig1, ax1 = plt.subplots()
# Profile this solver for 5 iterations
oneD_profile(ml, grid=np.linspace(0, 1, n), x0=np.random.rand(n,),
             b=np.zeros((n,)), iter=10, ax=ax1)

fig2, ax2 = plt.subplots()
# Plot the fine level's aggregates
oneD_coarse_grid_vis(ml, fig_num=20, level=0, ax=ax2)

fig3, ax3 = plt.subplots()
# Only plot the basis functions in P if n is small, e.g. 20
oneD_P_vis(ml, fig_num=30, level=0, interp=False, ax=ax3)

figname = './output/one_dimension_aggregates.png'
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == '--savefig':
        fig3.savefig(figname, bbox_inches='tight', dpi=150)
else:
    fig1.show()
    fig2.show()
    fig3.show()
