import tensorflow as tf
from tensorflow import keras
import numpy as np
A = 8
class neuralnet(object):
    def __init__(self, random_player_option, model_number, model_architecture, subtraction_needed):
        self.random_player_option = random_player_option
        self.model_architecture = model_architecture
        self.subtraction_needed = subtraction_needed
        if not self.random_player_option:
            if self.model_architecture == 0:
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
                self.model_filepath = 'model_folder_iteration_0/' + str(model_number)
                model.save(self.model_filepath)
            elif self.model_architecture == 1:
                model = tf.keras.Sequential()
                model.add(keras.layers.Conv2D(filters=32, kernel_size=3, padding='same',
                                activation='relu', input_shape=(8, 8, 2)))
                model.add(keras.layers.Conv2D(filters=32, kernel_size=3, padding='same',
                                activation='relu'))
                model.add(keras.layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
                model.add(keras.layers.Conv2D(filters=32, kernel_size=3, padding='same',
                                activation='relu'))
                model.add(keras.layers.Conv2D(filters=32, kernel_size=3, padding='same',
                                activation='relu'))
                model.add(keras.layers.Flatten())
                model.add(keras.layers.Dense(8, activation='softmax'))
                model.compile(optimizer="adam", loss="categorical_crossentropy")
                self.model_filepath = 'model_folder_iteration_0/' + str(model_number)
                model.save(self.model_filepath)
            elif self.model_architecture == 2:
                model = tf.keras.Sequential()
                model.add(keras.layers.Conv2D(filters=8, kernel_size=3, padding='same',
                                activation='relu', input_shape=(8, 8, 2)))
                model.add(keras.layers.Conv2D(filters=8, kernel_size=3, padding='same',
                                activation='relu'))
                model.add(keras.layers.Conv2D(filters=8, kernel_size=3, padding='same',
                                activation='relu'))
                model.add(keras.layers.Conv2D(filters=8, kernel_size=3, padding='same',
                                activation='relu'))
                model.add(keras.layers.Flatten())
                model.add(keras.layers.Dense(8, activation='softmax'))
                model.compile(optimizer="adam", loss="categorical_crossentropy")
                self.model_filepath = 'model_folder_iteration_0/' + str(model_number)
                model.save(self.model_filepath)
            elif self.model_architecture == 3:
                model = tf.keras.Sequential()
                model.add(keras.layers.Conv2D(filters=32, kernel_size=3, padding='same',
                                activation='relu', input_shape=(8, 8, 2)))
                model.add(keras.layers.Conv2D(filters=32, kernel_size=3, padding='same',
                                activation='relu'))
                model.add(keras.layers.Conv2D(filters=32, kernel_size=3, padding='same',
                                activation='relu'))
                model.add(keras.layers.Conv2D(filters=32, kernel_size=3, padding='same',
                                activation='relu'))
                model.add(keras.layers.Flatten())
                model.add(keras.layers.Dense(8, activation='softmax'))
                model.compile(optimizer="adam", loss="categorical_crossentropy")
                self.model_filepath = 'model_folder_iteration_0/' + str(model_number)
                model.save(self.model_filepath)
            elif self.model_architecture == 4:
                model = tf.keras.Sequential()
                model.add(keras.layers.Conv2D(filters=32, kernel_size=5, padding='same',
                                activation='relu', input_shape=(8, 8, 2)))
                model.add(keras.layers.Conv2D(filters=32, kernel_size=5, padding='same',
                                activation='relu'))
                model.add(keras.layers.Conv2D(filters=32, kernel_size=5, padding='same',
                                activation='relu'))
                model.add(keras.layers.Conv2D(filters=32, kernel_size=5, padding='same',
                                activation='relu'))
                model.add(keras.layers.Flatten())
                model.add(keras.layers.Dense(8, activation='softmax'))
                model.compile(optimizer="adam", loss="categorical_crossentropy")
                self.model_filepath = 'model_folder_iteration_0/' + str(model_number)
                model.save(self.model_filepath)
            elif self.model_architecture == 5:
                model = tf.keras.Sequential()
                model.add(keras.layers.Conv2D(filters=128, kernel_size=5, padding='same',
                                activation='relu', input_shape=(8, 8, 2)))
                model.add(keras.layers.Conv2D(filters=128, kernel_size=5, padding='same',
                                activation='relu'))
                model.add(keras.layers.Conv2D(filters=128, kernel_size=5, padding='same',
                                activation='relu'))
                model.add(keras.layers.Conv2D(filters=128, kernel_size=5, padding='same',
                                activation='relu'))
                model.add(keras.layers.Flatten())
                model.add(keras.layers.Dense(8, activation='softmax'))
                model.compile(optimizer="adam", loss="categorical_crossentropy")
                self.model_filepath = 'model_folder_iteration_0/' + str(model_number)
                model.save(self.model_filepath)
            
    def load_neural_net(self):
        if self.random_player_option:
            return None
        else:
            return keras.models.load_model(self.model_filepath)
    
    def save_neural_net(self, number, filepath, model):
        self.model_filepath = filepath + str(number)
        model.save(self.model_filepath)
        
    def calculate_response(self, gameboard, model):
        if self.random_player_option:
            return np.random.randint(0, A)
        else:
            if self.subtraction_needed:
                board = gameboard.gamestate - 0.5*np.ones((8,8,2))
            else:
                board = gameboard.gamestate
            self.neural_output = model.predict(np.resize(board, (1,8,8,2)))
            max_indices = self.neural_output[0].argsort()[::-1]
            for max_idx in max_indices:
                if gameboard.gamestate[0, max_idx, 0] + gameboard.gamestate[0, max_idx, 1] == 0:
                    return max_idx
        
if __name__ == '__main__':
    x = neuralnet(None, 1)
    gameboard = np.ones((1,8,8,2))
    print(x.calculate_response(gameboard))