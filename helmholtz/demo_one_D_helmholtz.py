import numpy as np
import scipy.linalg as sla
import matplotlib.pyplot as plt
import pyamg

from one_D_helmholtz import one_D_helmholtz

# Problem parameters
h = 1024
mesh_h = 1.0 / (float(h) - 1.0)
points_per_wavelength = 15.0

# Retrieve 1-D Helmholtz Operator
omega = (2 * np.pi) / (mesh_h * points_per_wavelength)
data = one_D_helmholtz(h, omega=omega, nplane_waves=2)
A = data['A']
B = data['B']
vertices = data['vertices']
np.random.seed(625)
x0 = np.random.rand(A.shape[0])
b = np.zeros_like(x0)

# Solver Parameters
# Note: the matrix is complex-symmetric, not Hermitian. symmetry = 'symmetric'.
smooth = ('energy', {'krylov': 'gmres'})
SA_solve_args = {'cycle': 'W', 'maxiter': 20,
                 'tol': 1e-8, 'accel': 'gmres'}
SA_build_args = {'max_levels': 10, 'max_coarse': 5, 'coarse_solver': 'pinv2',
                 'symmetry': 'symmetric'}
smoother = ('gauss_seidel_nr', {'sweep': 'symmetric', 'iterations': 1})

# Construct solver using the "naive" constant mode for B
sa = pyamg.smoothed_aggregation_solver(A,
                                       B=np.ones((A.shape[0], 1)),
                                       strength=('symmetric', {'theta': 0.0}),
                                       presmoother=smoother,
                                       postsmoother=smoother,
                                       smooth=smooth,
                                       **SA_build_args)

# Solve
residuals = []
x = sa.solve(b, x0=x0, residuals=residuals, **SA_solve_args)

print("*************************************************************")
print("A single constant mode for interpolation is an inefficient.")
for i, r in enumerate(residuals):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))

# Construct solver using the wave-like modes for B
sa = pyamg.smoothed_aggregation_solver(A,
                                       B=B,
                                       strength=('symmetric', {'theta': 0.0}),
                                       presmoother=smoother,
                                       postsmoother=smoother,
                                       smooth=smooth,
                                       **SA_build_args)

# Solve
residuals = []
x = sa.solve(b, x0=x0, residuals=residuals, **SA_solve_args)

print("*************************************************************")
print("The performance improves with wave-like interpolation.")
for i, r in enumerate(residuals):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))

# plot B vs. the lowest right singular vector, which represents
# the near null-space, for a segment of the domain
f, ax = plt.subplots(1, 1)
indys = np.arange(0, min(75, h))
line_styles = ["-b", "--m", ":k"]
for i in range(B.shape[1]):
    plt.plot(vertices[indys, 0], np.real(B[indys, i]),
             line_styles[i], label='NNS Mode {}'.format(i))

[U, S, V] = sla.svd(A.todense())
V = V.T.copy()
scale = 0.9 / max(np.real(V[indys, -1]))
plt.plot(vertices[indys, 0], scale * np.real(np.ravel(V[indys, -1])),
         line_styles[i + 1], label='Re$(\\nu)$')

plt.title('Near Null-Space (NNS) vs. Lowest Right Singular Vector $\\nu$')
plt.legend(framealpha=1.0)
plt.show()
