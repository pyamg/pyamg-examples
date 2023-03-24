# AIR Example
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
for dist in [1, 2]:
    for second_pass in [False, True]:
        if second_pass:
            if dist == 1:
                print("Distance-1 AIR using RS coarsening *with* second pass.")
            else:
                print("Distance-2 AIR using RS coarsening *with* second pass.")
        else:
            if dist == 1:
                print("Distance-1 AIR using RS coarsening *without* second pass.")
            else:
                print("Distance-2 AIR using RS coarsening *without* second pass.")

        # Specify restriction and coarsening
        restrict=('air', {'theta': 0.1, 'degree': dist})
        CF =('RS', {'second_pass': second_pass})
        ml = pyamg.air_solver(A, CF=CF, restrict=restrict)

        # Solve Ax=b
        residuals = []
        x = ml.solve(b, tol=1e-10, accel=None, residuals=residuals)
        conv = (residuals[-1]/residuals[0])**(1.0/(len(residuals)-1))
        print("\tLevels in hierarchy:        {}".format(len(ml.levels)))
        print("\tOperator complexity:        {}".format(ml.operator_complexity()))
        print("\tNumber of iterations:       {}".format(len(residuals)-1))
        print("\tAverage convergence factor: {}\n".format(conv))
