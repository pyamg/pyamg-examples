# Linear Elasticity Example

import numpy as np
import pyamg
import sys

# Create matrix and right-hand side, with inflow BCs enforced
# strongly and moved to the right-hand side. 
nx = 500
ny = 500
theta = np.pi/6.0
A, b = pyamg.gallery.advection_2d((ny,nx), theta)

# Construct AIR solver
for second_pass in [False, True]:
    if second_pass:
        print("AIR using RS coarsening *with* second pass.\n")
    else:
        print("AIR using RS coarsening *without* second pass.\n")

    CF=('RS', {'second_pass': second_pass})
    ml = pyamg.air_solver(A, CF=CF)

    # Display hierarchy information
    print(ml)

    # Solve Ax=b
    residuals = []
    x = ml.solve(b, tol=1e-10, accel=None, residuals=residuals)
    conv = (residuals[-1]/residuals[0])**(1.0/(len(residuals)-1))
    print("Number of iterations:       {}\n".format(len(residuals)-1))
    print("Average convergence factor: {}\n".format(conv))
