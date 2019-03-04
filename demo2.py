import numpy as np
import math

d = np.array([0, 1, 2 , 3, 4, 1, 0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0, 1, 4, 3, 2, 1, 0]).reshape(5, 5)
x = np.array([0, d[0, 1], 0])
y = np.array([0, 0, 0])
z = np.array([0, 0, 0])

x[2] = (math.pow(d[0, 2], 2) - math.pow(d[1, 2], 2) + math.pow(d[0, 1], 2)) / (2 * d[0, 1])
y[2] = (math.pow(d[0, 2], 4) + math.pow(d[1, 2], 4) + math.pow(d[0, 1], 4) - 2 * math.pow(d[0, 2], 2) * math.pow(d[1, 2], 2) - 2 * math.pow(d[0, 1], 2) * math.pow(d[1, 2], 2) - 2 * math.pow(d[0, 1], 2) * math.pow(d[0, 2], 2)) / (4 * math.pow(d[0, 1], 2))

A = np.mat(np.zeros(shape=(0, 3)))
b = np.mat([])

# def lsp(d, A, b):
n = len(x)

for i in range(n-2):
    # A.append([2 * (x[i+1]-x[n-1]), 2 * (y[i+1]-y[n-1]), 2 * (z[i+1]-z[n-1])])
    # b.append(math.pow(x[i+1], 2) - math.pow(x[n-1], 2) + math.pow(y[i+1], 2) - math.pow(y[n-1], 2) + math.pow(z[i+1], 2) - math.pow(z[n-1], 2) - math.pow(d[i+1, 0], 2) + math.pow(d[n-1, 0], 2))
    A = np.r_[A, np.mat([2 * (x[i+1]-x[n-1]), 2 * (y[i+1]-y[n-1]), 2 * (z[i+1]-z[n-1])])]
    b = np.c_[b, (math.pow(x[i+1], 2) - math.pow(x[n-1], 2) + math.pow(y[i+1], 2) - math.pow(y[n-1], 2) + math.pow(z[i+1], 2) - math.pow(z[n-1], 2) - math.pow(d[i+1, 0], 2) + math.pow(d[n-1, 0], 2))]


X = (A.T * A).I * A.T * b.T
x.append(X[0])
y.append(X[1])
z.append(X[2])

    # return A, b, x, y, z




