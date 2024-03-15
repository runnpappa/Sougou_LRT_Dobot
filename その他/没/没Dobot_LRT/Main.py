import sys
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import serial
import cv2
from cv2 import aruco
import numpy as np
import time
import copy
from serial.tools import list_ports
import pydobot


import motion.Dobot as D_dobot
from motion.Dobot_object import DBT_obj as D_object
from motion.Dobot_Yellow import yellow as D_yellow
from motion.Dobot_Green import green as D_green
from motion.Dobot_Setup1 import setup1 as D_setup1
from motion.Dobot_Setup2 import setup2 as D_setup2
from motion.LRT_Senro import LRT_senro as L_senro
from motion.LRT_Object import LRT_object as L_object




class setting :
    trans_mat0 = None
    trans_mat1 = None
    trans_mat1_a = None
    trans_mat2_a = None
    yel = None
    test_a = None
    test_b = None
    grn_a = None
    grn_b = None
    move = 0

# たまにカメラのポート番号が変わることがある(番号はUSBの認識順らしい)
D_cap0 = cv2.VideoCapture(0)
D_cap1 = cv2.VideoCapture(2)
D_cap2 = cv2.VideoCapture(1)
L_cap = cv2.VideoCapture(f"rtsp://192.168.1.1:7070/webcam/RTSP/1.0")  # キャプチャの準備 

L_Size = np.array((600, 400))
D_Size = np.array((1280,960))

width, height = D_Size # 変形後画像サイズ
line_Color = ([0,100,255])
available_ports = list_ports.comports()
port = available_ports[2].device #port番号を指定 
device = pydobot.Dobot(port=port, verbose=None) # デバイスを指定 

#シリアル通信(PC⇔Arduino)
ser = serial.Serial()
ser.port = "COM3"     #デバイスマネージャでArduinoのポート確認
ser.baudrate = 115200 #Arduinoと合わせる
ser.setDTR(False)     #DTRを常にLOWにしReset阻止
ser.open()            #COMポートを開く



# # 動画ファイル保存用の設定
# fps = int(D_cap0.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
# video = cv2.VideoWriter('video.mp4', fourcc, fps, (width, height))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
 


s = setting()

def Dobot(s):
    s.move = 1
    while(True):
        try:
            ret, frame = L_cap.read()  # 読み込み
            _,frame0 = D_cap0.read()
            _,frame1 = D_cap1.read()
            _,frame2 = D_cap2.read()

            frame0 = cv2.resize(frame0,D_Size)
            frame1 = cv2.resize(frame1,D_Size)
            frame2 = cv2.resize(frame2,D_Size)

            frame_o = cv2.warpPerspective(frame1,s.trans_mat1,(width, height))
            frame_g1 = cv2.warpPerspective(frame1,s.trans_mat1_a,(width, height))# Dobotの座標(カメラ1)
            frame_g2 = cv2.warpPerspective(frame2,s.trans_mat2_a,(width,height)) # Dobotの座標(カメラ2)
            frame_y = cv2.warpPerspective(frame0,s.trans_mat0,(width, height)) # Dobotの座標(上)
            frame0 = cv2.flip(frame0,-1) # カメラのx座標とDobotのxy座標の方向が逆だったので上下左右反転
            frame_g2 = cv2.resize(frame_g2,(height,width)) 

            if s.move == 1:
                print("move1")
                D_yellow(s,frame_y) # 黄色検出を実行
                D_object(s,frame_o, flag = True) # 物体検出を実行
                cv2.waitKey(1)
                if all(s.yel) == True:
                    D_dobot.move1(s,device,s.yel,s.test_a)
                else:
                    continue

            elif s.move == 2:
                D_green(s,frame_g1,flag = True)
                D_green(s,frame1,flag = None)
                D_object(s,frame1,flag = None)
                cv2.imshow("a",frame1) 
                cv2.waitKey(1)
                if all(s.grn_a) == True:
                    
                    D_dobot.move2(s,device,s.test_a,s.test_b,s.grn_a,s.grn_b)
                else:
                    continue

            elif s.move == 3:
                D_green(s,frame_g2,flag = True)
                D_green(s,frame2,flag = None)
                D_object(s,frame2,flag = None)
                cv2.imshow("a",frame2)
                cv2.waitKey(1)

                if all(s.grn_a) == True:
                    D_dobot.move3(s,device,s.test_a,s.test_b,s.grn_a,s.grn_b)
                else:
                    continue

            elif s.move == 4:
                D_dobot.pick(s,device)

            else:
                cv2.destroyWindow("a")
                break

        except:
            time.sleep(0.5)
            continue



device.move_to(130, 0, -10, 0, wait=True)
D_setup1(s,D_cap0,D_cap1,D_Size)
D_setup2(s,D_cap1,D_cap2,D_Size)
device.move_to(200, 0, -10, 0, wait=True)
print("ready")

while(L_cap.isOpened()):
    _,frame1 = L_cap.read()
    frame1 = cv2.resize(frame1,L_Size)
    frame1 = cv2.rotate(frame1,cv2.ROTATE_90_COUNTERCLOCKWISE) # ウィンドウを90度回転

    cv2.imshow("a",frame1)
    # video.write(frame1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# cv2.destroyWindow("0")


while L_cap.isOpened():
    ret, frame = L_cap.read()  # 読み込み
    img = cv2.resize(frame, L_Size) # ウィンドウの大きさを変える
    img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE) # ウィンドウを90度回転

    Object,img_obj = L_object(img) # 物体検知 Objectには障害物があるかどうか(NoneとTrueはどちらも文字列なので注意)　img_objには検出後の画像

    if Object == False: # 障害物がなかったら
        Senro,img_sen = L_senro(img) # 直線かどうかの判断
        cv2.imshow("a",img_sen)
        
        if Senro == True: # 直線だったら
            ser.write(b's') 

        elif Senro == False: # カーブだったら
            ser.write(b'c')


    elif Object == True: # 障害物があったら
        ser.write(b'z') # 止まれの信号
        time.sleep(1)
        Dobot(s)
        
        print("Dobot_compreat")
        time.sleep(1)

        while (Object != False):
            ret, frame = L_cap.read()  # 読み込み
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
ser.close()
cv2.destroyAllWindows()
sys.exit()


