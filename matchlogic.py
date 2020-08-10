import numpy as np
import gamelogic
import neuronal_keras
import copy

class match(object):
    def __init__(self, number_rows, number_columns, number_contiguous):
        self.ongoing = True
        self.winner = None
        self.illegal_loss = False
        self.movelist_p1 = []
        self.movelist_p2 = []
        self.positionlist_p1 = []
        self.positionlist_p2 = []
        self.gameboard = gamelogic.board(number_rows, number_columns, number_contiguous)
        self.gameboard_list = [copy.deepcopy(self.gameboard)]
    
    
    def play(self, net_1, net_2, model_1, model_2, show=False, random_move_prob=0):
        while self.ongoing:
            if self.gameboard.player_on_move == 0:
                self.positionlist_p1.append(np.copy(self.gameboard.gamestate))
                if np.random.randint(0, 101) < random_move_prob:
                    column = np.random.randint(0, 8)
                    while not self.gameboard.check_if_legal(column):
                        column = np.random.randint(0, 8)
                else:
                    column = net_1.calculate_response(self.gameboard, model_1)
                self.movelist_p1.append(column)
            else:
                self.positionlist_p2.append(np.copy(self.gameboard.gamestate))
                if np.random.randint(0, 101) < random_move_prob:
                    column = np.random.randint(0, 8)
                    while not self.gameboard.check_if_legal(column):
                        column = np.random.randint(0, 8)
                else:
                    column = net_2.calculate_response(self.gameboard, model_2)
                self.movelist_p2.append(column)
            if self.gameboard.check_if_legal(column):
                self.gameboard.makemove(column)
                if show:
                    self.gameboard.show()
                    input('press enter to continue')
                else:
                    pass
                if self.gameboard.check_if_prev_player_has_won():
                    self.ongoing = False
                    self.winner = 1 - self.gameboard.player_on_move
                if self.gameboard.move_number + 1 == self.gameboard.number_columns * self.gameboard.number_rows:
                    self.ongoing = False
                self.gameboard_list.append(copy.deepcopy(self.gameboard))
            else:
                self.illegal_loss = True
                self.winner = 1 - self.gameboard.player_on_move
                self.ongoing = False
    
    def play_moves_random(self, amount_moves):
        for _ in range(amount_moves):
            if self.gameboard.player_on_move == 0:
                self.positionlist_p1.append(np.copy(self.gameboard.gamestate))
                column = np.random.randint(0, 8)
                self.movelist_p1.append(column)
            else:
                self.positionlist_p2.append(np.copy(self.gameboard.gamestate))
                column = np.random.randint(0, 8)
                self.movelist_p2.append(column)
            self.gameboard.makemove(column)
            self.gameboard_list.append(copy.deepcopy(self.gameboard))
                
    
    def play_vs_human(self, net_1, model_1, show=True):
        while self.ongoing:
            if self.gameboard.player_on_move == 0:
                self.positionlist_p1.append(np.copy(self.gameboard.gamestate))
                column = net_1.calculate_response(self.gameboard, model_1)
                self.movelist_p1.append(column)
            else:
                self.positionlist_p2.append(np.copy(self.gameboard.gamestate))
                column = int(input('which column do you want to place the ball in?'))
                self.movelist_p2.append(column)
            if self.gameboard.check_if_legal(column):
                self.gameboard.makemove(column)
                if show:
                    self.gameboard.show()
                else:
                    pass
                if self.gameboard.check_if_prev_player_has_won():
                    self.ongoing = False
                    self.winner = 1 - self.gameboard.player_on_move
                if self.gameboard.move_number + 1 == self.gameboard.number_columns * self.gameboard.number_rows:
                    self.ongoing = False
            else:
                self.illegal_loss = True
                self.winner = 1 - self.gameboard.player_on_move
                self.ongoing = False
        

            