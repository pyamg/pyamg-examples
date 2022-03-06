# This example solves a diffusion problem and demonstrates the use of
# applying boundary condition patches.
try:
    import fipy
except ImportError:
    raise ImportError('Problem with FiPy Installation')

from PyAMGSolver import PyAMGSolver

nx = 20
ny = nx
dx = 1.0
dy = dx
L = dx * nx
mesh = fipy.Grid2D(dx=dx, dy=dy, nx=nx, ny=ny)
phi = fipy.CellVariable(name="solution variable", mesh=mesh, value=0.)

# Apply Dirichlet boundary conditions (else Neumann by default)
valueTopLeft = 0
valueBottomRight = 1
x, y = mesh.getFaceCenters()
facesTopLeft = ((mesh.getFacesLeft() & (y > L / 2)) | (mesh.getFacesTop() & (x < L / 2)))
facesBottomRight = ((mesh.getFacesRight() & (y < L / 2)) | (mesh.getFacesBottom() & (x > L / 2)))
BCs = (fipy.FixedValue(faces=facesTopLeft, value=valueTopLeft),
       fipy.FixedValue(faces=facesBottomRight, value=valueBottomRight))

# set solver
# solver = LinearLUSolver(tolerance = 1.e-6, iterations = 100)
MGSetupOpts = {'max_coarse': 10}
MGSolveOpts = {'maxiter': 100, 'tol': 1e-8}
solver = PyAMGSolver(verbosity=1, MGSetupOpts=MGSetupOpts, MGSolveOpts=MGSolveOpts)

# solve diffusion equation with solver above
fipy.ImplicitDiffusionTerm().solve(var=phi,
                                   boundaryConditions=BCs,
                                   solver=solver)

# view result
viewer = fipy.Viewer(vars=phi, datamin=0., datamax=1.)
viewer.plot()
