import tensorflow as tf
import keras
from tensorflow.keras.models import load_model
import numpy as np

"""
Expected data format to make prediction:
data = np.array([1,1,1,1,1,1], ndmin=2)
"""

X_test = pd.read_csv("X_test.csv")
y_test = pd.read_csv("y_test.csv")

model = tf.keras.models.load_model("resultPredV4.h5", custom_objects={'relu6': tf.nn.relu6})

eval["preds"] = get_result(nmodel.predict(X_test))
correct = 0
for i in y_test.index:
  if eval.result[i] == eval.preds[i]:
    correct+=1
print(f"{correct/len(y_test.index)}")
