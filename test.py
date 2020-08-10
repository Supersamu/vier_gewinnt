import tensorflow as tf
from tensorflow import keras
import numpy as np
import pickle
import os.path
import secrets
import time
model = tf.keras.Sequential()
model.add(keras.layers.Conv2D(filters=8, kernel_size=3, padding='same', 
                activation='relu', input_shape=(8, 8, 2)))
model.add(keras.layers.Conv2D(filters=8, kernel_size=3, padding='same', 
                activation='relu'))
model.add(keras.layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
model.add(keras.layers.Conv2D(filters=8, kernel_size=3, padding='same', 
                activation='relu'))
model.add(keras.layers.Conv2D(filters=8, kernel_size=3, padding='same', 
                activation='relu'))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(8, activation='softmax'))
model.compile(optimizer="adam", loss="categorical_crossentropy")
empty_list = []
for i in range(100):
    empty_list.append(np.random.rand(8,8,2))
empty_list = np.array(empty_list)
a = []
for i in range(100):
    a.append(np.random.rand(8))
a = np.array(a)
model.fit(empty_list, a)