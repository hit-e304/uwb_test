import time
import serial
import numpy as np
import math

n = 4
portx = "COM3"
bps = 921600
timex = 5

ser = serial.Serial(portx, bps, timeout=timex)

def Location(ser):
    while True:
        if ser.in_waiting:
            a = ser.read(ser.in_waiting)
            # Judge whether a is available
            if len(a) < 70:
                # print('wrong message')
                continue
            if a[15] != 4:
                # print('not enough tags')    
                continue

            # print("%i tags found" % a[15])
            # print(len(a))

            id0 = []
            d = []
            A = np.zeros([2, 3])
            b = np.zeros([2, 1])

            # Get all distance from anchors
            for k in range(a[15]):
                id0.append(a[16 * (k+1)])
                d.append((65536 * a[16 * (k+1) + 3] + a[16 * (k+1) + 2] * 256 + a[16 * (k+1) + 1]) / 1000)
                # print(" the %i tag is %f away" % (id0[-1], d[-1]))

            # Calculate position by least squares
            for i in range(n-2):
                A[i, :] = ([2 * (x[i+1]-x[n-1]), 2 * (y[i+1]-y[n-1]), 2 * (z[i+1]-z[n-1])])
                b[i] = (math.pow(x[i+1], 2) - math.pow(x[n-1], 2) + math.pow(y[i+1], 2) - math.pow(y[n-1], 2) + 
                        math.pow(z[i+1], 2) - math.pow(z[n-1], 2) - math.pow(d[i+1], 2) + math.pow(d[n-1], 2))
            A = np.mat(A)
            b = np.mat(b)
            X = (A.T * A).I * A.T * b
            print(X)

Location(ser)