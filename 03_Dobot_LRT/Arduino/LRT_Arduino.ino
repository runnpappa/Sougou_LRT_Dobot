#include <Adafruit_MotorShield.h>
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
    
    if (port == 'c') { //カーブの時
      myMotor->run(FORWARD);
      myMotor->setSpeed(100);
      
    }else if (port == 's') { //直線の時
      myMotor->run(FORWARD);
      myMotor->setSpeed(150);
      
    }else if (port == 'z') { //障害物があるとき
      myMotor->run(RELEASE);
      myMotor->setSpeed(0); 
    }
  }
}



