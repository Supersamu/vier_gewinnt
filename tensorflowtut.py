import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

model = tf.keras.Sequential()
model.add(keras.layers.Conv2D(filters=16, kernel_size=5, padding='same',
                activation='relu', input_shape=(8, 8, 2)))
model.add(keras.layers.Conv2D(filters=16, kernel_size=5, padding='same',
                activation='relu'))
model.add(keras.layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
model.add(keras.layers.Conv2D(filters=16, kernel_size=5, padding='same',
                activation='relu'))
model.add(keras.layers.Conv2D(filters=16, kernel_size=5, padding='same',
                activation='relu'))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(8, activation='softmax'))
model.compile(optimizer="adam", loss="categorical_crossentropy")

model.summary()
