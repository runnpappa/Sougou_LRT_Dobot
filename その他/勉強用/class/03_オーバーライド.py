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

    # 名前取得メソッド
    def get_name(self):
        return self.name

# Humanクラスを継承して、HumanHealthを定義
class HumanHealth(Human):

    # コンストラクタ
    def __init__(self, name, year, birth, height, weight):

        #親クラスのコンストラクタを呼び出す
        super().__init__(name, year, birth)

        self.height = height
        self.weight = weight

    # BMIメソッドを追加
    def get_bmi(self):
        return round(self.weight/(self.height**2),2)

    # 自己紹介メソッドをオーバーライド
    def introduce(self):
        text = "私の名前は、{}です。今年で{}歳になります。BMIは{}です。"
        return text.format(self.name, self.year, self.get_bmi())

souma = HumanHealth("souma", 26, "19931013", 1.7, 70)
# オーバーライド
print (souma.introduce())