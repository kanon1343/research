import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from keras.models import Sequential
from keras.layers import Dense,  Activation
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from keras.utils import np_utils

iris = datasets.load_iris() # データを取得
x = iris.data   
y = iris.target 

y = np_utils.to_categorical(y)  
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8)    # 教師データとテストデータに分割
x = preprocessing.scale(x)  # 標準化

# モデルの生成
model = Sequential()
model.add(Dense(10, input_dim=4))    # 入力層4ノード, 隠れ層に10ノード, 全結合
model.add(Activation("softmax"))    
model.add(Dense(3)) # 出力層3ノード,全結合
model.add(Activation("softmax"))

model.compile(loss="categorical_crossentropy",   # 誤差関数
              optimizer="adam",     # 最適化手法
              metrics=['accuracy'])


model.summary()
history = model.fit(x_train, y_train, epochs=500, batch_size=32) # 学習
# 学習過程のプロット
plt.plot(history.epoch, history.history["accuracy"], label="accuracy")
plt.plot(history.epoch, history.history["loss"], label="loss")
plt.xlabel("epoch")
plt.legend()
plt.savefig("harada.png")
from tensorflow.keras.utils import plot_model
plot_model(
    model,
    show_shapes=True,
)

# 評価
score = model.evaluate(x_test, y_test, verbose=1)
print("Test score", score[0])
print("Test accuracy", score[1])

