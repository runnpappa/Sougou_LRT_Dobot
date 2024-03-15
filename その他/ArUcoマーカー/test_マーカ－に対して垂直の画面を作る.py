

# 4つのマーカーが検出できないとエラーが出ます

import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
from cv2 import aruco
import numpy as np

cap = cv2.VideoCapture(1)

ret, frame = cap.read()
frame = cv2.resize(frame,(1280,960))
size = frame.shape

focal_length = size[1] 
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
  

            image_points_2D = np.array(points[0],dtype="double") #画像上の座標(マーカー認識の結果)
            # データ型"double"は倍精度浮動小数点数で64ビットの浮動小数点数表現　numpyのnp.float64と同じ
            figure_points_3D = np.array([ # 画像上の点の３次元空間での座標 マーカーの四隅の座標と合わせてベクトルの計算に使ってるっぽい
                (-0.5,0.5,0.0),
                (0.5,0.5,0.0),
                (0.5,-0.5,0.0),
                (-0.5,-0.5,0.0),

            ])

            # 上記を対応させて姿勢などを算出する
            sus,rvec,tvec=cv2.solvePnP(figure_points_3D, image_points_2D,cameraMatrix,distCoeff) # susはsuccessの略　算出に成功するとTrueになる rvecは回転ベクトル tvecは平行移動ベクトル

            if id == 0:
                marker0_points = points
                marker0_rvec = rvec
                marker0_tvec = tvec
            elif id == 1:
                marker1_points = points
                marker1_rvec = rvec
                marker1_tvec = tvec
            elif id == 2:
                marker2_points = points
                marker2_rvec = rvec
                marker2_tvec = tvec
            else:
                marker3_points = points
                marker3_rvec = rvec
                marker3_tvec = tvec

            cv2.polylines(frame,np.array(points).astype(int),color=(255,0,255),isClosed=True,thickness=1) # 検出したマーカーの外側の輪郭線を描く
            cv2.drawMarker(frame,np.array(points[0][0]).astype(int),color=(255,0,255),markerType=cv2.MARKER_SQUARE,thickness=1,markerSize= 10) # マーカーの左上に四角い目印をつける
            cv2.putText(frame,str(id[0]),np.array(points[0][0]).astype(int),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.0,color=(255,0,0),thickness=2,lineType=cv2.LINE_AA) # マーカーのIDを表示



        

        point0_x = np.array((marker0_points[0][0][0] + marker3_points[0][3][0])/2)
        point0_y = np.array((marker3_points[0][3][1] + marker0_points[0][0][1])/2)
        point0 = np.array([point0_x,point0_y]) # 変形後の左下の座標
        point0_rvec = np.array((marker0_rvec + marker3_rvec)/2)
        point0_tvec = np.array((marker0_tvec + marker3_tvec)/2)
        end_point3D_0 = np.array([[-0.5,-0.5,4]])
        end_point2D_0,_ = cv2.projectPoints(end_point3D_0,point0_rvec,point0_tvec,cameraMatrix,distCoeff) # 3D座標を2D座標に投影
        start_point2D_0 = np.array([[point0]]) # 高さの線の始点

        point0s = (int(start_point2D_0[0][0][0]),int(start_point2D_0[0][0][1])) # 始点の配列を整数のタプル型で展開
        point0e = (int(end_point2D_0[0][0][0]),int(end_point2D_0[0][0][1])) # 終点の配列を整数のタプル型で展開
        cv2.line(frame,point0s,point0e,(0,255,0),1) # 始点から終点へ線を描く これが高さの線になる



        point1_x = np.array((marker1_points[0][1][0] + marker2_points[0][2][0])/2)
        point1_y = np.array((marker2_points[0][2][1] + marker1_points[0][1][1])/2)
        point1 = np.array([point1_x,point1_y]) # 変形後の右下の座標
        point1_rvec = np.array((marker1_rvec + marker2_rvec)/2)
        point1_tvec = np.array((marker1_tvec + marker2_tvec)/2)
        end_point3D_1 = np.array([[0.5,-0.5,4]]) # 3次元座標に高さをプラスする 1の場合(マーカーの1辺の長さ×1)
        end_point2D_1,_ = cv2.projectPoints(end_point3D_1,point1_rvec,point1_tvec,cameraMatrix,distCoeff) # 3D座標を2D座標に投影
        start_point2D_1 = np.array([[point1]]) # 高さの線の始点

        point1s = (int(start_point2D_1[0][0][0]),int(start_point2D_1[0][0][1])) # 始点の配列を整数のタプル型で展開
        point1e = (int(end_point2D_1[0][0][0]),int(end_point2D_1[0][0][1])) # 終点の配列を整数のタプル型で展開
        cv2.line(frame,point1s,point1e,(0,255,0),1) # 始点から終点へ線を描く これが高さの線になる   

        cv2.line(frame,point0s,point1s,(0,255,0),1)
        cv2.line(frame,point0e,point1e,(0,255,0),1)

        m = np.empty((4,2)) # 要素数2の配列を4行作る
        m[0] = point0e
        m[1] = point1e
        m[2] = point1s
        m[3] = point0s

        width, height = (1280,960) # 変形後画像サイズ
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
