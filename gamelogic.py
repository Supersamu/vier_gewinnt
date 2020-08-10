import numpy as np
import matplotlib.pyplot as plt

class board(object):
    def __init__(self, number_rows, number_columns, number_contiguous):
        self.number_rows = number_rows
        self.number_columns = number_columns
        self.number_contiguous = number_contiguous
        self.gamestate = np.zeros((self.number_rows, 
                                          self.number_columns, 2))
        self.player_on_move = 0 # first player is on move at start
        self.move_number = 0
        self.type_win = None
        
        
    def show(self):
        show_array = np.zeros((8,8,1))
        if self.player_on_move == 0:
            show_array = np.concatenate((np.resize(self.gamestate[:,:,0], (8,8,1)), show_array), axis=2)
            show_array = np.concatenate((np.resize(self.gamestate[:,:,1], (8,8,1)), show_array), axis=2)
        else:
            show_array = np.concatenate((np.resize(self.gamestate[:,:,1], (8,8,1)), show_array), axis=2)
            show_array = np.concatenate((np.resize(self.gamestate[:,:,0], (8,8,1)), show_array), axis=2)
        plt.imshow(show_array)
        plt.show()
    
    
    def check_if_legal(self, column):
        """ 
        returns True if the move supplied is valid
        """
        if self.gamestate[0, column, 0] + self.gamestate[0, column, 1] == 0:
            # neither of the players has a ball at the top pósition of that column
            return True
        else:
            return False
        
        
    def makemove(self, column):
        # makes a move, assuming the move is valid
        pos = np.sum(self.gamestate[:, column, :] == 1)
        self.gamestate[self.number_rows - 1 - pos, column, 0] = 1
        self.player_on_move = 1 - self.player_on_move
        self.move_number += 1
        tmp = np.zeros((8,8,2))
        tmp[:,:,0] = self.gamestate[:,:,1]
        tmp[:,:,1] = self.gamestate[:,:,0]
        self.gamestate = tmp
        
    
    def check_liste(self, liste):
        """
        returns True if the list has self.number_contiguous 1's in a row, False otherwise
        """
        for i in range(len(liste)-(self.number_contiguous - 1)):
            if sum(liste[i:i+self.number_contiguous]) == self.number_contiguous:
                return True
        return False


    def check_if_prev_player_has_won(self):
        """
        returns True if previous player has won, False otherwise
        """
        A = self.gamestate[:, :, 1]
        for i in range(self.number_rows):
            if self.check_liste(A[i, :]):
                self.type_win = 'leftandright'
                return True
        for i in range(self.number_columns):
            if self.check_liste(A[:, i]):
                self.type_win = 'upanddown'
                return True
        for i in range(self.number_rows - (self.number_contiguous -1)):
            for j in range(self.number_columns - (self.number_contiguous -1)):
                list_to_check = []
                for k in range(self.number_contiguous):
                    list_to_check.append(A[i + k, j + k])
                if list_to_check == [1 for x in range(self.number_contiguous)]: return True
        for i in range((self.number_contiguous -1), A.shape[0]):
            for j in range(0, A.shape[1] - (self.number_contiguous -1)):
                list_to_check = []
                for k in range(0,self.number_contiguous):
                    list_to_check.append(A[i - k, j + k])
                if list_to_check == [1 for x in range(self.number_contiguous)]: return True
        return False


if __name__ == "__main__":
    X = board(8, 8, 4)
    X.makemove(0) #P1
    X.makemove(1)
    X.makemove(1) #P1
    X.makemove(2)
    X.makemove(2) #P1
    X.makemove(3)
    X.makemove(2) #P1
    X.makemove(3)
    X.show()
    input("Press Enter to continue...")
    print()
    if X.check_if_prev_player_has_won():
        print('continuing not allowed')
    else:
        print('continuing allowed')
    print()
    X.makemove(3)
    X.show()
    input("Press Enter to continue...")
    print()
    if X.check_if_prev_player_has_won():
        print('continuing not allowed')
    else:
        print('continuing allowed')
    print()
    X.makemove(2)
    X.show()
    input("Press Enter to continue...")
    print()
    if X.check_if_prev_player_has_won():
        print('continuing not allowed')
    else:
        print('continuing allowed')
    X.makemove(3)
    X.show()
    input("Press Enter to continue...")
    print()
    if X.check_if_prev_player_has_won():
        print('continuing not allowed')
    else:
        print('continuing allowed')

    