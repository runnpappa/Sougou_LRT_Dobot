from serial.tools import list_ports
import pydobot
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import threading

available_ports = list_ports.comports()
port = available_ports[2].device #port番号を指定 
device = pydobot.Dobot(port=port, verbose=None) # デバイスを指定
(x, y, z, r, j1, j2, j3, j4) = device.pose() # 取得した座標をそれぞれ格納　
print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

endflag = 0
capture = cv2.VideoCapture(0)
windowsize = (800,600)

def Camera():
    global endflag
    while(True):
        ret, frame = capture.read()
        frame = cv2.resize(frame,windowsize)
        cv2.imshow('title',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
             endflag = 1
             break
        

def Dobot():
    while(True):
        device.move_to(x+30, y, z, r, wait=True)
        device.move_to(x+30,y+30,z,r,wait=True)
        device.move_to(x,y+30,z,r,wait=True)
        device.move_to(x, y, z, r, wait=True)
        if cv2.waitKey(1) & endflag == 1:
             break
             

thread_1 = threading.Thread(target=Camera)
thread_2 = threading.Thread(target=Dobot)

thread_1.start()
thread_2.start()

thread_1.join() 
thread_2.join()

device.close()
capture.release()
cv2.destroyAllWindows()
