# Linear Elasticity Example

import numpy as np
import pyamg

print("Test convergence for a 200x200 Grid, Linearized Elasticity Problem")
choice = input('\n Input Choice:\n' +
               '1:  Run smoothed_aggregation_solver\n' +
               '2:  Run rootnode_solver\n')

# Create matrix and candidate vectors.  B has 3 columns, representing
# rigid body modes of the mesh. B[:,0] and B[:,1] are translations in
# the X and Y directions while B[:,2] is a rotation.
A, B = pyamg.gallery.linear_elasticity((200, 200), format='bsr')

# Construct solver using AMG based on Smoothed Aggregation (SA)
choice = int(choice)
if choice == 1:
    ml = pyamg.smoothed_aggregation_solver(A, B=B, smooth='energy')
elif choice == 2:
    ml = pyamg.rootnode_solver(A, B=B, smooth='energy')
else:
    raise ValueError("Enter a choice of 1 or 2")

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
