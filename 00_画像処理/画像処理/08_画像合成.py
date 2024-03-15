import cv2
import numpy as np

size = (720, 450)
img1 = cv2.imread(r"LRT_Dobot\sample\img2.png")
img2 = cv2.imread(r"LRT_Dobot\sample\img6.png")
img1 = cv2.resize(img1, size)
img2 = cv2.resize(img2,size)

overlay_img = cv2.addWeighted(src1=img1,alpha=1,src2=img2,beta=0.3,gamma=0)

cv2.imshow("img1",img1)
cv2.imshow("img2",img2)
cv2.imshow("overlay_img",overlay_img)

cv2.waitKey()
cv2.destroyAllWindows()

# (解説・注意点)

# cv2.addWeighted(引数1,引数2,引数3,引数4,引数5)
    # cv2.addWeighttedは画像を合成する関数
    # 引数1:src1  一つめの画像
    # 引数2:alpha
    # 引数3:src2  二つめの画像
    # 引数4:beta
    # 引数5:gamma
# alphaとbetaの値によって画像1と画像2の合成の割合がきまる(画像1：画像2＝alpha:beta)
# gammaは全ての画素値に加えられる数
