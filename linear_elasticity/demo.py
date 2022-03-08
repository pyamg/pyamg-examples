# Linear Elasticity Example

import numpy as np
import pyamg
import sys

solvernum = 1
if '--solver' in sys.argv:
    i = sys.argv.index('--solver')
    solvernum = int(sys.argv[i+1])
else:
    print('Usage: python demo.py --solver N, with N=1 or 2.\n'
          'Test convergence for a 200x200 Grid, Linearized Elasticity Problem\n'
          'Input Choice:\n'
          '1:  Run smoothed_aggregation_solver\n'
          '2:  Run rootnode_solver\n')
    sys.exit()

# Create matrix and candidate vectors.  B has 3 columns, representing
# rigid body modes of the mesh. B[:,0] and B[:,1] are translations in
# the X and Y directions while B[:,2] is a rotation.
A, B = pyamg.gallery.linear_elasticity((200, 200), format='bsr')

# Construct solver using AMG based on Smoothed Aggregation (SA)
if solvernum == 1:
    ml = pyamg.smoothed_aggregation_solver(A, B=B, smooth='energy')
elif solvernum == 2:
    ml = pyamg.rootnode_solver(A, B=B, smooth='energy')
else:
    raise ValueError("Enter a solver of 1 or 2")

# Display hierarchy information
print(ml)

# Create random right hand side
b = np.random.rand(A.shape[0], 1)

# Solve Ax=b
residuals = []
x = ml.solve(b, tol=1e-10, residuals=residuals)
print("Number of iterations:  {}d\n".format(len(residuals)))

# Output convergence
for i, r in enumerate(residuals):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))
