from pyinstrument import Profiler

import numpy as np
import pyamg

profiler = Profiler()
profiler.start()

n = int(1e3)
A = pyamg.gallery.poisson((n, n), format='csr')
b = np.random.rand(A.shape[0])

ml = pyamg.smoothed_aggregation_solver(A, max_coarse=10)
res = []
x = ml.solve(b, accel='cg', residuals=res)
print(len(res))

profiler.stop()

print(profiler.output_text(unicode=True, color=True))
