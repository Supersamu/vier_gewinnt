import numpy as np
import tensorflow as tf
from tensorflow import keras

class neuralnet(object):
    def __init__(self, number_rows, number_columns):
        model = keras.Sequential([
            keras.layers.Conv3D(input_shape=(number_rows, number_columns, 2), 
                                filters=),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(10, activation=tf.nn.softmax)
            ])
    
    
    def calculate_response(self, input_state):
        for bias, layer, weight in zip(self.biases, self.layers, self.weights):
            input_state = np.matmul(weight, expit((input_state - bias) * layer))
        output = expit(input_state - self.biases[-1]) * self.layers[-1]
        return output

    
    
    def update(self, good_positions, good_moves, bad_positions, bad_moves):
        i = 0
        j = 0
        while i < 10 and j < 1000:
            j += 1
            cost_orig = self.calculate_cost(good_positions, good_moves, bad_positions, bad_moves)
            choice_1, choice_2, choice_3, choice_4, random_float = self.modify()
            cost_new = self.calculate_cost(good_positions, good_moves, bad_positions, bad_moves)
            if cost_new < cost_orig:
                i += 1
            else:
                self.revert_modification(choice_1, choice_2, choice_3, choice_4, random_float)