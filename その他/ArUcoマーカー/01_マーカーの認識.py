# 参考
# https://www.delftstack.com/ja/howto/python/opencv-solvepnp/
# https://docs.opencv.org/4.8.0/d2/d1a/classcv_1_1aruco_1_1ArucoDetector.html#a0c1d14251bf1cbb06277f49cfe1c9b61

import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
from cv2 import aruco
import numpy as np

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
frame = cv2.resize(frame,(960,1280))
size = frame.shape

focal_length = size[1] # 縦の長さ?
center = (size[1]/2, size[0]/2) # 画面の中心座標

fx,fy,cx,cy=focal_length,focal_length,center[0],center[1] #fx,fyは      cx,cyは画面の中心座標
cameraMatrix=np.array([[fx,0,cx],[0,fy,cy],[0,0,1]])

distCoeff=np.zeros((4,1)) # カメラによって発生する歪みに対処するために必要
# print(distCoeff)

marker_type=aruco.DICT_4X4_50
dict_aruco = aruco.getPredefinedDictionary(marker_type) # ARマーカーは「4x4ドット，ID番号50まで」の辞書を使う


detector=aruco.ArucoDetector(dict_aruco)

while(cap.isOpened()): # キャプチャーが有効なら
    ret,frame = cap.read()
    frame = cv2.resize(frame,(1280,960))
    corners,ids,rejectedCandidates = detector.detectMarkers(frame) # 映像からマーカーを検出する 戻り値:検出されたマーカーの四隅の座標 マーカーのID(配列) 3つ目は検出された候補?

    if len(corners)>0: # もしマーカーが検出されたら
        for points,id in zip (corners,ids): # zip関数を使ってマーカーの四隅の座標とIDを紐づける
        # for文で複数の変数にそれぞれ値を入れるにはzipを使う

            cv2.polylines(frame,np.array(points).astype(int),color=(255,0,255),isClosed=True,thickness=1) # 検出したマーカーの外側の輪郭線を描く
            cv2.drawMarker(frame,np.array(points[0][0]).astype(int),color=(255,0,255),markerType=cv2.MARKER_SQUARE,thickness=1,markerSize= 10) # マーカーの左上に四角い目印をつける
            cv2.putText(frame,str(id[0]),np.array(points[0][0]).astype(int),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.0,color=(255,0,0),thickness=2,lineType=cv2.LINE_AA) # マーカーのIDを表示

    # GUIに表示
    cv2.imshow("Camera",frame)
    # qキーが押されたら途中終了
    if cv2.waitKey(1) == ord("q"):
        break


# 終了処理
cap.release()
cv2.destroyAllWindows()