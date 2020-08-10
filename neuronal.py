import numpy as np

def sigmoid(layer_result, deriv=False):
    return 1/(1+np.exp(-layer_result))

A = 7
class neuralnet(object):
    def __init__(self, shapes, random_player_option):
        self.neural_net = [[], []]
        self.random_player_option = random_player_option
        if not random_player_option:
            for i in range(0, len(shapes)):
                self.neural_net[0].append(np.random.random_sample(shapes[i]) - 0.5 )
            for i in range(0, len(shapes)):
                self.neural_net[1].append(np.random.random_sample(shapes[i][0]) - 0.5)
        
    def calculate_response(self, gameboard):
        if self.random_player_option:
            return np.random.randint(0, A)
        else:
            if gameboard.player_on_move == 0:
                neural_input = np.concatenate((gameboard.gamestate[0], gameboard.gamestate[1])).flatten()
            else:
                neural_input = np.concatenate((gameboard.gamestate[1], gameboard.gamestate[0])).flatten()
            for i in range(0, len(self.neural_net[0])):
                neural_input += self.neural_net[1][i]
                neural_input = sigmoid(np.dot(neural_input, self.neural_net[0][i]))
            self.neural_output = sigmoid(neural_input)
            max_idx = np.argmax(self.neural_output)
            return max_idx
        
    def train(self, cycles, amounts, winning_moves, winning_positions, losing_moves, losing_positions, weights, stepsize):
        def calculate_score(winning_moves, winning_positions, losing_moves, losing_positions, weights):
            score = 0
            for winning_position, winning_move in zip(winning_positions, winning_moves):
                self.calculate_response(winning_position)
                correct_response = []
                for i in range(A):
                    if i == winning_move:
                        correct_response.append(1)
                    else:
                        correct_response.append(0)
                score += weights[0] * np.linalg.norm(correct_response - self.neural_output)
            for losing_position, losing_move in zip(losing_positions, losing_moves):
                self.calculate_response(losing_position)
                correct_response = []
                for i in range(A):
                    if i == losing_move:
                        correct_response.append(0)
                    else:
                        correct_response.append(1.0/(A-1.0))
                score += weights[1] * np.linalg.norm(correct_response - self.neural_output)
            return score
        previous_score = None
        for _ in range(cycles):
            if previous_score is None:
                current_score = calculate_score(winning_moves, winning_positions, losing_moves, losing_positions, weights)
            else:
                current_score = previous_score
            self.modify(amounts, stepsize)
            new_score = calculate_score(winning_moves, winning_positions, losing_moves, losing_positions, weights)
            while new_score > current_score:
                self.undo_modify()
                self.modify(amounts, stepsize)
                new_score = calculate_score(winning_moves, winning_positions, losing_moves, losing_positions, weights)
            previous_score = new_score
                
            
            
    def modify(self, amounts, step_size=0.5):
        self.list_of_changes = []
        for _ in range(amounts):
            current_changes = []
            mult_or_add = np.random.randint(0, 1)
            if mult_or_add == 0:
                which_matrix = np.random.randint(0, 3)
                x = self.neural_net[0][which_matrix].shape
                a = np.random.randint(0, x[0])
                b = np.random.randint(0, x[1])
                change = (np.random.random() - 0.5) * step_size
                self.neural_net[0][which_matrix][a, b] += change
            else:
                which_matrix = np.random.randint(0, 3)
                x = self.neural_net[1][which_matrix].shape
                a = np.random.randint(0, x[0])
                b = None
                change = (np.random.random() - 0.5) * step_size
                self.neural_net[1][which_matrix][a] += change
            current_changes.append(mult_or_add)
            current_changes.append(which_matrix)
            current_changes.append(a)
            current_changes.append(b)
            current_changes.append(change)
        self.list_of_changes.append(current_changes)
    
    def undo_modify(self):
        for change_list in self.list_of_changes:
            mult_or_add = change_list[0]
            which_matrix = change_list[1]
            a = change_list[2]
            b = change_list[3]
            change = change_list[4]
        if mult_or_add == 0:
            self.neural_net[0][which_matrix][a, b] -= change
        else:
            self.neural_net[1][which_matrix][a] -= change
