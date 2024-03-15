import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2

capture0 = cv2.VideoCapture(0)
capture1 = cv2.VideoCapture(1)
capture2 = cv2.VideoCapture(2)

windowsize = (800,600)

while(True):
    
    _,frame0 = capture0.read()
    _,frame1 = capture1.read()
    _,frame2 = capture2.read()

    frame0 = cv2.resize(frame0,windowsize)
    frame1 = cv2.resize(frame1,windowsize)
    frame2 = cv2.resize(frame2,windowsize)

    cv2.imshow("00",frame0)
    cv2.imshow("01",frame1)
    cv2.imshow("02",frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture0.release()
capture1.release()
capture2.release()
cv2.destroyAllWindows()

# USBハブなどを使って一つのUSBポートに複数のカメラを接続すると上手くいかないので注意