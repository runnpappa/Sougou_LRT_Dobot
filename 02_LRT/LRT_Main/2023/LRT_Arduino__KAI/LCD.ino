#define I2Cadr 0x3e
byte contrast = 10;

//I2C初期化関数
void lcd_init(void){
  Wire.begin();
  lcd_cmd(0x38);
  lcd_cmd(0x39);
  lcd_cmd(0x14);
  lcd_cmd(0x4);
  lcd_cmd(0x70 | (contrast & 0xF));
  lcd_cmd(0x5C | ((contrast>>4) & 0x3));
  lcd_cmd(0x6C);
  delay(200);
  lcd_cmd(0x38);
  lcd_cmd(0x0C);
  lcd_cmd(0x01);
  delay(2);
}
//I2C_LCD書き込み
void lcd_cmd(byte x){
  Wire.beginTransmission(I2Cadr);
  Wire.write(0x00);
  Wire.write(x);
  Wire.endTransmission();
}
//画面クリア
void lcd_clear(void){
  lcd_cmd(0x01);
}
//画面表示OFF
void lcd_DisplayOff(){
  lcd_cmd(0x08);
}
//画面表示ON
void lcd_DisplayOn(){
  lcd_cmd(0x0C);
}
//サブ関数１
void lcd_contdata(byte x){
  Wire.write(0xC0);
  Wire.write(x);
}
//サブ関数２
void lcd_lastdata(byte x){
  Wire.write(0x40);
  Wire.write(x);
}
//文字の表示関数
void lcd_printStr(const char *s){
  Wire.beginTransmission(I2Cadr);
  while(*s){
    if(*(s+1)){
      lcd_contdata(*s);
    }else{
      lcd_lastdata(*s);
    }
    s++;
  }
  Wire.endTransmission();
}

//表示位置の指定関数
void lcd_setCursor(byte x,byte y){
  lcd_cmd(0x80 | (y * 0x40 + x));
}
