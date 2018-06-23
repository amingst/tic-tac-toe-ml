from __future__ import print_function

from builtins import range

import numpy as np

LENGTH = 3


class Environment:
    def __init__(self):
        self.board = np.zeros((LENGTH, LENGTH))
        self.x_piece = -1
        self.o_piece = 1
        self.winner = None
        self.is_game_over = False
        self.num_states = 3 ** (LENGTH * LENGTH)

    def is_board_empty(self, i, j):
        return self.board[i, j] == 0

    def reward(self, symbol):
        if not self.game_over():
            return 0

        return 1 if self.winner == symbol else 0

    def get_state(self):
        k = 0
        h = 0
        for i in range(LENGTH):
            for j in range(LENGTH):
                if self.board[i, j] == 0:
                    value = 0
                elif self.board[i, j] == self.x_piece:
                    value = 1
                elif self.board[i, j] == self.o_piece:
                    value = 2
            h += (3 ** k) * value
            k += 1
        return h

    def game_over(self, force_recalculation=False):
        if not force_recalculation and self.is_game_over:
            return self.is_game_over

        # check rows
        for i in range(LENGTH):
            for player in (self.x_piece, self.o_piece):
                if self.board[i].sum() == player * LENGTH:
                    self.winner = player
                    self.is_game_over = True
                    return True

        # check columns
        for j in range(LENGTH):
            for player in (self.x_piece, self.o_piece):
                if self.board[:, j].sum() == player * LENGTH:
                    self.winner = player
                    self.is_game_over = True
                    return True

        # check diagonals
        for player in (self.x_piece, self.o_piece):
            # top-left -> bottom-right diagonal
            if self.board.trace() == player * LENGTH:
                self.winner = player
                self.is_game_over = True
                return True

            # top-right -> bottom-left diagonal
            if np.fliplr(self.board).trace() == player * LENGTH:
                self.winner = player
                self.is_game_over = True
                return True

        # check for a draw
        if np.all((self.board == 0) == False):
            self.winner = None
            self.is_game_over = True
            return True

        self.winner = None
        return False

    def draw_board(self):
        for i in range(LENGTH):
            print("-------------")
            for j in range(LENGTH):
                print(" ", end="")
                if self.board[i, j] == self.x_piece:
                    print("x ", end="")
                elif self.board[i, j] == self.o_piece:
                    print("o ", end="")
                else:
                    print(" ", end="")
            print(" ", end="")
        print("-------------")
