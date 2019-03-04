import time
import serial

portx = "COM5"
bps = 921600
timex = 5

ser = serial.Serial(portx, bps, timeout=timex)

def ReadData(ser):
    while True:
        if ser.in_waiting:
            str_dis = []

            a = ser.read(ser.in_waiting)
            if len(a) < 16 or len(a) < (a[15]+1) * 16:
                print('not enough tags')
                continue
            if a[15] not in [1, 2, 3, 4, 5]:
                continue
            print("%i tags found" % a[15])

            for k in range(a[15]):
                id0 = a[16 * (k+1)]
                d = (65536 * a[16 * (k+1) + 3] + a[16 * (k+1) + 2] * 256 + a[16 * (k+1) + 1]) / 1000
                print(" the %i tag is %f away" % (id0, d))
                str_dis.append(str(d))

            send_dis = ",".join(str_dis)
            ser.write((send_dis +'\n').encode())
    ser.close()

ReadData(ser)
