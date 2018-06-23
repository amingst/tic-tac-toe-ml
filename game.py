from __future__ import print_function, division
from builtins import input

from Agent import Agent
from Environment import Environment
from Human import Human
import helpers

EPOCHS = 10000


def main():
    player_1 = Agent()
    player_2 = Agent()

    environent = Environment()

    state_winner_triples = helpers.get_state_hash_and_winner(environent)

    x_Values = helpers.initial_value_x(environent, state_winner_triples)
    o_Values = helpers.initial_value_o(environent, state_winner_triples)
    player_1.setV(x_Values)
    player_2.setV(o_Values)

    player_1.set_symbol(environent.x_piece)
    player_2.set_symbol(environent.o_piece)

    helpers.train_agents(player_1, player_2, EPOCHS, environent)

    human = Human()
    human.set_symbol(environent.o_piece)
    while True:
        player_1.set_verbose(True)
        helpers.play_game(player_1, human, Environment(), draw=2)
        answer = input("Play again? [Y/n]: ")
        if answer and answer.lower()[0] == 'n':
            break
