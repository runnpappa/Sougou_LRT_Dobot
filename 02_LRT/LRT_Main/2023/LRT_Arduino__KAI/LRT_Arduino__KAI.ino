#include <Wire.h> //ライブラリ"Wire"をインクルード(pythonのインポートみたいなもの?)
#include <Adafruit_MotorShield.h>
//#include "utility/Adafruit_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *myMotor = AFMS.getMotor(1);
bool sensor = false; //ブール型(TrueかFalse)で定義

int port;
int recv_data;
char mode[1]; //要素数1の配列をchar型で定義

void setup() {
  Serial.begin(9600);//通信速度9600bps
  Serial.println("Adafruit Motorshield v2 - DC Motor test!");
  AFMS.begin();
  myMotor->setSpeed(0);//プログラム開始時の初速
  myMotor->run(RELEASE);//止まる
//  lcd_init();
  mode[0] = 'z';
  pinMode(2, INPUT);
  pinMode(3, INPUT);
}

void loop() {
//  char d[3];
  //dtosrtf(小数,桁数,小数点以下桁数,格納する文字列);
//  dtostrf(recv_data, 3, 0, d);
//  //LCD１行目表示
//  lcd_setCursor(0, 0);
//  lcd_printStr("moX:");
//  lcd_setCursor(5, 0);
//  lcd_printStr(d);
//  lcd_setCursor(0, 1);
//  lcd_printStr("mode:");

  Serial.write(255);//データを送信する
  if (Serial.available() == 1) { //シリアルポートからデータを受け取ったら
    port = Serial.read(); //受信したデータを読み込む
    if (port == 'a' || port == 'b' || port == 'c' || port == 'd' || port == 'z') {
      mode[0] = port;
//      lcd_setCursor(6, 1);
//      lcd_printStr(mode);
      if (mode[0] == 'c' || mode[0] == 'd') {
        if (digitalRead(3) == HIGH) {
          sensor = true;
        }
        if (sensor == true) {
          recv_data = recv_data - 1;
          if (recv_data <= 80) {
            recv_data = 80;
          }
          if (digitalRead(2) == HIGH) {
            recv_data = 0;
            delay(5000);
            sensor = false;
          }
          delay(100);
        } else if (digitalRead(2) == LOW) {
          if (mode[0] == 'c') {
            recv_data = 180;
          } else if (mode[0] == 'd') {
            recv_data = 130;
          }
        }
      }
      else if (mode[0] == 'z') {
        recv_data = 0;
      }
    }
  }

  if (Serial.available() > 2) {
    byte head = Serial.read();  // 1番目のデータ
    if ( head >= 128 ) {          // 128以上であれば先頭データなので、それに続くデータを読み取る
      byte high = Serial.read();  // 2番目のデータ
      byte low  = Serial.read();  // 3番目のデータ
      recv_data = ((head - 128) << 14) + (high << 7) + low;  // 受信データ
    }
    if (mode[0] == 'a' || mode[0] == 'c' || mode[0] == 'd') {
      myMotor->run(FORWARD);
    } else if (mode[0] == 'b') {
      myMotor->run(BACKWARD);
    }
  }
  myMotor->setSpeed(recv_data);
}

