# 参考
# https://tanalib.com/opencv-mask/


import cv2
import numpy as np

img = cv2.imread(r"LRT_Dobot\sample\img2.png")
size = (480,300)
img = cv2.resize(img,size)


# マスク画像の作成
mask = np.zeros_like(img) # 元の画像と同じサイズのマスク画像を作る
cv2.circle(mask, (240,150), 120, (255, 255, 255), thickness = -1) # マスク画像に円を描画
masked_edges = cv2.bitwise_and(img,mask) # 元の画像にマスク画像を被せる


cv2.imshow("before",img)
cv2.imshow("mask",mask)
cv2.imshow("after",masked_edges)

cv2.waitKey()
cv2.destroyAllWindows()



# (解説・注意点)

# マスク処理で必要な領域だけを切り取ることで処理を軽くできる

# np.zeros_like("入力画像")
# 入力画像と同じ配列で0を並べる ≒ 入力画像と同じサイズの真っ黒な画像データを作る

# cv2.circle("マスク画像",円の中心座標,円の半径,色,線のサイズ)
# 円を描画する関数
# 線のサイズをマイナスにすると内側が塗りつぶされる

# cv2.bitwise_and"元の画像", "マスク画像")
# cv2.bitwise_andは元の画像の上にマスク画像をかぶせて,マスク画像の白い領域と重なっているところのみ元の画像を表示する
