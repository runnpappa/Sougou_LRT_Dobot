

# 要調整


import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
Size = (800,600)
line_Color = ([0,100,255])

def blue(cap_Size):
    cap_hsv = cv2.cvtColor(cap_Size, cv2.COLOR_BGR2HSV)

    # 検出のしきい値
    limit = np.array([[100,50,70],[160,255,255]])

    global mask
    mask = cv2.inRange(cap_hsv,limit[0],limit[1])
    
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((10, 10), np.uint8)) #ノイズ除去
    # print(type(mask))
    
    
    # 輪郭取得
    contours,_ = cv2.findContours(mask,
                                   cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # 小さい輪郭は誤検出として削除する
    # contours = list(filter(lambda x: cv2.contourArea(x) > 100, contours))
    
    # 輪郭までの距離を計算する
    dist_img = np.empty(mask.shape, dtype = np.float32) # 二値化画像と同じ大きさの空の配列を作成(浮動小数型)
    for i in range(mask.shape[0]):# 画像の横の大きさの分だけ繰り返す
        for j in range(mask.shape[1]):#　画像の縦の大きさの分だけ繰りかえす
            # print(contours)
    #         # 1周目は(i,j)= (0,0)
    #         # 2周目は(i,j)= (0,1)


            dist_img[i,j] = cv2.pointPolygonTest(contours[0],(j,i),True)
    #         # dist_img の指定の座標にその座標から輪郭までの距離を入れる



    # 最小値, 最大値, 最小値の座標, 最大値の座標
    minVal,maxVal,min_loc,max_loc = cv2.minMaxLoc(dist_img) # 配列dist_img の最大値と最小値,それぞれの座標を取得 
    minVal = abs(minVal) # 輪郭から一番離れている点までの距離(外側)
    maxVal = abs(maxVal) # 輪郭から一番離れている点までの距離(内側)
    # print (minVal)
    # print (maxVal)
    
    # height,width,_ = cap_Size.shape

    # 輪郭までの距離を視覚的に分かりやすく描画する(処理がめちゃくちゃ重くなるのでなくてもいい)
    # dw_img = np.zeros((height,width,3),dtype=np.uint8) # 配列の形状が(height,width,3)になる理由がわからない
    # for y in range(mask.shape[0]):
    #   0  for x in range(mask.shape[1]):
    #         if dist_img[y,x] < 0: # もし[y,x]の座標に入っている値が0より小さければ(＝ 輪郭の外側なら)

    #             v = int (255.0 - abs(dist_img[y,x])*255.0 / minVal)
    #             # print(v)
    #             dw_img[y,x] = (0,v,v)

    #         elif dist_img[y,x] > 0:  # もし[y,x]の座標に入っている値が0より大きければ(＝ 輪郭の内側なら)

    #             v = 255 - dist_img[y,x]*255 / maxVal
    #             dw_img[y,x] = (0,0,v)

    #         else: # もし[y,x]の座標に入っている値が0なら(＝ 輪郭線上なら)
    #             # 輪郭(白)
    #             dw_img[y,x] = (255,255,255)
    
    # 距離と内接円
    # dw_img2 = np.zeros((height,width),dtype=np.uint8)
    # dw_img2.fill(255)

    # 上の二行はこれ↓でいいのでは?
    # dw_img2 = np.full((height,width),255,dtype=np.uint8)
    # print (dw_img2)

    # (dw_img2,contours,図形の番号,色,輪郭の太さ(塗りつぶし:-1))
    # cv2.drawContours(dw_img2,contours[0],2,(255,0,255),0)


    # 距離イメージで求めた最大値,最小値の座標
    # radius = int(maxVal)
    # print(radius)
    # cv2.circle(dw_img2,max_loc,radius,(100,0,0),2,cv2.LINE_AA)
    # cv2.circle(dw_img2,max_loc,0,(100,0,0),2,cv2.LINE_AA)


    # cv2.imshow("00",dw_img)
    # cv2.imshow("01",dw_img2)
    # cv2.imshow("02",mask)
    
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
           
            jx,jy = max_loc #中心座標を取り出す

            cv2.rectangle(cap_Size,(x,y),(x+width,y+height),line_Color,2)
            cv2.putText(cap_Size, f"[{i}]:{area}{x,y}", (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1, line_Color, 1, cv2.LINE_AA)
            cv2.circle(cap_Size, (int(jx),int(jy)), 3, line_Color, -1)


while(True):
    frame = cap.read()[1]
    cap_Size = cv2.resize(frame,Size)
    blue(cap_Size)
    cv2.imshow("test",cap_Size)
    cv2.imshow("2",mask)

    cv2.waitKey()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

