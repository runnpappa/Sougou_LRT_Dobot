import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import numpy as np
import serial

#認識範囲
xmin,xmax=130,285
ymin,ymax=326,482

cap = cv2.VideoCapture(f"rtsp://192.168.1.1:7070/webcam/track0 RTSP/1.0")
# cap = cv2.VideoCapture(0)
size = (600, 400)
# 検出のしきい値
# limit1 = np.array([[0,127,0],[10,255,255]]) #しきい値1
# limit2 = np.array([[150,127,0],[179,255,255]]) #しきい値2

limit1 = np.array([[0,127,0],[10,255,255]]) #しきい値1
limit2 = np.array([[20,150,0],[35,255,255]]) #しきい値2

#シリアル通信(PC⇔Arduino)
ser = serial.Serial()
ser.port = "COM3"     #デバイスマネージャでArduinoのポート確認
ser.baudrate = 115200 #Arduinoと合わせる
ser.setDTR(False)     #DTRを常にLOWにしReset阻止
ser.open()            #COMポートを開く



while cap.isOpened():
    #画像読み込み
    ret,img = cap.read()
    img = cv2.resize(img,size)
    img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = cv2.blur(img,   # 入力画像
                    (15,15)  # 畳込配列
                     )
    
    #マスク画像の生成（マスク画像を重ねる画像のサイズと同じ）
    mask = np.zeros(img.shape,dtype =np.uint8)

    #四角形の描画
    cv2.rectangle(mask,(xmin,ymin),(xmax,ymax),(255,255,255),-1)
    # cv2.imshow("mask",mask)
    # cv2.waitKey(0)

  

    # #画像の合成
    img_masked = cv2.bitwise_and(img,mask)

    cap_hsv = cv2.cvtColor(img_masked, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(cap_hsv,limit1[0],limit1[1]) 
    mask2 = cv2.inRange(cap_hsv,limit2[0],limit2[1])
    cap_overlay = cv2.addWeighted(src1=mask1,alpha=1,src2=mask2,beta=1,gamma=0) 
    # kernel = np.ones((50,50),np.uint8)
    # cap_overlay = cv2.erode(cap_overlay,kernel,iterations = 1)
    # cap_overlay = cv2.morphologyEx(cap_overlay, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) #ノイズ除去

    #画面の表示
    cv2.imshow("img_masked",cap_overlay)
    # cv2.waitKey(0)

    #輪郭情報の取得
    contours ,_ = cv2.findContours(cap_overlay,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    contours_filterd = list(filter(lambda x : cv2.contourArea(x)>5000,contours))
    # print(contours_filterd)

    if not len(contours_filterd) == 0 :
    #輪郭の処理
        for i in contours_filterd:
            x,y,width,height = cv2.boundingRect(i)
            cv2.rectangle(img_masked,(x,y),(x+width,y+height),color=(0,0,255))
            cv2.putText(img_masked,'DANGER',(x+10,y+10),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255))   
            cv2.imshow("Result",img_masked)
        ser.write(b'z') 
        print("True")

    else :
        # for i in contours:
            # x,y,width,height = cv2.boundingRect(i)
            # cv2.rectangle(img_masked,(x,y),(x+width,y+height),color=(0,255,0))
            # # cv2.putText(img_masked,'SAFE',(x+10,y+10),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0))
        cv2.imshow("Result",img_masked)
        print("None")
        ser.write(b'c') 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
