"""
2D Helmholz Problem
"""
import numpy as np
import pyamg
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

from smoothed_aggregation_helmholtz_solver import smoothed_aggregation_helmholtz_solver, planewaves

# Retrieve 2-D Helmholtz Operator and problem data.
# This is operator was discretized with a local
# discontinuous Galerkin method.
data = pyamg.gallery.load_example('helmholtz_2D')
A = data['A'].tocsr()
omega = data['omega']
h = data['h']
ppw = data['ppw']
elements = data['elements']
vertices = data['vertices']

print("\nRunning 2D Helmholtz Example")
print("-- %1.2f Points-per-wavelength" % ppw)
print("-- %1.2e = h,  %1.2f = omega" % (h, omega))
print("-- Discretized with a local discontinuous Galerkin method\n   on annulus-shaped domain")

# random initial guess for zero right-hand-side
np.random.seed(625)
x0 = np.random.rand(A.shape[0])
b = np.zeros_like(x0)

# Use constant in B for interpolation at all levels
use_constant = (True, {'last_level': 10})

# Strength -- For level 0, aggregate based on distance so that only algebraic
# neighbors at the same spatial location are aggregated together.  For all
# coarse levels, all algebraic connections are considered strong.
strength = [('distance', {'V': vertices, 'theta': 1e-5, 'relative_drop': False}),
            ('symmetric', {'theta': 0.00})]

# Prolongator smoother
smooth = ('energy', {'krylov': 'cgnr', 'weighting': 'diagonal'})

# Aggregation -- non-standard 'naive' aggregation is done on level 0 so that
# only algebraic neighbors at the same spatial location are aggregated
# together.
aggregate = ['naive', 'standard']

# Note the matrix is complex-symmetric, not Hermitian, i.e. symmetry =
# 'symmetric'.
SA_build_args = {
    'max_levels': 10,
    'max_coarse': 50,
    'coarse_solver': 'pinv2',
    'symmetry': 'symmetric'}
SA_solve_args = {
    'cycle': 'W',
    'maxiter': 20,
    'tol': 1e-8,
    'accel': 'gmres'}

# Pre- and post-smoothers -- gauss_seidel is an acceptable relaxation method
# for resolved Helmholtz problems
smoother = [('gauss_seidel', {'iterations': 4, 'sweep': 'forward'}),
            ('gauss_seidel_nr', {'iterations': 4, 'sweep': 'forward'})]

# improve_candidates[k] -- stipulates the relaxation method on level k
# used to "improve" B
improve_candidates = [
    ('gauss_seidel', {'iterations': 2, 'sweep': 'forward'}),
    ('gauss_seidel_nr', {'iterations': 1, 'sweep': 'forward'})]

# Construct solver using the "naive" constant mode for B
sa = smoothed_aggregation_helmholtz_solver(A,
                                           planewaves=[None],
                                           use_constant=use_constant,
                                           strength=strength,
                                           smooth=smooth,
                                           aggregate=aggregate,
                                           improve_candidates=improve_candidates,
                                           presmoother=smoother,
                                           postsmoother=smoother,
                                           **SA_build_args)

# Solve
residuals = []
x = sa.solve(b, x0=x0, residuals=residuals, **SA_solve_args)

print("Using only a constant mode for interpolation yields an inefficient solver.")
print("This is due to aliasing oscillatory, but algebraically smooth, modes on the coarse levels.")
for i, r in enumerate(residuals):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))

# Now run a solver that introduces planewaves
# Setup planewave parameters, such that planewaves[k] defines which planewaves
# to introduce at level[k].  The final entry of None stipulates to introduce no
# new planewaves from that level on down.
X = vertices[:, 0].copy()
Y = vertices[:, 1].copy()
pwave_args = [None,
              (planewaves, {'X': X, 'Y': Y, 'omega': omega,
                            'angles': list(np.linspace(0., np.pi / 2., 2))}),
              (planewaves, {'X': X, 'Y': Y, 'omega': omega,
                            'angles': list(np.linspace(-np.pi / 8., 5 * np.pi / 8., 4))}),
              None]

##
# Use constant in B for interpolation, but only between levels 0 and 1
use_constant = (True, {'last_level': 0})

# Construct solver using planewaves
sa = smoothed_aggregation_helmholtz_solver(
    A,
    planewaves=pwave_args,
    use_constant=use_constant,
    strength=strength,
    smooth=smooth,
    aggregate=aggregate,
    improve_candidates=improve_candidates,
    presmoother=smoother,
    postsmoother=smoother,
    **SA_build_args)

# Solve
residuals = []
x = sa.solve(b, x0=x0, residuals=residuals, **SA_solve_args)
print("Note the improved performance from using planewaves in B.")
for i, r in enumerate(residuals):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))

#elements2, vertices2 = shrink_elmts(elements, vertices)
#my_vis(sa, vertices2, error=abs(x), fname='helmholtz_', E2V=elements2)

print(sa)
# first shrink the elements
E = elements
Vs = np.zeros((3*E.shape[0], 3))
shrink = 0.75
for i, e in enumerate(E):
    xy = vertices[e, :]
    xymean = xy.mean(axis=0)
    Vs[e,:] = shrink * xy + (1-shrink) * np.kron(xy.mean(axis=0), np.ones((3, 1)))

AggOp = sa.levels[0].AggOp
count = np.array(AggOp.sum(axis=0)).ravel()
Vc = AggOp.T @ vertices
Vc[:,0] /= count
Vc[:,1] /= count
I  = E.ravel()
J = AggOp.indices[I]
Ec = J.reshape(E.shape)

fig, ax = plt.subplots()
ax.triplot(Vs[:,0], Vs[:,1], E, lw=0.5)

from cycler import cycler
for aggs in AggOp.T:
    I = aggs.indices
    ax.plot(Vs[I,0], Vs[I,1], 'o', ms=2)
ax.set_title('Level-0 aggregates')
ax.axis('square')
ax.axis('off')
figname = f'./output/helmholtz2dagg.png'
import sys
if '--savefig' in sys.argv:
    plt.savefig(figname, bbox_inches='tight', dpi=150)
else:
    plt.show()

fig, axs = plt.subplots(nrows=2, ncols=2)
for i, ax in enumerate(axs.ravel()):
    B0 = sa.levels[1].B[:,i]
    ax.tripcolor(Vc[:,0], Vc[:,1], B0.real, Ec, lw=1.5)
    ax.set_title(f'Level-1 $B_{i}$')
    ax.axis('square')
    ax.axis('off')

figname = f'./output/helmholtz2dB.png'
import sys
if '--savefig' in sys.argv:
    plt.savefig(figname, bbox_inches='tight', dpi=150)
else:
    plt.show()
