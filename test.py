"""
import pickle
import tournamentlogic
import neuronal
"""
import numpy as np


x = np.random.ranf((5,))
y = np.random.ranf((5,))
print(x)
z = np.random.ranf((3,5))
print(z)
print(np.matmul(z,x))
print(np.random.random())
print(np.flatten(z))
"""
Shapes = [(36, 126), (14, 36), (7, 14)]
b = 7 #Amount of available columns
h = 6 #Amount of available rows
list_of_neural_nets = []
for i in range(0,30):
    list_of_neural_nets.append(neuronal.initialize_neuralnet(Shapes))

def training(list_of_neural_nets, number_of_tournaments):
    for i in range(0, number_of_tournaments):
        list_of_results = tournamentlogic.tournament(list_of_neural_nets, h, b)
        tournamentlogic.update_neural_nets(list_of_neural_nets, list_of_results)
    return list_of_neural_nets


data = training(list_of_neural_nets, 100)
f = open("neural_nets_first_try.pickle", "wb")
pickle.dump(data, f)
f.close()
"""