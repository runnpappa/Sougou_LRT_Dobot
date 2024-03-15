def color(frame,num):
    import cv2
    import numpy as np

    class ColorDetection:
        def __init__(self,frame,num):
            self.n = num
            self.frame = frame

            if num == 1: # Dobotの上の目印
                self.limit = np.array([[20,80,10],[24,255,255]]) # 抽出する色(黄色)
                self.Noise_num = np.ones((10, 10), np.uint8) # ノイズ除去を行う回数
                self.border = 1000 # この面積以上だったらマークとみなす

            elif num == 2: # Dobotの下の目印
                self.limit = np.array([[60, 94, 20],[100, 255, 255]]) # 緑
                self.Noise_num = np.ones((25, 25), np.uint8)
                self.border = 1000

            elif num == 3: # 物体の目印
                # limit = np.array([[25,120,150],[30,255,255]]) # 緑
                self.limit = np.array([[150,70,105],[200,255,255]]) # ピンク
                self.Noise_num = np.ones((5, 10), np.uint8)
                self.border = 50

            
        def  detection(self):
            line_Color = ([0,100,255])
            cap_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(cap_hsv,self.limit[0],self.limit[1])
            mask2 = cv2.morphologyEx(mask, cv2.MORPH_OPEN,self.Noise_num) #ノイズ除去
            retval,labels,stats,centroids = cv2.connectedComponentsWithStats(mask2)# ラベリング
            # retval:ラベル数
            # labels:ラベル番号が振られた配列
            # stats:物体ごとの座標と面積
            # centroids:物体ごとの中心座標

            for i in range(1, retval):#ラベルの数だけ繰りかえす
                #statsの中身 [x座標, y座標, 幅, 高さ, 面積]
                
                area= stats[i][4] # 初めに面積のみを取り出す

                if area > self.border: # 面積がボーダーラインよりも大きければ
                    x, y, width, height= stats[i][:4] # x座標, y座標, 幅, 高さを取り出す
                
                    jx,jy = centroids[i] #中心座標を取り出す
                    jx = int(jx)
                    jy = int(jy)
                    cv2.rectangle(frame,(x,y),(x+width,y+height),line_Color,2)
                    cv2.putText(frame, f"[{i}]:{area}{x,y}", (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1, line_Color, 1, cv2.LINE_AA)
                    cv2.circle(frame, (jx,jy), 3, line_Color, -1)
                    return frame, jx,jy
    

    C = ColorDetection(frame,num)
    frame,x,y = C.detection()
    xy = np.array([x,y])

    return frame,xy