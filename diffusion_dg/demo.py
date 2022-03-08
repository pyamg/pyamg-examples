"""
Test the convergence of a small diffusion problem discretized with the local
discontinuous Galerkin method.  The polynomial order is 5.  To utilize the
visualization capabilities, you need to have Paraview and scikits.delaunay
installed.

References
----------
[1] L. N. Olson and J. B. Schroder.  Smoothed Aggregation Multigrid Solvers for
High-Order Discontinuous Galerkin Methods.  Journal of Computational Physics.
Submitted 2010.

"""
import numpy as np
import pyamg
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
#from my_vis import shrink_elmts, my_vis

print("\nDiffusion problem discretized with p=5 and the local\n" +
      "discontinuous Galerkin method.")

# Discontinuous Galerkin Diffusion Problem
data = pyamg.gallery.load_example('local_disc_galerkin_diffusion')
A = data['A'].tocsr()
B = data['B']
elements = data['elements']
vertices = data['vertices']
np.random.seed(625)
x0 = np.random.rand(A.shape[0])
b = np.zeros_like(x0)

# For demonstration, show that a naive SA solver
# yields unsatisfactory convergence
smooth = 'jacobi'
strength = ('symmetric', {'theta': 0.1})
SA_solve_args = {'cycle': 'W', 'maxiter': 20, 'tol': 1e-8, 'accel': 'cg'}
SA_build_args = {
    'max_levels': 10,
    'max_coarse': 25,
    'coarse_solver': 'pinv2',
    'symmetry': 'hermitian',
    'keep': True}
presmoother = ('gauss_seidel', {'sweep': 'symmetric', 'iterations': 1})
postsmoother = ('gauss_seidel', {'sweep': 'symmetric', 'iterations': 1})

##
# Construct solver and solve
sa = pyamg.smoothed_aggregation_solver(
    A,
    B=B,
    smooth=smooth,
    strength=strength,
    presmoother=presmoother,
    postsmoother=postsmoother,
    **SA_build_args)
resvec = []
x = sa.solve(b, x0=x0, residuals=resvec, **SA_solve_args)
print("Observe that standard SA parameters for this p=5 discontinuous \n" +
      "Galerkin system yield an inefficient solver.\n")
for i, r in enumerate(resvec):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))

##
# Now, construct and solve with appropriate parameters
p = 5
improve_candidates = [
    ('block_gauss_seidel', {
        'sweep': 'symmetric', 'iterations': p}), ('gauss_seidel', {
            'sweep': 'symmetric', 'iterations': p})]
aggregate = ['naive', 'standard']
# the initial conforming aggregation step requires no prolongation
# smoothing
smooth = [None, ('energy', {'krylov': 'cg', 'maxiter': p})]
strength = [('distance',
             {'V': data['vertices'], 'theta':5e-5, 'relative_drop':False}),
            ('evolution',
             {'k': 4, 'proj_type': 'l2', 'epsilon': 2.0})]
sa = pyamg.smoothed_aggregation_solver(
    A,
    B=B,
    smooth=smooth,
    improve_candidates=improve_candidates,
    strength=strength,
    presmoother=presmoother,
    aggregate=aggregate,
    postsmoother=postsmoother,
    **SA_build_args)
resvec = []
x = sa.solve(b, x0=x0, residuals=resvec, **SA_solve_args)
print("\nNow use appropriate parameters, especially \'energy\' prolongation\n" +
      "smoothing and a distance based strength measure on level 0.  This\n" +
      "yields a much more efficient solver.\n")
for i, r in enumerate(resvec):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))

# generate visualization files
#elements2, vertices2 = shrink_elmts(elements, vertices)
#my_vis(sa, vertices2, error=x, fname="DG_Example_", E2V=elements2[:, 0:3])

print(sa)
# first shrink the elements
E = elements
m = E.shape[1]
Vs = np.zeros((m*E.shape[0], 2))
Es = np.zeros((E.shape[0], m), dtype=np.int32)
shrink = 0.75
k = 0
for i, e in enumerate(E):
    xy = vertices[e, :]
    xymean = xy.mean(axis=0)
    Vs[k:k+m,:] = shrink * xy + (1-shrink) * np.kron(xy.mean(axis=0), np.ones((m, 1)))
    Es[i,:] = np.arange(k, k+m)
    k += m

AggOp = sa.levels[0].AggOp
count = np.array(AggOp.sum(axis=0)).ravel()
Vc = AggOp.T @ vertices
Vc[:,0] /= count
Vc[:,1] /= count
I  = Es.ravel()
J = AggOp.indices[I]
Ec = J.reshape(Es.shape)

fig, ax = plt.subplots()
ax.triplot(Vs[:,0], Vs[:,1], Es[:,:3], lw=0.5)

for aggs in AggOp.T:
    I = aggs.indices
    if len(I) == 1:
        ax.plot(Vs[I,0], Vs[I,1], 'o', ms=5)
    if len(I) == 2:
        ax.plot(Vs[I,0], Vs[I,1], '-', lw=4, solid_capstyle='round')
    if len(I) > 2:
        patch = Polygon(Vs[I,:], False)
        ax.add_patch(patch)
ax.set_title('Level-0 aggregates')
ax.axis('square')
ax.axis('off')
figname = f'./output/dgaggs.png'
import sys
if '--savefig' in sys.argv:
    plt.savefig(figname, bbox_inches='tight', dpi=150)
else:
    plt.show()

fig, ax = plt.subplots()
B0 = sa.levels[1].B[:,0]
ax.tripcolor(Vc[:,0], Vc[:,1], B0, Ec, lw=1.5)
ax.set_title('Level-1 $B$')
ax.axis('square')
ax.axis('off')

figname = f'./output/dgmodes.png'
import sys
if '--savefig' in sys.argv:
    plt.savefig(figname, bbox_inches='tight', dpi=150)
else:
    plt.show()
