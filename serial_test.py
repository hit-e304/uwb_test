import time
import serial
import numpy as np

portx = "COM3"
bps = 921600
timex = 5
self_num = 0
num_flight = 2
dis = {}
str_dis = []
ser = serial.Serial(portx, bps, timeout=timex)

def data_ctr(a):
    if len(a) < 16 or len(a) < (a[15]+1) * 16:
        print('wrong data')
        return False
    if a[15] != (num_flight - 1):
        print('not enough tags')
        return False
    print("%i tags found" % a[15])
    return True

def read_data(a):
    global_dis = np.zeros([num_flight, num_flight])
    decay = 0

    for k in range(a[15]):
        id0 = a[16 * (k+1) + decay]
        d = (65536 * a[16 * (k+1) + 3 + decay] + a[16 * (k+1) + 2 + decay] * 256 + a[16 * (k+1) + 1 + decay]) / 1000
        info_len = a[30 + 16 * k + decay]
        info_get = a[(32 + 16 * k) : (32 + 16 * k + decay)]
        dis[id0] = d
        decay += info_len

        for key in dis:
            global_dis[self_num][key] = dis[key]

    return dis, global_dis

def send_data(global_dis):
    str_dis = []    

    for i in range(num_flight):
        str_dis += global_dis[self_num][i]

    send_dis = ",".join(str_dis)
    ser.write((send_dis +'\n').encode())

while True:
    if ser.in_waiting:
        a = ser.read(ser.in_waiting)
        if not data_ctr:
            break

        distance, global_distance = read_data(a)
        send_data(global_distance)
