def DBT_obj(s,frame,flag):
    import cv2
    import numpy as np

    line_Color = ([0,100,255])
    cap_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # 検出のしきい値
    # limit1 = np.array([[25,120,150],[30,255,255]])　# 緑
    # limit = np.array([[30, 94, 100],[60, 255, 255]])
    limit = np.array([[150,0,105],[200,255,255]]) # ピンク

    mask = cv2.inRange(cap_hsv,limit[0],limit[1]) 
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((10, 10), np.uint8)) #ノイズ除去


    # ラベリング
    retval,labels,stats,centroids = cv2.connectedComponentsWithStats(mask)
    # retval:ラベル数
    # labels:ラベル番号が振られた配列
    # stats:物体ごとの座標と面積
    # centroids:物体ごとの中心座標
    
    for i in range(1, retval):#ラベルの数だけ繰りかえす
        #statsの中身 [x座標, y座標, 幅, 高さ, 面積]
        
        area= stats[i][4] # 初めに面積のみを取り出す

        # if area > 1800: # 面積が10000画素以上なら
        if area > 100:
            x, y, width, height= stats[i][:4] # x座標, y座標, 幅, 高さを取り出す
            jx,jy = centroids[i] #中心座標を取り出す

            if flag == True:
                s.test_a = np.array((int(jx),int(jy)))
            else:
                s.test_b = np.array((int(jx),int(jy)))
              

            cv2.rectangle(frame,(x,y),(x+width,y+height),line_Color,2)
            cv2.putText(frame, f"[{i}]:{area}{int(jx),int(jy)}", (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1, line_Color, 1, cv2.LINE_AA)
            cv2.circle(frame, (int(jx),int(jy)), 3, line_Color, -1)
    return frame
