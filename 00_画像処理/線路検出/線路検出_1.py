import cv2
import numpy as np

def draw_ext_lines(img1, lines, color=[0, 255, 0], thickness=2):
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



# (解説・注意点)

# 配列'lines'の中身
# lines = [[[306 155 346 365]]　　直線1の座標配列　[ 始点のx座標　始点のy座標　終点のx座標　終点のy座標 ]
#          [[257 398 308 155]]    直線2の座標配列
#          [[191 172 410 168]]]   直線3の座標配列


# def draw_ext_lines(img1, lines, color=[0, 255, 0], thickness=2): 
# draw_ext_lines(画像,直線の座標,直線の色,線の太さ)
# 検出された直線を延長する関数

# d = 100 延長線の長さ
# i = 0  描いた直線の数

#for line in lines:
# 変数'line'に配列'直線1'を格納
# 1ループ目では line = [306 155 346 365]となる

# for x1, y1, x2, y2 in line:
# lineに格納されている座標をそれぞれ格納
# [306 155 346 365]
#  ↓   ↓   ↓   ↓
# [x1  y1  x2  y2]