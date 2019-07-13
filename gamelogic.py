import numpy as np


class board(object):
    def __init__(self, number_rows, number_columns, number_contiguous):
        self.number_rows = number_rows
        self.number_columns = number_columns
        self.number_contiguous = number_contiguous
        y = np.array(np.zeros(shape=(self.number_rows, self.number_columns)), ndmin=3)
        self.gamestate = np.append(y, np.array(np.zeros(shape=(self.number_rows, self.number_columns)), ndmin=3), axis=0)
        self.player_on_move = 0
        self.legal_gamestate = True
        self.move_number = 0
        
        
    def show(self):
        display_gamestate = np.array(np.zeros
                              (shape=(self.number_rows,
                                      self.number_columns)))
        for i in range(0, 2):
            display_gamestate[self.gamestate[i] == 1] = i + 1
            x = input()
        print(display_gamestate)
    
    
    def check_if_legal(self, column):
        if sum(self.gamestate[0, :, column]) + sum(self.gamestate[1, :, column]) == self.number_rows:
            return False
        else:
            return True
        
        
    def makemove(self, column):
        pos = int(sum(self.gamestate[0, :, column]) + sum(self.gamestate[1, :, column]))
        if pos < self.number_rows:
            self.gamestate[self.player_on_move, pos, column] = 1
            self.player_on_move = 1 - self.player_on_move
            self.move_number += 1
        else:
            self.legal_gamestate = False
    
    
    def check_liste(self, liste):
        """
        returns True if the list has self.number_contiguous 1's in a row, False otherwise
        """
        for i in range(len(liste)-(self.number_contiguous -1)):
            if sum(liste[i:i+self.number_contiguous]) == self.number_contiguous:
                return True
        return False


    def check_if_continue(self):
        """
        returns True if nobody has won, False otherwise
        """
        player_to_test = 1 - self.player_on_move
        A = self.gamestate[player_to_test]
        for i in range(self.number_rows):
            if self.check_liste(A[i, :]): return False
        for i in range(self.number_columns):
            if self.check_liste(A[:, i]): return False
        for i in range(self.number_rows - (self.number_contiguous -1)):
            for j in range(self.number_columns - (self.number_contiguous -1)):
                list_to_check = []
                for k in range(self.number_contiguous):
                    list_to_check.append(A[i + k, j + k])
                if list_to_check == [1 for x in range(self.number_contiguous)]: return False
        for i in range((self.number_contiguous -1), A.shape[0]):
            for j in range(0, A.shape[1] - (self.number_contiguous -1)):
                list_to_check = []
                for k in range(0,self.number_contiguous):
                    list_to_check.append(A[i - k, j + k])
                if list_to_check == [1 for x in range(self.number_contiguous)]: return False
        return True
    
    
    def checkifdraw(self):
        if self.move_number == self.number_columns * self.number_rows - 1:
            return True
        else:
            return False