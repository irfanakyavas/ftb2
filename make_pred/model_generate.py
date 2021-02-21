import numpy as np
import pandas as pd
import random
import tensorflow as tf
from sklearn.model_selection import train_test_split, GridSearchCV
import keras
from tensorflow.keras.models import load_model

data = pd.read_csv("PL_data.csv")

"""
X = data[["attack","skill","movement",'power','mentality','defending']]
y = data[["home_goals","away_goals"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=45)
"""
X_train = pd.read_csv("X_train.csv")
X_test = pd.read_csv("X_test.csv")
y_train = pd.read_csv("y_train.csv")
y_test = pd.read_csv("y_test.csv")

model = tf.keras.Sequential([
    tf.keras.layers.Dense(20, activation=tf.nn.relu6, input_shape=(6,)),
    tf.keras.layers.Dense(10, activation=tf.nn.relu6),
    tf.keras.layers.Dense(2, activation=tf.nn.relu6)
])

model.compile(optimizer = 'adam',loss = 'mean_absolute_error',metrics=['accuracy'])
model.fit(X_train, y_train, batch_size=30, epochs = 200, verbose=2, validation_data=(X_test, y_test))

print(model.evaluate(X_test,y_test))
