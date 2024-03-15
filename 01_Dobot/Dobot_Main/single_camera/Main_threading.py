import sys
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"


from serial.tools import list_ports
import pydobot


from Red import red
from Yellow import yellow
from Dobot import dobot
import cv2
import threading


available_ports = list_ports.comports()
port = available_ports[2].device #port番号を指定 
device = pydobot.Dobot(port=port, verbose=None) # デバイスを指定 
# (x, y, z, r, j1, j2, j3, j4) = device.pose() # 取得した座標をそれぞれタプル型で格納　

cap = cv2.VideoCapture(0)
Size = (1200,800)


try:
    class point : # 関数Captureで返ってきた値を関数Trackingで使いたいのでクラスを利用する
        point = None

    def Capture(p):
        while (True):
            frame = cap.read()[1]
            frame = cv2.resize(frame,Size)
            frame = cv2.flip(frame,1) # カメラのx座標とDobotのx座標の方向が逆だったので左右反転
            

            frame,red_jx,red_jy = red(frame) # 赤色検出を実行　座標が描画された画像と検出された中心座標が返ってくる
            frame,yel_jx,yel_jy = yellow(frame) # 黄色検出を実行

            cv2.imshow('title1',frame)
            cv2.waitKey(1)

            p.point = (red_jx,red_jy,yel_jx,yel_jy) # 返ってきたそれぞれの中心座標をpointにまとめて入れる
    
    def Tracking(p):
        while(True):
            if p.point == None:
                pass
            else:
                dobot(device,p.point)

    p = point()
    
    thread_1 = threading.Thread(target=Capture,args=(p,)) #argsは引数 引数が一つの場合でもカンマをつける必要がある
    thread_2 = threading.Thread(target=Tracking,args=(p,))

    thread_1.start()
    thread_2.start()

except:
    device.close()
    cap.release()
    cv2.destroyAllWindows()
    sys.exit()
