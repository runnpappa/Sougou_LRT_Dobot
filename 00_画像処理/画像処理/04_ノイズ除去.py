# 参考
# https://di-acc2.com/programming/python/19062/
# https://qiita.com/jin237/items/8da25b95e00f37ab6d7a

import cv2

img = cv2.imread(r"LRT_Dobot\sample\img1.png")
size = (480,300)
img1 = cv2.resize(img,size)
img2 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY) # グレースケール化
ret, img3 = cv2.threshold(img2, 60, 255, cv2.THRESH_BINARY_INV) # ノイズ除去なし

# 平滑化フィルタ
smooth_img = cv2.blur(img2,   # 入力画像
                      (3,3)  # 畳込配列
                     )
ret, img4 = cv2.threshold(smooth_img, 60, 255, cv2.THRESH_BINARY_INV) # ノイズ除去あり



cv2.imshow("Original",img1)
cv2.imshow("a",img3) # ノイズ除去なし
cv2.imshow("b",img4) # ノイズ除去あり

cv2.waitKey()
cv2.destroyAllWindows()
