from sklearn import datasets                           # データロード用
from sklearn.model_selection import train_test_split  # 学習/テストデータ作成用
from sklearn.naive_bayes import GaussianNB             # ガウシアンナイーブベイズ実行用

# データ用意
iris = datasets.load_iris()
X = iris.data
Y = iris.target
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0, stratify = Y)

# ガウシアンナイーブベイズ実行
model = GaussianNB()              # インスタンス生成
model.fit(X_train, Y_train)       # モデル作成実行

# 予測実行
Y_pred = model.predict(X_test)
predicted = model.predict(X_test) # 予測実行

print("実行結果", Y_pred)
print("実際の値", Y_test)

print("訓練データ正解率:", model.score(X_train, Y_train))
print("テストデータの正解率:", model.score(X_test, Y_test))