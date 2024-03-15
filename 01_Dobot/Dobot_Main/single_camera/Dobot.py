def dobot(device,point):
    from serial.tools import list_ports
    import pydobot
    import time

    red_x,red_y,yel_x,yel_y = point
    diff_x = red_x - yel_x # アームと対象のx座標の差
    diff_y = red_y - yel_y # アームと対象のy座標の差

    if -10 < diff_x < 10: # もし差が10未満なら
        # print("Pass")
        time.sleep(0.1)
        pass

    else: # もし差が10より大きければ
        x1,y1,z1,r1,_,_,_,_ = device.pose() # 現在のDobotの座標を取得
        movement_x = abs(diff_x)/5 # 移動量の計算


        # 動かす方向によって分岐する
        if 0 < diff_x:
            # print("+x")
            x1 += movement_x # 取得した現在の座標に移動量を足す
            device.move_to(x1, y1, z1, r1, wait=True)

        else:
            # print("-x")
            x1 -= movement_x # 取得した現在の座標から移動量を引く
            device.move_to(x1, y1, z1, r1, wait=True)
