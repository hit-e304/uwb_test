import serial
import numpy as np
import math

serialPort="COM3"
baudRate = 921600
ser=serial.Serial(serialPort,baudRate,timeout=0.5)  

while 1:
    if ser.in_waiting:
        a = ser.read(ser.in_waiting)
        if len(a) < 16 or len(a) < (a[15]+1) * 16:
            print('not enough tags')
            continue
        if a[15] not in [1, 2, 3, 4, 5]:
            continue
        print("%i tags found" % a[15])

        print("%i tags found" % a[15])

        decay = 0
        for k in range(a[15]):
            decay += a[30 + 16 * k + decay]
            id0 = a[16 * (k+1) + decay]
            d = (65536 * a[16 * (k+1) + 3 + decay] + a[16 * (k+1) + 2 + decay] * 256 + a[16 * (k+1) + 1 + decay]) / 1000
            print(" the %i tag is %f away" % (id0, d))
        print(len(a))

ser.close()  
