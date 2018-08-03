"""PyAMG and Dolfin

This example uses Dolfin version 0.9.7 of the Fenics Project:
http://www.fenicsproject.org/
to construct a FE solution the Poisson problem on the Unit Square.

PyAMG is used to solve the resulting system.  Data is not copied when
constructing the scipy.sparse matrix

Steps:
    - Install fenics.  Using docker:

    docker run -ti -v $(pwd):/home/fenics/shared quay.io/fenicsproject/stable:latest

    - Install pyamg

    pip3 install pyamg --user

"""

import pyamg

############################################################
# Part I: Setup problem with Dolfin
try:
    import dolfin as dfn
except ImportError:
    raise ImportError('Problem with Dolfin Installation')

dfn.parameters['linear_algebra_backend'] = 'Eigen'

# Define mesh, function space
mesh = dfn.UnitSquareMesh(75, 35)
V = dfn.FunctionSpace(mesh, "CG", 1)

# Define basis and bilinear form
u = dfn.TrialFunction(V)
v = dfn.TestFunction(V)
a = dfn.dot(dfn.grad(v), dfn.grad(u)) * dfn.dx
f = dfn.Expression(
    '500.0 * exp(-(pow(x[0] - 0.5, 2) + pow(x[1] - 0.5, 2)) / 0.02)',
    degree=1)
L = v * f * dfn.dx

# Define Dirichlet boundary (x = 0 or x = 1)


class DirichletBoundary(dfn.SubDomain):
    def inside(self, x, on_boundary):
        return x[0] < dfn.DOLFIN_EPS or x[0] > 1.0 - dfn.DOLFIN_EPS


u0 = dfn.Constant(0.0)
bc = dfn.DirichletBC(V, u0, DirichletBoundary())

A, rhs = dfn.assemble_system(a, L, bcs=bc)
############################################################


############################################################
# Part II: Solve with PyAMG
Asp = dfn.as_backend_type(A).sparray()
b = dfn.as_backend_type(rhs).array_view()

ml = pyamg.smoothed_aggregation_solver(Asp, max_coarse=10)
residuals = []
x = ml.solve(b, tol=1e-10, accel='cg', residuals=residuals)

residuals = residuals / residuals[0]
print(ml)
############################################################


############################################################
# Part III: plot
# import matplotlib.pyplot as plt
# plt.figure(2)
# plt.semilogy(residuals)
# plt.show()
############################################################
