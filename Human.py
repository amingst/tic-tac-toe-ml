from __future__ import print_function


class Human:
    def __init__(self):
        pass

    def set_symbol(self, symbol):
        self.symbol = symbol

    def take_action(self, environment):
        while True:
            # break if a legal move is made
            move = input(
                "Enter coordinates i,j for your next move (i,j=0..2):")
            i, j = move.split(',')
            i = int(i)
            j = int(j)
            if environment.is_board_empty:
                environment.board[i, j] = self.symbol
                break

    def update(self, environment):
        pass

    def update_state_history(self, state):
        pass
