import cv2

img = cv2.imread(r"LRT_Dobot\sample\img1.png")
size = (480,300)
img1 = cv2.resize(img,size)

# 色空間の変更処理
img2 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY) #BGRをグレースケール化
img3 = cv2.cvtColor(img1,cv2.COLOR_BGR2BGRA) #BGRにアルファチャンネル(透明度)を追加
img4 = cv2.cvtColor(img1,cv2.COLOR_BGR2HSV) #BGRをHSVに変換


cv2.imshow("before",img1)
cv2.imshow("after",img2)

cv2.waitKey()
cv2.destroyAllWindows()



# (解説・注意点)

# [cv2.cvtColor]
# cv2.cvtColor(引数1,引数2)
# 引数1には変換したい画像、引数2には色空間変換コードを入れる
# 色空間変換コードはネットで検索すれば出てくる
# アルファチャンネル(透明度)を追加したときのデフォルトの値は100%なので元の画像と変わらない