from __future__ import print_function, division
from builtins import range

import numpy as np

def play_game(player_1, player_2, environment, draw=False):
	current_player = None
	while not environment.game_over():
		if current_player == player_1:
			current_player = player_2
		else:
			current_player = player_1
		
		if draw:
			if draw == 1 and current_player == player_1:
				environment.draw_board()
			if draw == 2 and current_player == player_2:
				environment.draw_board()
		
		current_player.take_action(environment)

		state = environment.get_state()
		player_1.update_state_history(state)
		player_2.update_state_history(state)
	
	if draw:
		environment.draw_board()

	player_1.update(environment)
	player_2.update(environment)

def get_state_hash_and_winner(environment, i=0, j=0):
	results = []
	for value in (0, environment.x_piece, environment.o_piece):
		# if the board is empty then environment.board[i, j] should
		# already be 0
		environment.board[i, j] = value
		if j == 2:
			# j goes back to 0, increase i, unless i = 2, then we're
			# done
			if i == 2:
				# the board is full, collect results and return
				state = environment.get_state()
				game_over = environment.game_over(force_recalculation=True)
				winner = environment.winner
				results.append((state, winner, game_over))
			else:
				results += get_state_hash_and_winner(environment, i + 1, 0)
		else:
			results += get_state_hash_and_winner(environment, i, j + 1)
	return results

def initial_value_x(environment, state_winner_tripes):
	# init state values as follows:
	# if x wins, Values(state) = 1
	# if x loses or draw, Values(state) = 0
	# otherwise, Values(state) = 0.5
	Values = np.zeros(environment.num_states)
	for state, winner, game_over in state_winner_tripes:
		if game_over:
			if winner == environment.x_piece:
				value = 1
			else:
				value = 0
		else:
			value = 0.5
		Values[state] = value
	return Values 

def initial_value_o(environment, state_winner_tripes):
	# almost the exact opposite of initialV_x
	# everywhere x wins(1), o loses(0)
	# but a draw is still 0 for o
	Values = np.zeros(environment.num_states)
	for state, winner, game_over in state_winner_tripes:
		if game_over:
			if winner == environment.o_piece:
				value = 1
			else:
				value = 0
		else:
			value = 0.5
		Values[state] = value
	return Values 

def train_agents(player_1, player_2, epochs, environment):
	for epoch in range(epochs):
		if epoch % 200 == 0:
			print(epoch)
		play_game(player_1, player_2, environment)