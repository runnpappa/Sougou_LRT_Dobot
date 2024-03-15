def senro(img):
    import cv2
    import numpy as np
    
    size = img.shape

    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img2 = cv2.threshold(img1, 100, 255, cv2.THRESH_BINARY_INV)  # 二値化の閾値

    # エッジ検出
    edges = cv2.Canny(img2, threshold1=150, threshold2=250) #エッジ検出閾値
    # cv2.imshow("edge",edges) #輪郭

    # 画像shapeに対する取得領域(4点)を、縦横の比率で指定
    imshape = np.array(edges.T.shape).T  # 画像のshape(W, H)
    left_bottom = imshape * np.array([0.2, 1])  # 左下の座標
    left_top = imshape * np.array([0.4, 0.4])  # 左上の座標
    right_top = imshape * np.array([0.6, 0.4])  # 右上の座標
    right_bottom = imshape * np.array([0.8, 1])  # 右下の座標
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

    # cv2.HoughLinesPによる直線検出
    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold,
                            np.array([]), minLineLength=200, maxLineGap=50)  # minなんとかとmaxなんとか重要　閾値

    # 直線をimgに描画する関数

    j = 0

    def draw_ext_lines(img, lines, color=[0, 255, 0], thickness=2):
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
                            cv2.line(img, (x3, y3), (x1, y1), color, thickness)
                        else:
                            x3 = int(x1 + d*np.cos(sita))
                            y3 = int(y1 + d*np.sin(sita))
                            cv2.line(img, (x3, y3), (x2, y2), color, thickness)
                    elif (slope < 0):
                        if (x2 > x1):
                            x3 = int(x1 - d*np.cos(sita))
                            y3 = int(y1 - d*np.sin(sita))
                            cv2.line(img, (x3, y3), (x2, y2), color, thickness)
                        else:
                            x3 = int(x2 - d*np.cos(sita))
                            y3 = int(y2 - d*np.sin(sita))
                            cv2.line(img, (x3, y3), (x1, y1), color, thickness)
            i += 1
        return i

    line_img = np.zeros((size[0], size[1], 3),
                        dtype=np.uint8)  # 元画像サイズの空の行列を返す

    # 直線が検出された場合は画像に描画する
    if (not isinstance(lines, type(None))):
        j = draw_ext_lines(line_img, lines)
        result = True

    else:
        result = False

    overlay_img = cv2.addWeighted(
        src1=img, alpha=1, src2=line_img, beta=1, gamma=0)  # 元画像に直線画像を重ね合わせ
    
    return result,overlay_img
