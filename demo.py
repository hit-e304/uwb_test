import numpy as np
import math
import pdb as ipdb

n = 5

x0 = np.random.rand(n) * 10
y0 = np.random.rand(n) * 10
z0 = np.random.rand(n) * 10

### add noise to GPS position ###
lam = 0.1
x = x0 + np.random.rand(n) *  lam
y = y0 + np.random.rand(n) *  lam
z = z0 + np.random.rand(n) *  lam

### test whether the last point have more influnce ###
# x[-1] += np.random.rand(1)
# y[-1] += np.random.rand(1)
# z[-1] += np.random.rand(1)

d = np.random.rand(n, n) * 0.001

A = []
b = []

for i in range(n):
    for j in range(n):
        if j == i:
            d[i, j] += 0
        else:
            d[i, j] += math.sqrt(math.pow((x0[i]-x0[j]), 2) + math.pow((y0[i]-y0[j]), 2) + math.pow((z0[i]-z0[j]), 2))

for i in range(n-2):
    A.append([2 * (x[i+1]-x[n-1]), 2 * (y[i+1]-y[n-1]), 2 * (z[i+1]-z[n-1])])
    b.append(math.pow(x[i+1], 2) - math.pow(x[n-1], 2) + math.pow(y[i+1], 2) - math.pow(y[n-1], 2) + math.pow(z[i+1], 2) - math.pow(z[n-1], 2) - math.pow(d[i+1, 0], 2) + math.pow(d[n-1, 0], 2))

A = np.mat(A)
b = np.mat(b)
X = (A.T * A).I * A.T * b.T

ipdb.set_trace()

print("Test with %i points" % n)
print("Lamda of noise %f " % lam)
print(X.T)
print(X[0]-x[0], X[1]-y[0], X[2]-z[0])
print(X[0]-x0[0], X[1]-y0[0], X[2]-z0[0])
























