# 参考
# https://qiita.com/code0327/items/c6e468da7007734c897f　
# https://note.nkmk.me/python-opencv-warp-affine-perspective/


import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
from cv2 import aruco
import numpy as np

cap = cv2.VideoCapture(0)
p_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
detector=aruco.ArucoDetector(p_dict)


while(cap.isOpened()):
    ret,frame = cap.read()
    frame = cv2.resize(frame,(1200,900))
    corners,ids,rejectedCandidates = detector.detectMarkers(frame) # 映像からマーカーを検出する

    # 時計回りで左上から順にマーカーの「中心座標」を m に格納
    m = np.empty((4,2)) # 要素数2の配列を4行作る

    # for i,c in zip(ids.ravel(), corners): # ravel関数は多次元配列を一次元配列に変換する 
    #     m[i] = c[0].mean(axis=0) # cには[四隅の座標,dtype]の二つのデータが入っているので四隅の座標のみを取り出し、その平均値(=マーカーの中心座標)を求めている


    corners2 = [np.empty((1,4,2))]*4
    for i,c in zip(ids.ravel(), corners):
        corners2[i] = c.copy()
    m[0] = corners2[0][0][0]
    m[1] = corners2[1][0][1]
    m[2] = corners2[2][0][2]
    m[3] = corners2[3][0][3]


    

    width, height = (1200,900) # 変形後画像サイズ

    marker_coordinates = np.float32(m) # 四隅のマーカーの中心座標(カメラに対して斜めの面)
    true_coordinates   = np.float32([[0,0],[width,0],[width,height],[0,height]]) # カメラに対して平行な面
    trans_mat = cv2.getPerspectiveTransform(marker_coordinates,true_coordinates) # 任意の四角形から別の任意の四角形への変換 引数のデータ型はfloat32でないといけないらしい
    img_trans = cv2.warpPerspective(frame,trans_mat,(width, height))

    point0 = np.array(m[0],dtype = int)
    point1 = np.array(m[1],dtype = int)
    point2 = np.array(m[2],dtype = int)
    point3 = np.array(m[3],dtype = int)

    # print(point0)
    cv2.line(frame,point0,point1,(0,255,0),8)
    cv2.line(frame,point1,point2,(0,255,0),8)
    cv2.line(frame,point2,point3,(0,255,0),8)
    cv2.line(frame,point3,point0,(0,255,0),8)
    # frame = cv2.flip(frame,-1)


    cv2.imshow("img_trans",img_trans)
    cv2.imshow("img",frame)
        # qキーが押されたら途中終了
    if cv2.waitKey(1) == ord("q"):
        break

# 終了処理
cap.release()
cv2.destroyAllWindows()

