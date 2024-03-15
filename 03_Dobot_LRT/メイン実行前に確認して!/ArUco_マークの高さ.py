
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
from cv2 import aruco
import numpy as np

cap = cv2.VideoCapture(1) # カメラ2

ret, frame = cap.read()
frame = cv2.resize(frame,(1280,960))
size = frame.shape
width = 1280
height = 960

focal_length = size[1] # 縦の長さ?
center = (size[1]/2, size[0]/2) # 画面の中心座標

fx,fy,cx,cy=focal_length,focal_length,center[0],center[1] #fx,fyは焦点の座標      cx,cyは画面の中心座標
cameraMatrix=np.array([[fx,0,cx],[0,fy,cy],[0,0,1]])

distCoeff=np.zeros((4,1)) # カメラによって発生する歪みに対処するために必要

mark_height = 0.9
marker_type=aruco.DICT_4X4_50
dict_aruco = aruco.getPredefinedDictionary(marker_type) # ARマーカーは「4x4ドット，ID番号50まで」の辞書を使う


detector=aruco.ArucoDetector(dict_aruco)

while(cap.isOpened()): # キャプチャーが有効なら
    ret,frame = cap.read()
    frame = cv2.resize(frame,(1280,960))
    corners,ids,rejectedCandidates = detector.detectMarkers(frame) # 映像からマーカーを検出する 戻り値:検出されたマーカーの四隅の座標 マーカーのID(配列) 3つ目は検出された候補?

    if len(corners)>0: # もしマーカーが検出されたら
        m = np.empty((4,2)) # 要素数2の配列を4行作る
   
        for points,id in zip (corners,ids): # zip関数を使ってマーカーの四隅の座標とIDを紐づける
            image_points_2D = np.array(points[0],dtype="double") #画像上の座標(マーカー認識の結果)
            # データ型"double"は倍精度浮動小数点数で64ビットの浮動小数点数表現　numpyのnp.float64と同じ
            figure_points_3D = np.array([ # 画像上の点の３次元空間での座標 マーカーの四隅の座標と合わせてベクトルの計算に使ってるっぽい
                (-0.5,0.5,0.0),
                (0.5,0.5,0.0),
                (0.5,-0.5,0.0),
                (-0.5,-0.5,0.0),
            ])

            # objPoints= image_points_2D
            # 上記を対応させて姿勢などを算出する
            sus,rvec,tvec=cv2.solvePnP(figure_points_3D, image_points_2D,cameraMatrix,distCoeff) # susはsuccessの略　算出に成功するとTrueになる rvecは回転ベクトル tvecは平行移動ベクトル
            cv2.polylines(frame,np.array(points).astype(int),color=(255,0,255),isClosed=True,thickness=1) # 検出したマーカーの外側の輪郭線を描く
            cv2.drawMarker(frame,np.array(points[0][0]).astype(int),color=(255,0,255),markerType=cv2.MARKER_SQUARE,thickness=1,markerSize= 10) # マーカーの左上に四角い目印をつける
            cv2.putText(frame,str(id[0]),np.array(points[0][0]).astype(int),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.0,color=(255,0,0),thickness=2,lineType=cv2.LINE_AA) # マーカーのIDを表示

            # 高さに当たる辺の描画
            for point2,point3 in zip(image_points_2D[id],figure_points_3D[id]): # zip関数で3D座標上の点と2D座標上の点を紐づける
                end_point3D = point3+np.array([[0,0,mark_height]]) # 3次元座標に高さをプラスする 1の場合(マーカーの1辺の長さ×1)
                start_point2D = np.array([[point2]]) # 高さの線の始点
                end_point2D,_ = cv2.projectPoints(end_point3D,rvec,tvec,cameraMatrix,distCoeff) # 3D座標を2D座標に投影

                point1 = (int(start_point2D[0][0][0]),int(start_point2D[0][0][1])) # 始点の配列を整数のタプル型で展開
                point2 = (int(end_point2D[0][0][0]),int(end_point2D[0][0][1])) # 終点の配列を整数のタプル型で展開

                cv2.line(frame,point1,point2,(0,255,0),3) # 始点から終点へ線を描く これが高さの線になる
              
                m[id] = point2
                
        # 上面に対応する辺の描画
        for i in range(4):
            point1 = np.array(m[i],dtype = int)
            point2 = np.array(m[(i+1)%4],dtype = int)
            cv2.line(frame,point1,point2,(0,255,0),3) # 上面の辺を描く
            if i==0:
                cv2.drawMarker(frame, point1,color=(255,255),markerType=cv2.MARKER_SQUARE,thickness=1,markerSize=10) # 描画した立方体の始点に目印をつける

        marker_coordinates = np.float32(m) # 四隅のマーカーの中心座標(カメラに対して斜めの面)
        true_coordinates   = np.float32([[0,0],[width,0],[width,height],[0,height]]) # カメラに対して平行な面
        trans_mat = cv2.getPerspectiveTransform(marker_coordinates,true_coordinates) # 任意の四角形から別の任意の四角形への変換 引数のデータ型はfloat32でないといけないらしい
        img_trans = cv2.warpPerspective(frame,trans_mat,(width, height))
    # GUIに表示
    cv2.imshow("Camera",frame)
    cv2.imshow("img_trans",img_trans)
    # qキーが押されたら途中終了
    if cv2.waitKey(1) == ord("q"):
        break


# 終了処理
cap.release()
cv2.destroyAllWindows()
