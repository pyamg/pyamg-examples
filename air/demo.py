# AIR Example
import numpy as np
import pyamg
import sys
import matplotlib.pyplot as plt

# Create matrix and right-hand side, with inflow BCs enforced
# strongly and moved to the right-hand side.
nx = 500
ny = 500
theta = np.pi/6.0
A, b = pyamg.gallery.advection_2d((ny,nx), theta)

# Construct AIR solver
print('500 x 500 mesh:')
for dist in [1, 2]:
    for second_pass in [False, True]:
        if second_pass:
            if dist == 1:
                print('Distance-1 AIR using RS coarsening *with* second pass.')
            else:
                print('Distance-2 AIR using RS coarsening *with* second pass.')
        else:
            if dist == 1:
                print('Distance-1 AIR using RS coarsening *without* second pass.')
            else:
                print('Distance-2 AIR using RS coarsening *without* second pass.')

        # Specify restriction and coarsening
        restrict=('air', {'theta': 0.1, 'degree': dist})
        CF =('RS', {'second_pass': second_pass})
        ml = pyamg.air_solver(A, CF=CF, restrict=restrict)

        # Solve Ax=b
        residuals = []
        x = ml.solve(b, tol=1e-10, accel=None, residuals=residuals)
        conv = (residuals[-1]/residuals[0])**(1.0/(len(residuals)-1))
        print(f'\tLevels in hierarchy:        {len(ml.levels)}')
        print(f'\tOperator complexity:        {ml.operator_complexity()}')
        print(f'\tNumber of iterations:       {len(residuals)-1}')
        print(f'\tAverage convergence factor: {conv}\n')

nx = 50
ny = 50
theta = np.pi/6.0
A, b = pyamg.gallery.advection_2d((ny,nx), theta)
restrict=('air', {'theta': 0.1, 'degree': 1})
CF =('RS', {'second_pass': True})

ml = pyamg.air_solver(A, CF=CF, restrict=restrict)
xx = np.linspace(0,1,nx-1)
x,y = np.meshgrid(xx,xx)
V = np.concatenate([[x.ravel()],[y.ravel()]],axis=0).T
splitting = ml.levels[0].splitting
F = np.where(splitting == 1)[0]

fig, ax = plt.subplots()
ax.pcolormesh(x, y, splitting.reshape(x.shape), cmap='bone')

ax.axis('square')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_title('$50 \\times 50$ mesh')

figname = './output/splitting.png'
import sys
if len(sys.argv) > 1:
    if sys.argv[1] == '--savefig':
        plt.savefig(figname, bbox_inches='tight', dpi=150)
else:
    plt.show()
