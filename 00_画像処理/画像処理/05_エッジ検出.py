# 参考
# https://qiita.com/hitomatagi/items/2c3a2bfefe73ab5c86a4

import cv2

img = cv2.imread(r"LRT_Dobot\sample\img1.png")
size = (480,300)
img1 = cv2.resize(img,size)
img2 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY) # グレースケール化
smooth_img = cv2.blur(img2,(3,3)) # ノイズ除去
ret, img3 = cv2.threshold(smooth_img, 100, 255, cv2.THRESH_BINARY_INV) #　二値化処理

# エッジ検出
edges = cv2.Canny(img3, threshold1=250, threshold2=250)

cv2.imshow("before",img1)
cv2.imshow("after",edges)

cv2.waitKey()
cv2.destroyAllWindows()

# 解説・注意点

# エッジ ≒ 輪郭

# [cv2.Canny(エッジ検出したい画像,引数1,引数2)]
# 引数1:minVal　引数2で検出されたエッジのゆるさのしきい値　この値を小さくすると途切れていたエッジがつながりやすくなる(ただし周りになにも検出されていない所に新たにエッジができることはない)
# 引数2:maxVal エッジかどうかの判断のしきい値

# minValとmaxVlの調整手順
# 1.threshold1(minVal)とthreshold2(maxVal)を同じ値にする
# 2.threshold2(maxVal)を調整して検出してほしいところにエッジが出るようにする
# 3.threshold1(minVal)で微調整


# 上記のminValとmaxValの値を自動で調整するプログラム
# med_val = np.median(img)
# sigma = 0.33  # 0.33
# min_val = int(max(0, (1.0 - sigma) * med_val))
# max_val = int(max(255, (1.0 + sigma) * med_val))
# img_edge1 = cv2.Canny(img, threshold1 = min_val, threshold2 = max_val)
