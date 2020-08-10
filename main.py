import pickle
import neuronal_keras
import tournamentlogic
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import time
import matplotlib.pyplot as plt
import copy
import os.path
#gameboard_dimensions:
width = 8
height = 8
connect = 4
model_path = ''
model_sub_path = 'model_sub_folder_iteration_'
tourney_filename = 'tournament_'
new_nn_filename = 'neural_nets_training_step_'
new_sub_nn_filename = 'neural_nets_sub_training_step_'
raw_data_filename = 'raw_data_'
amount = 48


def watch_games(number):
    with open(tourney_filename + str(number) + '.pickle', 'rb') as f:
        tournament = pickle.load(f)
    tournament = tournament[::-1]
    for match in tournament[0:5]:
        for gameboard in match.gameboard_list:
            gameboard.show()
            input('')

def create_batch(amount):
    list_of_neural_nets = []
    x = list(range(amount))
    a = np.array([1, 1])
    b = []
    for i in range(6):
        b.extend(list(a*i))
    print(b)
    for model_number, model_architecture in zip(x, b):
        list_of_neural_nets.append(neuronal_keras.neuralnet(False, model_number, model_architecture, True))
    with open('neural_nets_sub_training_step_0.pickle', 'wb') as f:
        pickle.dump(list_of_neural_nets, f, pickle.HIGHEST_PROTOCOL)
        

def play_tournament(number, random_play):
    with open(new_nn_filename + str(number) + '.pickle', 'rb') as f:
        list_of_nets = pickle.load(f)
    x = tourney_filename + str(number) + '.pickle'
    tournamentlogic.tournament_selfplay(list_of_nets, 8, 8, 4, x, random_play)


def create_target_vector(legal_moves, winning_moves):
    num_winning_moves = len(winning_moves)
    target_vector = []
    if num_winning_moves > 0 and num_winning_moves != len(legal_moves):
        if num_winning_moves > 3:
            return None
        else:
            for i in range(8):
                if i in winning_moves:
                    target_vector.append(1.0/(num_winning_moves*1.0))
                else:
                    target_vector.append(0)
            return target_vector
    else:
        print('uh-oh')
        return None

def can_win(gameboard, depth): #depth
    legal_moves = []
    winning_moves = []
    if depth == 0: 
        # returns True if at least one move immediately leads to a win
        # returns False if no immediate win can be achieved
        for move in range(8):
            temp_gameboard = copy.deepcopy(gameboard)
            if temp_gameboard.check_if_legal(move):
                legal_moves.append(move)
                temp_gameboard.makemove(move)
                if temp_gameboard.check_if_prev_player_has_won():
                    winning_moves.append(move)
                if len(winning_moves) != 0:
                    win_possible = True
                else:
                    win_possible = False
        return legal_moves, winning_moves, win_possible
    else:
        if depth%2 == 1: 
            # returns True if a defense is impossible
            # returns False if the player can win or defend
            num_win_possible = 0
            legal_moves = []
            defending_moves = []
            for move in range(8):
                temp_gameboard = copy.deepcopy(gameboard)
                if temp_gameboard.check_if_legal(move):
                    legal_moves.append(move)
                    temp_gameboard.makemove(move)
                    if temp_gameboard.check_if_prev_player_has_won():
                        defending_moves.append(move)
                    else:
                        _,_,win_possible = can_win(temp_gameboard, depth-1)
                        if win_possible:
                            num_win_possible += 1
                        else:
                            defending_moves.append(move)
            if num_win_possible == len(legal_moves): # every legal move leads to a loss
                return None, None, True # defense impossible
            else: # there exist moves that defend
                if len(legal_moves) == len(defending_moves):
                    return None, None, False # every move defends
                else: # a true subset of legal moves defends
                    return legal_moves, defending_moves, False
        if depth%2 == 0:
            winning_moves = []
            legal_moves = []
            num_win_possible = 0
            for move in range(8):
                temp_gameboard = copy.deepcopy(gameboard)
                if temp_gameboard.check_if_legal(move):
                    legal_moves.append(move)
                    temp_gameboard.makemove(move)
                    _,_,defense_impossible = can_win(temp_gameboard, depth-1)
                    if defense_impossible:
                        num_win_possible += 1
                        winning_moves.append(move)
            if num_win_possible > 0:
                return legal_moves, winning_moves, True
            else:
                return None, None, False

