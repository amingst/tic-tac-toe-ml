from __future__ import print_function

from builtins import range

import numpy as np

LENGTH = 3


class Agent:
    def __init__(self, epsilon=0.1, alpha=0.5):
        self.epsilon = epsilon
        self.alpha = alpha
        self.verbose_state = False
        self.state_history = []

    def setV(self, V):
        self.Values = V

    def set_symbol(self, symbol):
        self.symbol = symbol

    def set_verbose(self, verbose_state):
        self.verbose_state = verbose_state

    def reset_state_history(self):
        self.state_history = []

    def take_action(self, environment):
        # use the epsilon-greedy strategy to choose a random action
        random_action = np.random.randn()
        best_state = None
        if random_action < self.epsilon:
            # take a random action
            if self.verbose_state:
                print("Taking a random action")

            possible_moves = []
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if environment.is_board_empty(i, j):
                        possible_moves.append((i, j))
            index = np.random.choice(len(possible_moves))
            next_move = possible_moves[index]
        else:
            position_to_value = {}
            next_move = None
            best_value = -1
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if environment.is_board_empty(i, j):
                        # find the state if a move was made
                        environment.board[i, j] = self.symbol
                        state = environment.get_state()
                        environment.board[i, j] = 0
                        position_to_value[(i, j)] = self.Values[state]
                        if self.Values[state] > best_value:
                            best_value = self.Values[state]
                            best_state = state
                            next_move = (i, j)
            if self.verbose_state:
                print("Taking a greedy action")
                for i in range(LENGTH):
                    print("------------------")
                    for j in range(LENGTH):
                        if environment.is_empty(i, j):
                            # print the value
                            print(" %.2f|" %
                                  position_to_value[(i, j)], end="")
                        else:
                            print("  ", end="")
                            if environment.board[i, j] == environment.x_piece:
                                print("x  |", end="")
                            elif environment.board[i, j] == environment.o_piece:
                                print("o  |", end="")
                            else:
                                print("   |", end="")
                        print("")
                print("------------------")

    def draw_values(self, environment, position_to_value):
        if self.verbose_state:
            print("Taking a greedy action")
            for i in range(LENGTH):
                print("------------------")
                for j in range(LENGTH):
                    if environment.is_board_empty(i, j):
                        print(" %.2f|" % position_to_value[(i, j)], end="")
                    else:
                        print("  ", end="")
                        if environment.board[i, j] == environment.x_piece:
                            print("x  |", end="")
                        elif environment.board[i, j] == environment.o_piece:
                            print("o  |", end="")
                        else:
                            print("   |", end="")
                    print("")
            print("------------------")

    def update_state_history(self, state):
        self.state_history.append(state)

    def update(self, environment):
        reward = environment.reward(self.symbol)
        target = reward
        for previous in reversed(self.state_history):
            value = self.Values[previous] + self.alpha * \
                (target - self.Values[previous])
            self.Values[previous] = value
            target = value
        self.reset_state_history()
