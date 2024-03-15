import cv2
#NunPyをインポート
import numpy as np


img = cv2.imread(r"LRT_Dobot\sample\senro.png")
size = (600, 400)
img1 = cv2.resize(img, size)
img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

ret, img3 = cv2.threshold(img2, 85, 255, cv2.THRESH_BINARY_INV)  # 二値化の閾値
edges = cv2.Canny(img3, threshold1=150, threshold2=250)# エッジ検出

# 画像shapeに対する取得領域(4点)を、縦横の比率で指定
imshape = np.array(edges.T.shape).T  # 画像のshape(W, H)
left_bottom = imshape * np.array([0.2, 1])  # 左下の座標
left_top = imshape * np.array([0.40, 0.4])  # 左上の座標
right_top = imshape * np.array([0.45, 0.4])  # 右上の座標
right_bottom = imshape * np.array([0.6, 1])  # 右下の座標
region_coord = np.array([[left_bottom, left_top, right_top,
                        right_bottom]], dtype=np.int32)  # 先行車領域の座標4点(左下から時計回り)


# マスク画像の作成
mask = np.zeros_like(edges)
cv2.fillPoly(mask, region_coord, color=255)
masked_edges = cv2.bitwise_and(img2, mask)




print(mask[0])

cv2.imshow('00',img2)
cv2.imshow('01',mask)
cv2.imshow('02',masked_edges)

cv2.moveWindow('00',20,500)
cv2.moveWindow('01',670,500)
cv2.moveWindow('02',1320,500)

cv2.waitKey()
cv2.destroyAllWindows



# (解説・注意点)

# np.zeros_like('画像')
# 入力画像と同じ配列で0を並べる ≒ 入力画像と同じサイズの真っ黒な画像データを作る

# cv2.fillPoly('画像', '座標(ndarry型)', 色)
# cv2.fillPolyは画像上にポリゴン(多角形)を作図する命令
# 上記のプログラムの場合は先行車領域を作図している

# cv2.bitwise_and('元の画像', 'マスク画像')
# cv2.bitwise_andは元の画像の上にマスク画像をかぶせて,マスク画像の白い領域と重なっているところのみ元の画像を表示する命令