def calculate_best_move(position, ):
    legal_moves, winning_moves, win_possible = can_win(position, 0)
    if win_possible:
        target_vector = create_target_vector(legal_moves, winning_moves)
        return target_vector
    legal_moves, winning_moves, win_possible = can_win(position, 2)
    if win_possible:
        target_vector = create_target_vector(legal_moves, winning_moves)
        return target_vector
    legal_moves, defending_moves, defense_impossible = can_win(position, 1)
    if not defense_impossible and defending_moves is not None:
        target_vector = create_target_vector(legal_moves, defending_moves)
        return target_vector
    return None
    
    
def extract_from_match(match, statistic_dict):
    if match.illegal_loss:
        statistic_dict['number_illegal_losses'] += 1
    else:
        if match.winner == None:
            statistic_dict['draws'] += 1
        elif match.winner == 0:
            statistic_dict['player_1_won'] += 1
            
        else:
           statistic_dict['player_2_won'] += 1
        if match.winner == 0 or match.winner == 1:
            if match.gameboard.type_win == 'leftandright':
                statistic_dict['left_and_right_wins'] += 1
            elif match.gameboard.type_win == 'upanddown':
                statistic_dict['up_and_down_wins'] += 1
            else:
                statistic_dict['diagonal_wins'] += 1
    target_vector_list = []
    position_list = []
    
    if match.illegal_loss:
        gameboard_list = match.gameboard_list
    else:
        gameboard_list = match.gameboard_list[0:-1]
    for gameboard in gameboard_list:
        target_vector = calculate_best_move(gameboard)
        if target_vector is not None:
            target_vector_list.append(target_vector)
            position_list.append(gameboard.gamestate)
                    
                
    return position_list, target_vector_list
    
def insert(array_new, list_new, array_old, list_old):
    for new_element, new_vector in zip(array_new, list_new):
        flag = False
        for old_element, (index, old_vector) in zip(array_old, enumerate(list_old)):
            if np.array_equal(new_element, old_element):
                # the two positions are equal
                flag = True
                break
        if not flag: # the two positions are not equal
            array_old.append(new_element)
            list_old.append(new_vector)
        else:# the two positions are equal
            if not new_vector == old_vector:
                print('warning')
                max_new_vector = np.max(new_vector)
                max_old_vector = np.max(old_vector)
                if max_new_vector > max_old_vector:
                    list_old[index] = new_vector
    return array_old, list_old

def mirror(positions, moves):
    new_position_list = []
    new_move_list = []
    for position, move in zip(positions, moves):
        new_position_list.append(position[:,::-1,:])
        new_move_list.append(move[::-1])
    return new_position_list, new_move_list

def retrain(number, list_of_prev_successes):
    list_of_successes = []
    filename = 'raw_data_'
    if os.path.exists(new_nn_filename + str(number) + '_v2.pickle'):
        with open(new_nn_filename + str(number) + '_v2.pickle', 'rb') as f:
            neural_nets = pickle.load(f)
    else:
        with open(new_nn_filename + str(number) + '.pickle', 'rb') as f:
            neural_nets = pickle.load(f)
    new_neural_nets = []
    for index, neural_net in enumerate(neural_nets):
        if index in list_of_prev_successes:
            list_of_training_moves = []
            list_of_training_positions = []
            for i in range(1, number):
                with open(filename + str(i)+ '.pickle', 'rb') as f:
                    x = pickle.load(f)
                moves = x[0]
                positions = x[1]
                list_of_training_moves.append(moves)
                list_of_training_positions.append(positions)
            _, testing_positions, _, testing_moves = train_test_split(positions, moves, test_size=0.3, random_state=index)
            tf.keras.backend.clear_session()
            model = neural_net.load_neural_net()
            first_loss = model.evaluate(testing_positions, testing_moves)
            for positions, moves in zip(list_of_training_positions, list_of_training_moves):                
                training_positions, _, training_moves, _ = train_test_split(positions, moves, test_size=0.3, random_state=index)
                model.fit(training_positions[0:2300], training_moves[0:2300], epochs=2, batch_size=64)
            second_loss = model.evaluate(testing_positions, testing_moves)
            print('________________________________')
            if second_loss < first_loss:
                list_of_successes.append(index)
                neural_net.save_neural_net(index, 'model_folder_iteration_' + str(number) + '_v3/', model)
            new_neural_nets.append(neural_net)
    with open(new_nn_filename + str(number) + '_v3.pickle', 'wb') as f:
        pickle.dump(new_neural_nets, f, pickle.HIGHEST_PROTOCOL)
    return list_of_successes

