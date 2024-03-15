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
print(edges[0])
# print(imshape)


# (解説・注意点)

# 線路の形に合わせたマスク画像を作る

# [import ~ as ~]
# as を使うとインポートしたライブラリの呼び方を変更できる　
# # 例）[import cv2 as ABC]と打つと[ABC.imread ~ ]といった感じでライブラリを使える　

# 画像データには
# [[0 0 0 ... 0 0 0]
#  [0 0 0 ... 0 0 0]
#  [0 0 0 ... 0 0 0]
#  ...
#  [0 0 0 ... 0 0 0]
#  [0 0 0 ... 0 0 0]
#  [0 0 0 ... 0 0 0]]
# という感じで1ドットづつ色データ(二値化画像の場合は0~255の数字が一つ)が入っている (黒→0 ,白→255)
# この画像の場合はサイズが600×400なので,横に600個,縦に400個の数字が並んでいることになる

#[imshape = np.array(edges.T.shape).T] この行では上記の数字のならびを[横の数字の数 縦の数字の数]という配列でimshapeに格納している
# print(imshape)を実行すると[600 400]という結果になる


# left_bottom = imshape * np.array([0.2, 1])  # 左下の座標
# left_top = imshape * np.array([0.4, 0])  # 左上の座標
# right_top = imshape * np.array([0.6, 0])  # 右上の座標
# right_bottom = imshape * np.array([0.8, 1])  # 右下の座標
# この4行は読み込んだ画像の大きさに合わせて,先行車領域を作るための座標を指定している

# left_bottom = imshape * np.array([0.2, 1]) は 
# [600,400]*[0.2,1]　＝[600*0.2 , 400*1]　＝[120,400]　←これが左下の座標になる


# region_coord = np.array([[left_bottom, left_top, right_top,right_bottom]], dtype=np.int32) 
#求めた四つの座標を[左下,左上,右上,右下] の順番でregion_coordにint型で格納

