import cv2

img = cv2.imread(r"LRT_Dobot\sample\img1.png")
size = (480,300)
img1 = cv2.resize(img,size)
img2 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY) # グレースケール化

# 二値化処理
ret, img3 = cv2.threshold(img2, 100, 255, cv2.THRESH_BINARY_INV) # しきい値より大きい値を最大値、それ以外を0にする
ret, img4 = cv2.threshold(img2, 100, 255, cv2.THRESH_BINARY)  # しきい値より大きい値を0、それ以外を最大値にする
ret, img5 = cv2.threshold(img2, 100, 255, cv2.THRESH_TRUNC)  # しきい値より大きい値をしきい値に、それ以外はそのままにする
ret, img6 = cv2.threshold(img2, 100, 255, cv2.THRESH_TOZERO) # しきい値より大きい値はそのまま、それ以外を0にする


cv2.imshow("Original",img1)
cv2.imshow("Gray",img2)
cv2.imshow("Binarization",img3) 


cv2.waitKey()
cv2.destroyAllWindows()

# (解説・注意点)

# [ret, ]
# 戻り値
# 二値化処理に成功した場合はTrueとなる


# [cv2.threshold] 二値化処理
# 二値化とは簡単に言うとグレースケール化した画像を0か255かの白黒画像に変換すること(最大値は変えられる　0か110など)

# cv2.threshold(引数1,引数2,引数3,引数4)
# 引数1:二値化したい画像
# 引数2:二値化のしきい値
# 引数3:二値化処理後の最大値　通常は255にする　これを255にすると白黒,100にするとグレー黒になる
# 引数4:二値化処理方法を指定　ネットで検索すればいろいろ出てくる

