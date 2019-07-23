import time
import struct
import binascii

import serial
import json


portx = 'COM3'
bps = 921600
timex = 5
self_num = 0
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


def read_unit(b, width=6):
    '''read information of one unit
    output:
    '''
    ans = []

    ans.append(b[6] * 65536 + b[5] * 256 + b[4])
    ans.append(b[9] * 65536 + b[8] * 256 + b[7])
    ans.append(b[12] * 65536 + b[11] * 256 + b[10])

    for i, pos in enumerate(ans):
        if pos > 16 ** (width - 1) -1:
            ans[i] = pos - 16 ** width
        ans[i] = ans[i] / 1000

    return ans


if __name__ == '__main__':

    while(True):
        if ser.in_waiting:
            start_time = time.time()
            data = ser.read(ser.in_waiting)
            if data[0] == 85 and data[1] == 1:
                test = read_unit(data)
                save_inf = json.dumps({'pos_x': test[0], 
                                       'pos_y': test[1],
                                       'pos_z': test[2]})
                with open('user_info.json', 'w', encoding='utf-8') as json_file:
                    json.dump(save_inf, json_file, ensure_ascii=False)
                # print(test[0], test[1], test[2])
                print(time.time() - start_time)
            else:
                continue