def train_from_tournament(number):
    with open(tourney_filename + str(number) + '.pickle', 'rb') as f:
        tournament = pickle.load(f)
    number_games = len(tournament)
    result_dictionary = dict()
    result_dictionary['number_illegal_losses'] = 0
    result_dictionary['player_1_won'] = 0
    result_dictionary['player_2_won'] = 0
    result_dictionary['up_and_down_wins'] = 0
    result_dictionary['left_and_right_wins'] = 0
    result_dictionary['diagonal_wins'] = 0
    result_dictionary['draws'] = 0
    total_positions = []
    total_moves = []
    
    for match_number, match in enumerate(tournament):
        print('analyzing match number ' +str(match_number) + ' out of ' +str(number_games))
        positions, moves = extract_from_match(match, result_dictionary)
        total_positions.extend(positions)
        total_moves.extend(moves)
    print('finding unique positions')
    unique_position_list = total_positions[0:2]
    unique_moves_list = total_moves[0:2]
    rest_of_positions = total_positions[2::]
    rest_of_moves = total_moves[2::]
    unique_position_list, unique_moves_list = insert(rest_of_positions, rest_of_moves, unique_position_list, unique_moves_list)
    print('mirroring positions')
    mirrored_position_list, mirrored_move_list = mirror(unique_position_list, unique_moves_list)
    print('finding unique positions part 2')
    unique_position_list, unique_moves_list = insert(mirrored_position_list, mirrored_move_list, unique_position_list, unique_moves_list)
    
    """
    for position, move in zip(unique_position_list, unique_moves_list):
        show_array = np.zeros((8,8,1))
        show_array = np.concatenate((np.resize(position[:,:,0], (8,8,1)), show_array), axis=2)
        show_array = np.concatenate((np.resize(position[:,:,1], (8,8,1)), show_array), axis=2)
        plt.imshow(show_array)
        plt.show()
        print(move)
        input('')
    """
    
    moves = np.array(unique_moves_list)
    positions = np.array(unique_position_list)
    with open(raw_data_filename + str(number) + '.pickle', 'wb') as f:
        pickle.dump([moves, positions], f, pickle.HIGHEST_PROTOCOL)
    print(moves.shape)
    print(positions.shape)
    print(str(number_games) + ' games were being played')
    print('of these, ' + str(result_dictionary['number_illegal_losses']) + ' were illegal losses')
    print('of these, ' + str(result_dictionary['draws']) + ' were draws')
    print('of these, ' + str(result_dictionary['player_1_won']) + ' were player 1 wins')
    print('of these, ' + str(result_dictionary['player_2_won']) + ' were player 2 wins')
    print('of these, ' + str(result_dictionary['up_and_down_wins']) + ' were up and down wins')
    print('of these, ' + str(result_dictionary['left_and_right_wins']) + ' were left and right wins')
    print('of these, ' + str(result_dictionary['diagonal_wins']) + ' were diagonal wins')
    """
    with open('raw_data_6.pickle', 'rb') as f:
        x = pickle.load(f)
    moves = x[0]
    positions = x[1]
    """
    with open(new_nn_filename + str(number) + '.pickle', 'rb') as f:
        neural_nets = pickle.load(f)
    new_neural_nets = []
    
    for index, neural_net in enumerate(neural_nets):
        tf.keras.backend.clear_session()
        model = neural_net.load_neural_net()
        training_positions, testing_positions, training_moves, testing_moves = train_test_split(positions, moves, test_size=0.3, random_state=index)
        model.evaluate(testing_positions, testing_moves)
        model.fit(training_positions, training_moves, epochs=2, batch_size=64)
        model.evaluate(testing_positions, testing_moves)
        print('______________________')
        neural_net.save_neural_net(index, 'model_folder_iteration_' + str(number+1)+'/', model)
        new_neural_nets.append(neural_net)
    
    print(str(number_games) + ' games were being played')
    print('of these, ' + str(result_dictionary['number_illegal_losses']) + ' were illegal losses')
    print('of these, ' + str(result_dictionary['draws']) + ' were draws')
    print('of these, ' + str(result_dictionary['player_1_won']) + ' were player 1 wins')
    print('of these, ' + str(result_dictionary['player_2_won']) + ' were player 2 wins')
    print('of these, ' + str(result_dictionary['up_and_down_wins']) + ' were up and down wins')
    print('of these, ' + str(result_dictionary['left_and_right_wins']) + ' were left and right wins')
    print('of these, ' + str(result_dictionary['diagonal_wins']) + ' were diagonal wins')
    with open(new_nn_filename + str(number+1) + '.pickle', 'wb') as f:
        pickle.dump(new_neural_nets, f, pickle.HIGHEST_PROTOCOL)
        
