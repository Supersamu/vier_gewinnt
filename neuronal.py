import numpy as np


def initialize_neuralnet(shapes):
    neural_net = [[],[]]
    for i in range(0, len(shapes)):
        neural_net[0].append( 2 * np.random.random_sample(shapes[i]) - 1 )
    for i in range(0, len(shapes)):
        neural_net[1].append( 2 * np.random.random_sample(shapes[i][0]))
    return neural_net

    

def calculate_response(gamestate, neural_net):
    neural_input = gamestate.flatten()
    for i in range(0, len(neural_net[0])):
        neural_input = np.dot(neural_net[0][i], neural_input)
        neural_input += neural_net[1][i]
    max_idx = np.argmax(neural_input)
    return max_idx

def modify(neural_net):
    which_matrix = np.random.randint(0, 3)
    x = neural_net[0][which_matrix].shape
    a = np.random.randint(0, x[0])
    b = np.random.randint(0, x[1])
    neural_net[0][which_matrix][a, b] += (np.random.random() - 0.5)*0.5

#todo refactor, so that gamestate.flatten() is unnecessary