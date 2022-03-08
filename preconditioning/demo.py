# Examples of AMG as a preconditioner

import sys
import numpy as np
import pyamg
import matplotlib.pyplot as plt

# Create test cases
trials = []
A, B = pyamg.gallery.poisson((500, 500), format='csr'), None
trials.append(('Poisson', A, B))
A, B = pyamg.gallery.linear_elasticity((200, 200), format='bsr')
trials.append(('Elasticity', A, B))

solvernum = 1
if '--solver' in sys.argv:
    i = sys.argv.index('--solver')
    solvernum = int(sys.argv[i+1])
else:
    print('Usage: python demo.py --solver N, with N=1 or 2.\n'
          'Show advantages of accleration for two example problems\n'
          'Test convergence for a simple 100 x 100 grid, Gauge Laplacian.\n'
          'Input Choice:\n'
          '1:  Run smoothed_aggregation_solver\n'
          '2:  Run rootnode_solver\n')
    sys.exit()

if solvernum == 1:
    method = pyamg.smoothed_aggregation_solver
elif solvernum == 2:
    method = pyamg.rootnode_solver
else:
    raise ValueError("Enter a solver of 1 or 2")


for name, A, B in trials:
    # Construct solver using AMG based on Smoothed Aggregation (SA)
    mls = method(A, B=B)

    # Display hierarchy information
    print('Matrix: %s' % name)
    print(mls)

    # Create random right hand side
    b = np.random.rand(A.shape[0], 1)

    # Solve Ax=b with no acceleration ('standalone' solver)
    standalone_residuals = []
    x = mls.solve(b, tol=1e-10, accel=None, residuals=standalone_residuals)

    # Solve Ax=b with Conjugate Gradient (AMG as a preconditioner to CG)
    accelerated_residuals = []
    x = mls.solve(b, tol=1e-10, accel='cg', residuals=accelerated_residuals)

    # Compute relative residuals
    standalone_residuals = np.array(
        standalone_residuals) / standalone_residuals[0]
    accelerated_residuals = np.array(
        accelerated_residuals) / accelerated_residuals[0]

    # Plot convergence history
    fig, ax = plt.subplots()
    ax.set_title(f'Convergence History ({name})')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Relative Residual')
    ax.semilogy(standalone_residuals,
                label='Standalone', linestyle='None', marker='.')
    ax.semilogy(accelerated_residuals,
                label='Accelerated', linestyle='None', marker='.')
    ax.legend()

    figname = f'./output/convergence_{name.lower()}.png'
    import sys
    if '--savefig' in sys.argv:
        plt.savefig(figname, bbox_inches='tight', dpi=150)
    else:
        plt.show()
