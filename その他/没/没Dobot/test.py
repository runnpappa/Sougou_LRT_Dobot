import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

from Color import color 
import cv2

cap = cv2.VideoCapture(1)
size = (600,400)

ret,frame = cap.read()
frame = cv2.resize(frame,size)
frame_c,xy = color(frame,num=1)

# cv2.imshow("0",frame)
cv2.imshow("a",frame_c)

cv2.waitKey()
cap.release()
cv2.destroyAllWindows()