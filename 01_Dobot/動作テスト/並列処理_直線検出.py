from serial.tools import list_ports
import pydobot
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import threading
import numpy as np


available_ports = list_ports.comports()
port = available_ports[2].device #port番号を指定 
device = pydobot.Dobot(port=port, verbose=None) # デバイスを指定
(x, y, z, r, j1, j2, j3, j4) = device.pose() # 取得した座標をそれぞれ格納　
print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')


img = cv2.VideoCapture(0)
size = (800,600)

def Camera():
    def kensyutu(img1):
        img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        ret, img3 = cv2.threshold(img2, 85, 255, cv2.THRESH_BINARY_INV)  # 二値化の閾値

        # エッジ検出のしきい値を自動で計算
        med_val = np.median(img3)
        sigma = 0.33  # 0.33
        min_val = int(max(0, (1.0 - sigma) * med_val))
        max_val = int(max(255, (1.0 + sigma) * med_val))    

        edges = cv2.Canny(img3, threshold1= min_val, threshold2=max_val)# エッジ検出



        # 画像shapeに対する取得領域(4点)を、縦横の比率で指定
        imshape = np.array(edges.T.shape).T  # 画像のshape(W, H)
        left_bottom = imshape * np.array([0.2, 1])  # 左下の座標
        left_top = imshape * np.array([0.4, 0])  # 左上の座標
        right_top = imshape * np.array([0.6, 0])  # 右上の座標
        right_bottom = imshape * np.array([0.8, 1])  # 右下の座標
        region_coord = np.array([[left_bottom, left_top, right_top,
                                right_bottom]], dtype=np.int32)  # 先行車領域の座標4点(左下から時計回り)

        # マスク画像の作成
        mask = np.zeros_like(edges)
        cv2.fillPoly(mask, region_coord, color=255)
        masked_edges = cv2.bitwise_and(edges, mask)


        # cv2.HoughLinesPによる直線検出
        rho = 1
        theta = np.pi/180
        threshold = 70  # 直線検出の閾値


        # lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, minLineLength=200, maxLineGap=50) #先行車領域のみ直線検出
        lines = cv2.HoughLinesP(edges, rho, theta, threshold, minLineLength=100, maxLineGap=50) #全画面対象

        # print(lines)

        j = 0

        def draw_ext_lines(img1, lines, color=[0, 255, 0], thickness=2):
            d = 0  # required extend length
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
                                cv2.line(img1, (x3, y3), (x1, y1), color, thickness)
                            else:
                                x3 = int(x1 + d*np.cos(sita))
                                y3 = int(y1 + d*np.sin(sita))
                                cv2.line(img1, (x3, y3), (x2, y2), color, thickness)
                        elif (slope < 0):
                            if (x2 > x1):
                                x3 = int(x1 - d*np.cos(sita))
                                y3 = int(y1 - d*np.sin(sita))
                                cv2.line(img1, (x3, y3), (x2, y2), color, thickness)
                            else:
                                x3 = int(x2 - d*np.cos(sita))
                                y3 = int(y2 - d*np.sin(sita))
                                cv2.line(img1, (x3, y3), (x1, y1), color, thickness)
                i += 1
            return i


        line_img = np.zeros((size[1], size[0], 3),dtype=np.uint8)  # 元画像サイズの空の行列を返す

        # 直線が検出された場合は画像に描画する
        if (not isinstance(lines, type(None))):
            j = draw_ext_lines(line_img, lines)

            # 自作の直線描画関数、作った空の行列に直線がある場所のみ色のデータを入れる
        global overlay_img
        overlay_img = cv2.addWeighted(src1=img1,alpha=1,src2=line_img,beta=1,gamma=0)
        return overlay_img
    while True :
        ret, img0 = img.read()
        img1 = cv2.resize(img0, size)
        kensyutu(img1)
        cv2.imshow('00',overlay_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    


def Dobot():
    global aaa
    aaa = 0
    while(True):
        device.move_to(x+30, y, z, r, wait=True)
        device.move_to(x+30,y+30,z,r,wait=True)
        device.move_to(x,y+30,z,r,wait=True)
        device.move_to(x, y, z, r, wait=True)
        if cv2.waitKey(1) & aaa == (1):
            break


thread_1 = threading.Thread(target=Camera)
thread_2 = threading.Thread(target=Dobot)

thread_1.start()
thread_2.start()


thread_1.join() 
aaa = 1
thread_2.join()
device.close()