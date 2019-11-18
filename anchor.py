import time
import struct
import binascii

import serial
import json


portx = 'COM9'
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


def read_unit(b, width=6, a=0):
    '''read information of one unit
    output:
    '''
    ans = []

    ans.append(b[31+a] * 65536 + b[30+a] * 256 + b[29+a])
    ans.append(b[34+a] * 65536 + b[33+a] * 256 + b[32+a])
    ans.append(b[37+a] * 65536 + b[36+a] * 256 + b[35+a])

    for i, pos in enumerate(ans):
        if pos > 16 ** (width - 1) -1:
            ans[i] = pos - 16 ** width
        ans[i] = ans[i] / 1000

    return ans


if __name__ == '__main__':

    test_id = -25
    while True:
        if ser.inWaiting:
            data = ser.read(ser.inWaiting())
            # print(data)
            if len(data) < 40:
                continue
            if data[0] == 85 and data[1] == 0:
                test = read_unit(data, a = test_id)
                save_inf = json.dumps({'pos_x': test[0], 
                                       'pos_y': test[1],
                                       'pos_z': test[2]})
                with open('user_info.json', 'w', encoding='utf-8') as json_file:
                    json.dump(save_inf, json_file, ensure_ascii=False)
                print(test[0], test[1], test[2], test_id)
                # print(time.time() - start_time)
            # else:
            #     print('Data Error')
