import numpy as np
from scipy.special import expit
import numpy.linalg as LA


class neuralnet(object):
    def __init__(self, layer_sizes):
        list_of_layers = []
        list_of_biases = []
        for layer_size in layer_sizes:
            list_of_layers.append(np.random.ranf((layer_size,)))
            list_of_biases.append(np.random.ranf((layer_size,)))
        list_of_weight_matrices = []
        for size_1, size_2 in zip(layer_sizes[:-1], layer_sizes[1:]):
            list_of_weight_matrices.append(np.random.ranf((size_2, size_1)))
        self.layers = list_of_layers
        self.biases = list_of_biases
        self.weights = list_of_weight_matrices
        
        
    def show(self):
        for layer in self.layers:
            print(layer)
        for bias in self.biases:
            print(bias)
        for weight in self.weights:
            print(weight)
    
    
    def calculate_response(self, input_state):
        for bias, layer, weight in zip(self.biases, self.layers, self.weights):
            input_state = np.matmul(weight, expit((input_state - bias) * layer))
        output = expit(input_state - self.biases[-1]) * self.layers[-1]
        return output
    
    
    def modify(self):
        random_float = 0.5 * np.random.random() - 0.25
        choice_1 = np.random.randint(3)
        choice_4 = 0
        if choice_1 == 0:
            choice_2 = np.random.randint(len(self.layers))
            choice_3 = np.random.randint(len(self.layers[choice_2]))
            self.layers[choice_2][choice_3] += random_float
        if choice_1 == 1:
            choice_2 = np.random.randint(len(self.biases))
            choice_3 = np.random.randint(len(self.biases[choice_2]))
            self.biases[choice_2][choice_3] += random_float
        if choice_1 == 2:
            choice_2 = np.random.randint(len(self.weights))
            choice_3 = np.random.randint(self.weights[choice_2].shape[0])
            choice_4 = np.random.randint(self.weights[choice_2].shape[1])
            self.weights[choice_2][choice_3, choice_4] += random_float
        return choice_1, choice_2, choice_3, choice_4, random_float
    
    
    def revert_modification(self, choice_1, choice_2, choice_3, choice_4, random_float):
        if choice_1 == 0:
            self.layers[choice_2][choice_3] -= random_float
        if choice_1 == 1:
            self.biases[choice_2][choice_3] -= random_float
        if choice_1 == 2:
            self.weights[choice_2][choice_3, choice_4] -= random_float
    
    
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
            
    
    def calculate_cost(self, good_positions, good_moves, bad_positions, bad_moves):
        cost = 0
        for good_position, good_move in zip(good_positions, good_moves):
            perfect_move = np.zeros(shape=(3))
            perfect_move[good_move] = 1
            cost += LA.norm(self.calculate_response(good_position) - perfect_move)
        for bad_position, bad_move in zip(bad_positions, bad_moves):
            perfect_move = np.ones(shape=(3))/2
            perfect_move[bad_move] = 0
            cost += LA.norm(self.calculate_response(bad_position) - perfect_move)
        return cost