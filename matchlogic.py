import numpy as np
import gamelogic


class match(object):
    def __init__(self, number_rows, number_columns, number_contiguous):
        self.result = None
        self.movelist = []
        self.winner = None
        self.positions = []
        self.gameboard = gamelogic.board(number_rows, number_columns, number_contiguous)
    
    
    def play(self, net_1, net_2):
        while self.gameboard.legal_gamestate and self.gameboard.check_if_continue():
            gamestate_as_array = self.gameboard.gamestate.flatten()
            if self.gameboard.player_on_move == 0:
                output = net_1.calculate_response(gamestate_as_array)
            else:
                output = net_2.calculate_response(gamestate_as_array)
            column = np.argmax(output)
            self.movelist.append(column)
            self.gameboard.makemove(column)
            self.gameboard.show()
            self.positions.append(gamestate_as_array)
            #self.gameboard.show()
            if self.gameboard.checkifdraw():
                return 2
        self.winner = 1 - self.gameboard.player_on_move
        return self.gameboard.player_on_move