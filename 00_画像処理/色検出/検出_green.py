import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
import numpy as np

cap = cv2.VideoCapture(2)
Size = (1280,960)
line_Color = ([0,100,255])

def green(cap_Size):
    cap_hsv = cv2.cvtColor(cap_Size, cv2.COLOR_BGR2HSV)

    # # 検出のしきい値
    # limit = np.array([[30, 64, 0],[90, 255, 255]])

    # global mask
    # mask = cv2.inRange(cap_hsv,limit[0],limit[1]) 
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((10, 10), np.uint8)) #ノイズ除去
    
    limit = np.array([[60, 94, 0],[100, 255, 255]])

    global mask
    mask = cv2.inRange(cap_hsv,limit[0],limit[1]) 
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((25, 25), np.uint8)) #ノイズ除去

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

            cv2.rectangle(cap_Size,(x,y),(x+width,y+height),line_Color,2)
            cv2.putText(cap_Size, f"[{i}]:{area}{x,y}", (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1, line_Color, 1, cv2.LINE_AA)
            cv2.circle(cap_Size, (int(jx),int(jy)), 3, line_Color, -1)


while(True):
    ret,frame = cap.read()
    cap_Size = cv2.resize(frame,Size)
    green(cap_Size)
    cv2.imshow("test",cap_Size)
    cv2.imshow("2",mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

