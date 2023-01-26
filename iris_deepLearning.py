import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from keras.models import Sequential
from keras.layers import Dense,  Activation
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from keras.utils import np_utils

iris = datasets.load_iris() # データを取得
x = iris.data   # 花の特徴量、長さなど
y = iris.target # 0, 1, 2のラベル
x = preprocessing.scale(x)  # 標準化

y = np_utils.to_categorical(y)  # one-hotエンコード.例) 1 => [0, 1, 0]
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8)    # 教師データとテストデータに分割

# モデルの生成
model = Sequential()
model.add(Dense(10, input_dim=4))    # 入力層4ノード, 隠れ層に10ノード, 全結合
model.add(Activation("sigmoid"))    # 活性化関数はsigmoid
model.add(Dense(3)) # 出力層3ノード,全結合
model.add(Activation("sigmoid"))

model.compile(loss="categorical_crossentropy",   # 誤差関数
              optimizer="adam",     # 最適化手法
              metrics=['accuracy'])

history = model.fit(x_train, y_train, epochs=500, batch_size=32) # 学習
# 学習過程のプロット
plt.plot(history.epoch, history.history["accuracy"], label="accuracy")
plt.plot(history.epoch, history.history["loss"], label="loss")
plt.xlabel("epoch")
plt.legend()
plt.savefig("harada.png")

# 評価
score = model.evaluate(x_test, y_test, verbose=1)
print("Test score", score[0])
print("Test accuracy", score[1])

# 個々のデータを入力して学習できているか見てみる
print("====================================")
print("-----------correct answer-----------")
print(y_test[0])
print(y_test[10])
print("-----------predict answer-----------")
print(np.round(model.predict(x_test)[0]))
print(np.round(model.predict(x_test)[10]))