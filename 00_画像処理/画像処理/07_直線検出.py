import cv2
#NunPyをインポート
import numpy as np

img = cv2.imread(r"LRT_Dobot\sample\img2.png")
size = (480, 300)
img1 = cv2.resize(img, size)
img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) # グレースケール化
ret, img3 = cv2.threshold(img2, 85, 255, cv2.THRESH_BINARY_INV)  # 二値化
edges = cv2.Canny(img3, threshold1=150, threshold2=250)# エッジ検出

# cv2.HoughLinesPによる直線検出
rho = 1
theta = np.pi/180
threshold = 70  # 直線検出の閾値
lines = cv2.HoughLinesP(edges, rho, theta, threshold, minLineLength=200, maxLineGap=40)

"""
linesには直線が検出された座標が格納される
lines=[[[x1,y1,x1',y1'] #一つ目の直線の座標（始点、終点）
        x2,y2,x2',y2']] #二つ目の直線の座標（始点、終点）
        x3,y3,x3',y3']]] #三つ目の直線の座標（始点、終点）
"""
print(lines)

for line in lines:
        for x1, y1, x2, y2 in line:
                cv2.line(img1, (x1, y1), (x2, y2), color = (0, 255, 0), thickness = 2)
cv2.imshow("before",edges)
cv2.imshow("after",img1)
cv2.waitKey()
cv2.destroyAllWindows()

# (解説・注意点)

# cv2.HoughLinesP(引数1,引数2,引数3,引数4,引数5,引数6)
# 引数1:img(画像)
# 引数2:rho(直角座標点と直線の距離)   デフォルトの値(rho=1)で問題ない
# 引数3:theta(直角座標点と直線の角度)　デフォルトの値(theta=360)で問題ない　
# 引数4:threshold(直線のしきい値)　直線状にある点の数がこの値以上になったときに直線とみなす (100前後が目安)
# 引数5:minLineLength(直線とみなす最小長さ)　この値よりも長い直線を検出対象にする
# 引数6:maxLineGap(直線とみなす点間隔の長さ)  点と点の距離がこの値より小さければ直線とみなす

# 引数5と引数6が重要