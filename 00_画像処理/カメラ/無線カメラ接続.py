# 参考
# https://qiita.com/haseshin/items/59aed8bae8a1fa88fa21

import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2


cap = cv2.VideoCapture(f"rtsp://192.168.1.1:7070/webcam/track0 RTSP/1.0")
size = (600,400) # 処理を軽くするためにこの大きさにしている

while(True):
    ret, frame = cap.read()
    
    frame = cv2.resize(frame,size)
    frame = cv2.rotate(frame,cv2.ROTATE_90_COUNTERCLOCKWISE) # カメラが90度傾いているので回転

    cv2.imshow('title',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

