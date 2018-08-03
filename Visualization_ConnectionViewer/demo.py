# Import ConnectionViewer writers
# java -jar ~/Downloads/ConnectionViewer.jar test_A0.mat
import numpy as np
import pyamg

from cvoutput import outputML
from convergence_tools import print_cycle_history

##
# Run Rotated Anisotropic Diffusion
n = 10
nx = n
ny = n
stencil = pyamg.gallery.diffusion_stencil_2d(type='FE', epsilon=0.001, theta=np.pi / 3)
A = pyamg.gallery.stencil_grid(stencil, (nx, ny), format='csr')
np.random.seed(625)
x = np.random.rand(A.shape[0])
b = A * np.random.rand(A.shape[0])

ml = pyamg.rootnode_solver(A, strength=('evolution', {'epsilon': 2.0}),
                           smooth=('energy', {'degree': 2}), max_coarse=10)
resvec = []
x = ml.solve(b, x0=x, maxiter=20, tol=1e-14, residuals=resvec)
print_cycle_history(resvec, ml, verbose=True, plotting=False)

##
# Write ConnectionViewer files for multilevel hierarchy ml
xV, yV = np.meshgrid(
    np.arange(
        0, ny, dtype=float), np.arange(
            0, nx, dtype=float))
Verts = np.concatenate([[xV.ravel()], [yV.ravel()]], axis=0).T
outputML("test", Verts, ml)


print("\n\nOutput files for matrix stencil visualizations in ConnectionViewer are: \n  \
test_A*.mat \n  test_fine*.marks \n  test_coarse*.marks \n  \
test_R*.mat \n  test_P*.mat \nwhere \'*\' is the level number")
##
print("\n\nYou can download ConnectionViewer from \nhttp://gcsc.uni-frankfurt.de/Members/mrupp/connectionviewer/ \n\nWhen you open test_A0.mat with ConnectionViewer, you'll get")
##
print("\nIn ConnectionViewer, you can zoom in with the mousewheel\n \
and drag the grid around. By clicking on a node, you can see its\n \
matrix connections.")
