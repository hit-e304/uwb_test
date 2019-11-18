import numpy as np
import math
import pdb as ipdb
import matplotlib.pyplot as plt


n = 5

x0 = np.random.rand(n) * 10
y0 = np.random.rand(n) * 10
# z0 = np.random.rand(n) * 10

### add noise to GPS position ###
lam = 0.1
x = x0 + np.random.rand(n) *  lam
y = y0 + np.random.rand(n) *  lam
# z = z0 + np.random.rand(n) *  lam

# d = np.random.rand(n, n) * 0.001
d = np.zeros([n, n])

for i in range(n):
    for j in range(n):
        if j == i:
            d[i, j] += 0
        else:
            # d[i, j] += math.sqrt(math.pow((x0[i]-x0[j]), 2) + math.pow((y0[i]-y0[j]), 2) + math.pow((z0[i]-z0[j]), 2))
            d[i, j] += math.sqrt(math.pow((x0[i]-x0[j]), 2) + math.pow((y0[i]-y0[j]), 2))

X = np.zeros(n)
Y = np.zeros(n)

X[1] = d[0][1]
Y[2] = d[0][2]

for i in range(2, n):
    X[i] = (math.pow(d[i][0], 2) - math.pow(d[i][1], 2) + math.pow(x[0], 2)) / (2 * x[1])
    Y[i] = (math.pow(d[i][0], 2) - math.pow(d[i][2], 2) + math.pow(y[0], 2)) / (2 * y[2])

plt.figure()
plt.scatter(X, Y)
plt.figure()
plt.scatter(x0, y0)
plt.show()

# ipdb.set_trace()

