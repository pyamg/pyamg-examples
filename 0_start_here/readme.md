As a starting example, this demo considers a rotated anisotropic
diffusion problem from the `pyamg.gallery`.  First, a basic
smoothed aggregation solver is constructed.  Then, many of the
options are modified to yield a more effective solver.

The comments in `demo.py` follow several steps that walk through the demo:

- Step 1: import scipy and pyamg packages
- Step 2: setup up the system using pyamg.gallery
- Step 3: setup of the multigrid hierarchy
- Step 4: solve the system
- Step 5: print details
- Step 6: change the hierarchy
- Step 7: print details
- Step 8: plot convergence history
