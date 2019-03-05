import time
import serial
import numpy as np

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--portx', type=str, default='COM3')
parser.add_argument('--num', type=int, default=4)
args = parser.parse_args()

portx = args.portx
bps = 921600
timex = 10
# self_num = 0
num_flight = args.num
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

def read_byte():
    read_flag = 0
    out_a = []
    while read_flag in [0, 1]:
        read_byte = ser.read()[0]
        if read_byte == 85:
            read_flag += 1
        if read_flag == 1:
            out_a.append(read_byte)
    return out_a

def init_data():
    init_flag = False
    dis = {}
    global_dis = np.zeros([num_flight, num_flight])

    while not init_flag:
        a = read_byte()
        if len(a) < 16 * num_flight:
            print('init erro: wrong length', len(a))
            continue
        if a[15] != num_flight - 1:
            print('init error: not enough target')
            continue
        else:
            self_num = a[2]

            for k in range(a[15]):
                id0 = a[16 * (k+1)]
                d = (65536 * a[16 * (k+1) + 3] + a[16 * (k+1) + 2] * 256 + a[16 * (k+1) + 1]) / 1000
                dis[id0] = d
            for key in dis:
                global_dis[self_num][key] = dis[key]

            init_flag = True
    
    print('finish init')

    return self_num, global_dis, init_flag



def data_ctr(a):
    if len(a) < 16 or len(a) < (a[15]+1) * 16:
        print('wrong data')
        return False
    if a[15] != (num_flight - 1):
        print('not enough tags')
        return False
    return True

def read_data(a, global_dis):
    decay = 0
    con_sign = True
    dis = {}

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

        info = a[(32 + 16 * k + decay) : (32 + 16 * k + decay + info_len)]
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

    self_num, global_distance, init_flag = init_data()
    
    while init_flag:
        start_time = time.time()
        send_data(global_distance)

        a = read_byte()
        a_sign = data_ctr(a)
        if not a_sign:
            continue

        global_distance, continue_sign = read_data(a, global_distance)

        # if not continue_sign:
        #     print('data_error')
        #     continue
        
        send_data(global_distance)
        print(global_distance)
    
    ser.close()
