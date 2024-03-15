# 参考
# https://qiita.com/k_zoo/items/cbeda6736d727113b7cd

import serial

#シリアル通信(PC⇔Arduino)
ser = serial.Serial()
ser.port = "COM3"     #デバイスマネージャでArduinoのポート確認
ser.baudrate = 115200 #Arduinoと合わせる
ser.setDTR(False)     #DTRを常にLOWにしReset阻止　この一行はopenより上に必ず書いて
ser.open()            #COMポートを開く

# ser.write(b'a')       #送りたい内容をバイト列で送信
ser.write(b'z')     #止めたいときはこっち

ser.close()           #COMポートを閉じる

