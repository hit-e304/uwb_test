import time
import serial
import numpy as np

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--portx', type=str, default='COM3')
parser.add_argument('--num', type=int, default=2)
args = parser.parse_args()

portx = args.portx
bps = 921600
timex = 5
self_num = 0
num_flight = args.num
dis = {}
str_dis = []
ser = serial.Serial(portx, bps, timeout=timex)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def data_ctr(a):
    if len(a) < 16 or len(a) < (a[15]+1) * 16:
        print('wrong data')
        return False
    if a[15] != (num_flight - 1):
        print('not enough tags')
        return False
    return True

def read_data(a):
    global_dis = np.zeros([num_flight, num_flight])
    decay = 0
    con_sign = True

    if a[15] != (num_flight - 1):
        con_sign = False
        return global_dis, con_sign

    for k in range(a[15]):
        id0 = a[16 * (k+1) + decay]
        d = (65536 * a[16 * (k+1) + 3 + decay] + a[16 * (k+1) + 2 + decay] * 256 + a[16 * (k+1) + 1 + decay]) / 1000
        info_len = a[30 + 16 * k + decay]
        if info_len > 20:
            con_sign = False
            return global_dis, con_sign

        info_get = a[(32 + 16 * k + decay) : (32 + 16 * k + decay + info_len)].decode()
        info_get = info_get.replace('\n', '')
        info = info_get.split(',')
        if len(info) == 0:
            con_sign = False
            return global_dis, con_sign

        for i in range(len(info)):
            if not is_number(info[i]):
                con_sign = False
                return global_dis, con_sign                

            if i <= k:
                global_dis[id0][i] = float(info[i])
            else:
                global_dis[id0][i+1] = float(info[i])
        
        if global_dis.max() > 100:
            con_sign = False
            return global_dis, con_sign
            
        dis[id0] = d
        decay += info_len

        for key in dis:
            global_dis[self_num][key] = dis[key]

    return global_dis, con_sign

def send_data(global_dis):
    str_dis = []    

    for i in range(num_flight):
        str_dis += global_dis[self_num][i]

    send_dis = ",".join(str_dis)
    ser.write((send_dis +'\n').encode())

if __name__ == '__main__':
    
    while True:
        start_time = time.time()
        if ser.in_waiting:

            a = ser.read(ser.in_waiting)
            a_sign = data_ctr(a)
            if not a_sign:
                print('a_error')
                continue

            global_distance, continue_sign = read_data(a)
    
            if not continue_sign:
                print('data_error')
                continue
            
            send_data(global_distance)
            print(global_distance)
            print(time.time() - start_time)        

    ser.close()
