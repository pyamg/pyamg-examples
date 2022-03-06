import numpy as np
import pyamg
import matplotlib.pyplot as plt

n = 20
A = pyamg.gallery.poisson((n,n)).tocsr()

xx = np.linspace(0,1,n)
x,y = np.meshgrid(xx,xx)
V = np.concatenate([[x.ravel()],[y.ravel()]],axis=0).T

splitting = pyamg.classical.cr.CR(A)

C = np.where(splitting == 0)[0]
F = np.where(splitting == 1)[0]
plt.scatter(V[C, 0], V[C, 1], marker='s', s=18,
            color=[232.0/255, 74.0/255, 39.0/255])
plt.scatter(V[F, 0], V[F, 1], marker='s', s=18,
            color=[19.0/255, 41.0/255, 75.0/255])
plt.legend(['Cpts', 'Fpts'], fontsize=16)
plt.show()
