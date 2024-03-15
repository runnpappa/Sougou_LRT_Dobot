import processing.net.*;
import processing.serial.*;
//シリアル通信するためのファイルをインポート
import java.nio.charset.StandardCharsets;
import java.util.Objects;
int data;
//受け取ったデータを格納するためのint型の定義

int straight_spd = 125;
int curve_spd = 75;


int port = 10001;
String whatClientSaid;
char wc;
float  mouse1;
int mouse;
String straight="t";
String curve="f";
Server server;
Serial serial;
//Serialクラスの名前（今回はserial）の定義

void setup() {
  serial=new Serial(this, "COM3", 9600);
  //使用可能なポートの表示、通信速度の設定
  server=new Server(this, port);
  println("server address: " + server.ip()); 
  // IPアドレスを出力
  size(1300, 900);//表示するwindowのサイズ設定
  x=0;
  DriveReverX=700;
  y=0;
  MoveReverX=700;
  SpeedReverX=50;
  status=1;

  
  
}

void serialEvent(Serial port) {
  //シリアル通信を行ったときに割り込む
  if (port.available()>=1) {
    //シリアルポートからデータを受け取ったら
    //print("a");

    if (Amode==true||Bmode==true) {
      mouse=int(map(SpeedReverX, 50, 1170, 0, 255));//50~1170の範囲を0~255に分ける
      sendIntData(int(mouse));
    } else if (Cmode==true) {
      sendIntData(straight_spd);
    } else if (Dmode==true) {
      sendIntData(curve_spd);
    }
  }
}
