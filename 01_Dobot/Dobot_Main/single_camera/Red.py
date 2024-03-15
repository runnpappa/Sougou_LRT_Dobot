def red(frame):
    import cv2
    import numpy as np

    line_Color = ([0,100,255])
    cap_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # 検出のしきい値
    limit1 = np.array([[0,127,0],[10,255,255]]) #しきい値1
    limit2 = np.array([[150,127,0],[179,255,255]]) #しきい値2

    mask1 = cv2.inRange(cap_hsv,limit1[0],limit1[1]) 
    mask2 = cv2.inRange(cap_hsv,limit2[0],limit2[1])

    global cap_overlay
    mask = cv2.addWeighted(src1=mask1,alpha=1,src2=mask2,beta=1,gamma=0)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((30, 30), np.uint8)) #ノイズ除去


    # ラベリング
    retval,labels,stats,centroids = cv2.connectedComponentsWithStats(mask)
    # retval:ラベル数
    # labels:ラベル番号が振られた配列
    # stats:物体ごとの座標と面積
    # centroids:物体ごとの中心座標
    
    for i in range(1, retval):#ラベルの数だけ繰りかえす
        #statsの中身 [x座標, y座標, 幅, 高さ, 面積]
        
        area= stats[i][4] # 初めに面積のみを取り出す

        if area > 10000: # 面積が10000画素以上なら
            x, y, width, height= stats[i][:4] # x座標, y座標, 幅, 高さを取り出す
            jx,jy = centroids[i] #中心座標を取り出す
            jx = int(jx)
            jy = int(jy)

            cv2.rectangle(frame,(x,y),(x+width,y+height),line_Color,2)
            cv2.putText(frame, f"[{i}]:{area}{x,y}", (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1, line_Color, 1, cv2.LINE_AA)
            cv2.circle(frame, (jx,jy), 3, line_Color, -1)
    return frame,jx,jy
