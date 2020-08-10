import gamelogic
import neuronal
import numpy as np


def play_match(neural_net_1, neural_net_2, gamestate, ai_to_move):
    if np.any([gamestate[0] == 1]):
        if ai_to_move == 1:
            neural_net_active = neural_net_1
        else:
            neural_net_active = neural_net_2
        move = neuronal.calculate_response(gamestate, neural_net_active)
        if gamelogic.makemove(gamestate, move, ai_to_move):
            if gamelogic.check_if_continue(gamestate, ai_to_move):
                if ai_to_move == 1:
                    ai_to_move = 2
                else:
                    ai_to_move = 1
                return play_match(neural_net_1, neural_net_2, gamestate, ai_to_move)
            else:
                return ai_to_move
        else:
            return 3
    else:
        return 0
    
"""
b = 7 #Amount of available columns
h = 6 #Amount of available rows

b = 7 #Amount of available columns
h = 6 #Amount of available rows
Shapes = [(36, 126), (14, 36), (7, 14)]
neural_net_1 = neuronal.initialize_neuralnet(Shapes)
neural_net_2 = neuronal.initialize_neuralnet(Shapes)
gamestate = np.array([np.ones(shape=(h,b)), 
                      np.zeros(shape=(h,b)), 
                      np.zeros(shape=(h,b))])

    play_match(neural_net_1, neural_net_2, gamestate, 1)

"""


#1.6 ms per game
"""
gamestate = np.array([np.ones(shape=(h,b)), 
                          np.zeros(shape=(h,b)), 
                          np.zeros(shape=(h,b))])



"""

#print(neural_net_1)
"""
#def neural_vs_neural(gamestate, neural_net_1, neural_net_2):
"""