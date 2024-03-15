def move(s,device,Size):
    import time
    import numpy as np

    class DobotMove:
        def __init__(self,s,Size):
            Obj_xy   = s.Obj_xy
            Dbt_xy   = s.Dbt_xy
            Obj_xy_T = s.Obj_xy_T
            Dbt_xy_T = s.Dbt_xy_T

            # カメラの歪みに対処するためにDobotの座標を補正する
            if s.move == 2 or s.move == 3:
                centerX = int(Size[0]/2)
                Dbt_x = Dbt_xy[0]
                sign = np.sign(Dbt_x - centerX) # 符号判定
                a = int(abs((Dbt_x - centerX))**1.2/50) # 補正値の計算 Dobotの座標がカメラの中心から離れるほど補正が強くなる

                # Dobotの座標を補正後の値に書き換える
                if sign == 1:
                    Dbt_xy[0] = Dbt_x - a
                elif sign == -1:
                    Dbt_xy[0] = Dbt_x + a

            self.diff_x_T,self.diff_y_T = Obj_xy_T - Dbt_xy_T
            self.diff_x,self.diff_y = Obj_xy - Dbt_xy
            self.movement_x = 0
            self.movement_y = 0

        def calculation(self,s): # 座標差からDobotの移動量を計算する関数

            # s.move == 1   カメラ1で調整(上から)
            # s.move == 2   カメラ2で調整(側面から)
            # s.move == 3   カメラ3で調整(正面から)

            if s.move == 3:
                if abs(self.diff_x) > 10:
                    self.movement_y = int(self.diff_x/10) # カメラ3のX座標＝Dobotのy座標なのでmovement_yに格納
                    self.movement_x = 0 # x軸は移動しない
                else:
                    s.move = 4 # 次の動作へ
                    time.sleep(0.4)

            elif s.move == 2:
                if abs(self.diff_x) > 10:
                    self.movement_x = int(self.diff_x/10)
                    self.movement_y = 0 # y軸は移動しない
                else:
                    s.move = 3 # 次の動作へ
                    time.sleep(0.4)

            elif s.move == 1:
                if abs(self.diff_x_T) > 20 and abs(self.diff_y_T) > 20:
                    self.movement_x = int(self.diff_x_T/20) # 移動量の計算
                    self.movement_y = int(-self.diff_y_T/20) # 画像のy軸の方向がDobotと逆なのでマイナスをつける
                else:
                    s.move = 2 # 次の動作へ
                    time.sleep(0.4)

        def move(self,device): # 計算した移動量をもとにDobotを動かす関数
            x,y,z,r = device.pose()[:4] # 現在のDobotの座標を取得

            if self.movement_x != 0: # 移動量が0じゃなかったら
                x += self.movement_x # 取得した現在の座標に移動量を足す
                device.move_to(x, y, z, r, wait=True)
                time.sleep(0.1)

            if self.movement_y != 0:
                y += self.movement_y
                device.move_to(x, y, z, r, wait=True)
                time.sleep(0.1)


    D = DobotMove(s,Size)
    D.calculation(s)
    D.move(device)



def pick(s,device): # 吸引時の動作
    import time
    x, y, z, r = device.pose()[:4]

    device.move_to(x, y, -39, r, wait=True) # 吸引時の高さ(手動で調整)
    device.suck(True) # 吸引ON
    time.sleep(0.5)
    device.move_to(x, y, z+30, r, wait=True)
    time.sleep(0.5)
    device.move_to(65, -150, z+30, 0, wait=True)
    time.sleep(0.5)
    device.move_to(65, -150, -20, 0, wait=True)
    time.sleep(0.5)
    device.suck(False) # 吸引OF
    time.sleep(0.5)
    device.move_to(200, 0, -8, 0, wait=True)

    s.move = False


