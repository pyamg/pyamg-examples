import numpy as np
import pyamg
import matplotlib.pyplot as plt

n = int(1e2)
stencil = pyamg.gallery.diffusion_stencil_2d(type='FE', epsilon=0.001, theta=np.pi / 3)
A = pyamg.gallery.stencil_grid(stencil, (n, n), format='csr')
b = np.random.rand(A.shape[0])
x0 = 0 * b

runs = []
options = []
options.append(('symmetric', {'theta': 0.0}))
options.append(('symmetric', {'theta': 0.25}))
options.append(('evolution', {'epsilon': 4.0}))
options.append(
    ('algebraic_distance', {
        'epsilon': 2.0, 'p': np.inf, 'R': 10, 'alpha': 0.5, 'k': 20}))
options.append(
    ('algebraic_distance', {
        'epsilon': 3.0, 'p': np.inf, 'R': 10, 'alpha': 0.5, 'k': 20}))
options.append(('affinity', {'epsilon': 3.0, 'R': 10, 'alpha': 0.5, 'k': 20}))
options.append(('affinity', {'epsilon': 4.0, 'R': 10, 'alpha': 0.5, 'k': 20}))

for opt in options:
    optstr = opt[0] + '\n    ' + \
        ',\n    '.join(['%s=%s' % (u, v) for (u, v) in list(opt[1].items())])
    print("running %s" % (optstr))

    ml = pyamg.smoothed_aggregation_solver(
        A,
        strength=opt,
        max_levels=10,
        max_coarse=5,
        keep=False)
    res = []
    x = ml.solve(b, x0, tol=1e-12, residuals=res)
    runs.append((res, optstr))

fig = plt.figure()
ax = plt.subplot(111)
for run in runs:
    ax.semilogy(run[0], label=run[1], linewidth=3)
ax.set_xlabel('Iteration')
ax.set_ylabel('Relative Residual')

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.setp(plt.gca().get_legend().get_texts(), fontsize='x-small')

plt.show()
