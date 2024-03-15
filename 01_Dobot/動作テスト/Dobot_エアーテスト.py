from serial.tools import list_ports
import time

import pydobot

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[2].device
device = pydobot.Dobot(port=port, verbose=None)


device.suck(True) # 吸引ON

time.sleep(1) # 1秒待つ

device.suck(False) # 吸引OF