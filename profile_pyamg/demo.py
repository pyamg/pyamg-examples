from pyinstrument import Profiler

import numpy as np
import pyamg

n = int(1e3)
A = pyamg.gallery.poisson((n, n), format='csr')
b = np.random.rand(A.shape[0])

profiler = Profiler()
profiler.start()
ml = pyamg.smoothed_aggregation_solver(A, max_coarse=10)
profiler.stop()

x = ml.solve(b)

print(profiler.output_text(unicode=True, color=True))
