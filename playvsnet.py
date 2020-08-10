import neuronal_keras
import pickle
import matchlogic
import random
def play_against_neural_net():
    #x = input('which neural net generation do you want to play against?')
    path = 'neural_nets_training_step_'+str(28)+'.pickle'
    with open(path, 'rb') as f:
        neural_nets = pickle.load(f)
    #y = int(input('which version do you want to play against? 0,1,2,3,4,5'))
    y = 5
    random_net = random.randint(y*2, (y+1)*2-1)
    neural_net = neural_nets[random_net]
    model = neural_net.load_neural_net()
    match = matchlogic.match(8,8,4)
    match.play_moves_random(2)
    match.gameboard.show()
    match.play_vs_human(neural_net, model)
    print(match.gameboard.type_win)
    if input('play again? y/n') == 'y':
        play_against_neural_net()
    
play_against_neural_net()