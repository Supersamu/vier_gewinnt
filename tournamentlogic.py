import matchlogic
import numpy as np
import neuronallogic
import pickle
rows = 4
columns = 3
contiguous = 3
class tournament_no_shuffle(object):
    def __init__(self, list_of_neural_nets_p1, list_of_neural_nets_p2, 
                 list_to_shuffle_p1, list_to_shuffle_p2, number_rows, 
                 number_columns):
        number_p1_wins = 0
        number_p2_wins = 0
        for neural_net_p1, neural_net_p2 in zip(list_of_neural_nets_p1, 
                                                list_of_neural_nets_p2):
            match = matchlogic.match(number_rows, number_columns, contiguous)
            match.play(neural_net_p1, neural_net_p2)
            if match.winner == 0:
                #number_p1_wins += 1
                neural_net_p2.update([], [], match.positions[1:2], 
                                     match.movelist[1:2])
                neural_net_p1.update(match.positions[0:2], 
                                     match.movelist[0:2], [], [])
            elif match.winner == 1:
                #print("ja")
                neural_net_p2.update(match.positions[1:2], 
                                     match.movelist[1:2], [], [])
                neural_net_p1.update([], [], match.positions[0:2], 
                                     match.movelist[0:2])
        

class tournament_semi_shuffle(object):
    def __init__(self, list_of_neural_nets_p1, list_of_neural_nets_p2, 
                 list_to_shuffle_p1, list_to_shuffle_p2, number_rows, 
                 number_columns):
        number_p1_wins = 0
        number_p2_wins = 0
        for i in range(0, 1):
            part_list_p1 = list_to_shuffle_p1[i*10:(i + 1)*10]
            part_list_p2 = list_to_shuffle_p2[i*10:(i + 1)*10]
            list_p2_good_positions = [[] for x in range(10)]
            list_p2_good_moves = [[] for x in range(10)]
            list_p2_bad_positions = [[] for x in range(10)]
            list_p2_bad_moves = [[] for x in range(10)]
            for j in range(0, 10):
                list_p1_good_positions = []
                list_p1_good_moves = []
                list_p1_bad_positions = []
                list_p1_bad_moves = []
                for k in range(0, 10):
                    match = matchlogic.match(number_rows, number_columns, contiguous)
                    match.play(list_of_neural_nets_p1[part_list_p1[j]],
                               list_of_neural_nets_p2[part_list_p2[k]])
                    if match.winner == 0:
                        number_p1_wins += 1
                        list_p1_good_positions.extend(match.positions[::2])
                        list_p1_good_moves.extend(match.movelist[::2])
                        list_p2_bad_positions[k].extend(match.positions[1:2])
                        list_p2_bad_moves[k].extend(match.movelist[1:2])
                    elif match.winner == 1:
                        number_p2_wins += 1
                        list_p1_bad_positions.extend(match.positions[::2])
                        list_p1_bad_moves.extend(match.movelist[::2])
                        list_p2_good_positions[k].extend(match.positions[1:2])
                        list_p2_good_moves[k].extend(match.movelist[1:2])
                list_of_neural_nets_p1[part_list_p1[j]].update(list_p1_good_positions,
                                       list_p1_good_moves, list_p1_bad_positions, 
                                       list_p1_bad_moves)
            for k in range(0, 10):
                list_of_neural_nets_p2[part_list_p2[k]].update(list_p2_good_positions[k], 
                                      list_p2_good_moves[k], list_p2_bad_positions[k],
                                      list_p2_bad_moves[k])
        print(number_p1_wins)
        print(number_p2_wins)
        
        
list_of_nets_p1 = []
list_to_shuffle_p1 = []
list_of_nets_p2 = []
list_to_shuffle_p2 = []
for i in range(0, 1):
    list_of_nets_p1.append(neuronallogic.neuralnet([rows * columns * 2, 
                                                    rows * columns, columns]))
    list_to_shuffle_p1.append(i)
    list_of_nets_p2.append(neuronallogic.neuralnet([rows * columns * 2, 
                                                    rows * columns, columns]))
    list_to_shuffle_p2.append(i)
    
with open("test" + '.pickle', 'rb') as f:
    data = pickle.load(f)
list_of_nets_p1 = data[0]
list_of_nets_p2 = data[1]
for neural_net in list_of_nets_p2:
    neural_net.show()
for i in range(30):
    if i%100 == 0:
        print(i)
    z = tournament_no_shuffle(list_of_nets_p1, list_of_nets_p2, list_to_shuffle_p1, 
                   list_to_shuffle_p2, rows, columns)
with open("test" + '.pickle', 'wb') as f:
    pickle.dump([list_of_nets_p1, list_of_nets_p2], f, pickle.HIGHEST_PROTOCOL)
for neural_net in list_of_nets_p2:
        neural_net.show()
        
"""
def tournament(list_of_neural_nets, h, b):
    list_of_results = np.zeros(shape=(len(list_of_neural_nets),))
    list_of_wins = [0, 0, 0, 0]
    empty_gamestate = np.array([np.ones(shape=(h,b)), 
                      np.zeros(shape=(h,b)), 
                      np.zeros(shape=(h,b))])
    for i in range(0, len(list_of_neural_nets)):
        for j in range(i+1, len(list_of_neural_nets)):
            neural_net_1 = list_of_neural_nets[i]
            neural_net_2 = list_of_neural_nets[j]
            gamestate = np.copy(empty_gamestate)
            result = match.play_match(neural_net_1, neural_net_2, gamestate, 1)
            if result == 1:
                list_of_results[i] += 1
                list_of_wins[0] += 1
            elif result == 2:
                list_of_results[j] += 1
                list_of_wins[1] += 1
            else:
                if result == 3:
                    list_of_wins[3] += 1
                else:
                    list_of_wins[2] += 1
                list_of_results[i] += 0.5
                list_of_results[j] += 0.5
            gamestate = np.copy(empty_gamestate)
            result = match.play_match(neural_net_1, neural_net_2, gamestate, 2)
            if result == 2:
                list_of_results[i] += 1
                list_of_wins[0] += 1
            elif result == 1:
                list_of_results[j] += 1
                list_of_wins[1] += 1
            else:
                if result == 3:
                    list_of_wins[3] += 1
                else:
                    list_of_wins[2] += 1
                list_of_results[i] += 0.5
                list_of_results[j] += 0.5
    print(list_of_wins)
    return list_of_results
#todo genauere aufschlüsselung von resultaten


def update_neural_nets(list_of_neural_nets, results):
    z = int(len(list_of_neural_nets)/2)
    best_neural_nets = np.argsort(results)[::-1][:z]
    list_of_new_neural_nets = []
    for i in range(0,z):
        list_of_new_neural_nets.append(list_of_neural_nets[best_neural_nets[i]])
    for i in range(0, z):
        list_of_new_neural_nets.append(neuronal.modify(list_of_new_neural_nets[i]))
    return list_of_new_neural_nets
"""