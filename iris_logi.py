from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import *
from sklearn import datasets

iris = datasets.load_iris()
X = iris.data
Y = iris.target

#標準化する
scaler = StandardScaler() #標準化インスタンスを生成
std_X = scaler.fit_transform(X) #学習と変換

#データセットを訓練データ、訓練ラベル、テストデータ、テストラベルに分割。
(X_train, X_test, Y_train, Y_test) = train_test_split(X, Y, test_size = 0.2, random_state = 0, stratify = Y)

#モデル作成
lr = LogisticRegression(random_state=0, multi_class="multinomial")

#訓練
lr.fit(X_train, Y_train)

#予測結果
Y_pred = lr.predict(X_test)
print("予測結果：", Y_pred)
print("実際の値：", Y_test)

#正解率
print("訓練データの正解率：", lr.score(X_train, Y_train))
print("テストデータの正解率：", lr.score(X_test, Y_test))
