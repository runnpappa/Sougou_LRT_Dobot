import cv2
import numpy as np


img = cv2.imread(r"LRT_Dobot\sample\senro.png")
size = (600, 400)
img1 = cv2.resize(img, size)
img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

ret, img3 = cv2.threshold(img2, 60, 255, cv2.THRESH_BINARY_INV)  # 二値化の閾値
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
masked_edges = cv2.bitwise_and(edges, mask)


# cv2.HoughLinesPによる直線検出
rho = 1
theta = np.pi/180
threshold = 70  # 直線検出の閾値


lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, minLineLength=170, maxLineGap=150)
# print(lines)

j = 0

def draw_ext_lines(img1, lines, color=[0, 255, 0], thickness=2):
    d = 100  # required extend length
    i = 0
    for line in lines:
        for x1, y1, x2, y2 in line:
            if (x2 != x1):
                slope = (y2-y1)/(x2-x1)
                sita = np.arctan(slope)
                if (slope > 0):  # 傾きに応じて場合分け
                    if (x2 > x1):
                        x3 = int(x2 + d*np.cos(sita))
                        y3 = int(y2 + d*np.sin(sita))
                        cv2.line(img1, (x3, y3), (x1, y1), color, thickness)
                    else:
                        x3 = int(x1 + d*np.cos(sita))
                        y3 = int(y1 + d*np.sin(sita))
                        cv2.line(img1, (x3, y3), (x2, y2), color, thickness)
                elif (slope < 0):
                    if (x2 > x1):
                        x3 = int(x1 - d*np.cos(sita))
                        y3 = int(y1 - d*np.sin(sita))
                        cv2.line(img1, (x3, y3), (x2, y2), color, thickness)
                    else:
                        x3 = int(x2 - d*np.cos(sita))
                        y3 = int(y2 - d*np.sin(sita))
                        cv2.line(img1, (x3, y3), (x1, y1), color, thickness)
        i += 1
    return i


line_img = np.zeros((size[1], size[0], 3),dtype=np.uint8)  # 元画像サイズの空の行列を返す


# 直線が検出された場合は画像に描画する
if (not isinstance(lines, type(None))):
    j = draw_ext_lines(line_img, lines)

    # 自作の直線描画関数、作った空の行列に直線がある場所のみ色のデータを入れる

overlay_img = cv2.addWeighted(src1=img1,alpha=1,src2=line_img,beta=1,gamma=0)

cv2.imshow("line",line_img)
cv2.imshow("img",overlay_img)
cv2.waitKey()
cv2.destroyAllWindows()

# (解説・注意点)

# numpy.zeros(shape, dtype=float, order=’C’) 任意のサイズの0の配列を作る(真っ黒な画像を作る)
    # shapeは配列の形状 (size[1], size[0], 3)の部分
    # dtype はデータの型　デフォルトは'numpy.float64'　省略可
    # order は配列の向きを指定する 省略可
 
    # (size[1], size[0], 3)
    # size[]はウィンドウのサイズを取得する 0の場合は横の長さ 1の場合は縦の長さ
    # 3は並べるデータの中身 色をRGBで指定するために3にしている
    #
    # このプログラムはウィンドウサイズを600×400に指定してるので生成される配列は次のようになる
    # 
    # 　　　　　　　　　          　横に600
    #        縦 [0 0 0][0 0 0][0 0 0]...[0 0 0][0 0 0][0 0 0]
    #        に [0 0 0][0 0 0][0 0 0]...[0 0 0][0 0 0][0 0 0]
    #        4  [0 0 0][0 0 0][0 0 0]...[0 0 0][0 0 0][0 0 0] 
    #        0                        :
    #        0  [0 0 0][0 0 0][0 0 0]...[0 0 0][0 0 0][0 0 0]
    #           [0 0 0][0 0 0][0 0 0]...[0 0 0][0 0 0][0 0 0]
    # 
    # dtype=np.uint8
    # np.unit8 は符号なし8ビット整数型
    # 符号は＋や－のこと　負の数を使う場合はnp.uintではなくnp.intを使う
    # 8ビットは値の範囲 (8ビットだと0~255　16ビットだと0~65535)


# if (not isinstance(lines, type(None))):
    # isinstance(引数1,引数2)は型の判定を行う関数
    # 引数1には関数を入れ,引数2に入っているタイプと一致したらTrueを返す
    # if (not isinstance(lines, type(None))):　はもしlinesに値が入っていたら(= 直線を検出したら)という条件式になる


