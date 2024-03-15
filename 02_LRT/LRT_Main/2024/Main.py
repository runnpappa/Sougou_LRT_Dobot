import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import serial
from Senro import senro
from Object import object

capture = cv2.VideoCapture(f"rtsp://192.168.1.1:7070/webcam/RTSP/1.0")
size = (600, 400)

#シリアル通信(PC⇔Arduino)
ser = serial.Serial()
ser.port = "COM3"     #デバイスマネージャでArduinoのポート確認
ser.baudrate = 115200 #Arduinoと合わせる
ser.setDTR(False)     #DTRを常にLOWにしReset阻止
ser.open()            #COMポートを開く

while capture.isOpened():
    ret, frame = capture.read()
    img = cv2.resize(frame, size)
    img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE) # ウィンドウを90度回転

    Object,img_obj = object(img) # 物体検知 Objectには障害物があるかどうか(TrueまたはFalse)　img_objには検出後の画像

    if Object == True:
        ser.write(b'z') # 止まれの信号
        cv2.imshow("sen",img)
    
    elif Object == False:
        Straight,img_sen = senro(img) # 直線検出
        cv2.imshow("sen",img_sen)
        
        if Straight == True: # 直線だったら
            ser.write(b's') 

        elif Straight == False: # カーブだったら
            ser.write(b'c')

    cv2.imshow("obj",img_obj)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
ser.write(b'z')
ser.close()


# 動作環境
# pip           23.2.1 
# numpy         1.26.2 
# opencv-python 4.8.1.78
# pyserial      3.5   