# 参考
# https://tech.hipro-job.jp/column/771
# https://office54.net/python/class-insatance-variable

import sys
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

from serial.tools import list_ports
import pydobot
import cv2
import numpy as np
import time
import threading

from ArUco_Setup import setup # ArUcoマーカー関連の関数
from Color_Detection import color # 色を検出する関数
import Dobot_Move as Dobot # Dobotを動かす関数


# たまにカメラのポート番号が変わることがある(番号はUSBの認識順らしい)
capture1 = cv2.VideoCapture(2) # カメラ1
capture2 = cv2.VideoCapture(1) # カメラ2
capture3 = cv2.VideoCapture(0) # カメラ3

# ウィンドウのサイズ
Size = np.array((1280,960))
width, height = Size

# Dobotのポート指定
available_ports = list_ports.comports()
port = available_ports[2].device #port番号を指定 
device = pydobot.Dobot(port=port, verbose=None) # デバイスを指定 

# 動画ファイル保存用の設定
# fps = int(cap1.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
# video = cv2.VideoWriter('video.mp4', fourcc, fps, (width, height))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
 
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

def Capture(s): # カメラのプログラム
    while (capture1.isOpened() and capture2.isOpened() and capture3.isOpened()): # キャプチャーが有効なら

        ret,frame1 = capture1.read()
        ret,frame2 = capture2.read()
        ret,frame3 = capture3.read()
        frame1 = cv2.flip(frame1,-1) # カメラ1のx座標とDobotのxy座標の方向が逆だったので上下左右反転

        cap1 = cv2.resize(frame1,Size)
        cap2 = cv2.resize(frame2,Size)
        cap3 = cv2.resize(frame3,Size)

        cap1_trn = cv2.warpPerspective(cap1,s.trans_mat1,(width, height)) # カメラ1の台形変換後の画像
        cap2_trn = cv2.warpPerspective(cap2,s.trans_mat2,(width, height)) # カメラ2の台形変換後の画像
        # cap3_trn = cv2.warpPerspective(cap3,s.trans_mat3,(height, width)) # カメラ3の台形変換後の画像 (今回は使ってない)

        if s.move == 1:
            _,s.Obj_xy_T = color(cap2_trn,num=3)
            capture,s.Dbt_xy_T = color(cap1_trn,num=1)

        elif s.move == 2:
            _,s.Obj_xy = color(cap2,num=3)
            capture,s.Dbt_xy = color(cap2,num=2) 

        elif s.move == 3:
            _,s.Obj_xy = color(cap3,num=3)
            capture,s.Dbt_xy = color(cap3,num=2)

        else:
            capture = cap2
            
        cv2.imshow("a",capture)
        # video.write(capture)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def Tracking(s): # Dobotのプログラム

    # s.move == 1       カメラ1で調整(上から)
    # s.move == 2       カメラ2で調整(側面から)
    # s.move == 3       カメラ3で調整(正面から)
    # s.move == 4       吸引
    # s.move == False   動作完了

    while(True):
        if s.move != False:
            if s.move < 4:
                Dobot.move(s,device,Size)
            elif s.move == 4:
                Dobot.pick(s,device)

        elif s.move == False:
            break


thread_1 = threading.Thread(target=Capture,args=(s,)) # スレッドを定義　argsは引数 引数が一つの場合でもカンマをつける必要がある
thread_2 = threading.Thread(target=Tracking,args=(s,))


device.move_to(130, 0, 0, 0, wait=True) # arucoマーカーが隠れないようにDobotを退避点まで移動
setup(s,Size,capture1,capture2,capture3) # arucoマーカーのセットアップ
device.move_to(200, 0, -8, 0, wait=True) # Dobotを初期位置に移動
print("ready") # 準備完了

while(True): # 準備完了後,スタートするまでカメラ2の映像を映す
    _,frame = capture2.read()
    frame = cv2.resize(frame,Size)
    cv2.imshow("0",frame)
    # video.write(frame) # 映像保存用

    if cv2.waitKey(1) & 0xFF == ord('q'): # Qキーを押すとこのループを抜けてプログラムがスタートする
        break

cv2.destroyWindow("0")

s.move = 1
thread_1.start() # カメラのプログラムスタート
time.sleep(1) # 一秒待つ
thread_2.start() # Dobotのプログラムスタート

"""
プログラム実行中
"""

thread_2.join() # Dobotの動きがすべて終了するまで待機
time.sleep(1)
device.close()
capture1.release()
capture2.release()
capture3.release()
cv2.destroyAllWindows()
sys.exit()
