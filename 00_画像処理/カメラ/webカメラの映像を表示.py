
# ↓この二行を書くとキャプチャー画面の表示が爆速になる(約40秒→約1秒)　import cv2よりも上に書かないと意味ない
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2

capture = cv2.VideoCapture(1)
windowsize = (800,600)


while(True):
    ret, frame = capture.read() # capture.read()を実行すると[画像を取得できたかどうか,画像のデータ]の二つのデータが返ってくるのでretとframeにそれぞれ格納する必要がある
    
    # frameに画像データを入れることができれば動作するので↓の書き方でもいける
    # frame = capture.read()[1]


    frame = cv2.resize(frame,windowsize)

    cv2.imshow('title',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



capture.release()
cv2.destroyAllWindows()