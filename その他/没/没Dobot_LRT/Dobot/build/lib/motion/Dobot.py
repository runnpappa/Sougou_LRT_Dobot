def move1(s,device,yel,red):
    import time

    yel[0] = yel[0]-50 # Dobotの目印の位置と吸盤の位置が若干違うので補正

    diff_x = red[0] - yel[0] # アームと対象のx座標の差
    diff_y = red[1] - yel[1] # アームと対象のy座標の差

    if (-30 < diff_x < 30) & (-20 < diff_y < 20)  : # もし差が20未満なら
        print("move1_compreat")
        print("move2_start")
        s.move = 2
        time.sleep(1)
        

    else: # もし差が20より大きければ
        x,y,z,r,_,_,_,_ = device.pose() # 現在のDobotの座標を取得
        movement_x = abs(diff_x)/10 # 移動量の計算
        movement_y = abs(diff_y)/10

        # 動かす方向によって分岐する
        if 0 > diff_y:
            y += movement_y # 取得した現在の座標に移動量を足す
            device.move_to(x, y, z, r, wait=True)
            time.sleep(0.1)

        else:
            y -= movement_y # 取得した現在の座標から移動量を引く
            device.move_to(x, y, z, r, wait=True)
            time.sleep(0.1)

        if 0 < diff_x:
            x += movement_x # 取得した現在の座標に移動量を足す
            device.move_to(x, y, z, r, wait=True)
            time.sleep(0.1)

        else:
            x -= movement_x # 取得した現在の座標から移動量を引く
            device.move_to(x, y, z, r, wait=True)
            time.sleep(0.1)



def move2(s,device,red_a,red_b,grn_a,grn_b):
    import time

    diff_x1 = red_a[0] - grn_a[0] # アームと対象のx座標の差
    diff_x2 = red_b[0] - grn_b[0]
    diff_x = (diff_x1 + diff_x2)/2

    if -20 < diff_x < 20   : # もし差が50未満なら
        print("move2_compreat")
        print("move3_start")
        s.move = 3
        time.sleep(1)

    else: # もし差が10より大きければ
        x,y,z,r,_,_,_,_ = device.pose() # 現在のDobotの座標を取得
        movement_x = abs(diff_x)/20 # 移動量の計算
   
        # 動かす方向によって分岐する
        if 0 < diff_x:
            x += movement_x # 取得した現在の座標に移動量を足す
            device.move_to(x, y, z, r, wait=True)
            time.sleep(0.1)

        else:
            x -= movement_x # 取得した現在の座標から移動量を引く
            device.move_to(x, y, z, r, wait=True)
            time.sleep(0.1)

def move3(s,device,red_a,red_b,grn_a,grn_b):
    import time

    
    # diff_y1 = 960 - red_a[1] - grn_b[0]
    diff_y2 = red_b[0] - grn_b[0]
    # diff3 = (diff3_y1 + diff3_y2*3)/2
    diff_y = diff_y2



    if -15 < diff_y < 15   : # もし差が50未満なら
        print("move3_compreat")
        print("pick_start")
        s.move = 4
        time.sleep(1)

    else: # もし差が10より大きければ
        x,y,z,r,_,_,_,_ = device.pose() # 現在のDobotの座標を取得
        movement_y = abs(diff_y)/20 # 移動量の計算

        # 動かす方向によって分岐する
        if 0 < diff_y:
            y += movement_y # 取得した現在の座標に移動量を足す
            device.move_to(x, y, z, r, wait=True)
            time.sleep(0.1)

        else:
            y -= movement_y # 取得した現在の座標から移動量を引く
            device.move_to(x, y, z, r, wait=True)
            time.sleep(0.1)

def pick(s,device):
    import time

    x, y, z, r, j1, j2, j3, j4 = device.pose()
    # device.move_to(x, y, -70, r, wait=True)
    device.move_to(x, y, -35, r, wait=True)
    device.suck(True) # 吸引ON
    time.sleep(0.5) # 1秒待つ
    device.move_to(x, y, z+20, r, wait=True)
    time.sleep(0.5)
    device.move_to(65, -150, -20, 0, wait=True)
    time.sleep(0.5)
    device.suck(False) # 吸引OF
    time.sleep(0.5)
    device.move_to(130, 0, 0, 0, wait=True)

    print("pick_compreat")

    s.move = None


