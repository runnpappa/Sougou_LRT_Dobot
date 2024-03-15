def setup2(s,cap1,cap2,Size):
    import numpy as np
    import cv2
    from cv2 import aruco

        # マーカー検出用の設定
    width, height = (Size) # 変形後画像サイズ
    p_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    detector=aruco.ArucoDetector(p_dict)
    true_coordinates  = np.float32([[0,0],[width,0],[width,height],[0,height]]) # カメラに対して平行な面
    center = (height/2, width/2) # 画面の中心座標
    focal_length = height
    fx,fy,cx,cy=focal_length,focal_length,center[0],center[1] #fx,fyは焦点の座標  cx,cyは画面の中心座標
    cameraMatrix=np.array([[fx,0,cx],[0,fy,cy],[0,0,1]])
    distCoeff=np.zeros((4,1)) # カメラによって発生する歪みに対処するために必要


    # カメラ2でマーカーに対して垂直の面をとる
    _,frame1 = cap1.read()
    frame1 = cv2.resize(frame1,Size)
    corners1,ids1,_= detector.detectMarkers(frame1) # 画像からマーカーを検出する
    
    for points1,id1 in zip (corners1,ids1): # zip関数を使ってマーカーの四隅の座標とIDを紐づける
            image_points_2D = np.array(points1[0],dtype=np.float64) # 画像上の座標(マーカー認識の結果)
            figure_points_3D = np.array([ # 画像上の点の３次元空間での座標 マーカーの四隅の座標と合わせてベクトルの計算に使ってるっぽい
                (-0.5,0.5,0.0),
                (0.5,0.5,0.0),
                (0.5,-0.5,0.0),
                (-0.5,-0.5,0.0),

            ])
            # 上記を対応させて姿勢などを算出する
            sus,rvec,tvec=cv2.solvePnP(figure_points_3D, image_points_2D,cameraMatrix,distCoeff) # susはsuccessの略　算出に成功するとTrueになる rvecは回転ベクトル tvecは平行移動ベクトル

            if id1 == 0:
                marker0_points = points1
                marker0_rvec = rvec
                marker0_tvec = tvec
            elif id1 == 1:
                marker1_points = points1
                marker1_rvec = rvec
                marker1_tvec = tvec
            elif id1 == 2:
                marker2_points = points1
                marker2_rvec = rvec
                marker2_tvec = tvec
            else:
                marker3_points = points1
                marker3_rvec = rvec
                marker3_tvec = tvec

    Left_point_x = np.array((marker0_points[0][0][0] + marker3_points[0][3][0])/2)
    Left_point_y = np.array((marker3_points[0][3][1] + marker0_points[0][0][1])/2)
    Right_point_x = np.array((marker1_points[0][1][0] + marker2_points[0][2][0])/2)
    Right_point_y = np.array((marker2_points[0][2][1] + marker1_points[0][1][1])/2)
    Left_point = np.array([Left_point_x,Left_point_y]) # 変形後の左下の座標
    Right_point = np.array([Right_point_x,Right_point_y]) # 変形後の右下の座標

    Left_rvec = np.array((marker0_rvec + marker3_rvec)/2)
    Left_tvec = np.array((marker0_tvec + marker3_tvec)/2)    
    Right_rvec = np.array((marker1_rvec + marker2_rvec)/2)
    Right_tvec = np.array((marker1_tvec + marker2_tvec)/2)


    Left_end_point3D = np.array([[-0.5,-0.5,4]])
    Left_end_point2D,_ = cv2.projectPoints(Left_end_point3D,Left_rvec,Left_tvec,cameraMatrix,distCoeff) # 3D座標を2D座標に投影
    Left_start_point2D = np.array([[Left_point]]) # 高さの線の始点
    Left_start_point = (int(Left_start_point2D[0][0][0]),int(Left_start_point2D[0][0][1])) # 始点の配列を整数のタプル型で展開
    Left_end_point = (int(Left_end_point2D[0][0][0]),int(Left_end_point2D[0][0][1])) # 終点の配列を整数のタプル型で展開


    Right_end_point3D = np.array([[0.5,-0.5,4]]) # 3次元座標に高さをプラスする 1の場合(マーカーの1辺の長さ×1)
    Right_end_point2D,_ = cv2.projectPoints(Right_end_point3D,Right_rvec,Right_tvec,cameraMatrix,distCoeff) # 3D座標を2D座標に投影
    Right_start_point2D = np.array([[Right_point]]) # 高さの線の始点
    Right_start_point = (int(Right_start_point2D[0][0][0]),int(Right_start_point2D[0][0][1])) # 始点の配列を整数のタプル型で展開
    Right_end_point = (int(Right_end_point2D[0][0][0]),int(Right_end_point2D[0][0][1])) # 終点の配列を整数のタプル型で展開

    m1 = np.empty((4,2)) # 要素数2の配列を4行作る
    m1[0] = Left_end_point
    m1[1] = Right_end_point
    m1[2] = Right_start_point
    m1[3] = Left_start_point

    marker_coordinates = np.float32(m1) # 四隅のマーカーの中心座標(カメラに対して斜めの面)
    true_coordinates   = np.float32([[0,0],[width,0],[width,height],[0,height]]) # カメラに対して平行な面
    s.trans_mat1_T = cv2.getPerspectiveTransform(marker_coordinates,true_coordinates) # 任意の四角形から別の任意の四角形への変換 引数のデータ型はfloat32でないといけないらしい




    # カメラ3でマーカーに対して垂直の面をとる
    _,frame2 = cap2.read()
    frame2 = cv2.resize(frame2,Size)
    corners2,ids2,_= detector.detectMarkers(frame2) # 画像からマーカーを検出する
    
    for points2,id2 in zip (corners2,ids2): # zip関数を使ってマーカーの四隅の座標とIDを紐づける
            image_points_2D = np.array(points2[0],dtype=np.float64) # 画像上の座標(マーカー認識の結果)
            figure_points_3D = np.array([ # 画像上の点の３次元空間での座標 マーカーの四隅の座標と合わせてベクトルの計算に使ってるっぽい
                (-0.5,0.5,0.0),
                (0.5,0.5,0.0),
                (0.5,-0.5,0.0),
                (-0.5,-0.5,0.0),

            ])
            # 上記を対応させて姿勢などを算出する
            sus,rvec,tvec=cv2.solvePnP(figure_points_3D, image_points_2D,cameraMatrix,distCoeff) # susはsuccessの略　算出に成功するとTrueになる rvecは回転ベクトル tvecは平行移動ベクトル

            if id2 == 0:
                marker0_points = points2
                marker0_rvec = rvec
                marker0_tvec = tvec
            elif id2 == 1:
                marker1_points = points2
                marker1_rvec = rvec
                marker1_tvec = tvec
            elif id2 == 2:
                marker2_points = points2
                marker2_rvec = rvec
                marker2_tvec = tvec
            else:
                marker3_points = points2
                marker3_rvec = rvec
                marker3_tvec = tvec

    Left_point_x = np.array((marker3_points[0][3][0] + marker2_points[0][2][0])/2)
    Left_point_y = np.array((marker3_points[0][3][1] + marker2_points[0][2][1])/2)
    Right_point_x = np.array((marker0_points[0][0][0] + marker1_points[0][1][0])/2)
    Right_point_y = np.array((marker0_points[0][0][1] + marker1_points[0][1][1])/2)
    Left_point = np.array([Left_point_x,Left_point_y]) # 変形後の左下の座標
    Right_point = np.array([Right_point_x,Right_point_y]) # 変形後の右下の座標

    Left_rvec = np.array((marker3_rvec + marker2_rvec)/2)
    Left_tvec = np.array((marker3_tvec + marker2_tvec)/2)    
    Right_rvec = np.array((marker0_rvec + marker1_rvec)/2)
    Right_tvec = np.array((marker0_tvec + marker1_tvec)/2)


    Left_end_point3D = np.array([[0.5,-0.5,4]])
    Left_end_point2D,_ = cv2.projectPoints(Left_end_point3D,Left_rvec,Left_tvec,cameraMatrix,distCoeff) # 3D座標を2D座標に投影
    Left_start_point2D = np.array([[Left_point]]) # 高さの線の始点
    Left_start_point = (int(Left_start_point2D[0][0][0]),int(Left_start_point2D[0][0][1])) # 始点の配列を整数のタプル型で展開
    Left_end_point = (int(Left_end_point2D[0][0][0]),int(Left_end_point2D[0][0][1])) # 終点の配列を整数のタプル型で展開


    Right_end_point3D = np.array([[0.5,0.5,4]]) # 3次元座標に高さをプラスする 1の場合(マーカーの1辺の長さ×1)
    Right_end_point2D,_ = cv2.projectPoints(Right_end_point3D,Right_rvec,Right_tvec,cameraMatrix,distCoeff) # 3D座標を2D座標に投影
    Right_start_point2D = np.array([[Right_point]]) # 高さの線の始点
    Right_start_point = (int(Right_start_point2D[0][0][0]),int(Right_start_point2D[0][0][1])) # 始点の配列を整数のタプル型で展開
    Right_end_point = (int(Right_end_point2D[0][0][0]),int(Right_end_point2D[0][0][1])) # 終点の配列を整数のタプル型で展開

    m2 = np.empty((4,2)) # 要素数2の配列を4行作る
    m2[0] = Left_end_point
    m2[1] = Right_end_point
    m2[2] = Right_start_point
    m2[3] = Left_start_point

    marker_coordinates = np.float32(m2) # 四隅のマーカーの中心座標(カメラに対して斜めの面)
    true_coordinates   = np.float32([[0,0],[width,0],[width,height],[0,height]]) # カメラに対して平行な面
    s.trans_mat2_a = cv2.getPerspectiveTransform(marker_coordinates,true_coordinates) # 任意の四角形から別の任意の四角形への変換 引数のデータ型はfloat32でないといけないらしい

