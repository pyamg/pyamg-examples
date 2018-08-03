"""
Simple example of one dimensional diffusion that makes use of
the included one dimensional visualization tools for a
stand-along SA solver.

Usage
-----
$ python oneD_diffusion.py  npts

"""
import numpy as np
import pyamg
import matplotlib.pyplot as plt
from oneD_tools import oneD_profile, oneD_P_vis, oneD_coarse_grid_vis
import sys

# Ensure repeatability of tests
np.random.seed(625)

# Generate system and solver
if len(sys.argv) < 2:
    n = 10
else:
    n = int(sys.argv[1])

# setup 1D Poisson problem
A = pyamg.gallery.poisson((n,), format='csr')
ml = pyamg.smoothed_aggregation_solver(
    A, max_coarse=5, coarse_solver='pinv2', keep=True)

# Profile this solver for 5 iterations
oneD_profile(ml, grid=np.linspace(0, 1, n), x0=np.random.rand(n,),
             b=np.zeros((n,)), iter=10)

# Plot the fine level's aggregates
oneD_coarse_grid_vis(ml, fig_num=20, level=0)

if True:
    # Only plot the basis functions in P if n is small, e.g. 20
    oneD_P_vis(ml, fig_num=30, level=0, interp=False)

plt.show()
