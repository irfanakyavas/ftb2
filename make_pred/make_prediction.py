import tensorflow as tf
import keras
from tensorflow.keras.models import load_model
import numpy as np

"""
Expected data format to make prediction:
data = np.array([1,1,1,1,1,1], ndmin=2)
"""
data = pd.read_csv("PL_data.csv")

X_test = pd.read_csv("X_test.csv")
y_test = pd.read_csv("y_test.csv")

model = tf.keras.models.load_model("resultPredV4.h5", custom_objects={'relu6': tf.nn.relu6})

# Making score prediction
preds = model.predict(X_test)
# Loading real results (1,0,-1) 
result = data.result[y_test.index]

# Converting score predictions to match result predictions (1,0,-1)
def get_result(preds):
  predicted_results = np.array([])
  for pred in preds:
    if abs(pred[0] - pred[1]) <= 0.16:
      predicted_results = np.append(predicted_results,0)
    elif pred[0] - pred[1] > 0.16:
      predicted_results = np.append(predicted_results,1)
    else : predicted_results = np.append(predicted_results,-1)
  return predicted_results

eval = y_test.copy()
eval["result"] = result
eval["preds"] = get_result(preds)

eval["preds"] = get_result(nmodel.predict(X_test))
correct = 0
for i in y_test.index:
  if eval.result[i] == eval.preds[i]:
    correct+=1
print(f"{correct/len(y_test.index)}")
