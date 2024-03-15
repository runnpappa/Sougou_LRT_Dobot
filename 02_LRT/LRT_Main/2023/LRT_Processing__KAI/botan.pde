int x, DriveReverX;
//運転停止(x=0で停止,1で運転/DriveReverXは運転レバーのX座標)

int y, MoveReverX;
//前進後退(y=0で後退,1で前進/MoveXは運転レバーのX座標)

int SpeedReverX;//スピード調節のレバー

int status;//画面切り替え用

boolean Amode=false, Bmode=false, Cmode=false, Dmode=false;
//それぞれのモードをfalse,trueで表している
//Amode=手動の前進,Bmode=手動の後退,Cmode=自動の直線時,Dmode=自動の曲線時

String receive;

void draw() {
  serial.read();//Aruduino側からデータを受け取る
  Client client=server.available();//読み取ったデータを箱に入れる

  background(0);//背景の色の設定

  //運転の設定
  fill(0, 0, 255);//色(青)
  rect(950, 50, 250, 200);//座標x950y50~x+250y+200の四角形

  //前進後退の設定
  fill(0, 255, 0);//色(緑)
  rect(950, 300, 250, 200);//座標x950y300~x+250y+200の四角形

  //スピードメーター
  fill(255);//白
  rect(50, 650, 200, 200);//座標x50y200~x+650y+200の四角形
  fill(0, 250, 255);//水色
  rect(250, 650, 200, 200);//座標x250y200~x+650y+200の四角形
  fill(0, 255, 100);//黄緑
  rect(450, 650, 200, 200);//座標x450y200~x+650y+200の四角形
  fill(255, 255, 0);//黄
  rect(650, 650, 200, 200);//座標x650y200~x+650y+200の四角形
  fill(255, 50, 0);//橙
  rect(850, 650, 200, 200);//座標x850y200~x+650y+200の四角形
  fill(255, 0, 0);//赤
  rect(1050, 650, 200, 200);//座標x1050y200~x+650y+200の四角形
  fill(150);//灰色
  rect(SpeedReverX, 640, 80, 220);//座標x'SpeedReverX'y200~x+650y+200の四角形

  //画面切り替え
  if (status==1) {//手動の時
    fill(255);//色(白)
  }
  if (status==2) {//自動の時
    fill(255, 0, 0);//色(赤)
  }
  rect(50, 50, 200, 200);//ボタンのサイズ
  fill(0);//色(黒)
  textSize(40);//文字の大きさ
  if (status==1) {//手動の時
    text("MANUAL", 50, 250);//MANUALをx50,y250に表示
  }
  if (status==2) { 
    text("AUTO", 50, 250);//AUTOをx50,y250に表示
  }

  fill(255);//色(白)
  textSize(100);//文字の大きさ
  if (x==0) {//停止の時
    text("STOP", 350, 180);//STOPをx350,y180に表示
  } else if (x==1) {//運転の時
    text("DRIVE", 325, 180);//DRIVEをx325,y180に表示
  }

  if (y==0) {//前進の時
    text("FORWARD", 150, 425);//FORWARDをx150,y425に表示
  } else if (y==1) {//後退の時
    text("BACKWARD", 125, 425);//BACKWARDをx125,y425に表示
  }

  textSize(60);//文字の大きさ
  text("speed", 30, 620);//speedを30
  textSize(90);//
  
  if (Amode==true||Bmode==true) {
    text(mouse, 225, 620);//
  }
  else if (Cmode==true) {
    text(straight_spd, 225, 620);
  }
  else if (Dmode==true) {
    text(curve_spd, 225, 620);
  }

  if (mousePressed==true) {
    if (mouseX>=SpeedReverX&&mouseX<=SpeedReverX+80) {
      if (mouseY>=640&&mouseY<=860) {
        SpeedReverX=mouseX-40;
      }
    }
  }

  if (SpeedReverX<=50) {
    SpeedReverX=50;
  }

  if (SpeedReverX>=1170) {
    SpeedReverX=1170;
  }

  if (client!=null) {
    //println("OK");
    byte[]b=client.readBytes();
    receive=new String(b, StandardCharsets.UTF_8);
    if (receive!=null) {
    }
  }

  if (x==1&&status==1&&y==0&&Amode==false) {//運転できる状態
    Bmode=false;
    Cmode=false;
    Dmode=false;
    serial.write('a');
    delay(50);
    serial.write('a');
    Amode=true;
   // print("aaaaa");
  } else if (x==1&&status==1&&y==1&&Bmode==false) {
    Amode=false;
    Cmode=false;
    Dmode=false;
    serial.write('b');
    delay(50);
    serial.write('b');    
    Bmode=true;
  } else if (x==1&&status==2&&Objects.equals(receive, straight)) {//自動
    SpeedReverX=int(map(straight_spd, 0, 255, 50, 1170));
    Amode=false;
    Bmode=false;
    Dmode=false;
    serial.write('c');
    delay(50);
    serial.write('c');   
    Cmode=true;
  } else if (x==1&&status==2&&Objects.equals(receive, curve)) {
    SpeedReverX=int(map(curve_spd,0, 255, 50, 1170));
    Amode=false;
    Bmode=false;
    Cmode=false;
    serial.write('d');
    delay(50);
    serial.write('d');     
    
    Dmode=true;
  } else if (x==0) {
    SpeedReverX=50;
    Amode=false;
    Bmode=false;
    Cmode=false;
    Dmode=false;
    delay(50);
    serial.write('z');
   // print("zzzzz");

    
    
    //println("Zmode");
  }
  //print("Amode");
 // println(Amode);
 // print("Bmode");
 // println(Bmode);
 // print("Cmode");
 // println(Cmode);
 // print("Dmode");
 // println(Dmode);
}

void mousePressed() {
  if (mouseX>=50&&mouseX<=250) {
    if (mouseY>=50&&mouseY<=250) {
      if (status==1) {
        status=2;
      } else if (status==2) {
        status=1;
      }
    }
  }
  if (mouseX>=950&&mouseX<=1200) {
    if (mouseY>=50&&mouseY<=250) {
      if (x==0) {
        x=1;
        //delay(10);
      } else if (x==1) {
        x=0;
      }
    }
  }
  if (x==0) {
    if (mouseX>=950&&mouseX<=1200) {
      if (mouseY>=300&&mouseY<=500) {
        if (y==0) {
          y=1;
        } else if (y==1) {
          y=0;
        }
      }
    }
  }
}
void sendIntData(int value) {
  byte low=(byte)(value&127);
  byte high=(byte)((value>>7)&127);
  byte head=(byte)(((value>>14)&127)+128);
  //println(value);
  serial.write(head);
  serial.write(high);
  serial.write(low);
}
