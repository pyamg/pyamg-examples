"""
Test the scalability of SA for rotated diffusion while
highlighting the performance of different strength measures.
Try different values for classic_theta and evolution_theta.
"""
import numpy as np

import pyamg

# Ensure repeatability of tests
np.random.seed(625)

# Grid sizes to test
nlist = [100, 200, 300, 400]

factors_classic = np.zeros((len(nlist),))
complexity_classic = np.zeros((len(nlist),))
nnz_classic = np.zeros((len(nlist),))
sizelist_classic = np.zeros((len(nlist),))

factors_evo = np.zeros((len(nlist),))
complexity_evo = np.zeros((len(nlist),))
nnz_evo = np.zeros((len(nlist),))
sizelist_evo = np.zeros((len(nlist),))

factors_evo_root = np.zeros((len(nlist),))
complexity_evo_root = np.zeros((len(nlist),))
nnz_evo_root = np.zeros((len(nlist),))
sizelist_evo_root = np.zeros((len(nlist),))

run = 0

# Smoothed Aggregation Parameters
theta = np.pi / 8.0                                # Angle of rotation
epsilon = 0.001                                     # Anisotropic coefficient
mcoarse = 10                                        # Max coarse grid size
prepost = ('gauss_seidel',                          # pre/post smoother
           {'sweep': 'symmetric', 'iterations': 1})
smooth = ('energy', {'maxiter': 9, 'degree': 3})    # Prolongation Smoother
classic_theta = 0.0                                 # Classic Strength Measure
#    Drop Tolerance
# evolution Strength Measure
evolution_theta = 4.0
#    Drop Tolerance

for n in nlist:
    nx = n
    ny = n
    print("Running Grid = (%d x %d)" % (nx, ny))

    # Rotated Anisotropic Diffusion Operator
    stencil = pyamg.gallery.diffusion_stencil_2d(type='FE', epsilon=epsilon, theta=theta)
    A = pyamg.gallery.stencil_grid(stencil, (nx, ny), format='csr')

    # Random initial guess, zero RHS
    x0 = np.random.rand(A.shape[0])
    b = np.zeros((A.shape[0],))

    # Classic SA strength measure
    ml = pyamg.smoothed_aggregation_solver(A,
                                           max_coarse=mcoarse,
                                           coarse_solver='pinv2',
                                           presmoother=prepost,
                                           postsmoother=prepost,
                                           smooth=smooth,
                                           strength=('symmetric', {'theta': classic_theta}))
    resvec = []
    x = ml.solve(b, x0=x0, maxiter=100, tol=1e-8, residuals=resvec)
    factors_classic[run] = (resvec[-1] / resvec[0])**(1.0 / len(resvec))
    complexity_classic[run] = ml.operator_complexity()
    nnz_classic[run] = A.nnz
    sizelist_classic[run] = A.shape[0]

    # Evolution strength measure
    ml = pyamg.smoothed_aggregation_solver(A,
                                           max_coarse=mcoarse,
                                           coarse_solver='pinv2',
                                           presmoother=prepost,
                                           postsmoother=prepost,
                                           smooth=smooth,
                                           strength=('evolution', {'epsilon': evolution_theta, 'k': 2}))
    resvec = []
    x = ml.solve(b, x0=x0, maxiter=100, tol=1e-8, residuals=resvec)
    factors_evo[run] = (resvec[-1] / resvec[0])**(1.0 / len(resvec))
    complexity_evo[run] = ml.operator_complexity()
    nnz_evo[run] = A.nnz
    sizelist_evo[run] = A.shape[0]

    # Evolution strength measure
    ml = pyamg.rootnode_solver(A,
                               max_coarse=mcoarse,
                               coarse_solver='pinv2',
                               presmoother=prepost,
                               postsmoother=prepost,
                               smooth=smooth,
                               strength=('evolution', {'epsilon': evolution_theta, 'k': 2}))
    resvec = []
    x = ml.solve(b, x0=x0, maxiter=100, tol=1e-8, residuals=resvec)
    factors_evo_root[run] = (resvec[-1] / resvec[0])**(1.0 / len(resvec))
    complexity_evo_root[run] = ml.operator_complexity()
    nnz_evo_root[run] = A.nnz
    sizelist_evo_root[run] = A.shape[0]

    run += 1

# Print Problem Description
print("\nAMG Scalability Study for Ax = 0, x_init = rand\n")
print("Emphasis on Robustness of Evolution Strength ")
print("Measure and Root-Node Solver\n")
print("Rotated Anisotropic Diffusion in 2D")
print("Anisotropic Coefficient = %1.3e" % epsilon)
print("Rotation Angle = %1.3f" % theta)

# Print Tables
print("{:^9s} | {:^9s} | {:^9s} | {:^9s} | {:^9s}".format(
    "n", "nnz", "rho", "OpCx", "Work"))
print("--------------------------------------------------------")
print(" Classic strength ")
print("--------------------------------------------------------")
for i, n in enumerate(sizelist_classic):
    print("{:^9d} | {:^9d} | {:^9.2g} | {:^9.2g} | {:^9.2g}".format(
        int(n), int(nnz_classic[i]), factors_classic[i], complexity_classic[i],
        complexity_classic[i] / abs(np.log10(factors_classic[i]))))
print("--------------------------------------------------------")
print(" Evolution strength ")
print("--------------------------------------------------------")
for i, n in enumerate(sizelist_evo):
    print("{:^9d} | {:^9d} | {:^9.2g} | {:^9.2g} | {:^9.2g}".format(
        int(n), int(nnz_evo[i]), factors_evo[i], complexity_evo[i],
        complexity_evo[i] / abs(np.log10(factors_evo[i]))))
print("--------------------------------------------------------")
print(" Evolution strength with Rootnode ")
print("--------------------------------------------------------")
for i, n in enumerate(sizelist_evo_root):
    print("{:^9d} | {:^9d} | {:^9.2g} | {:^9.2g} | {:^9.2g}".format(
        int(n), int(nnz_evo_root[i]), factors_evo_root[i], complexity_evo_root[i],
        complexity_evo_root[i] / abs(np.log10(factors_evo_root[i]))))
