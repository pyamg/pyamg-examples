"""
Test the convergence for a simple 100x100 Grid, Gauge Laplacian Matrix

For this problem, the matrix A is complex, but this isn't problematic,
because complex arithmetic is natively supported.  There is _no_
implicit conversion to an equivalent real system.

"""
import numpy as np
import pyamg
from convergence_tools import print_cycle_history

n = 100

print("Test convergence for a simple 100x100 Grid, Gauge Laplacian")
choice = input('\n Input Choice:\n' +
               '1:  Run smoothed_aggregation_solver\n' +
               '2:  Run rootnode_solver\n')

np.random.seed(625)
A = pyamg.gallery.gauge_laplacian(n, beta=0.001)
x = np.random.rand(A.shape[0]) + 1.0j * np.random.rand(A.shape[0])
b = np.random.rand(A.shape[0]) + 1.0j * np.random.rand(A.shape[0])

choice = int(choice)

if choice == 1:
    ml = pyamg.smoothed_aggregation_solver(A, smooth='energy')
elif choice == 2:
    ml = pyamg.rootnode_solver(A, smooth='energy')
else:
    raise ValueError("Enter a choice of 1 or 2")

resvec = []
x = ml.solve(b, x0=x, maxiter=20, tol=1e-14, residuals=resvec)

for i, r in enumerate(resvec):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))
