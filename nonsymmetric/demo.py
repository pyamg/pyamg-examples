"""
Test the convergence of a small recirculating flow problem that generates a
nonsymmetric matrix

Usage: python demo.py --solver 1
"""

import sys
import numpy as np
import pyamg

solvernum = 1
if '--solver' in sys.argv:
    i = sys.argv.index('--solver')
    solvernum = int(sys.argv[i+1])
else:
    print('Usage: python demo.py --solver N, with N=1 or 2.\n'
          'Test convergence of a small recirculating flow problem '
          'that generates a nonsymmetric matrix n'
          'Input Choice:\n'
          '1:  Run smoothed_aggregation_solver\n'
          '2:  Run rootnode_solver\n')
    sys.exit()

# Recirculating flow, nonsymmetric matrix
data = pyamg.gallery.load_example('recirc_flow')
A = data['A'].tocsr()
B = data['B']
elements = data['elements']
vertice = data['vertices']

np.random.seed(625)
x0 = np.random.rand(A.shape[0])
b = A * np.random.rand(A.shape[0])

# For demonstration, show that a solver constructed for a symmetric
# operator fails for this matrix.
smooth = ('energy', {'krylov': 'cg'})
SA_build_args = {
    'max_levels': 10,
    'max_coarse': 25,
    'coarse_solver': 'pinv2',
    'symmetry': 'hermitian'}
SA_solve_args = {'cycle': 'V', 'maxiter': 15, 'tol': 1e-8}
strength = [('evolution', {'k': 2, 'epsilon': 4.0})]
presmoother = ('gauss_seidel', {'sweep': 'symmetric', 'iterations': 1})
postsmoother = ('gauss_seidel', {'sweep': 'symmetric', 'iterations': 1})

##
# Construct solver and solve
if solvernum == 1:
    sa_symmetric = pyamg.smoothed_aggregation_solver(
        A,
        B=B,
        smooth=smooth,
        strength=strength,
        presmoother=presmoother,
        postsmoother=postsmoother,
        **SA_build_args)
elif solvernum == 2:
    sa_symmetric = pyamg.rootnode_solver(
        A,
        B=B,
        smooth=smooth,
        strength=strength,
        presmoother=presmoother,
        postsmoother=postsmoother,
        **SA_build_args)
else:
    raise ValueError("Enter a solver of 1 or 2")

sa_symmetric = pyamg.smoothed_aggregation_solver(
    A,
    B=B,
    smooth=smooth,
    strength=strength,
    presmoother=presmoother,
    postsmoother=postsmoother,
    **SA_build_args)
resvec = []
x = sa_symmetric.solve(b, x0=x0, residuals=resvec, **SA_solve_args)
print("\nObserve that standard multigrid parameters for Hermitian systems\n" +
      "yield a nonconvergent stand-alone solver.\n")
for i, r in enumerate(resvec):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))

# Now, construct and solve with nonsymmetric SA parameters
smooth = ('energy', {'krylov': 'gmres', 'degree': 2})
SA_build_args['symmetry'] = 'nonsymmetric'
strength = [('evolution', {'k': 2, 'epsilon': 1.5})]
presmoother = ('gauss_seidel_nr', {'sweep': 'symmetric', 'iterations': 1})
postsmoother = ('gauss_seidel_nr', {'sweep': 'symmetric', 'iterations': 1})
improve_candidates = [
    ('gauss_seidel_nr', {
        'sweep': 'symmetric', 'iterations': 4}), None]

# Construct solver and solve
if solvernum == 1:
    sa_nonsymmetric = pyamg.smoothed_aggregation_solver(
        A,
        B=B,
        smooth=smooth,
        strength=strength,
        presmoother=presmoother,
        postsmoother=postsmoother,
        improve_candidates=improve_candidates,
        **SA_build_args)
elif solvernum == 2:
    sa_nonsymmetric = pyamg.rootnode_solver(
        A,
        B=B,
        smooth=smooth,
        strength=strength,
        presmoother=presmoother,
        postsmoother=postsmoother,
        improve_candidates=improve_candidates,
        **SA_build_args)
else:
    raise ValueError("Enter a solver of 1 or 2")

resvec = []
x = sa_nonsymmetric.solve(b, x0=x0, residuals=resvec, **SA_solve_args)
print("*************************************************************")
print("Now using nonsymmetric parameters for multigrid , we obtain a\n" +
      "convergent stand-alone solver. \n")
for i, r in enumerate(resvec):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))

##
# Now, we accelerate GMRES with the nonsymmetric solver to obtain
# a more efficient solver
SA_solve_args['accel'] = 'gmres'
resvec = []
x = sa_nonsymmetric.solve(b, x0=x0, residuals=resvec, **SA_solve_args)
print("*************************************************************")
print("Now, we use the nonsymmetric solver to accelerate GMRES. \n")
for i, r in enumerate(resvec):
    print("residual at iteration {0:2}: {1:^6.2e}".format(i, r))
