from serial.tools import list_ports

import pydobot

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}') #利用可能ポートを表示
port = available_ports[2].device #port番号を指定 

device = pydobot.Dobot(port=port, verbose=None) # デバイスを指定 
(x, y, z, r, j1, j2, j3, j4) = device.pose() # 取得した座標をそれぞれタプル型で格納　
print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')


device.close()



