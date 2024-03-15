def setup1(s,cap0,cap1,Size):
    import numpy as np
    import cv2
    from cv2 import aruco

    # マーカー検出用の設定
    width, height = (Size) # 変形後画像サイズ
    
    mark_height = 0.9 # マークの高さ

    p_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    detector=aruco.ArucoDetector(p_dict)
    true_coordinates  = np.float32([[0,0],[width,0],[width,height],[0,height]]) # カメラに対して平行な面
    focal_length = Size[1]
    center = (Size[1]/2, Size[0]/2) # 画面の中心座標
    fx,fy,cx,cy=focal_length,focal_length,center[0],center[1] #fx,fyは焦点の座標      cx,cyは画面の中心座標
    cameraMatrix=np.array([[fx,0,cx],[0,fy,cy],[0,0,1]])
    distCoeff=np.zeros((4,1)) # カメラによって発生する歪みに対処するために必要
    figure_points_3D = np.array([ # 画像上の点の３次元空間での座標
                (-0.5,0.5,0.0),
                (0.5,0.5,0.0),
                (0.5,-0.5,0.0),
                (-0.5,-0.5,0.0),
            ])

    # カメラ１のマーカー検出
    _,frame0 = cap0.read()
    frame0 = cv2.resize(frame0,Size)
    corners0,ids0,_= detector.detectMarkers(frame0)
    if len(corners0)>0: # もしマーカーが検出されたら
        m0 = np.empty((4,2)) # 要素数2の配列を4行作る
        for points,id in zip (corners0,ids0): # zip関数を使ってマーカーの四隅の座標とIDを紐づける
            image_points_2D = np.array(points[0],dtype="double") #画像上の座標(マーカー認識の結果)
            # データ型"double"は倍精度浮動小数点数で64ビットの浮動小数点数表現　numpyのnp.float64と同じ

            # 上記を対応させて姿勢などを算出する
            sus,rvec,tvec=cv2.solvePnP(figure_points_3D, image_points_2D,cameraMatrix,distCoeff) # susはsuccessの略　算出に成功するとTrueになる rvecは回転ベクトル tvecは平行移動ベクトル

            for point2,point3 in zip(image_points_2D[id],figure_points_3D[id]): # zip関数で3D座標上の点と2D座標上の点を紐づける
                end_point3D = point3+np.array([[0,0,mark_height]]) # 3次元座標に高さをプラスする 1の場合(マーカーの1辺の長さ×1)
                start_point2D = np.array([[point2]]) # 高さの線の始点
                end_point2D,_ = cv2.projectPoints(end_point3D,rvec,tvec,cameraMatrix,distCoeff) # 3D座標を2D座標に投影

                point1 = (int(start_point2D[0][0][0]),int(start_point2D[0][0][1])) # 始点の配列を整数のタプル型で展開
                point2 = (int(end_point2D[0][0][0]),int(end_point2D[0][0][1])) # 終点の配列を整数のタプル型で展開
                m0[id] = point2
        marker_coordinates0 = np.float32(m0) # 四隅のマーカーの中心座標(カメラに対して斜めの面)
        s.trans_mat0 = cv2.getPerspectiveTransform(marker_coordinates0,true_coordinates) # 任意の四角形から別の任意の四角形への変換 引数のデータ型はfloat32でないといけないらしい

    # カメラ2のマーカー検出
    _,frame1 = cap1.read()
    frame1 = cv2.resize(frame1,Size)
    corners1,ids1,_= detector.detectMarkers(frame1) # 画像からマーカーを検出する
    if len(corners1)>0: # もしマーカーが検出されたら
            m1 = np.empty((4,2)) # 要素数2の配列を4行作る
            for points,id in zip (corners1,ids1): # zip関数を使ってマーカーの四隅の座標とIDを紐づける
                image_points_2D = np.array(points[0],dtype="double") #画像上の座標(マーカー認識の結果)
                # データ型"double"は倍精度浮動小数点数で64ビットの浮動小数点数表現　numpyのnp.float64と同じ

                # 上記を対応させて姿勢などを算出する
                sus,rvec,tvec=cv2.solvePnP(figure_points_3D, image_points_2D,cameraMatrix,distCoeff) # susはsuccessの略　算出に成功するとTrueになる rvecは回転ベクトル tvecは平行移動ベクトル

                for point2,point3 in zip(image_points_2D[id],figure_points_3D[id]): # zip関数で3D座標上の点と2D座標上の点を紐づける
                    end_point3D = point3+np.array([[0,0,mark_height]]) # 3次元座標に高さをプラスする 1の場合(マーカーの1辺の長さ×1)
                    start_point2D = np.array([[point2]]) # 高さの線の始点
                    end_point2D,_ = cv2.projectPoints(end_point3D,rvec,tvec,cameraMatrix,distCoeff) # 3D座標を2D座標に投影

                    point1 = (int(start_point2D[0][0][0]),int(start_point2D[0][0][1])) # 始点の配列を整数のタプル型で展開
                    point2 = (int(end_point2D[0][0][0]),int(end_point2D[0][0][1])) # 終点の配列を整数のタプル型で展開
                    m1[id] = point2
            marker_coordinates1 = np.float32(m1) # 四隅のマーカーの中心座標(カメラに対して斜めの面)
            s.trans_mat1 = cv2.getPerspectiveTransform(marker_coordinates1,true_coordinates) # 任意の四角形から別の任意の四角形への変換

