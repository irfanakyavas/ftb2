import numpy as np
import pandas as pd
import random
import tensorflow as tf
from sklearn.model_selection import train_test_split, GridSearchCV
import keras
from tensorflow.keras.models import load_model

data = pd.read_csv("/content/PL_data.csv")

X = data[["attack","skill","movement",'power','mentality','defending']]
y = data[["home_goals","away_goals"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=45)

def get_result(preds):
  predicted_results = np.array([])
  for pred in preds:
    if abs(pred[0] - pred[1]) <= 0.16:
      predicted_results = np.append(predicted_results,0)
    elif pred[0] - pred[1] > 0.16:
      predicted_results = np.append(predicted_results,1)
    else : predicted_results = np.append(predicted_results,-1)
  return predicted_results
model = tf.keras.Sequential([
    tf.keras.layers.Dense(20, activation=tf.nn.relu6, input_shape=(6,)),
    tf.keras.layers.Dense(10, activation=tf.nn.relu6),
    tf.keras.layers.Dense(2, activation=tf.nn.relu6)
])

model.compile(optimizer = 'adam',loss = 'mean_absolute_error',metrics=['accuracy'])
model.fit(X_train, y_train, batch_size=30, epochs = 200, verbose=2, validation_data=(X_test, y_test))

preds = model.predict(X_test)
result = data.result[y_test.index]

eval = y_test.copy()
eval["result"] = result
eval["preds"] = get_result(preds)
model.evaluate(X_test,y_test)

correct = 0
for i in y_test.index:
  if eval.result[i] == eval.preds[i]:
    correct+=1
print(f"{correct/len(y_test.index)}")