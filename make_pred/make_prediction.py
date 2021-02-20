import tensorflow as tf
import keras
from tensorflow.keras.models import load_model
import numpy as np

model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation=tf.nn.tanh, input_shape=(6,)),
    tf.keras.layers.Dense(1)
])

# RMSprop and Adadelta denenecek,
model.compile(optimizer = 'adam',loss = 'mean_absolute_error',metrics=['accuracy'])

model_path = "/content/savedModel.h5"
model.save(model_path)

example_data = np.array([1.6,-3,3,0.4,1.4,1.5],ndmin=2)
pred = model.predict(example_data)
if pred < 0.55 and pred > -0.55:
  print("Predicted result: DRAW")
if pred >= 0.55:
  print("Predicted result: HOME WIN")
if pred <= -0.55:
  print("Predicted result: AWAY WIN")

