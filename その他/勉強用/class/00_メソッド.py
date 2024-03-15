# class宣言
class Human:

    # コンストラクタ
    def __init__(self, name, year, birth):
        self.name = name
        self.year = year
        self.birth = birth

    # 自己紹介メソッド
    def introduce(self):
        text = "私の名前は、{}です。今年で{}歳になります。"
        return text.format(self.name, self.year)

    # 加齢メソッド
    def grow_old(self, after):
        self.year += after

# インスタンス作成
souma_human = Human("souma", 26, "19931013")
print (souma_human.introduce())
# 加齢メソッド呼び出し
souma_human.grow_old(2)
print (souma_human.introduce())