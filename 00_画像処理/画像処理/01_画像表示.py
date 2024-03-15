# cv2をインポートする
import cv2

# 画像を読み込む
img = cv2.imread(r"LRT_Dobot\sample\img1.png") # 相対パスで画像ファイルの指定

# 画像サイズの調整
size = (480,300)
img = cv2.resize(img,size)


# 画像を表示する
cv2.imshow("hyoji", img)

# ウィンドウの位置を変える
cv2.moveWindow("hyoji",x=900,y=50)

# キー入力待ち状態　
cv2.waitKey()

# すべてのウィンドウを閉じる
cv2.destroyAllWindows()



# (解説・注意点)

# [import]
# openCVというライブラリを使用するためにはインポートする必要がある

# [cv2.imread]
# 画像ファイル指定時のパスに日本語が含まれているとエラーが出る
# バックスラッシュ\は使えないため,スラッシュ/に置き換える必要がある　例）C:\Users\User\Documents → C:/Users/User/Documents
# ただしパスの前にrを入れればスラッシュに置き換えなくてもいける cv2.imread(r"C:\Users\User\Documents")

# [cv2.imshow]
# 一つ目の引数にウィンドウの名前を入れないとエラーが出る
# 複数のウィンドウに同じ名前をつけると後に実行されたプログラムが優先される(これを利用すれば別の映像に切り換えるときに無駄が少なくなる)

# [cv2.waitKey]
# キー入力を待っている間はこれ以降のプログラムは実行されない
# ()の中が1の場合1msの間だけ待つ
# 何もない or 0の場合　無制限に待つ

# [cv2.destroyAllWindows]
# 現在開いているすべてのウィンドウを閉じる
# 特定のウィンドウだけ消したい場合は cv2.destroyWindows("ウィンドウの名前")