def rank(number):
    with open('raw_data_'+str(number-1)+'.pickle', 'rb') as f:
        x = pickle.load(f)
    moves = x[0]
    positions = x[1]
    with open(new_nn_filename + str(number) + '.pickle', 'rb') as f:
        neural_nets = pickle.load(f)
    list_of_losses = []
    for index, neural_net in enumerate(neural_nets):
        tf.keras.backend.clear_session()
        model = neural_net.load_neural_net()
        training_positions, testing_positions, training_moves, testing_moves = train_test_split(positions, moves, test_size=0.3, random_state=index)
        loss = model.evaluate(testing_positions, testing_moves)
        list_of_losses.append(loss)
    list_of_to_remove = []
    for i in range(6):
        a = np.array([list_of_losses[3*i+0], list_of_losses[3*i+1], list_of_losses[3*i+2]])
        list_of_to_remove.append((3*i)+np.argmax(a))
    print(list_of_to_remove)
    new_neural_nets = []
    for i in range(len(neural_nets)):
        if i in list_of_to_remove:
            pass
        else:
            new_neural_nets.append(neural_nets[i])
    with open(new_nn_filename + str(number) + '.pickle', 'wb') as f:
        pickle.dump(new_neural_nets, f, pickle.HIGHEST_PROTOCOL)

def name(numbers):
    for number in numbers:
        with open(new_sub_nn_filename + str(number) + '.pickle', 'rb') as f:
            neural_nets = pickle.load(f)
        new_neural_nets = []
        for index, neural_net in enumerate(neural_nets):
            neural_net.model_filepath = 'model_sub_folder_iteration_0/' + str(index)
            new_neural_nets.append(neural_net)
        with open(new_sub_nn_filename + str(number) + '.pickle', 'wb') as f:
            pickle.dump(new_neural_nets, f, pickle.HIGHEST_PROTOCOL)
        
        
def test_ability(number):
    filename = 'raw_data_'
    with open(new_sub_nn_filename + str(number) + '.pickle', 'rb') as f:
        neural_nets = pickle.load(f)
    new_neural_nets = []
    list_of_successes = []
    for index, neural_net in enumerate(neural_nets):
        list_of_training_moves = []
        list_of_training_positions = []
        list_of_testing_moves = []
        list_of_testing_positions = []
        for i in range(6, 26):
            if os.path.exists(filename + str(i) + '.pickle'):
                with open(filename + str(i) + '.pickle', 'rb') as f:
                    x = pickle.load(f)
                moves = x[0]
                positions = x[1]
                if neural_net.subtraction_needed:
                    new_positions = []
                    for position in positions:
                        new_positions.append(position - 0.5*np.ones((8,8,2)))
                    positions = new_positions
                training_positions, testing_positions, training_moves, testing_moves = train_test_split(positions, moves, test_size=0.3, random_state=index)
                list_of_training_moves.extend(training_moves)
                list_of_training_positions.extend(training_positions)
                list_of_testing_moves.extend(testing_moves)
                list_of_testing_positions.extend(testing_positions)
        testing_positions = np.array(list_of_testing_positions)
        testing_moves = np.array(list_of_testing_moves)
        training_positions = np.array(list_of_training_positions)
        training_moves = np.array(list_of_training_moves)
        tf.keras.backend.clear_session()
        model = neural_net.load_neural_net()
        first_loss = model.evaluate(testing_positions, testing_moves)
        model.fit(training_positions, training_moves, epochs=3, batch_size=128)
        second_loss = model.evaluate(testing_positions, testing_moves)
        print('________________________________')
        if second_loss < first_loss:
            list_of_successes.append(index)
            neural_net.save_neural_net(index, model_sub_path + str(number+1) + '/', model)
        else:
            tf.keras.backend.clear_session()
            model = neural_net.load_neural_net()
            neural_net.save_neural_net(index, model_sub_path + str(number+1) + '/', model)
        new_neural_nets.append(neural_net)
    with open(new_sub_nn_filename + str(number+1) + '.pickle', 'wb') as f:
        pickle.dump(new_neural_nets, f, pickle.HIGHEST_PROTOCOL)
    return list_of_successes
    
#name([0]) 
print(test_ability(5))


#tournamentlogic.tournament_both_random(2112, 'tournament_0.pickle')
#create_batch(24)
#run_pre_training_tournament(new_nn_filename, tourney_filename, 0)
#train_from_tournament(new_nn_filename, tourney_filename, new_nn_filename)
#
# start tournament games with random moves
# write scripts that allow the showing of progress