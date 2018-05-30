import random

# actions
CATCH_UP = 0
CATCH_LEFT = 1
CATCH_DOWN = 2
CATCH_RIGHT = 3
MOVE_UP = 4
MOVE_LEFT = 5
MOVE_DOWN = 6
MOVE_RIGHT = 7

# state
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

state2action_fruit = {UP:CATCH_UP, LEFT:CATCH_LEFT, DOWN:CATCH_DOWN, RIGHT:CATCH_RIGHT}
state2action_move= {UP:MOVE_UP, LEFT:MOVE_LEFT, DOWN:MOVE_DOWN, RIGHT:MOVE_RIGHT}

class React:

	def execute(self, perception):
		action = self.process(perception)
		return action

	def process(self, perception):


		fruit_pos = [i for i in range(len(perception)) if perception[i] > 0]
		
		# no fruits -> move to empty cell
		if len(fruit_pos) == 0:
			empty_pos = [i for i in range(len(perception)) if perception[i] == 0]
			random_pos = random.choice(empty_pos)

			action = state2action_move[random_pos]
		
		# only 1 fruit -> grab it
		elif len(fruit_pos) == 1: 
			action = state2action_fruit[fruit_pos[0]]
		
		else:
			random_fruit = random.choice(fruit_pos)
			action = state2action_fruit[random_fruit]

		return action
