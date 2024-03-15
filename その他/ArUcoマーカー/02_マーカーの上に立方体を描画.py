# 参考
# https://qiita.com/am8/items/5c5343a21c9b27bbb2c0
# https://docs.opencv.org/4.8.0/d9/d0c/group__calib3d.html#ga549c2075fac14829ff4a58bc931c033d


import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
from cv2 import aruco
import numpy as np

cap = cv2.VideoCapture(2)

ret, frame = cap.read()
frame = cv2.resize(frame,(1280,960))
size = frame.shape

focal_length = size[1] # 縦の長さ?
center = (size[1]/2, size[0]/2) # 画面の中心座標

fx,fy,cx,cy=focal_length,focal_length,center[0],center[1] #fx,fyは焦点の座標      cx,cyは画面の中心座標
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
            

            image_points_2D = np.array(points[0],dtype="double") #画像上の座標(マーカー認識の結果)
            # データ型"double"は倍精度浮動小数点数で64ビットの浮動小数点数表現　numpyのnp.float64と同じ

      

            figure_points_3D = np.array([ # 画像上の点の３次元空間での座標 マーカーの四隅の座標と合わせてベクトルの計算に使ってるっぽい
                (-0.5,0.5,0.0),
                (0.5,0.5,0.0),
                (0.5,-0.5,0.0),
                (-0.5,-0.5,0.0),

                # openCVのsolvePnPのページには以下の記載がある
                # Special case suitable for marker pose estimation. Number of input points must be 4. Object points must be defined in the following order:
                    # point 0: [-squareLength / 2, squareLength / 2, 0]
                    # point 1: [ squareLength / 2, squareLength / 2, 0]
                    # point 2: [ squareLength / 2, -squareLength / 2, 0]
                    # point 3: [-squareLength / 2, -squareLength / 2, 0]

                # マーカーの一辺の長さを1/2にする(= 0.5をかけるってこと?)
            ])

            # objPoints= image_points_2D
            # 上記を対応させて姿勢などを算出する
            sus,rvec,tvec=cv2.solvePnP(figure_points_3D, image_points_2D,cameraMatrix,distCoeff) # susはsuccessの略　算出に成功するとTrueになる rvecは回転ベクトル tvecは平行移動ベクトル

  

            cv2.polylines(frame,np.array(points).astype(int),color=(255,0,255),isClosed=True,thickness=1) # 検出したマーカーの外側の輪郭線を描く
            cv2.drawMarker(frame,np.array(points[0][0]).astype(int),color=(255,0,255),markerType=cv2.MARKER_SQUARE,thickness=1,markerSize= 10) # マーカーの左上に四角い目印をつける
            cv2.putText(frame,str(id[0]),np.array(points[0][0]).astype(int),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.0,color=(255,0,0),thickness=2,lineType=cv2.LINE_AA) # マーカーのIDを表示

            # 高さに当たる辺の描画
            for point2,point3 in zip(image_points_2D,figure_points_3D): # zip関数で3D座標上の点と2D座標上の点を紐づける

    

                end_point3D = point3+np.array([[0,0,1]]) # 3次元座標に高さをプラスする 1の場合(マーカーの1辺の長さ×1)
                start_point2D = np.array([[point2]]) # 高さの線の始点
                end_point2D,_ = cv2.projectPoints(end_point3D,rvec,tvec,cameraMatrix,distCoeff) # 3D座標を2D座標に投影

                point1 = (int(start_point2D[0][0][0]),int(start_point2D[0][0][1])) # 始点の配列を整数のタプル型で展開
                point2 = (int(end_point2D[0][0][0]),int(end_point2D[0][0][1])) # 終点の配列を整数のタプル型で展開

                cv2.line(frame,point1,point2,(0,255,0),1) # 始点から終点へ線を描く これが高さの線になる

            
            # 上面に対応する辺の描画
            for i in range(4):
                end_point3D = figure_points_3D[i]+np.array([[0,0,1]]) # [[-0.5 0.5 1.]]
                end_point2D,_ = cv2.projectPoints(end_point3D,rvec,tvec,cameraMatrix,distCoeff) 
                point1 = (int(end_point2D[0][0][0]),int(end_point2D[0][0][1]))

                start_point3D = figure_points_3D[(i+1)%4]+np.array([[0,0,1]]) # 上辺の始点 終点と被らないように(i+1)%4という計算を入れている
                start_point2D,_ = cv2.projectPoints(start_point3D,rvec,tvec,cameraMatrix,distCoeff)
                point2 = (int(start_point2D[0][0][0]),int(start_point2D[0][0][1]))

                cv2.line(frame,point1,point2,(0,255,0),1) # 上面の辺を描く

                if i==0:
                    cv2.drawMarker(frame, point1,color=(255,255),markerType=cv2.MARKER_SQUARE,thickness=1,markerSize=10) # 描画した立方体の始点に目印をつける
        
    # GUIに表示
    cv2.imshow("Camera",frame)
    # qキーが押されたら途中終了
    if cv2.waitKey(1) == ord("q"):
        break


# 終了処理
cap.release()
cv2.destroyAllWindows()
