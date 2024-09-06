
"""A simple performance test adopted from sciket-fem.
"""
from timeit import timeit
import numpy as np
import skfem as skf
from skfem.models.poisson import laplace, unit_load
import pyamg

def pre(N=3):
    m = skf.MeshTet.init_tensor(*(3 * (np.linspace(0., 1., N),)))
    return m

def assembler(m):
    basis = skf.Basis(m, skf.ElementTetP1())
    return (
        laplace.assemble(basis),
        unit_load.assemble(basis),
    )

times  = []
fw = 10
kmin =  6
kmax = 20
Nlist = [int(2 ** (k / 3)) for k in range(kmin, kmax)]
# print(Nlist)

print('| N | DoFs | Assembly | Solve prep | Solve setup | Solve |')
print('| ---- | ---- | ---- | ---- | ---- | ---- |')
for N in Nlist:
    m = pre(N)

    assemble_time = timeit(lambda: assembler(m), number=1)
    A, b = assembler(m)
    D = m.boundary_nodes()

    condense_time = timeit(lambda: skf.condense(A, b, D=D), number=1)
    A, b, _, _ = skf.condense(A, b, D=D)

    setup_time = timeit(lambda: pyamg.smoothed_aggregation_solver(A).aspreconditioner(), number=1)
    ml = pyamg.smoothed_aggregation_solver(A,
                                           max_coarse=10).aspreconditioner()

    mlsolver = skf.solver_iter_pcg(verbose=False, M=ml, rtol=1e-8)
    solve_time = timeit(lambda: skf.solve(A, b, solver=mlsolver), number=1)

    times.append([N, len(b), assemble_time, condense_time, setup_time, solve_time])
    print(f'| {N:10d} | {len(b):10d} | {assemble_time:>{fw}.5f} | {condense_time:{fw}.5f} | {setup_time:{fw}.5f} | {solve_time:{fw}.5f} |')

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
n = [t[1] for t in times]
ax.loglog(n, [t[2] for t in times], label='Assembly')
ax.loglog(n, [t[3] for t in times], label='Solve prep')
ax.loglog(n, [t[4] for t in times], label='Solve setup')
ax.loglog(n, [t[5] for t in times], label='Solve')
ax.set_xlabel('# DoFs')
ax.set_ylabel('time (s)')
ax.grid(True)
plt.legend()

figname = f'./output/performance.png'
import sys
if '--savefig' in sys.argv:
    plt.savefig(figname, bbox_inches='tight', dpi=150)
else:
    plt.show()
