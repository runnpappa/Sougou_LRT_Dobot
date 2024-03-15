#include <Adafruit_MotorShield.h>　//ライブラリ"Adafruit_MotorShield"をインクルード(pythonのインポートみたいなもの?)
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *myMotor = AFMS.getMotor(1);


void setup() {
  Serial.begin(115200);//通信速度115200bps
  Serial.println("Adafruit Motorshield v2 - DC Motor test!");
  AFMS.begin();
  myMotor->setSpeed(0);//プログラム開始時の初速
  myMotor->run(RELEASE);//止まる
}

void loop() {

  if (Serial.available() > 0) { //シリアルポートからデータを受け取ったら
    int port =  Serial.read(); //受信したデータを読み込む
 
    if (port == 'a' ) { // 動かす
      myMotor->run(FORWARD);
      myMotor->setSpeed(100);//LRTの速さ(0～255で指定)
      
    }else if (port == 'z' ) { // 止める
      myMotor->setSpeed(0);
    }
  }
}


