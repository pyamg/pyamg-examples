"""
Test the scalability of AMG for the anisotropic diffusion equation
"""
import numpy as np
import pyamg

nlist = [100, 200, 300, 400, 500, 600]

factors = np.zeros((len(nlist), 1)).ravel()
complexity = np.zeros((len(nlist), 1)).ravel()
nnz = np.zeros((len(nlist), 1)).ravel()
sizelist = np.zeros((len(nlist), 1)).ravel()
run = 0

for n in nlist:
    nx = n
    ny = n
    print("n = %-10d of %-10d" % (n, nlist[-1]))

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
    x = ml.solve(b, x0=x, maxiter=200, tol=1e-8, residuals=resvec)
    factors[run] = (resvec[-1] / resvec[0])**(1.0 / len(resvec))
    complexity[run] = ml.operator_complexity()
    nnz[run] = A.nnz
    sizelist[run] = A.shape[0]
    run += 1

print("{:^9s} | {:^9s} | {:^9s} | {:^9s} | {:^9s}".format(
    "n", "nnz", "rho", "OpCx", "Work"))
print("--------------------------------------------------------")
for i, n in enumerate(sizelist):
    print("{:^9d} | {:^9d} | {:^9.2g} | {:^9.2g} | {:^9.2g}".format(
        int(n), int(nnz[i]), factors[i], complexity[i],
        complexity[i] / np.log10(factors[i])))
