from serial.tools import list_ports

import pydobot

import time

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}') #利用可能ポートを表示
port = available_ports[2].device #port番号を指定 

device = pydobot.Dobot(port=port, verbose=None) # デバイスを指定  verboseをTrueにすると通信の詳細？が表示される
(x, y, z, r, j1, j2, j3, j4) = device.pose() # 取得した座標をそれぞれタプル型で格納　
print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

device.move_to(x, y+10, z, r, wait=True)
(x, y, z, r, j1, j2, j3, j4) = device.pose() # 取得した座標をそれぞれタプル型で格納　

device.move_to(x, y, z, r, wait=True)  # この動作が終わるまで待つ
(x, y, z, r, j1, j2, j3, j4) = device.pose() # 取得した座標をそれぞれタプル型で格納　


# device.move_to(130, 0, 0, 0, wait=True)

device.close()


# 解説・注意点
# available_ports[2].device
    # 利用可能なポートの左から順に0,1,2...と番号が振られる? 
    # 利用可能なポートが['COM1', 'COM2', 'COM3']でCOM3にDobotが繋がっている場合は[]の中に2を入れる

# device.pose()
# 取得した現在の座標が格納されている
# 左から順に(x,y,z,r,j1,j2,j3,j4)



