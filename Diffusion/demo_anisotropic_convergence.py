"""
Test the convergence of a 100x100 anisotropic diffusion equation
"""
import numpy as np
import pyamg

n = 100
nx = n
ny = n

# Rotated Anisotropic Diffusion
stencil = pyamg.gallery.diffusion_stencil_2d(
    type='FE', epsilon=0.001, theta=np.pi / 3)

A = pyamg.gallery.stencil_grid(stencil, (nx, ny), format='csr')
S = pyamg.strength.classical_strength_of_connection(A, 0.0)

np.random.seed(625)
x = np.random.rand(A.shape[0])
b = A * np.random.rand(A.shape[0])

ml = pyamg.ruge_stuben_solver(A, max_coarse=10)

resvec = []
x = ml.solve(b, x0=x, maxiter=20, tol=1e-14, residuals=resvec)

for i, r in enumerate(resvec):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))
