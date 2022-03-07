import numpy as np
import scipy.sparse as sparse
import pyamg
import scipy.optimize

__all__ = ['one_D_helmholtz', 'min_wave']


def min_wave(A, omega, x, tol=1e-5, maxiter=25):
    '''

    parameters
    ----------
    A {matrix}
        1D Helmholtz Operator
    omega {scalar}
        Wavenumber used to discretize Helmholtz problem
    x {array}
        1D mesh for the problem
    tol {scalar}
        minimization tolerance
    maxit {integer}
        maximum iters for minimization algorithm

    returns
    -------
    Applies minimization algorithm to find numerically lowest energy wavenumber
    for the matrix A, i.e., the omega shift that minimizes <Ac, c> / <c, c>,
    for c = cosine((omega+shift)x)

    '''

    x = np.ravel(x)

    # Define scalar objective function, ignoring the
    # boundaries by only considering A*c at [1:-1]
    def obj_fcn(alpha):
        c = np.cos((omega + alpha) * x)
        Ac = (A * c)[1:-1]
        return np.linalg.norm(Ac) / np.linalg.norm(c[1:-1])

    (xopt, fval, ierr, numfunc) = scipy.optimize.fminbound(
        obj_fcn, -0.99 * omega,
        0.99 * omega, xtol=tol, maxfun=maxiter, full_output=True, disp=0)

    # print "Minimizer = %1.4f,  Function Value at Min = %1.4e\nError Flag = %d,\
    #        Number of function evals = %d" % (xopt, fval, ierr, numfunc)

    return xopt


def one_D_helmholtz(h, omega=1.0, nplane_waves=2):
    '''

    parameters
    ----------
    h {int}
        Number of grid spacings for 1-D Helmholtz
    omega {float}
        Defines Helmholtz wave number
    nplane_waves {int}
        Defines the number of planewaves used for the near null-space modes, B.
        1: B = [ exp(ikx) ]
        2: B = [ real(exp(ikx)), complex(exp(ikx)) ]

    returns
    -------
    dictionary containing:

    A {matrix-like}
        LHS of linear system for Helmholtz problem,
        -laplace(u) - omega^2 u = f
    mesh_h {float}
        mesh size
    vertices {array-like}
        [X, Y]
    elements {None}
        None, just using 1-D finite-differencing

    '''

    # Ensure Repeatability of "random" initial guess
    np.random.seed(10)

    # Mesh Spacing
    mesh_h = 1.0 / (float(h) - 1.0)

    # Construct Real Operator
    reA = pyamg.gallery.poisson((h,), format='csr')
    reA = reA - mesh_h * mesh_h * omega * omega *\
        sparse.eye(reA.shape[0], reA.shape[1], format='csr')
    dimen = reA.shape[0]

    # Construct Imaginary Operator
    imA = sparse.csr_matrix(sparse.coo_matrix((np.array([2.0 * mesh_h * omega]),
                            (np.array([0]), np.array([0]))), shape=reA.shape))

    # Enforce Radiation Boundary Conditions at first grid point
    reA.data[1] = -2.0

    # In order to maintain symmetry scale the first equation by 1/2
    reA.data[0] = 0.5 * reA.data[0]
    reA.data[1] = 0.5 * reA.data[1]
    imA.data[0] = 0.5 * imA.data[0]

    # Create complex-valued system
    complexA = reA + 1.0j * imA

    # For this case, the CG (continuous Galerkin) case is the default elements and vertices
    # because there is no DG mesh to speak of
    elements = None
    vertices = np.hstack((np.linspace(-1.0, 1.0, h).reshape(-1, 1),
                          np.zeros((h, 1))))

    # Near null-space modes are 1-D Plane waves: [exp(ikx), i exp(ikx)]
    B = np.zeros((dimen, nplane_waves), dtype=complex)
    shift = min_wave(complexA, omega, vertices[:, 0], tol=1e-9, maxiter=15)
    if nplane_waves == 1:
        B[:, 0] = np.exp(1.0j * (omega + shift) * vertices[:, 0])
    elif nplane_waves == 2:
        B[:, 0] = np.cos((omega + shift) * vertices[:, 0])
        B[:, 1] = np.sin((omega + shift) * vertices[:, 0])

    return {'A': complexA, 'B': B, 'mesh_h': mesh_h,
            'elements': elements, 'vertices': vertices}
