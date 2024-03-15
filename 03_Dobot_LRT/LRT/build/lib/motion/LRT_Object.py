def LRT_object(img):

    import numpy as np
    import cv2

    result = False

    # 認識範囲
    xmin,xmax=120,280
    ymin,ymax=320,520
    # マスク画像の生成（マスク画像を重ねる画像のサイズと同じ）
    mask = np.zeros(img.shape,dtype =np.uint8)
    # 四角形の描画
    cv2.rectangle(mask,(xmin,ymin),(xmax,ymax),(255,255,255),-1)
    # 画像の合成
    img_masked = cv2.bitwise_and(img,mask)
    

    # 色による物体検出
    # 検出のしきい値
    limit1 = np.array([[0,127,0],[10,255,255]]) #しきい値1
    limit2 = np.array([[20,150,0],[35,255,255]]) #しきい値2

    cap_hsv = cv2.cvtColor(img_masked, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(cap_hsv,limit1[0],limit1[1]) 
    mask2 = cv2.inRange(cap_hsv,limit2[0],limit2[1])
    cap_overlay = cv2.addWeighted(src1=mask1,alpha=1,src2=mask2,beta=1,gamma=0) 

    # 輪郭情報の取得
    contours ,_ = cv2.findContours(cap_overlay,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours_filterd = list(filter(lambda x : cv2.contourArea(x)>2500,contours))

    if len(contours_filterd) != 0 : # もし障害物があったら
        #輪郭の処理
        for i in contours_filterd:
            x,y,width,height = cv2.boundingRect(i)
            cv2.rectangle(img_masked,(x,y),(x+width,y+height),color=(0,0,255))
            cv2.putText(img_masked,'DANGER',(x+10,y+10),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255))   
        result = True

    else :
        result = False
    
    return  result,img_masked
