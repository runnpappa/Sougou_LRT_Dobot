def setup(s,Size,cap1,cap2,cap3):
    import numpy as np
    import cv2
    from cv2 import aruco

    class Aruco:
        def __init__(self,Size): # 初期設定
            self.Size = Size

            # 使用するマーカーの辞書を指定
            p_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
            self.detector=aruco.ArucoDetector(p_dict)

            self.mark_height = 0.9 # マークの高さ

            width, height = Size # 画像の幅と高さを格納
            focal_length = height # 焦点の長さ
            center = (width/2, height/2) # 画面の中心座標
            fx,fy,cx,cy=focal_length,focal_length,center[0],center[1] #fx,fyは焦点の座標     cx,cyは画面の中心座標
            self.cameraMatrix=np.array([[fx,0,cx],[0,fy,cy],[0,0,1]])
            self.true_coordinates  = np.float32([[0,0],[width,0],[width,height],[0,height]]) # カメラに対して平行な面
            self.distCoeff=np.zeros((4,1)) # カメラによって発生する歪みに対処するために必要
            self.figure_points_3D = np.array([ # 画像上の点の３次元空間での座標
                        (-0.5,0.5,0.0),
                        (0.5,0.5,0.0),
                        (0.5,-0.5,0.0),
                        (-0.5,-0.5,0.0),
                    ])

        def detection(self,cap1,cap2,cap3):
            ret,frame1 = cap1.read()
            ret,frame2 = cap2.read()
            # ret,frame3 = cap3.read()
            frame1 = cv2.resize(frame1,self.Size)
            frame2 = cv2.resize(frame2,self.Size)
            # frame3 = cv2.resize(frame3,self.Size)
            frame1 = cv2.flip(frame1,-1)      
            m1 = self.fourcorners(frame1)
            m2 = self.fourcorners(frame2)
            # m3 = self.fourcorners(frame3)
            
            # デバック用
            # print(m1)
            # for i in range(4):
            #     point1 = np.array(m3[i],dtype = int)
            #     point2 = np.array(m3[(i+1)%4],dtype = int)
            #     cv2.line(frame3,point1,point2,(0,255,0),3) # 上面の辺を描く
            #     if i==0:
            #         cv2.drawMarker(frame3, point1,color=(255,255),markerType=cv2.MARKER_SQUARE,thickness=1,markerSize=10) # 描画した立方体の始点に目印をつける
            # cv2.imshow("im",frame3)

            s.trans_mat1 = self.correction(m1)
            s.trans_mat2 = self.correction(m2)
            # s.trans_mat3 = self.correction(m3)
            # cap2_t = cv2.warpPerspective(frame1,s.trans_mat1,(width, height))
        
        def fourcorners(self,frame,vertical=False): # 画像から台形補正に使う四隅の座標を求める関数
            corners,ids,_= self.detector.detectMarkers(frame)
            m = np.empty((4,2))
            for fourpoints,id in zip (corners,ids): # zip関数を使ってマーカーの四隅の座標とIDを紐づける
                image_points_2D = np.array(fourpoints[0],dtype=np.float64) # 画像上の座標(マーカー認識の結果)
                # 上記を対応させて姿勢などを算出する
                sus,rvec,tvec=cv2.solvePnP(self.figure_points_3D, image_points_2D,self.cameraMatrix,self.distCoeff) # susはsuccessの略　算出に成功するとTrueになる rvecは回転ベクトル tvecは平行移動ベクトル
                points = self.figure_points_3D[id]
                point3D = points+np.array([[0,0,self.mark_height]]) # 3次元座標に高さをプラスする
                point2D,_ = cv2.projectPoints(point3D,rvec,tvec,self.cameraMatrix,self.distCoeff) # 3D座標を2D座標に投影
                point = (int(point2D[0][0][0]),int(point2D[0][0][1]))
                m[id] = point
            return m            

        def correction(self,m): # 台形補正をする関数
            marker_coordinates = np.float32(m) #　補正前の四隅の座標(台形)
            trans_mat = cv2.getPerspectiveTransform(marker_coordinates,self.true_coordinates)
            return trans_mat
    C = Aruco(Size)
    C.detection(cap1,cap2,cap3)
   
