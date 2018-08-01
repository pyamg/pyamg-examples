# ------------------------------------------------------------------
# Step 1: import scipy and pyamg packages
# ------------------------------------------------------------------
import numpy as np
import pyamg
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Step 2: setup up the system using pyamg.gallery
# ------------------------------------------------------------------
n = 200
X, Y = np.meshgrid(np.linspace(0, 1, n), np.linspace(0, 1, n))
stencil = pyamg.gallery.diffusion_stencil_2d(type='FE', epsilon=0.001, theta=np.pi / 3)
A = pyamg.gallery.stencil_grid(stencil, (n, n), format='csr')
b = np.random.rand(A.shape[0])                     # pick a random right hand side

# ------------------------------------------------------------------
# Step 3: setup of the multigrid hierarchy
# ------------------------------------------------------------------
ml = pyamg.smoothed_aggregation_solver(A)   # construct the multigrid hierarchy

# ------------------------------------------------------------------
# Step 4: solve the system
# ------------------------------------------------------------------
res1 = []
x = ml.solve(b, tol=1e-12, residuals=res1)  # solve Ax=b to a tolerance of 1e-12

# ------------------------------------------------------------------
# Step 5: print details
# ------------------------------------------------------------------
print("\n")
print("Details of the multilevel object")
print("--------------------------------")
print(ml)                                 # print hierarchy information

print("The residual norm is {}".format(np.linalg.norm(b - A * x)))  # compute norm of residual vector

# notice that there are 5 (or maybe 6) levels in the hierarchy
#
# we can look at the data in each of the levels
# e.g. the multigrid components on the finest (0) level
#      A: operator on level 0
#      P: prolongation operator mapping from level 1 to level 0
#      R: restriction operator mapping from level 0 to level 1
#      B: near null-space modes for level 0
#      presmoother: presmoothing function taking arguments (A,x,b)
#      postsmoother: postsmoothing function taking arguments (A,x,b)
print("\n")
print("The Multigrid Hierarchy")
print("-----------------------")
for l in range(len(ml.levels)-1):
    print("A_{}: {}x{}   P_{}: {}x{}".format(l, ml.levels[l].A.shape[0], ml.levels[l].A.shape[1],
                                             l, ml.levels[l].P.shape[0], ml.levels[l].P.shape[1]))

# There is no P on the coarsest level:
print("A_{}: {}x{}".format(l, ml.levels[-1].A.shape[0], ml.levels[-1].A.shape[1]))

# ------------------------------------------------------------------
# Step 6: change the hierarchy
# ------------------------------------------------------------------
# we can also change the details of the hierarchy
ml = pyamg.smoothed_aggregation_solver(A,  # the matrix
                                       B=X.reshape(n * n, 1),             # the representation of the near null space (this is a poor choice)
                                       BH=None,                           # the representation of the left near null space
                                       symmetry='hermitian',              # indicate that the matrix is Hermitian
                                       strength='evolution',              # change the strength of connection
                                       aggregate='standard',              # use a standard aggregation method
                                       smooth=('jacobi', {'omega': 4.0 / 3.0, 'degree': 2}),   # prolongation smoothing
                                       presmoother=('block_gauss_seidel', {'sweep': 'symmetric'}),
                                       postsmoother=('block_gauss_seidel', {'sweep': 'symmetric'}),
                                       improve_candidates=[('block_gauss_seidel',
                                                           {'sweep': 'symmetric', 'iterations': 4}), None],
                                       max_levels=10,                     # maximum number of levels
                                       max_coarse=5,                      # maximum number on a coarse level
                                       keep=False)                        # keep extra operators around in the hierarchy (memory)

# ------------------------------------------------------------------
# Step 7: print details
# ------------------------------------------------------------------
res2 = []                                               # keep the residual history in the solve
x = ml.solve(b, tol=1e-12, residuals=res2)              # solve Ax=b to a tolerance of 1e-12
print("\n")
print("The Multigrid Hierarchy")
print("-----------------------")
print(ml)                                               # print hierarchy information
print("The residual norm is {}".format(np.linalg.norm(b - A * x)))  # compute norm of residual vector
print("\n")

# ------------------------------------------------------------------
# Step 8: plot convergence history
# ------------------------------------------------------------------
plt.semilogy(res1)
plt.semilogy(res2)
plt.title('Residual Histories')
plt.legend(['Default Solver', 'Specialized Solver'])
plt.xlabel('Iteration')
plt.ylabel('Relative Residual')
plt.show()
