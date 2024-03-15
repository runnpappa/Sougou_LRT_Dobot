import sys
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import serial
from serial.tools import list_ports
import pydobot
import cv2
import numpy as np
import time

from motion.ArUco_Setup import setup as D_setup # ArUcoマーカー関連の関数
from motion.Color_Detection import color as D_color # 色を検出する関数
import motion.Dobot_Move as D_Dobot # Dobotを動かす関数
from motion.LRT_Senro import LRT_senro as L_senro
from motion.LRT_Object import LRT_object as L_object



# たまにカメラのポート番号が変わることがある(番号はUSBの認識順らしい)
D_capture1 = cv2.VideoCapture(2) # カメラ1
D_capture2 = cv2.VideoCapture(1) # カメラ2
D_capture3 = cv2.VideoCapture(0) # カメラ3
L_capture = cv2.VideoCapture(f"rtsp://192.168.1.1:7070/webcam/RTSP/1.0")  # 無線カメラ

# ウィンドウのサイズ
L_Size = np.array((600, 400))
D_Size = np.array((1280,960))
width, height = D_Size

# Dobotのポート指定
available_ports = list_ports.comports()
port = available_ports[2].device #port番号を指定 
device = pydobot.Dobot(port=port, verbose=None) # デバイスを指定 

#シリアル通信(PC⇔Arduino)
ser = serial.Serial()
ser.port = "COM3"     #デバイスマネージャでArduinoのポート確認
ser.baudrate = 115200 #Arduinoと合わせる
ser.setDTR(False)     #DTRを常にLOWにしReset阻止
ser.open()            #COMポートを開く

class Setting :
    trans_mat1 = None
    trans_mat2 = None
    trans_mat3 = None

    Obj_xy = np.array([0,0])
    Dbt_xy = np.array([0,0])
    Obj_xy_T = np.array([0,0])
    Dbt_xy_T = np.array([0,0])
    move = None

s = Setting() # インスタンス化


def Dobot(s):
    s.move = 1
    while(True):
        try:
            ret,frame0 = L_capture.read()
            ret,frame1 = D_capture1.read()
            ret,frame2 = D_capture2.read()
            ret,frame3 = D_capture3.read()
            frame1 = cv2.flip(frame1,-1) # カメラ1のx座標とDobotのxy座標の方向が逆だったので上下左右反転

            cap1 = cv2.resize(frame1,D_Size)
            cap2 = cv2.resize(frame2,D_Size)
            cap3 = cv2.resize(frame3,D_Size)

            cap1_trn = cv2.warpPerspective(cap1,s.trans_mat1,(width, height)) # カメラ1の台形変換後の画像
            cap2_trn = cv2.warpPerspective(cap2,s.trans_mat2,(width, height)) # カメラ2の台形変換後の画像

            if s.move != False:
                if s.move < 4:
                    if s.move == 1:
                        _,s.Obj_xy_T = D_color(cap2_trn,num=3)
                        capture,s.Dbt_xy_T = D_color(cap1_trn,num=1)

                    elif s.move == 2:
                        _,s.Obj_xy = D_color(cap2,num=3)
                        capture,s.Dbt_xy = D_color(cap2,num=2) 

                    elif s.move == 3:
                        _,s.Obj_xy = D_color(cap3,num=3)
                        capture,s.Dbt_xy = D_color(cap3,num=2)

                    D_Dobot.move(s,device,D_Size)

                elif s.move == 4:
                    D_Dobot.pick(s,device)
                    capture = cap2

                cv2.imshow("a",capture)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            elif s.move == False:
                break
        except:
            time.sleep(0.3)
            continue

device.move_to(130, 0, 0, 0, wait=True) # arucoマーカーが隠れないようにDobotを退避点まで移動
D_setup(s,D_Size,D_capture1,D_capture2,D_capture3) # arucoマーカーのセットアップ
device.move_to(200, 0, -8, 0, wait=True) # Dobotを初期位置に移動
print("ready") # 準備完了


while(L_capture.isOpened()): # 準備完了後,スタートするまで無線カメラの映像を映す
    _,frame = L_capture.read()
    frame = cv2.resize(frame,L_Size)
    frame = cv2.rotate(frame,cv2.ROTATE_90_COUNTERCLOCKWISE) # ウィンドウを90度回転
    cv2.imshow("a",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): # Qキーを押すとこのループを抜けてプログラムがスタートする
        break



while (L_capture.isOpened()):
    ret, frame = L_capture.read()  # 読み込み
    img = cv2.resize(frame, L_Size) # ウィンドウの大きさを変える
    img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE) # ウィンドウを90度回転

    Object,img_obj = L_object(img) # 物体検知 Objectには障害物があるかどうか　img_objには検出後の画像

    if Object == False: # 障害物がなかったら
        Senro,img_sen = L_senro(img) # 直線かどうかの判断
        cv2.imshow("a",img_sen)
        
        if Senro == True: # 直線だったら
            ser.write(b's') # 直線の信号

        elif Senro == False: # カーブだったら
            ser.write(b'c') # カーブの信号


    elif Object == True: # 障害物があったら
        ser.write(b'z') # 止まれの信号
        time.sleep(1)

        Dobot(s) # Dobotを動かす

        """
        障害物除去中

        """
        print("Dobot_compreat")
        time.sleep(1)

        while (Object != False): # 障害物が除去されたことを確認できるまで繰り返す
            ret, frame = L_capture.read()  # 読み込み
            img = cv2.resize(frame, L_Size) # ウィンドウの大きさを変える
            img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE) # ウィンドウを90度回転
            Object,img_obj = L_object(img) # 物体検知 Objectには障害物があるかどうか(NoneとTrueはどちらも文字列なので注意)　img_objには検出後の画像
            cv2.imshow("obj",img_obj)

        continue

    cv2.imshow("obj",img_obj)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



ser.write(b'z')
time.sleep(2)
device.close()
D_capture1.release()
D_capture2.release()
D_capture3.release()
L_capture.release()
ser.close()
cv2.destroyAllWindows()
sys.exit()


