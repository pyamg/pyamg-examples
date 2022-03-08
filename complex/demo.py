"""
Test the convergence for a simple 100x100 Grid, Gauge Laplacian Matrix

For this problem, the matrix A is complex, but this isn't problematic,
because complex arithmetic is natively supported.  There is _no_
implicit conversion to an equivalent real system.

Usage: python demo.py --solver 1

"""
import sys
import numpy as np
import pyamg

n = 100

solvernum = 1
if '--solver' in sys.argv:
    i = sys.argv.index('--solver')
    solvernum = int(sys.argv[i+1])
else:
    print('Usage: python demo.py --solver N, with N=1 or 2.\n'
          'Test convergence for a simple 100 x 100 grid, Gauge Laplacian.\n'
          'Input Choice:\n'
          '1:  Run smoothed_aggregation_solver\n'
          '2:  Run rootnode_solver\n')
    sys.exit()
np.random.seed(625)
A = pyamg.gallery.gauge_laplacian(n, beta=0.001)
x = np.random.rand(A.shape[0]) + 1.0j * np.random.rand(A.shape[0])
b = np.random.rand(A.shape[0]) + 1.0j * np.random.rand(A.shape[0])

if solvernum == 1:
    ml = pyamg.smoothed_aggregation_solver(A, smooth='energy')
elif solvernum == 2:
    ml = pyamg.rootnode_solver(A, smooth='energy')
else:
    raise ValueError("Enter a choice of 1 or 2")

resvec = []
x = ml.solve(b, x0=x, maxiter=20, tol=1e-14, residuals=resvec)

for i, r in enumerate(resvec):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))

print(ml)
