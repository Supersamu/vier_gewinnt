import numpy as np
import neuronallogic
import matchlogic
import gamelogic

z = [[] for x in range(10)]
print(z)
rows = 5
columns = 6
winner = 0
player_1 = neuronallogic.neuralnet([rows * columns * 3, rows * columns, columns])
player_2 = neuronallogic.neuralnet([rows * columns * 3, rows * columns, columns])
match = matchlogic.match(rows, columns)
winner = 1 - match.play(player_1, player_2)
