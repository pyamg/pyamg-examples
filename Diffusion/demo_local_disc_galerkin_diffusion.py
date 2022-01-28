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
from my_vis import shrink_elmts, my_vis

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
print("*************************************************************")
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
print("*************************************************************")
print("Now use appropriate parameters, especially \'energy\' prolongation\n" +
      "smoothing and a distance based strength measure on level 0.  This\n" +
      "yields a much more efficient solver.\n")
for i, r in enumerate(resvec):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))

# generate visualization files
print("*************************************************************")
print("Generating visualization files in .vtu format for use with Paraview.")
s = """All values from coarse levels are interpolated using the aggregates,
i.e., there is no fixed geometric hierarchy.  Additionally, the mesh
has been artificially shrunk towards each element's barycenter, in order
to highlight the discontinuous nature of the discretization.

-- Near null-space mode from level * is in the file
   DG_Example_B_variable0_lvl*.vtu
-- Aggregtes from level * are in the two file
   DG_Example_aggs_lvl*_point-aggs,  and
   DG_Example_aggs_lvl*_aggs.vtu
-- The mesh from from level * is in the file
   DG_Example_mesh_lvl*.vtu
-- The error is in file
   DG_Example_error_variable0.vtu
"""
print(s)

elements2, vertices2 = shrink_elmts(elements, vertices)
my_vis(sa, vertices2, error=x, fname="DG_Example_", E2V=elements2[:, 0:3])
