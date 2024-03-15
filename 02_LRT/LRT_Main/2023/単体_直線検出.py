
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import sys
import cv2
import numpy as np
import serial
import socket

# host = "192.168.1.101" #Processingで立ち上げたサーバのIPアドレス
# port = 10001       #Processingで設定したポート番号
# socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成
# socket_client.connect((host, port))
capture = cv2.VideoCapture(f"rtsp://192.168.1.1:7070/webcam/RTSP/1.0")  # キャプチャの準備 rtsp://10.45.48.111:8554/unicast
# capture = cv2.VideoCapture(0)
size = (600, 400)

#シリアル通信(PC⇔Arduino)
ser = serial.Serial()
ser.port = "COM3"     #デバイスマネージャでArduinoのポート確認
ser.baudrate = 115200 #Arduinoと合わせる
ser.setDTR(False)     #DTRを常にLOWにしReset阻止
ser.open()            #COMポートを開く


while capture.isOpened():
    ret, frame = capture.read()  # 読み込み

    img = cv2.resize(frame, size)
    img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)
    img3 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img4 = cv2.threshold(img3, 100, 255, cv2.THRESH_BINARY_INV)  # 二値化の閾値(しきいち)
    cv2.imshow("img4",img4) #二値化、白黒

    # エッジ検出
    edges = cv2.Canny(img4, threshold1=150, threshold2=250) #エッジ検出閾値
    # cv2.imshow("edge",edges) #輪郭

    # 画像shapeに対する取得領域(4点)を、縦横の比率で指定
    imshape = np.array(edges.T.shape).T  # 画像のshape(W, H)
    left_bottom = imshape * np.array([0.2, 1])  # 左下の座標
    left_top = imshape * np.array([0.4, 0.4])  # 左上の座標
    right_top = imshape * np.array([0.6, 0.4])  # 右上の座標
    right_bottom = imshape * np.array([0.8, 1])  # 右下の座標
    region_coord = np.array([[left_bottom, left_top, right_top,
                            right_bottom]], dtype=np.int32)  # 先行車領域の座標4点(左下から時計回り)

    # マスク画像の作成
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, region_coord, color=255)
    masked_edges = cv2.bitwise_and(edges, mask)
    cv2.imshow("ede",masked_edges)

    # cv2.HoughLinesPによる直線検出
    rho = 1
    theta = np.pi/180
    threshold = 70  # 直線検出の閾値

    # cv2.HoughLinesPによる直線検出
    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold,
                            np.array([]), minLineLength=200, maxLineGap=50)  # minなんとかとmaxなんとか重要　閾値

    # 直線をimgに描画する関数

    j = 0

    def draw_ext_lines(img, lines, color=[0, 255, 0], thickness=2):
        d = 100  # required extend length
        i = 0
        for line in lines:
            for x1, y1, x2, y2 in line:
                if (x2 != x1):
                    slope = (y2-y1)/(x2-x1)
                    sita = np.arctan(slope)
                    if (slope > 0):  # 傾きに応じて場合分け
                        if (x2 > x1):
                            x3 = int(x2 + d*np.cos(sita))
                            y3 = int(y2 + d*np.sin(sita))
                            cv2.line(img, (x3, y3), (x1, y1), color, thickness)
                        else:
                            x3 = int(x1 + d*np.cos(sita))
                            y3 = int(y1 + d*np.sin(sita))
                            cv2.line(img, (x3, y3), (x2, y2), color, thickness)
                    elif (slope < 0):
                        if (x2 > x1):
                            x3 = int(x1 - d*np.cos(sita))
                            y3 = int(y1 - d*np.sin(sita))
                            cv2.line(img, (x3, y3), (x2, y2), color, thickness)
                        else:
                            x3 = int(x2 - d*np.cos(sita))
                            y3 = int(y2 - d*np.sin(sita))
                            cv2.line(img, (x3, y3), (x1, y1), color, thickness)
            i += 1
        return i

    line_img = np.zeros((size[0], size[1], 3),
                        dtype=np.uint8)  # 元画像サイズの空の行列を返す

    # 直線が検出された場合は画像に描画する
    if (not isinstance(lines, type(None))):
        j = draw_ext_lines(line_img, lines)

        # 自作の直線描画関数、作った空の行列に直線がある場所のみ色のデータを入れる

    overlay_img = cv2.addWeighted(
        src1=img, alpha=1, src2=line_img, beta=1, gamma=0)  # 元画像に直線画像を重ね合わせ
    cv2.imshow('imshow_test',overlay_img ) #masked_edgesQ

    if j >= 2: #直線を2本以上検出したとき
        print("TRUE")
        ser.write(b's')       #送りたい内容をバイト列で送信
        # socket_client.send('t'.encode('utf-8')) #データを送信 Python3


    #     # ser.write(bytes("t","utf-8"))  #"t"を送る

    else: #直線を2本以上検出しなかったとき
        print("FALSE")
        ser.write(b'c')       #送りたい内容をバイト列で送信
        # socket_client.send('f'.encode('utf-8'))

    #     # ser.write(bytes("f","utf-8")) #"f"を送る

    if cv2.waitKey(1) & 0xFF == ord('q'): #'q'を押すと画像処理が終わる
        break
cv2.destroyAllWindows()
ser.close()
