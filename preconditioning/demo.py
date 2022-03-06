# Examples of AMG as a preconditioner

import numpy as np
import pyamg
import matplotlib.pyplot as plt

# Create test cases
trials = []
A, B = pyamg.gallery.poisson((500, 500), format='csr'), None
trials.append(('Poisson', A, B))
A, B = pyamg.gallery.linear_elasticity((200, 200), format='bsr')
trials.append(('Elasticity', A, B))

print("Show advantages of accleration for two example problems")
choice = input('\n Input Choice:\n' +
               '1:  Run smoothed_aggregation_solver\n' +
               '2:  Run rootnode_solver\n')
choice = int(choice)
if choice == 1:
    method = pyamg.smoothed_aggregation_solver
elif choice == 2:
    method = pyamg.rootnode_solver
else:
    raise ValueError("Enter a choice of 1 or 2")


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
    plt.figure()
    plt.title('Convergence History (%s)' % name, fontsize=16)
    plt.xlabel('Iteration', fontsize=16)
    plt.ylabel('Relative Residual', fontsize=16)
    plt.semilogy(
        standalone_residuals,
        label='Standalone',
        linestyle='None',
        marker='.')
    plt.semilogy(
        accelerated_residuals,
        label='Accelerated',
        linestyle='None',
        marker='.')
    plt.legend(fontsize=16)
    print("Close window for program to proceed.\n")
    plt.show()
