import tensorflow as tf
import matchlogic
import numpy as np
import neuronal_keras
import pickle
import time
class tournament_selfplay(object):
    def __init__(self, list_of_neural_nets, number_rows, number_columns, number_contiguous, filepath, random_move_prob):
        player_index = list(range(len(list_of_neural_nets)))
        list_of_games = []
        # loading the models into the cache:
        tf.keras.backend.clear_session()
        list_of_models = []
        for index in player_index:
            neural_net = list_of_neural_nets[index]
            curr_time = time.time()
            tmp = neural_net.load_neural_net()
            after_time = time.time()
            print('loading model number ' + str(index) +', time taken = ' +str(after_time - curr_time))
            list_of_models.append(tmp)
        for model_1_index, player_1_index in enumerate(player_index):
            print(player_1_index)
            for model_2_index, player_2_index in enumerate(player_index):
                if player_1_index != player_2_index:
                    neural_net_p1 = list_of_neural_nets[player_1_index]
                    model_1 = list_of_models[model_1_index]
                    neural_net_p2 = list_of_neural_nets[player_2_index]
                    model_2 = list_of_models[model_2_index]
                    match = matchlogic.match(number_rows, number_columns, number_contiguous)
                    match.play(neural_net_p1, neural_net_p2, model_1, model_2, show=False, random_move_prob=random_move_prob)
                    list_of_games.append(match)
        tf.keras.backend.clear_session()
        with open(filepath, 'wb') as f:
            pickle.dump(list_of_games, f, pickle.HIGHEST_PROTOCOL)

class tournament_both_random(object):
    def __init__(self, number_games, filepath):
        counter = 0
        player_1 = neuronal_keras.neuralnet(True, None)
        player_2 = neuronal_keras.neuralnet(True, None)
        list_of_games = []
        while counter < number_games:
            counter += 1
            model_1 = player_1.load_neural_net()
            model_2 = player_2.load_neural_net()
            match = matchlogic.match(8, 8, 4)
            match.play(player_1, player_2, model_1, model_2)
            list_of_games.append(match)
        with open(filepath, 'wb') as f:
            pickle.dump(list_of_games, f, pickle.HIGHEST_PROTOCOL)
        

class tournament_pretraining(object):
    def __init__(self, list_of_neural_nets, training_partner, number_rows, number_columns, number_contiguous, depth):
        number_players = len(list_of_neural_nets)
        player_index = list(range(number_players))
        self.result_matrix_1 = np.zeros((number_players))
        self.result_matrix_2 = np.zeros((number_players))
        self.winning_positions = []
        self.winning_moves = []
        self.losing_positions = []
        self.losing_moves = []
        for player_1_index in player_index:
            print("Player " + str(player_1_index) + " plays")
            neural_net_p_1 = list_of_neural_nets[player_1_index]
            neural_net_p_2 = training_partner
            model_1 = neural_net_p_1.load_neural_net()
            model_2 = neural_net_p_2.load_neural_net()
            match = matchlogic.match(number_rows, number_columns, number_contiguous)
            match.play(neural_net_p_1, neural_net_p_2, model_1, model_2, depth)
            self.result_matrix_1[player_1_index] = match.winner
            self.winning_positions.extend(match.winning_positions)
            self.winning_moves.extend(match.winning_moves)
            self.losing_positions.extend(match.losing_positions)
            self.losing_moves.extend(match.losing_moves)
            neural_net_p_2 = list_of_neural_nets[player_1_index]
            neural_net_p_1 = training_partner
            match = matchlogic.match(number_rows, number_columns, number_contiguous)
            match.play(neural_net_p_1, neural_net_p_2, model_2, model_1, depth)
            self.result_matrix_1[player_1_index] = match.winner
            self.winning_positions.extend(match.winning_positions)
            self.winning_moves.extend(match.winning_moves)
            self.losing_positions.extend(match.losing_positions)
            self.losing_moves.extend(match.losing_moves)